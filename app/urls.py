from django.urls import path
from .views import news_list, HomePageView, ContactPageView, LocalPageView, SportPageView, ForeignPageView, \
    TechnologyPageView, NewsUpdateView, NewsDeleteView, NewsCreateView, SearchResultListView, \
    NewHitCountDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('list/', news_list, name='news'),
    path('detail/<slug:slug>/', NewHitCountDetailView.as_view(), name='news_detail_page'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_edit_page'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete_page'),
    path('news/create/', NewsCreateView.as_view(), name='news_create_page'),
    path('contact-page', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalPageView.as_view(), name='local_page'),
    path('sport/', SportPageView.as_view(), name='sport_page'),
    path('foreign/', ForeignPageView.as_view(), name='foreign_page'),
    path('technology/', TechnologyPageView.as_view(), name='technology_page'),
    path('search/list/', SearchResultListView.as_view(), name='search_page'),
]
