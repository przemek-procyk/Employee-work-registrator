from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy

from KRemployee import settings
from accounts.forms import LoginForm


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('today_info')
        return reverse('emp_home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_message = "Hasło zostało zmienione"
    success_url = reverse_lazy('emp_home')


class ResetPasswordView(PasswordResetView):
    html_email_template_name = 'accounts/password_reset_email.html'
    template_name = 'accounts/reset_password.html'
    from_email = settings.EMAIL_HOST_USER
    success_url = reverse_lazy('password_reset_splash')


class ResetPasswordSplashView(PasswordResetDoneView):
    template_name = 'accounts/reset_password_splash.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/reset_password_confirm.html'
    success_url = reverse_lazy('password_reset_finish')


class ResetPasswordFinishView(PasswordResetCompleteView):
    template_name = 'accounts/reset_password_finish.html'  