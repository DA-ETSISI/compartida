import requests
from decouple import config
from django.core.management.base import BaseCommand
from usrs.models import Asignatura, Titulacion


class Command(BaseCommand):
    help = "Carga titulaciones y asignaturas desde la UPM API"

    def handle(self, *args, **kwargs):

        print("Cargando titulaciones y asignaturas desde la API UPM...")
        titulaciones_url = f"{config('API_URL')}/{config('API_ANYO')}/planes_v2.json"
        resp = requests.get(titulaciones_url)

        if resp.status_code == 200:
            data_plan = resp.json()
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
            resp = requests.get(asignaturas_url)

            if resp.status_code == 200:
                data_asignaturas = resp.json()
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
