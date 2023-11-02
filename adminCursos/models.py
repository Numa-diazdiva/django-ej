from django.db import models

# Create your models here.

class BandaHoraria(models.Model):
    nombre = models.CharField(max_length=50)
    horario_inicio = models.DateTimeField()
    horario_fin = models.DateTimeField()
    def __str__(self) -> str:
        return self.nombre

class Curso(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=300, null=True)
    nota = models.IntegerField(null=True)
    banda_horaria = models.ForeignKey(BandaHoraria, on_delete=models.CASCADE, null=True)
    
    def __str__(self) -> str:
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.IntegerField(null=True)
    telefono = models.CharField(max_length=15, null=True)
    correo_electronico = models.EmailField(max_length=50,null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.nombre + self.apellido

class Resenia(models.Model):
    titulo = models.CharField(max_length=30, null=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True)
    contenido = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.titulo
    