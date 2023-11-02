from django.contrib import admin
from .models import Alumno, Curso, BandaHoraria

# Register your models here.
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "apellido"]

class CursoAdmin(admin.ModelAdmin):
    list_display = ["nombre"]

class BandaHorariaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "horario_inicio"]

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(BandaHoraria, BandaHorariaAdmin)