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

def guardarTarea(request):
    informacion_tarea = json.load(request)
    descripcion = informacion_tarea.get('descripcion')
    fechaCreacion = informacion_tarea.get('fechaCreacion')
    fechaEntrega = informacion_tarea.get('fechaEntrega')
    estadoTarea = informacion_tarea.get('estadoTarea')
    print(descripcion)
    print(fechaCreacion)
    print(fechaEntrega)
    print(estadoTarea)
    tareasExamen(fechaCreacion=fechaCreacion,fechaEntrega=fechaEntrega,descripcion=descripcion,estadoTarea=estadoTarea).save()
    newTask = tareasExamen.objects.latest('id')
    nueva_tarea = [newTask.id,fechaCreacion,fechaEntrega,descripcion,estadoTarea]
    
    return JsonResponse({
        'tarea': nueva_tarea
    })
    
    


def eliminarTarea(request):
    id_daeliminar = request.GET.get('id')
    tarea_eliminar = tareasExamen.objects.get(id=id_daeliminar)
    tarea_eliminar_lista = [tarea_eliminar.id,tarea_eliminar.fechaCreacion,tarea_eliminar.fechaEntrega,tarea_eliminar.descripcion,tarea_eliminar.estadoTarea]
    tareasExamen.objects.get(id=id_daeliminar).delete()
    return JsonResponse({
        'eliminar_tarea':tarea_eliminar_lista
    })

def actualizar_tarea(request,ind):
    usuario_eliminar = usuariosFinal.objects.get(id=ind)
    if usuario_eliminar.usuario.username == 'admin':
        return HttpResponseRedirect(reverse('usuarios'))
    else:
        usuario_eliminar.usuario.delete()
        usuario_eliminar.delete()
        return HttpResponseRedirect(reverse('usuarios'))