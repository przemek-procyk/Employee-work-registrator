from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import CustomLoginView, ChangePasswordView, ResetPasswordView, ResetPasswordSplashView, ResetPasswordConfirmView, ResetPasswordFinishView 


urlpatterns = [
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-splash', ResetPasswordSplashView.as_view(), name='password_reset_splash'),
    path('password-reset-confirm/<uidb64>/<token>', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-finish', ResetPasswordFinishView.as_view(), name='password_reset_finish'),
]