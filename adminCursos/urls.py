from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cursos", views.listar_cursos, name="listar_cursos"),
    path("listarAlumnos", views.listar_alumnos, name="listar_alumnos"),
    path("alumno/", views.alumno, name="alumno"),
    path("cargarAlumnos/", views.cargar_alumnos, name="cargar_alumnos"),
    path("reseñas/ver", views.ver_reseñas, name="ver_reseñas"),
    path("reseñas/crear", views.crear_reseñas, name="crear_reseñas")
]