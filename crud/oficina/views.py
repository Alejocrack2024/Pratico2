from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Oficina

class OficinaListView(ListView):
    model = Oficina
    template_name = 'oficina/lista.html'
    context_object_name = 'oficinas'

class OficinaDetailView(DetailView):
    model = Oficina
    template_name = 'oficina/detalle.html'
    context_object_name = 'oficina'

class OficinaCreateView(CreateView):
    model = Oficina
    template_name = 'oficina/crear.html'
    fields = ['nombre', 'nombre_corto']
    success_url = reverse_lazy('oficina:lista')

class OficinaUpdateView(UpdateView):
    model = Oficina
    template_name = 'oficina/crear.html'
    fields = ['nombre', 'nombre_corto']
    success_url = reverse_lazy('oficina:lista') 

class OficinaDeleteView(DeleteView):
    model = Oficina
    template_name = 'oficina/eliminar.html'
    context_object_name = 'oficina'
    success_url = reverse_lazy('oficina:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'eliminar'
        return context