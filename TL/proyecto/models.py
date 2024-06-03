from django.db import models
from django.contrib.auth.models import User




class Proyecto(models.Model):
    nombre_estudiante=models.CharField(max_length=100)
    nombre_proyecto = models.CharField(max_length=100)
    tema = models.CharField(max_length=100)
    nombre_profesor=models.CharField(max_length=100,default="-")

    def __str__(self):
        return self.nombre_proyecto


