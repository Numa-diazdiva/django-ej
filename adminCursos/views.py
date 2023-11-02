from django.shortcuts import render
from .models import Alumno, Curso
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, FileResponse
import csv

# Create your views here.
def index(request):
    nombre_app = "Administrador de Academia"
    return render(request, "index.html", { "nombre": nombre_app })

def listar_cursos(request):
    cursos = Curso.objects.all()
    return render(request, "listar_cursos.html", {"cursos": cursos})

def listar_alumnos(request):
    alumnos = Alumno.objects.all()
    return render(request, "listar_alumnos.html", {"alumnos": alumnos})

def alumno(request):
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

def cargar_alumnos(request):
    with open("csv_carga.csv") as archivo:
        lector_csv = csv.DictReader(archivo)
        for alumno in lector_csv:
            if(not Alumno.objects.filter(dni=alumno["dni"])):
                print("agrego")
                nuevo_alumno = Alumno(dni=alumno["dni"], nombre=alumno["nombre"], apellido=alumno["apellido"])
                nuevo_alumno.save()

    return HttpResponse("Okay")