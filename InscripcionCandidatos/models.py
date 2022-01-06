from django.contrib.sessions.backends.db import SessionStore as DBStore
from django.contrib.sessions.base_session import AbstractBaseSession
from django.db import models




class EstatusAspirante(models.Model):
    estatus=models.CharField(max_length=45, null=False)
    descripcion=models.CharField(max_length=85, null=False)

    def __str__(self):
        return self.estatus

class Aspirante(models.Model):
    nombre = models.CharField(max_length=40, null=False)
    apellidopaterno = models.CharField(max_length=45,null=False)
    apellidomaterno = models.CharField(max_length=45,null=False)
    curp= models.CharField(max_length=18,null=False,unique=True)
    email= models.EmailField(unique=True)
    estatusaspirante = models.ForeignKey(EstatusAspirante, on_delete=models.CASCADE)
    Usuario=models.IntegerField(null=False)
    def __str__(self):
        return self.nombre + " "+ self.apellidopaterno + " " + self.apellidomaterno



class ExamenSeneval(models.Model):
    ICNE = models.IntegerField(null=False)
    PMA = models.IntegerField(null=False)
    PAN = models.IntegerField(null=False)
    ELE = models.IntegerField(null=False)
    CLE = models.IntegerField(null=False)
    MET = models.IntegerField(null=False)
    ICL = models.IntegerField(null=False)
    IUG = models.IntegerField(null=False)
    aspirante = models.OneToOneField(Aspirante, on_delete=models.CASCADE)

class EstatusRequisitoEstudiante(models.Model):
    nombre = models.CharField(max_length=45, null=False) 
    descripcion = models.CharField(max_length=85,null=False)
    def __str__(self):
        return self.nombre



class Requisito(models.Model):
    nombre = models.CharField(max_length=45, null=False)
    descripcion = models.CharField(max_length=85, null= False)
    detalle = models.ManyToManyField(Aspirante, through='DetalleRequisito')
    def __str__(self):
        return self.nombre

    

class DetalleRequisito(models.Model):
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE)
    requisito = models.ForeignKey(Requisito, on_delete=models.CASCADE)
    ruta = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True)
    observaciones = models.CharField(max_length=85,blank=True, null=True)
    estatus = models.ForeignKey(EstatusRequisitoEstudiante, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.aspirante) + str(self.requisito)




class Docente(models.Model):
    Nombre = models.CharField(max_length=45,null = False)
    ApellidoPaterno= models.CharField(max_length=45,null=False)
    ApellidoMaterno= models.CharField(max_length=45,null=False)
    Curp= models.CharField(max_length=18, null=False, unique=True)
    Rfc=models.CharField(max_length=13,null=False, unique=True)
    CedulaProfesional = models.CharField(max_length=8, null=False, unique=True)
    Email = models.EmailField(null=False, unique=True)
    def __str__(self):
        return self.Nombre + " "+ self.ApellidoPaterno + " " + self.ApellidoMaterno


class Entrevista(models.Model):
    Fecha = models.DateField()
    HoraInicio = models.TimeField()
    HoraFinal = models.TimeField()
    Observaciones = models.CharField(max_length=45,blank=True, null=True)
    aspirante= models.OneToOneField(Aspirante, on_delete=models.CASCADE)
    DetalleEntrevista = models.ManyToManyField(Docente,through='DetalleEntrevista')
    def __int__(self):
        return self.id  

class DetalleEntrevista(models.Model):
    entrevista = models.ForeignKey(Entrevista, on_delete=models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.docente) + " " + str(self.entrevista)


class CursoPropedeutico(models.Model):
    Clave = models.CharField(max_length=45,null=False)
    FechaInicio= models.DateField()
    FechaFinalizacion= models.DateField()
    HoraInicio= models.TimeField()
    HoraFinalizacion = models.TimeField()
    docente = models.ForeignKey(Docente,on_delete=models.CASCADE)
    def __int__(self):
        return self.pk
    



class DetalleAspiranteCurso(models.Model):
    aspirante = models.ForeignKey(Aspirante, on_delete=models.CASCADE)
    cursopropedeutico = models.ForeignKey(CursoPropedeutico, on_delete=models.CASCADE)
    Calificacion= models.IntegerField(null=False)





class CatalogoPregunta(models.Model):
    Pregunta= models.CharField(max_length=200, null=False)
    descripcion = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.Pregunta


    

class Encuesta(models.Model):
    FechaHora=models.DateTimeField(blank=True,null=True)
    Observaciones= models.CharField(max_length=100,blank=True, null=True)
    detalleentrevista= models.OneToOneField(DetalleEntrevista,on_delete=models.CASCADE)
    detalleEncuesta = models.ManyToManyField(CatalogoPregunta, through='DetalleEncuesta')


class DetalleEncuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    catalogopreguntas = models.ForeignKey(CatalogoPregunta, on_delete=models.CASCADE)
    Respuesta = models.CharField(max_length=150,blank=True, null=True)



class Criterio(models.Model):
    Criterio=models.CharField(max_length=50,null=False)
    

class Rubrica(models.Model):
    Rubrica=models.CharField(max_length=50,null=False)
    detallecriteriorubricas = models.ManyToManyField(Criterio, through='DetalleCriterioRubrica')



class DetalleCriterioRubrica(models.Model):
    Descripcion = models.CharField(max_length=100,null=False)
    valor= models.IntegerField(null=False)
    rubrica=models.ForeignKey(Rubrica,on_delete=models.CASCADE)
    criterio=models.ForeignKey(Criterio,on_delete=models.CASCADE)

    
class Ponencia(models.Model):
    FechaHora=models.DateTimeField(blank=True,null=True)
    Observaciones= models.CharField(max_length=100,blank=True, null=True)
    detalleentrevista= models.OneToOneField(DetalleEntrevista,on_delete=models.CASCADE)
    detallePonencia = models.ManyToManyField(Criterio, through='DetallePonencia')


class DetallePonencia(models.Model):
    ponencia=models.ForeignKey(Ponencia,on_delete=models.CASCADE)
    criterio=models.ForeignKey(Criterio,on_delete=models.CASCADE)
    criterio=models.ForeignKey(Criterio,on_delete=models.CASCADE)








