from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


@login_required
def profile_view(request):
    user = request.user
    profile_info = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile_info': profile_info,
    }
    return render(request, 'pages/user_profile.html', context)


class SignUpView(View):

    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
        return render(request, 'account/register_done.html', {'user_form': user_form})


class EditUserView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profiles)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile_edit.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profiles,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_page')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile_edit.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_view(request):
    user_admins = User.objects.filter(is_superuser=True)
    context = {
        'user_admins': user_admins,
    }
    return render(request, 'pages/admin_page.html', context)

