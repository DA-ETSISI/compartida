import requests
from decouple import config
from django.core.management.base import BaseCommand
from usrs.models import Titulacion


class Command(BaseCommand):
    help = "Carga titulaciones y asignaturas desde la UPM API"

    def handle(self, *args, **kwargs):

        print("Cargando titulaciones y asignaturas desde la API UPM...")
        titulaciones_url = f"{config('API_URL')}/{config('API_ANYO')}/planes_v2.json"
        try:
            resp = requests.get(titulaciones_url, timeout=20)
        except requests.RequestException as e:
            print(f"Error al obtener las titulaciones: {e}")
            return

        if resp.status_code == 200:
            try:                                                                                                                                                                                                                                  
                data_plan = resp.json()                                                                                                                                                                                                           
            except requests.exceptions.JSONDecodeError as e:                                                                                                                                                                                      
                print(f"Error al parsear JSON de titulaciones: {e}")                                                                                                                                                                              
                return                                                                                                                                                                                                                            
                                    
            escula_plan = data_plan.get("datos", {}).get(
                config("CODIGO_DE_ESCUELA"), []
            )

            for plan in escula_plan:
                if (
                    plan.get("subtipo_estudio") == "GRA"
                    or plan.get("subtipo_estudio") == "MOF"
                ):

                    Titulacion.objects.get_or_create(
                        codigo=plan.get("codigo"),
                        defaults={
                            "nombre": plan.get("nombre"),
                            "tipo": plan.get("subtipo_estudio", "GRA"),
                        },
                    )

        else:
            print(f"Error al obtener titulaciones: {resp.status_code} - {resp.text}")

        titulaciones = Titulacion.objects.all()

        for titulo in titulaciones:
            asignaturas_url = (
                f"{config('API_URL')}/{config('API_ANYO')}/"
                f"{titulo.codigo}_asignaturas_v2.json"
            )
            try:
                resp = requests.get(asignaturas_url, timeout=20)
            except requests.RequestException as e:
                print(f"Error de conecion al obtener {titulo.nombre}: {e}")
                continue

            if resp.status_code == 200:
                try:
                    data_asignaturas = resp.json()
                except requests.exceptions.JSONDecodeError as e:
                    print(f"Error al parsear JSON de asignaturas para {titulo.nombre}: {e}")                                                                                                                                                          
                    continue

                asignaturas_plan = data_asignaturas.get("datos", {})

                for asignatura in asignaturas_plan:

                    try:
                        if asignaturas_plan.get(asignatura).get("ofertada") == "S":
                            asg = Asignatura.objects.get_or_create(
                                codigo=asignaturas_plan.get(asignatura).get("codigo"),
                                defaults={
                                    "nombre": asignaturas_plan.get(asignatura).get(
                                        "nombre"
                                    ),
                                    "creditos": asignaturas_plan.get(asignatura).get(
                                        "credects"
                                    ),
                                    "curso": asignaturas_plan.get(asignatura).get(
                                        "curso"
                                    ),
                                },
                            )
                            asg[0].grados.add(titulo)
                            if (
                                asignaturas_plan.get(asignatura).get(
                                    "codigo_tipo_asignatura"
                                )
                                == "O"
                            ):
                                asg[0].optativa = True
                            asg[0].save()
                    except ValueError:
                        print(
                            f"Error al cargar la asignatura "
                            f"{asignaturas_plan.get(asignatura).get('nombre')} "
                            f"({asignaturas_plan.get(asignatura).get('codigo')}) en el "
                            f"titulo {titulo.nombre} ({titulo.codigo})"
                        )
                        continue