# persona/management/commands/dedupe_personas.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from persona.models import Persona

class Command(BaseCommand):
    help = "Elimina duplicados de Persona manteniendo el registro con menor id."

    def handle(self, *args, **kwargs):
        duplicates = Persona.objects.values('nombre','apellido','oficina').annotate(ct=Count('id')).filter(ct__gt=1)
        total_deleted = 0
        for d in duplicates:
            qs = Persona.objects.filter(nombre=d['nombre'], apellido=d['apellido'], oficina=d['oficina']).order_by('id')
            keep = qs.first()
            to_delete = qs.exclude(id=keep.id)
            n = to_delete.count()
            to_delete.delete()
            total_deleted += n
            self.stdout.write(f"Mantengo id={keep.id} para {keep.nombre} {keep.apellido} en oficina={keep.oficina} — eliminados: {n}")
        self.stdout.write(self.style.SUCCESS(f"Total eliminados: {total_deleted}"))
