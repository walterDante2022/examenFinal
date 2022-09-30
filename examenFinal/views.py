from ast import Pass
from django.shortcuts import render
from django.urls import reverse
from .models import tareasExamen, usuariosFinal
from django.http import HttpResponse,HttpResponseRedirect ,JsonResponse
import json

# Create your views here.
def index(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario')
        passwordUsuario = request.POST.get('passwordUsuario')
        #Validacion de informacion
        usuario_registrado = 0
        usuarios_totales = usuariosFinal.objects.all()

        for usuario in usuarios_totales:
            if usuario.usuario == nombreUsuario and usuario.contra == passwordUsuario:
                usuario_registrado = 1
        
        if usuario_registrado == 1:
            return HttpResponseRedirect(reverse('examenFinal:dashboard'))
        else:
            return render(request,'examenFinal/ingresar.html',{
                'mensaje':'Los datos ingresados son incorrectos',
            })
    return render(request,'examenFinal/ingresar.html')

def dashboard(request):
    return render(request,'examenFinal/dashboard.html',{
        'tareas_totales':tareasExamen.objects.all().order_by('id')
    })

def obtener_info_tarea(request):
    id_tarea=str(request.GET.get('id'))
    tarea=tareasExamen.objects.get(id=id_tarea)
    return JsonResponse({
        'tarea_detalle':{
            'id' : tarea.id ,
            'fechaCreacion' : tarea.fechaCreacion ,
            'fechaEntrega' : tarea.fechaEntrega,
            'descripcion' : tarea.descripcion ,
            'estadoTarea' : tarea.estadoTarea 
        }
    })

    
    


def eliminar_tarea(request,ind):
    usuario_eliminar = usuariosFinal.objects.get(id=ind)
    if usuario_eliminar.usuario.username == 'admin':
        return HttpResponseRedirect(reverse('usuarios'))
    else:
        usuario_eliminar.usuario.delete()
        usuario_eliminar.delete()
        return HttpResponseRedirect(reverse('usuarios'))

def actualizar_tarea(request,ind):
    usuario_eliminar = usuariosFinal.objects.get(id=ind)
    if usuario_eliminar.usuario.username == 'admin':
        return HttpResponseRedirect(reverse('usuarios'))
    else:
        usuario_eliminar.usuario.delete()
        usuario_eliminar.delete()
        return HttpResponseRedirect(reverse('usuarios'))