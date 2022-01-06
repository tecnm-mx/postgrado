from typing import ChainMap
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context, loader
from .models import Aspirante, CatalogoPregunta, DetalleEncuesta, DetalleEntrevista, Docente, Encuesta, Entrevista, EstatusAspirante,Requisito,EstatusRequisitoEstudiante,DetalleRequisito,DetalleAspiranteCurso,CursoPropedeutico
from django.urls import reverse
from django.views import generic
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User






"""def index(request):
    latest_estatusalumno_list = EstatusAlumno.objects.order_by('estatus')
    context = {'latest_estatusalumno_list':latest_estatusalumno_list,}
    return render(request,'InscripcionCandidatos/Index.html',context)
    template= loader.get_template('InscripcionCandidatos/Index.html')
    return HttpResponse(template.render(context,request))

    output = ','.join([q.descripcion for q in latest_estatusalumno_list])    
    return HttpResponse(output)"""


class IndexView(generic.ListView):
    template_name = 'InscripcionCandidatos/index.html'
    context_object_name = 'latest_estatusalumno_list'
    
    def get_queryset(self):
        """Return the last five published questions."""
        return EstatusAspirante.objects.order_by('estatus')




"""def detail(request, estatus_id):
    
    try:
        estatusalumno = EstatusAlumno.objects.get(pk=estatus_id)
    except EstatusAlumno.DoesNotExist:
        raise Http404("Estatus no Existe")
    return render(request,'InscripcionCandidatos/detail.html',{'estatusalumno':estatusalumno})
    

    estatusalumno = get_object_or_404(EstatusAlumno,pk=estatus_id)
    return render(request,'InscripcionCandidatos/detail.html',{'estatusalumno':estatusalumno})"""

class DetailView(generic.DetailView):
    model = EstatusAspirante
    template_name = 'InscripcionCandidatos/detail.html'
   

"""def results(request, estatus_id):
    estatusalumno = get_object_or_404(EstatusAlumno, pk=estatus_id)
    return render(request, 'InscripcionCandidatos/results.html', {'estatusalumno': estatusalumno})"""


class ResultsView(generic.DetailView):
    model = EstatusAspirante
    template_name = 'InscripcionCandidatos/results.html'

def asignar(request, estatus_id):
    estatusalumnos = get_object_or_404(EstatusAspirante, pk=estatus_id)
    try:
        selected_aspirante = estatusalumnos.aspirante_set.get(pk=request.POST['aspirante'])
    except (KeyError, Aspirante.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'InscripcionCandidatos/detail.html', {
            'estatusalumno': estatusalumnos,
            'error_message': "You didn't select a choice.",
        })
    else:
        nuevoestatus = get_object_or_404(EstatusAspirante, pk=4)
        selected_aspirante.estatusalumno = nuevoestatus
        selected_aspirante.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('InscripcionCandidatos:results', args=(estatusalumnos.id,)))

"""
def login(request):
    m = Member.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")
"""

def Login(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('InscripcionCandidatos:index'))
        
    if request.method=='POST':
        if request.user.is_authenticated:
            return render(request, 'InscripcionCandidatos/index.html')
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                try:
                    aspirante = Aspirante.objects.get(email=request.user.email)
                    
                except Aspirante.DoesNotExist:
                    try:
                        docente = Docente.objects.get(Email=request.user.email)
                    except Docente.DoesNotExist:
                         logout(request)
                         return render(request,'InscripcionCandidatos/Login.html',{'error_message':'La Cuenta No Tiene Accesso'})
                    return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))  
                return HttpResponseRedirect(reverse('InscripcionCandidatos:index'))    
            else:
                return render(request,'InscripcionCandidatos/Login.html',{'error_message':'Cuenta o Contraseña Equivocada'})
    else:
        return render(request, 'InscripcionCandidatos/Login.html')
         
def Registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('InscripcionCandidatos:index'))
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            email= request.POST['email']
            user = User.objects.create_user(username,email,password)
            statusA = get_object_or_404(EstatusAspirante, pk=1)
            statusR = get_object_or_404(EstatusRequisitoEstudiante, pk=1)
            aspirante = Aspirante.objects.create(nombre=request.POST['nombre'],apellidopaterno=request.POST['apellidopaterno'],apellidomaterno=request.POST['apellidomaterno'],curp=request.POST['curp'],email=user.email,estatusaspirante=statusA,Usuario=user.id)
            ListaRequisitos = Requisito.objects.all()
            

            for requisitoN in ListaRequisitos:

                detalle = DetalleRequisito.objects.create(aspirante=aspirante,requisito=requisitoN,estatus=statusR,observaciones="--------")

            
            return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))

        else:
            return render(request, 'InscripcionCandidatos/Registro.html')
        
    return render(request, 'InscripcionCandidatos/Registro.html')



def index(request):
    if request.user.is_authenticated:

        try:
            aspirante01 = Aspirante.objects.get(email=request.user.email)
        except Aspirante.DoesNotExist:
            return HttpResponseRedirect(reverse('InscripcionCandidatos:Logout'))
        statusA= get_object_or_404(EstatusRequisitoEstudiante,pk=4)
        statusN= get_object_or_404(EstatusRequisitoEstudiante,pk=1)
        ListaRequisitos=DetalleRequisito.objects.filter(aspirante=aspirante01).order_by('id')
        listaaspirantecurso = DetalleAspiranteCurso.objects.filter(aspirante=aspirante01).order_by('cursopropedeutico')
        
        listaCurso = []
        
        for curso in listaaspirantecurso:
            listaCurso.append(get_object_or_404(CursoPropedeutico,pk=curso.cursopropedeutico) )

        # Pendiente para cuando tenga mas tienpo ListaCursosAspirante=list(ChainMap(listaaspirantecurso, listaCurso))
        return render(request,'InscripcionCandidatos/index.html',{'aspirante':aspirante01,'ListaRequisitos':ListaRequisitos,'ListaCurso':listaCurso,'listaaspirantecurso':listaaspirantecurso,'statusA':statusA,'statusN':statusN})
        
    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))



def UploadFile(request):

    if request.method == "POST":
        
        # Fetching the form data
        if request.FILES:
            requitisoid = request.POST['id']
            ListaRequisitos=get_object_or_404(DetalleRequisito,id=requitisoid)
            status =get_object_or_404(EstatusRequisitoEstudiante,pk=2)
            # Saving the information in the database
            ListaRequisitos.ruta = request.FILES['uploadedFile']
            ListaRequisitos.estatus=status
            ListaRequisitos.save()
           
        else:
            return HttpResponseRedirect(reverse('InscripcionCandidatos:index'))

    return HttpResponseRedirect(reverse('InscripcionCandidatos:index'))


def Logout(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            logout(request)
            return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))
        return HttpResponseRedirect(reverse('InscripcionCandidatos:index'))
    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))




def Subir(request,requisito_id):
    return render(request, 'InscripcionCandidatos/Subir.html',{'requisito_id':requisito_id})


def Maestro(request):

    if request.user.is_authenticated:

        try:
            docente1 = Docente.objects.get(Email=request.user.email)
        except Docente.DoesNotExist:
            return HttpResponseRedirect(reverse('InscripcionCandidatos:Logout'))
        listadocentecurso = CursoPropedeutico.objects.filter(docente=docente1).order_by('pk')

        
        try:
            listaendetalletrevista = DetalleEntrevista.objects.filter(docente=docente1).order_by('pk')
        except DetalleEntrevista.DoesNotExist:
            return render(request,'InscripcionCandidatos/Maestro.html',{'Docente':docente1,'listadocentecurso':listadocentecurso})
        
        listaentrevista = []
        
        for detalleentrevista in listaendetalletrevista:
            listaentrevista.append(get_object_or_404(Entrevista,pk=detalleentrevista.entrevista) )
        
        fecha=datetime.now()
        return render(request,'InscripcionCandidatos/Maestro.html',{'Docente':docente1,'listadocentecurso':listadocentecurso,'listaentrevista':listaentrevista,'fecha':fecha.date()})

    
    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))

