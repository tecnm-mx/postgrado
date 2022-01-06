from django.contrib.auth import authenticate, login, logout
from django.core import exceptions
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import Alumno,DetalleRequisito, Semestre,EstatusRequisitoAlumno,Requisito

def index(request):
    if request.user.is_authenticated:

        try:
            alumno01 = Alumno.objects.get(email=request.user.email)
        except Alumno.DoesNotExist:
            return HttpResponseRedirect(reverse('EgresadosMaestria:Logout'))
        statusA= get_object_or_404(EstatusRequisitoAlumno,pk=4)
        statusN= get_object_or_404(EstatusRequisitoAlumno,pk=1)
        requisitossemestre = Requisito.objects.filter(semestre=alumno01.alumnosemestre)
        listasemestre= Semestre.objects.all() 
        ListaRequisitos = []
        
        for requisitos in requisitossemestre:
            ListaRequisitos.append(get_object_or_404(DetalleRequisito,alumno=alumno01, requisito=requisitos) )
        return render(request,'EgresadosMaestria/index.html',{'alumno':alumno01,'ListaRequisitos':ListaRequisitos,'statusA':statusA,'statusN':statusN,'listasemestre':listasemestre})
        
    return HttpResponseRedirect(reverse('EgresadosMaestria:Login'))


def Login(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('EgresadosMaestria:index'))
        
    if request.method=='POST':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('EgresadosMaestria:index'))
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    alumno = Alumno.objects.get(email=user.email)
                except Alumno.DoesNotExist:
                    logout(request)
                    return render(request,'EgresadosMaestria/Login.html',{'error_message':'La Cuenta No Tiene Accesso'})
                return HttpResponseRedirect(reverse('EgresadosMaestria:index'))
            else:
                return render(request,'EgresadosMaestria/Login.html',{'error_message':'Cuenta o Contraseña Equivocada'})
    else:
        return render(request, 'EgresadosMaestria/Login.html')
    
def Registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('EgresadosMaestria:Inicio'))
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            email= request.POST['email']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return render(request, 'EgresadosMaestria/Registro.html',{'error_message':'El usuario ya Existe'})
            
            user = User.objects.create_user(username,email,password)
            semestre = get_object_or_404(Semestre, pk=1)
            statusR = get_object_or_404(EstatusRequisitoAlumno, id=1)
            try: 
                alumno = Alumno.objects.create(nombre=request.POST['nombre'],apellidopaterno=request.POST['apellidopaterno'],apellidomaterno=request.POST['apellidomaterno'],curp=request.POST['curp'],email=user.email,NumeroControl=request.POST['numerocontrol'], alumnosemestre=semestre,Usuario=user.id)
            except 	IntegrityError:
                user.delete()
                return render(request, 'EgresadosMaestria/Registro.html',{'error_message':'El verifique sus informacion'})
            
            
            ListaRequisitos = Requisito.objects.all()
            for requisitoN in ListaRequisitos: 
                detalle = DetalleRequisito.objects.create(alumno=alumno,requisito=requisitoN,estatusrequisitoalumno=statusR,observaciones=" ")
            
            return HttpResponseRedirect(reverse('EgresadosMaestria:Login'))
        else:
            return render(request, 'EgresadosMaestria/Registro.html')
        
    return render(request, 'EgresadosMaestria/Registro.html')


def UploadFile(request):


    if request.method == "POST":
        
        # Fetching the form data
        

        # Saving the information in the database
        if request.FILES:
            requitisoid = request.POST['id']
            ListaRequisitos=get_object_or_404(DetalleRequisito,id=requitisoid)
            status =get_object_or_404(EstatusRequisitoAlumno,pk=2)
            ListaRequisitos.ruta = request.FILES['uploadedFile']
            ListaRequisitos.estatusrequisitoalumno=status
            ListaRequisitos.observaciones=" "
            ListaRequisitos.save()
            
        else:
            return HttpResponseRedirect(reverse('EgresadosMaestria:index'))

    return HttpResponseRedirect(reverse('EgresadosMaestria:index'))

def Subir(request,requisito_id):
    requisitoAlumno= get_object_or_404(DetalleRequisito,pk=requisito_id)
    requisito01= get_object_or_404(Requisito,nombre=requisitoAlumno.requisito)

    return render(request, 'EgresadosMaestria/Subir.html',{'requisito_id':requisito_id,'Descripcion':requisito01.descripcion})

def VSemestre(request,semestre_id):
    if request.user.is_authenticated:

        try:
            alumno01 = Alumno.objects.get(email=request.user.email)
        except Alumno.DoesNotExist:
            return HttpResponseRedirect(reverse('EgresadosMaestria:Logout'))
        statusA= get_object_or_404(EstatusRequisitoAlumno,pk=4)
        statusN= get_object_or_404(EstatusRequisitoAlumno,pk=1)
        requisitossemestre = Requisito.objects.filter(semestre=semestre_id)
        listasemestre= Semestre.objects.all() 
        ListaRequisitos = []
        
        for requisitos in requisitossemestre:
            ListaRequisitos.append(get_object_or_404(DetalleRequisito,alumno=alumno01, requisito=requisitos) )
        return render(request,'EgresadosMaestria/index.html',{'alumno':alumno01,'ListaRequisitos':ListaRequisitos,'statusA':statusA,'statusN':statusN,'listasemestre':listasemestre})
        
    return HttpResponseRedirect(reverse('EgresadosMaestria:Login'))



def Logout(request):
    if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(reverse('EgresadosMaestria:Login'))
    return HttpResponseRedirect(reverse('EgresadosMaestria:Login'))