from django.db import models
from django.dispatch import receiver
import os
from django.db.models.signals import post_delete, pre_save


class Semestre(models.Model):
    semestre=models.CharField(max_length=45, null=False)
    descripcion=models.CharField(max_length=85, null=False)
    def __str__(self):
        return self.semestre

class Alumno(models.Model):
    nombre = models.CharField(max_length=40, null=False)
    apellidopaterno = models.CharField(max_length=45,null=False)
    apellidomaterno = models.CharField(max_length=45,null=False)
    curp= models.CharField(max_length=18,null=False,unique=True)
    email= models.EmailField(unique=True)
    NumeroControl=models.IntegerField(null=False, unique=True)
    alumnosemestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    Usuario=models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.nombre + " "+ self.apellidopaterno + " " + self.apellidomaterno

    

class EstatusRequisitoAlumno(models.Model):
    nombre = models.CharField(max_length=45, null=False) 
    descripcion = models.CharField(max_length=85,null=False)
    def __str__(self):
        return self.nombre


class Requisito(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=600, null= False)
    detalle = models.ManyToManyField(Alumno, through='DetalleRequisito')
    semestre= models.ForeignKey(Semestre, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

    

class DetalleRequisito(models.Model):
    ruta = models.FileField(upload_to='uploads/',null=True)
    observaciones = models.CharField(max_length=95,blank=True, null=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    requisito = models.ForeignKey(Requisito, on_delete=models.CASCADE)
    estatusrequisitoalumno = models.ForeignKey(EstatusRequisitoAlumno, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=DetalleRequisito)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Elimina el archivo de directorio si se elimina el objeto correspondiente.
    """
    if instance.ruta:
        if os.path.isfile(instance.ruta.path):
            print("path: ", instance.ruta.path)
            os.remove(instance.ruta.path)


@receiver(models.signals.pre_save, sender=DetalleRequisito)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Elimina el archivo antiguo del directorio cuando se actualiza el objeto correspondiente con un nuevo archivo
    """
    if not instance.pk:
        return False

    old_file = sender.objects.get(pk=instance.pk).ruta

    if old_file:
        new_file = instance.ruta
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
    else:
        pass