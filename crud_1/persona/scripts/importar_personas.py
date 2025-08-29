import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from oficina.models import Oficina
from persona.models import Persona

def run(*args):
    if not args:
        print("Error: favor de proporcionar la ruta del archivo.")
        print("Uso: ./manage.py runscrpt import_persona --script-args <ruta_del_archivo>")
        sys.exit(1)

    csv_file = args[0]

    oficina_map = {oficina.nombre_corto: oficina for oficina in Oficina.objects.all()}
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            personas_a_crear = []
            for row in reader:
                nombre = row['nombre']
                apellido = row['apellido']
                edad = row['edad']
                oficina_nombre_corto = row['oficina_nombre_corto']
                if not nombre or not apellido or not edad:
                    print(f"Error en la fila {row}. Falta el nombre o el apellido o la edad")
                    continue
                try:
                    edad = int(edad)
                except (ValueError, TypeError) as e:
                    print(f"Error de validación en la fila {row}. la edad no es un numero valido")
                    continue
                oficina_obj = None
                if oficina_nombre_corto:
                    oficina_obj = oficina_map.get(oficina_nombre_corto)
                    if not oficina_obj:
                        print(f"Warning: No existe la oficina mensionada")
                        print(f"Se creará el registro sin oficina")
                        continue
                try:
                    persona = Persona(nombre=nombre, apellido=apellido, edad=edad, oficina=oficina_obj)
                    persona.full_clean()  # Validar el modelo
                    personas_a_crear.append(persona)
                except ValidationError as e:
                    print(f"Error validación en la fila {row}. Detalle: {e}")
                except Exception as e:
                    print(f"Error inesperado en la fila {row}. Detalle: {e}")

            with transaction.atomic():
                Persona.objects.bulk_create(personas_a_crear)
                print(f"Se importaron {len(personas_a_crear)} registros.")
    except FileNotFoundError:
        print(f"Error. No se encontro el archivo: {csv_file}")
    except Exception as e:
        print(f"Ocurrio un error inesperado en la importación: {e}")
