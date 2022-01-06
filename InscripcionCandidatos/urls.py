from os import name
from django.urls import  path
from . import  views 
app_name = 'InscripcionCandidatos'
urlpatterns =  [
    #path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(),name='results'),
    path('<int:estatus_id>/asignar/',views.asignar,name='asignar'),
    path('Login/',views.Login,name='Login'),
    path('Registro/',views.Registro,name='Registro'),
    path('',views.index,name='index'),
    path('UploadFile/',views.UploadFile,name='UploadFile'),
    path('Riquisito/<int:requisito_id>/',views.Subir,name='Subir'),
    path('Logout/',views.Logout,name='Logout'),
    path('Maestro/',views.Maestro,name='Maestro'),
    path('Curso/',views.Curso,name='Curso'),
    path('Calificar/',views.Calificar,name='Calificar'),
    path('Encuesta/',views.Encuestas,name='Encuesta'),
    path('SaveEncuesta/',views.SaveEncuesta,name='SaveEncuesta'),
]

