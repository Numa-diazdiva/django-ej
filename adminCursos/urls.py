from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cursos", views.listar_cursos, name="listar_cursos"),
    path("listarAlumnos", views.listar_alumnos, name="listar_alumnos"),
    path("cargarAlumnos/", views.cargar_alumnos, name="cargar_alumnos"),
    path("cargarAlumnosFile", views.cargar_alumnos_file_upload, name="cargar_alumnos_file"),
    path("alumno/<int:dni>", views.alumno, name="alumno"),
    path("eliminarAlumno/", views.eliminar, name="eliminar"),
    path("eliminarAlumno/<int:dni>", views.eliminar_alumno, name="eliminar_alumno"),
    path("eliminarAlumnoClase/<int:pk>", views.EliminarAlumno.as_view(), name="eliminar_alumno_clase"),
    path("asignarCurso/<int:dni>/<int:id_curso>", views.asignar_alumno_curso, name="asignar_curso"),
    path("alumnosPorCurso/<int:id_curso>", views.alumnos_por_curso, name="alumnos_curso"),
    path("modificarAlumno/<int:dni>", views.modificar_alumno, name="modificar_alumno"),
    path("modificarAlumnoClase/<int:pk>", views.AlumnoUpdateView.as_view(), name="modificar_alumno_clase")
]