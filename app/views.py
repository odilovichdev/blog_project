from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView

from root.custom_permissions import OnlyLoggedSuperUser
from .forms import ContactForm, CommentForm
from .models import News


class LocalPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/local.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Mahalliy')


class SportPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Sport')


class ForeignPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/foreign.html'
    context_object_name = 'xorijiy_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Xorij')


class TechnologyPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/technology.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Texnologiya')


class ContactPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/contact.html'
    form_class = ContactForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h1>Biz bilan bog'langaningiz uchun tashakkur</h1>")
        return render(request, self.template_name, {'form': form})


class HomePageView(ListView):
    model = News
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news'] = News.published.filter(category__name='Mahalliy')[:5]
        context['sport_news'] = News.published.filter(category__name='Sport')[:5]
        context['technology_news'] = News.published.filter(category__name='Texnologiya')[:5]
        context['foreign_news'] = News.published.filter(category__name='Xorij')[:5]
        context['ommabop_news'] = News.published.all().order_by('-publish_time')[:5]
        return context


class SearchResultListView(ListView):
    model = News
    template_name = 'app/search.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        query = self.request.GET.get('search')
        return News.objects.filter(Q(title__icontains=query) |
                                   Q(body__icontains=query)
                                   )


@login_required
def news_list(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list,
    }
    return render(request, 'app/list.html', context)


class NewHitCountDetailView(FormMixin, HitCountDetailView):
    model = News
    template_name = 'app/detail.html'
    count_hit = True
    form_class = CommentForm

    def get_success_url(self):
        return reverse('news_detail_page', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            hit_count = get_hitcount_model().objects.get_for_object(self.object)
            hits = hit_count.hits
            context['hitcount'] = {'pk': hit_count.pk}

            if self.count_hit:
                hit_count_response = self.hit_count(self.request, hit_count)
                if hit_count_response.hit_counted:
                    hits = hits + 1
                context['hitcount']['hit_counted'] = hit_count_response.hit_counted
                context['hitcount']['hit_message'] = hit_count_response.hit_message

            context['hitcount']['total_hits'] = hits
        context['comments'] = self.object.comments.filter(active=True)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_form = form.save(commit=False)
        new_form.new = self.object
        new_form.user = self.request.user
        new_form.save()
        return super().form_valid(form)


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    queryset = News.objects.filter(status=News.Status.PUBLISHED)
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    queryset = News.objects.filter(status=News.Status.PUBLISHED)
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru',
              'body', 'body_uz', 'body_en', 'body_ru', 'image', 'category', 'status')
