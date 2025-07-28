from django.shortcuts import render
from django.views.generic import ListView
from .models import Oficina

class OficinaListView(ListView):
    model = Oficina
    template_name = 'oficina/lista.html'
    context_object_name = 'oficinas'

# Create your views here.