def Calificar(request):

    if request.user.is_authenticated:
        
        if request.method == "POST":
            idCurso=request.POST['id']
            try:
                listaalumnocurso = DetalleAspiranteCurso.objects.filter(cursopropedeutico=idCurso).order_by('pk')
            except Docente.DoesNotExist:
                 return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
            
            try:
                docente1 = Docente.objects.get(Email=request.user.email)
            except Docente.DoesNotExist:
                return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
            return render(request,'InscripcionCandidatos/Curso.html',{'listaalumnocurso':listaalumnocurso,'Docente':docente1})
        return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
           
    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))

def Curso(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            idCalificacion=request.POST['id']

            try:
                calificacion=request.POST['calificacion']
                calificaion=get_object_or_404(DetalleAspiranteCurso,pk=idCalificacion)
                calificaion.Calificacion=calificacion
                calificaion.save()
                try:
                    listaalumnocurso = DetalleAspiranteCurso.objects.filter(cursopropedeutico=calificaion.cursopropedeutico).order_by('pk')
                except Docente.DoesNotExist:
                 return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
                
                try:
                    docente1 = Docente.objects.get(Email=request.user.email)
                except Docente.DoesNotExist:
                    return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
                return render(request,'InscripcionCandidatos/Curso.html',{'listaalumnocurso':listaalumnocurso,'Docente':docente1})
            except KeyError:
                idCurso=request.POST['id']
                try:
                     listaalumnocurso = DetalleAspiranteCurso.objects.filter(cursopropedeutico=idCurso).order_by('pk')
                except Docente.DoesNotExist:
                    return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
                
                
                try:
                    docente1 = Docente.objects.get(Email=request.user.email)
                except Docente.DoesNotExist:
                    return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
                return render(request,'InscripcionCandidatos/Curso.html',{'listaalumnocurso':listaalumnocurso,'Docente':docente1})
        return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))   

    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))



def Encuestas(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            identrevista = request.POST['idEntrevista']
            docente1 = Docente.objects.get(Email=request.user.email)
            entrevista =get_object_or_404(DetalleEntrevista,entrevista=identrevista,docente=docente1)
            fecha=datetime.now()

            try:
                Encuesta01 = Encuesta.objects.get(detalleentrevista=entrevista)
            except Encuesta.DoesNotExist:
                 Encuesta01 = Encuesta.objects.create(FechaHora=fecha,detalleentrevista=entrevista,Observaciones="--------")
                 ListaPreguntas = CatalogoPregunta.objects.all()
                 
                 for pregunta in ListaPreguntas:
                     detalle = DetalleEncuesta.objects.create(encuesta=Encuesta01,catalogopreguntas=pregunta,Respuesta="--------")
                 
                 listapreguntas = DetalleEncuesta.objects.filter(encuesta=Encuesta01).order_by('pk')
                 return render(request,'InscripcionCandidatos/Encuesta.html',{'listapreguntas':listapreguntas,'entrevista':entrevista,'Encuesta01':Encuesta01})
                 


            listapreguntas = DetalleEncuesta.objects.filter(encuesta=Encuesta01).order_by('pk')
            return render(request,'InscripcionCandidatos/Encuesta.html',{'Docente':docente1,'listapreguntas':listapreguntas,'entrevista':entrevista,'Encuesta01':Encuesta01.id})
        return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
   
    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))


def SaveEncuesta(request):

    if request.user.is_authenticated:
        if request.method == "POST":
            Encuesta01 = Encuesta.objects.get(pk=request.POST['Encuestaid'])
            listapreguntas = DetalleEncuesta.objects.filter(encuesta=Encuesta01).order_by('pk')
            for pregunta in listapreguntas:
                pregunta.Respuesta=request.POST[str(pregunta.id)]
                pregunta.save()
            Encuesta01.Observaciones=request.POST['observaciones']
            Encuesta01.save()
            return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
        return HttpResponseRedirect(reverse('InscripcionCandidatos:Maestro'))
    return HttpResponseRedirect(reverse('InscripcionCandidatos:Login'))
    
    