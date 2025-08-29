# oficina/management/commands/load_oficinas.py
import csv
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from oficina.models import Oficina

class Command(BaseCommand):
    help = "Carga masiva de oficinas desde CSV. Acepta CSV con o sin columna 'id'."

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='Ruta al archivo CSV')
        parser.add_argument('--delimiter', type=str, default=',', help='Delimitador CSV (por defecto ",")')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']
        delimiter = kwargs['delimiter']
        creadas = actualizadas = omitidas = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            for row in reader:
                try:
                    nombre = row.get('nombre', '').strip()
                    nombre_corto = row.get('nombre_corto', '').strip()
                    id_val = row.get('id', '').strip()

                    if not nombre and not nombre_corto:
                        omitidas += 1
                        self.stderr.write(f"Omitida (sin nombre/nombre_corto): {row}")
                        continue

                    # Si viene id válido, intenta crear/actualizar por id
                    if id_val:
                        try:
                            oficina_id = int(id_val)
                            oficina, creada = Oficina.objects.update_or_create(
                                id=oficina_id,
                                defaults={'nombre': nombre, 'nombre_corto': nombre_corto}
                            )
                        except ValueError:
                            # id no numérico -> fallback por nombre_corto si existe
                            oficina, creada = Oficina.objects.update_or_create(
                                nombre_corto=nombre_corto or nombre,
                                defaults={'nombre': nombre, 'nombre_corto': nombre_corto}
                            )
                    else:
                        # Sin id: usar nombre_corto como clave si está; si no, usar nombre
                        lookup_field = 'nombre_corto' if nombre_corto else 'nombre'
                        lookup = {lookup_field: nombre_corto if lookup_field == 'nombre_corto' else nombre}
                        oficina, creada = Oficina.objects.update_or_create(
                            **lookup,
                            defaults={'nombre': nombre, 'nombre_corto': nombre_corto}
                        )

                    if creada:
                        creadas += 1
                    else:
                        actualizadas += 1

                except IntegrityError as e:
                    omitidas += 1
                    self.stderr.write(f"Omitida: {row} — IntegrityError: {e}")
                except Exception as e:
                    omitidas += 1
                    self.stderr.write(f"Omitida: {row} — Error: {e}")

        self.stdout.write(self.style.SUCCESS(
            f"Resumen: creadas={creadas}, actualizadas={actualizadas}, omitidas={omitidas}"
        ))
