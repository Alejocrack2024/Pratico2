from django.shortcuts import render

# Create your views here.
# CBV for signup view
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

class SignUpView(CreateView):
    """
    View for creating a new user account, with a response rendered by a template.
    """
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login') # Redirect to login page after successful signup

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

class LogoutMessageView(TemplateView):
    """
    View to display a logout message.
    """
    template_name = 'accounts/logout_message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Deslogearse'
        return context