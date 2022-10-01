from . import views
from django.urls import path

app_name = 'examenFinal'

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('obtener_info_tarea',views.obtener_info_tarea, name='obtener_info_tarea'),
    path('guardarTarea',views.guardarTarea,name='guardarTarea'),
    path('eliminarTarea',views.eliminarTarea,name='eliminarTarea'),

    path('actualizar_tarea',views.actualizar_tarea,name='actualizar_tarea'),
]