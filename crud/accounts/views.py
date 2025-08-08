from django.shortcuts import render

# Create your views here.
# CBV for signup view
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from .forms import VerificacionForm

def verificacion_view(request):
    mensaje = ""
    if request.method == "POST":
        form = VerificacionForm(request.POST)
        if form.is_valid():
            mensaje = "¡Verificación exitosa!"
            form = VerificacionForm()
    else:
        form = VerificacionForm()
    return render(request, "accounts/verificacion.html", {"form": form, "mensaje": mensaje})

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