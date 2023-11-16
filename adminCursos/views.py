from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, FileResponse, JsonResponse
from django.views.generic.edit import DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
import csv
import json
from .models import Alumno, Curso
from .forms import UploadFileForm

def index(request):
    """ Página home con links a las distintas secciones """
    nombre_app = "Administrador de Academia"
    return render(request, "index.html", { "nombre": nombre_app })

def listar_cursos(request):
    """ Lista todos los cursos haciendo una consulta a la base de datos """
    cursos = Curso.objects.all()
    return render(request, "listar_cursos.html", {"cursos": cursos})

def listar_alumnos(request):
    """ Lista todos los alumnos haciendo una consulta a la base de datos """
    alumnos = Alumno.objects.all()
    return render(request, "listar_alumnos.html", {"alumnos": alumnos})

def cargar_alumnos(request):
    """ Abre un archivo csv con datos de alumnos y los agrega a la base de datos chequeando que no se repitan por dni como clave primaria """
    with open("csv_carga.csv") as archivo:
        lector_csv = csv.DictReader(archivo)
        for alumno in lector_csv:
            if(not Alumno.objects.filter(dni=alumno["dni"])):
                nuevo_alumno = Alumno(dni=alumno["dni"], nombre=alumno["nombre"], apellido=alumno["apellido"])
                nuevo_alumno.save()
    return HttpResponse("Okay")

def cargar_alumnos_file_upload(request):
    """ Abre un archivo csv que llega en el request con datos de alumnos y los agrega a la base de datos chequeando que no se repitan por dni como clave primaria """
    if request.method == "POST":
        form_subido = UploadFileForm(request.FILES["file"]) # Faltaría checar que sea válido
        # Los archivos llegan en el dict FILES de request
        archivo = request.FILES["file"]
        # Leemos y decodificamos el archivo
        archivo_raw = archivo.read().decode('utf-8')
        # Ya tenemos el archivo "crudo", tenemos que separarlo en líneas para poder iterarlo con un dictReader y que reconozca el header
        lector_csv = csv.DictReader(archivo_raw.splitlines())
        for alumno in lector_csv:
            try:
                if(not Alumno.objects.filter(dni=alumno["dni"])):
                    print("agrego")
                    nuevo_alumno = Alumno(dni=alumno["dni"], nombre=alumno["nombre"], apellido=alumno["apellido"])
                    nuevo_alumno.save()
            except Exception as e:
                print(e)

        return redirect("listar_alumnos")
    else:
        form = UploadFileForm()
    return render(request, "cargar_alumnos.html", {"form": form})


def asignar_alumno_curso(request, dni, id_curso):
    """ Asigna un curso a un alumno, en caso de existir ambos en la base de datos """
    try:
        alumno = Alumno.objects.get(dni=dni)
        curso = Curso.objects.get(pk=id_curso)
        alumno.curso.add(curso)
        alumno.save()
    except:
        return HttpResponseNotFound("El curso y/o el alumno no existen")
    return HttpResponse(f"Cursos del alumno {alumno.nombre} actualizados")

def alumno(request, dni):
    if request.method == "GET":
        alumno = Alumno.objects.get(dni=dni)
        alumno_res = {
            "dni": alumno.dni,
            "nombre": alumno.nombre,
            "apellido": alumno.apellido
        }
        return JsonResponse(alumno_res)
    return HttpResponseBadRequest("Solo aceptamos get")

def eliminar(request):
    """ Vista que muestra los alumnos para eliminarlos """
    alumnos = Alumno.objects.all()
    return render(request, "eliminar.html", { "alumnos": alumnos })

@csrf_exempt
def eliminar_alumno(request, dni):
    """ Elimina un alumno chequeando que exista previamente en la base de datos """
    try:
        alumno = Alumno.objects.get(dni=dni)
    except:
        return HttpResponseNotFound("El alumno no existe en la base de datos")
    
    if request.method == "DELETE" or request.method == "POST":
        alumno.delete()
        return redirect("listar_alumnos")
    
    return render(request, "alumno_eliminar.html", {"alumno": alumno})

def alumnos_por_curso(request, id_curso):
    """ Retorna la información de los alumnos correspondientes al curso pasado por parámetro en formato JSON """
    try:
        alumnos = Alumno.objects.filter(curso__id=id_curso)
        lista_alumnos = []
        for alumno in alumnos:
            nuevo_al = {
                "nombre": alumno.nombre,
                "apellido": alumno.apellido            
            }
            lista_alumnos.append(nuevo_al)

    except Exception as e:
        print(e)
        return HttpResponseNotFound("El curso no existe en la base de datos")
    return JsonResponse(lista_alumnos, safe=False)

@csrf_exempt
def modificar_alumno(request, dni):
    """ Modifica la información de un alumno siempre que el método sea PUT y haya un json en el body con el formato acorde """
    response = HttpResponseBadRequest("Sólo se acepta el método PUT")
    if request.method == "PUT":
        try:
            alumno = Alumno.objects.get(dni=dni)
            actualizacion = json.loads(request.body)
            alumno.nombre = actualizacion["nombre"]
            alumno.apellido = actualizacion["apellido"]
            alumno.save()
            response = HttpResponse("OKAY")
        except KeyError:
            print("keyerror")
            response = HttpResponseBadRequest("El payload enviado es incorrecto")
        except Exception as e:
            print(e)
            response = HttpResponseNotFound("El alumno que se quiere modificar no existe")
    return response

def alumno_query_param(request):
    """ Una alternativa al parámetro del dni por url, para ejemplificar el uso de query params """
    query = request.GET
    try:
        dni = query["dni"]
        alumno = Alumno.objects.filter(dni=dni)
        print(alumno.exists())
        if(alumno.exists() > 0):
            alumno_obj = alumno[0]
            with open("csv_response.csv", "w") as file_response:
                writer = csv.writer(file_response)
                writer.writerow(["Nombre", "Apellido", "Dni", "Curso"])
                writer.writerow([alumno_obj.nombre, alumno_obj.apellido, alumno_obj.dni, alumno_obj.curso.nombre])
            
            response = FileResponse(open("csv_response.csv", "rb"), as_attachment=True, filename="response.csv")
            return response
    except KeyError:
        return HttpResponseBadRequest
    return HttpResponseNotFound

# View para eliminar manejada con herencia.
# Requiere un formulario de tipo submit con un botón y un token csrf para confirmar.
# Toma la clave primaria del modelo desde la url.
class EliminarAlumno(DeleteView):
    model = Alumno
    template_name = "alumno_eliminar.html"
    success_url = "/listarAlumnos"


def eliminar_alumno_get(request, dni):
    """ Elimina un alumno chequeando que exista previamente en la base de datos """
    if request.method == "GET":
        try:
            alumno = Alumno.objects.get(dni=dni)
            alumno.delete()
        except:
            return HttpResponseNotFound("El alumno no existe en la base de datos")
    else:
        return HttpResponseBadRequest("Bad request")
    return HttpResponse("Se borró lo que es el alumno") 


class AlumnoUpdateView(UpdateView):
    """ Generic view para hacer un update del modelo """
    model = Alumno
    fields = ["nombre", "apellido"]
    template_name = "alumno_editar.html"
    success_url = "/listarAlumnos"