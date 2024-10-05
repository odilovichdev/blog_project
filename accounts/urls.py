from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from accounts.views import logout_view, profile_view, SignUpView, EditUserView, admin_view

urlpatterns = [
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login_page'),
    path('logout/', logout_view, name='logout_page'),
    path('profile/', profile_view, name='profile_page'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', SignUpView.as_view(), name='signup_page'),
    path('profile/edit/', EditUserView.as_view(), name='user_profile_info'),
    path('adminpages/', admin_view, name='admin_page'),
]
