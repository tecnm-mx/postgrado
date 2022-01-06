from django.contrib import admin

from .models import EstatusAspirante,Aspirante,EstatusRequisitoEstudiante,Requisito,DetalleRequisito, Docente,Entrevista,DetalleEntrevista,CursoPropedeutico,DetalleAspiranteCurso,ExamenSeneval, CatalogoPregunta,Encuesta,DetalleEncuesta,Criterio,Rubrica,DetalleCriterioRubrica,Ponencia,DetallePonencia


class ExamenSenevalAdmin(admin.ModelAdmin):
    list_display=('aspirante','ICNE','PMA','PAN','ELE','CLE','MET','ICL','IUG')

class ExamenSenevalline(admin.StackedInline):
    model=ExamenSeneval
    
class DetalleRequisitoline(admin.StackedInline):
    model=DetalleRequisito

class AspiranteAdmin(admin.ModelAdmin):
    
    list_display = ('nombre','apellidopaterno','apellidomaterno','curp','email','estatusaspirante')
    inlines= [ExamenSenevalline]


class DocenteAdmin(admin.ModelAdmin):

    list_display = ('Nombre','ApellidoPaterno','ApellidoMaterno','Curp','Rfc','CedulaProfesional','Email')


class EstatusAspiranteAdmin(admin.ModelAdmin):

    list_display=('estatus','descripcion')

class DetalleEntrevistaline(admin.StackedInline):
    model=DetalleEntrevista
class DetalleEncuestaline(admin.StackedInline):
    model=DetalleEncuesta
class CatalogoPreguntaAdmin(admin.ModelAdmin):
    list_display=('Pregunta','descripcion')


class EncuestaAdmin(admin.ModelAdmin):
    inlines = [DetalleEncuestaline]

class EntrevistaAdmin(admin.ModelAdmin):
    inlines= [DetalleEntrevistaline]

class DetalleRequisitoAdmin(admin.ModelAdmin):
    list_display=('requisito','observaciones','estatus','aspirante','ruta')

class DetalleRequisitolineAdmin(admin.ModelAdmin):
    list_display=('Clave','FechaInicio','HoraInicio','docente')







admin.site.register(EstatusAspirante,EstatusAspiranteAdmin)
admin.site.register(Aspirante,AspiranteAdmin)
admin.site.register(EstatusRequisitoEstudiante)
admin.site.register(Requisito)
admin.site.register(DetalleRequisito,DetalleRequisitoAdmin)
admin.site.register(Docente,DocenteAdmin)
admin.site.register(Entrevista,EntrevistaAdmin)
admin.site.register(DetalleEntrevista)
admin.site.register(CursoPropedeutico)
admin.site.register(DetalleAspiranteCurso)
admin.site.register(ExamenSeneval,ExamenSenevalAdmin)
admin.site.register(CatalogoPregunta,CatalogoPreguntaAdmin)
admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(DetalleEncuesta)

admin.site.register(Criterio)
admin.site.register(Rubrica)
admin.site.register(DetalleCriterioRubrica)
admin.site.register(Ponencia)
admin.site.register(DetallePonencia)
