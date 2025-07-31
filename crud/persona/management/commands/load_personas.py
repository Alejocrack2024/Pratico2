# persona/management/commands/load_personas.py

import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from persona.models import Persona
from oficina.models import Oficina  # Importa el modelo Oficina de la app correspondiente


class Command(BaseCommand):
    help = 'Carga masiva de Personas desde un archivo CSV.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file', '-f',
            type=str,
            required=True,
            help='Ruta al archivo CSV de entrada. Debe tener columnas: nombre, apellido, edad, oficina.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Solo valida el archivo sin guardar nada en la base de datos.'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=500,
            help='Número de instancias a crear por lote en bulk_create (por defecto: 500).'
        )
        parser.add_argument(
            '--encoding',
            type=str,
            default='utf-8',
            help='Codificación del archivo CSV (por defecto: utf-8).'
        )
        parser.add_argument(
            '--error-log',
            type=str,
            help='Ruta de un CSV donde registrar filas con errores. Si no se provee, solo se muestran en consola.'
        )

    def handle(self, *args, **options):
        file_path      = options['file']
        dry_run        = options['dry_run']
        batch_size     = options['batch_size']
        encoding       = options['encoding']
        error_log_path = options.get('error_log')

        if not os.path.isfile(file_path):
            raise CommandError(f"El archivo '{file_path}' no existe o no es accesible.")

        error_writer = None
        if error_log_path:
            try:
                ef = open(error_log_path, 'w', newline='', encoding='utf-8')
            except Exception as e:
                raise CommandError(f"No se pudo abrir el error-log en '{error_log_path}': {e}")
            error_writer = csv.writer(ef)
            error_writer.writerow(['fila', 'campo', 'valor', 'mensajes'])
            self.stdout.write(f"Registrando errores en: {error_log_path}")

        created = updated = skipped = 0
        errores_detallados = []
        personas_para_crear = []
        apellidos_vistos = set()

        with open(file_path, newline='', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            expected = {'nombre', 'apellido', 'edad', 'oficina'}
            if not expected.issubset(reader.fieldnames or []):
                raise CommandError(
                    f"El CSV debe tener columnas: {', '.join(expected)}. "
                    f"Encontradas: {reader.fieldnames}"
                )

            for fila_num, row in enumerate(reader, start=2):
                nombre     = (row.get('nombre')   or '').strip()
                apellido   = (row.get('apellido') or '').strip()
                edad_str   = (row.get('edad')     or '').strip()
                oficina_nm = (row.get('oficina')  or '').strip()
                row_errors = []

                # Intentar actualizar si ya existe alguien con mismo apellido
                qs = Persona.objects.filter(apellido=apellido)
                if qs.exists():
                    try:
                        oficina_obj, created_off = Oficina.objects.get_or_create(
                            nombre=oficina_nm,
                            defaults={'nombre_corto': oficina_nm[:10]}
                        )
                        if created_off:
                            self.stdout.write(f"Fila {fila_num}: creada nueva Oficina “{oficina_nm}”")
                    except Exception as e:
                        row_errors.append(('oficina', oficina_nm, str(e)))

                    if row_errors:
                        skipped += 1
                        for campo, valor, msg in row_errors:
                            errores_detallados.append({'fila': fila_num, 'campo': campo, 'valor': valor, 'mensajes': msg})
                            if error_writer:
                                error_writer.writerow([fila_num, campo, valor, msg])
                        continue

                    persona = qs.first()
                    cambios = {}

                    # Validar edad para comparación
                    try:
                        edad = int(edad_str)
                    except:
                        edad = None

                    if nombre and persona.nombre != nombre:
                        cambios['nombre'] = (persona.nombre, nombre)
                        persona.nombre = nombre
                    if edad is not None and persona.edad != edad:
                        cambios['edad'] = (persona.edad, edad)
                        persona.edad = edad
                    if persona.oficina_id != (oficina_obj.id if 'oficina_obj' in locals() else None):
                        cambios['oficina'] = (persona.oficina_id, oficina_obj.id)
                        persona.oficina = oficina_obj

                    if cambios:
                        try:
                            persona.full_clean()
                            if not dry_run:
                                persona.save()
                            updated += 1
                            self.stdout.write(f"Fila {fila_num}: actualizado {apellido}. Cambios: {cambios}")
                        except Exception as e:
                            msg = str(e)
                            errores_detallados.append({'fila': fila_num, 'campo': 'validación', 'valor': str(row), 'mensajes': msg})
                            skipped += 1
                            if error_writer:
                                error_writer.writerow([fila_num, 'validación', str(row), msg])
                    continue

                # Validaciones básicas para nuevas instancias
                if not nombre:
                    row_errors.append(('nombre', nombre, 'Nombre vacío'))
                if not apellido:
                    row_errors.append(('apellido', apellido, 'Apellido vacío'))
                elif apellido in apellidos_vistos:
                    row_errors.append(('apellido', apellido, 'Apellido duplicado en archivo'))
                if not edad_str:
                    row_errors.append(('edad', edad_str, 'Edad vacía'))
                else:
                    try:
                        edad = int(edad_str)
                        if edad < 0:
                            row_errors.append(('edad', edad_str, 'Edad negativa'))
                    except ValueError:
                        row_errors.append(('edad', edad_str, 'Edad no es un entero válido'))

                if not oficina_nm:
                    row_errors.append(('oficina', oficina_nm, 'Oficina vacía'))
                else:
                    oficina_obj, created_off = Oficina.objects.get_or_create(
                        nombre=oficina_nm,
                        defaults={'nombre_corto': oficina_nm[:10]}
                    )
                    if created_off:
                        self.stdout.write(f"Fila {fila_num}: creada nueva Oficina “{oficina_nm}”")

                if row_errors:
                    skipped += 1
                    for campo, valor, msg in row_errors:
                        errores_detallados.append({'fila': fila_num, 'campo': campo, 'valor': valor, 'mensajes': msg})
                        if error_writer:
                            error_writer.writerow([fila_num, campo, valor, msg])
                    continue

                apellidos_vistos.add(apellido)
                edad = int(edad_str)

                instancia = Persona(
                    nombre=nombre,
                    apellido=apellido,
                    edad=edad,
                    oficina=oficina_obj,
                )
                try:
                    instancia.full_clean()
                except Exception as e:
                    for campo, msgs in getattr(e, 'message_dict', {None: [str(e)]}).items():
                        for m in msgs:
                            errores_detallados.append({'fila': fila_num, 'campo': campo or 'validación', 'valor': row.get(campo) or str(row), 'mensajes': m})
                            if error_writer:
                                error_writer.writerow([fila_num, campo or 'validación', row.get(campo) or str(row), m])
                    skipped += 1
                    continue

                personas_para_crear.append(instancia)

                if len(personas_para_crear) >= batch_size:
                    if not dry_run:
                        try:
                            with transaction.atomic():
                                Persona.objects.bulk_create(personas_para_crear)
                        except Exception:
                            for idx, inst in enumerate(personas_para_crear, start=fila_num - len(personas_para_crear) + 1):
                                try:
                                    inst.full_clean()
                                    inst.save()
                                    created += 1
                                except Exception as e_single:
                                    msg = str(e_single)
                                    errores_detallados.append({'fila': idx, 'campo': 'bulk->individual', 'valor': str(inst), 'mensajes': msg})
                                    skipped += 1
                                    if error_writer:
                                        error_writer.writerow([idx, 'bulk->individual', str(inst), msg])
                            personas_para_crear = []
                            continue
                    created += len(personas_para_crear)
                    self.stdout.write(f"Se crearon {len(personas_para_crear)} instancias (batch).")
                    personas_para_crear = []

        if personas_para_crear:
            if not dry_run:
                try:
                    with transaction.atomic():
                        Persona.objects.bulk_create(personas_para_crear)
                except Exception:
                    for idx, inst in enumerate(personas_para_crear, start=1):
                        try:
                            inst.full_clean()
                            inst.save()
                            created += 1
                        except Exception as e_single:
                            msg = str(e_single)
                            errores_detallados.append({'fila': 'desconocida', 'campo': 'bulk-final->individual', 'valor': str(inst), 'mensajes': msg})
                            skipped += 1
                            if error_writer:
                                error_writer.writerow(['desconocida', 'bulk-final->individual', str(inst), msg])
                    personas_para_crear = []
                else:
                    created += len(personas_para_crear)
                    self.stdout.write(f"Se crearon {len(personas_para_crear)} instancias (batch final).")
            else:
                created += len(personas_para_crear)
            personas_para_crear = []

        if error_writer:
            ef.close()

        self.stdout.write(self.style.SUCCESS(
            f"Resumen de carga masiva: creadas={created}, actualizadas={updated}, omitidas={skipped}."
        ))
        if errores_detallados and not error_log_path:
            self.stdout.write("Errores detallados (solo los primeros 20):")
            for err in errores_detallados[:20]:
                self.stdout.write(f"  Fila {err['fila']}: campo={err['campo']}, valor={err['valor']}, mensaje={err['mensajes']}")
            if len(errores_detallados) > 20:
                self.stdout.write(f"  ... y {len(errores_detallados) - 20} errores más. Usa --error-log para guardarlos en un CSV.")
