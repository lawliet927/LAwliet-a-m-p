from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Página de inicio
    path('projects/', views.project_list, name='project_list'),  # Lista de proyectos
    path('project/<int:pk>/', views.project_detail, name='project_detail'),  # Detalle del proyecto
    path('project/new/', views.create_project, name='create_project'),  # Crear un nuevo proyecto
    path('project/<int:pk>/task/new/', views.create_task, name='create_task'),  # Crear tarea nueva
    path('toggle-task-completion/', views.toggle_task_completion, name='toggle_task_completion'),  # Completar tarea
    path('project/edit/<int:pk>/', views.edit_project, name='edit_project'),  # Editar proyecto
    path('project/delete/<int:pk>/', views.delete_project, name='delete_project'),  # Eliminar proyecto
]