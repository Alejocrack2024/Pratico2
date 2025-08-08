from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Oficina
from django.db.models import Q
# Import login mixins if needed
from django.contrib.auth.mixins import LoginRequiredMixin
from persona.models import Persona

class OficinaListView(ListView):
    model = Oficina
    template_name = 'oficina/lista.html'
    context_object_name = 'oficinas'

class OficinaDetailView(DetailView):
    model = Oficina
    template_name = 'oficina/detalle.html'
    context_object_name = 'oficina'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personas'] = Persona.objects.filter(oficina=self.object)
        return context

class OficinaCreateView(LoginRequiredMixin, CreateView):
    model = Oficina
    template_name = 'oficina/crear.html'
    fields = ['nombre', 'nombre_corto']
    success_url = reverse_lazy('oficina:lista')

class OficinaUpdateView(LoginRequiredMixin, UpdateView):
    model = Oficina
    template_name = 'oficina/crear.html'
    fields = ['nombre', 'nombre_corto']
    success_url = reverse_lazy('oficina:lista') 

class OficinaDeleteView(LoginRequiredMixin, DeleteView):
    model = Oficina
    template_name = 'oficina/eliminar.html'
    context_object_name = 'oficina'
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        return context