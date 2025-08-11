from django.shortcuts import render

# Create your views here.
# CBV for signup view
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CaptchaAuthenticationForm, CaptchaUserCreationForm

class SignUpView(CreateView):
    """
    View for creating a new user account with captcha.
    """
    form_class = CaptchaUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CaptchaAuthenticationForm
    redirect_authenticated_user = True

class LogoutMessageView(TemplateView):
    """
    View to display a logout message.
    """
    template_name = 'accounts/logout_message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Deslogearse'
        return context