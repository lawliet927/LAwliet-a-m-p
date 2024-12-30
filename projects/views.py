from tokenize import Comment
from django.contrib import messages  # Importar mensajes flash correctamente
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task,Comment



def homepage(request):
    return render(request, 'homepage.html')
# Lista de proyectos
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


# Detalles del proyecto
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    # Eliminar tarea
    if 'delete_task' in request.POST:
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        task.delete()  # Eliminar la tarea
        messages.success(request, "La tarea se ha eliminado exitosamente.")
        return redirect('project_detail', pk=pk)  # Redirigir de nuevo a la página del proyecto

    if request.method == 'POST':
        # Agregar comentario
        if 'add_comment' in request.POST:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            author = request.POST.get('author', '').strip()
            content = request.POST.get('content', '').strip()

            # Validar que el autor y el contenido no estén vacíos
            if author and content:
                Comment.objects.create(task=task, author=author, content=content)
                messages.success(request, "Se ha agregado un comentario exitosamente.")

            return redirect('project_detail', pk=pk)

        # Finalizar tarea
        elif 'complete_task' in request.POST:
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            task.completed = True
            task.save()
            messages.success(request, "La tarea se ha finalizado exitosamente.")
            return redirect('project_detail', pk=pk)

    context = {
        'project': project,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'progress': progress,
    }
    return render(request, 'project_detail.html', context)



# Crear nuevo proyecto
def create_project(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        deadline = request.POST.get('deadline', '')

        if name and description and deadline:
            Project.objects.create(name=name, description=description, deadline=deadline)
            return redirect('project_list')

        return render(request, 'create_project.html', {'project_name': 'Proyecto', 'error': 'Todos los campos son obligatorios.'})
    
    return render(request, 'create_project.html', {'project_name': 'Proyecto'})

# Crear nueva tarea

def create_task(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('deadline')  # Cambia esto si usas 'due_date'
        assigned_to = request.POST.get('assigned_to')

        # Verifica los valores antes de guardar
        if title and description and due_date and assigned_to:
            Task.objects.create(
                project=project,
                title=title,
                description=description,
                due_date=due_date,
                assigned_to=assigned_to
            )
            # Agregar mensaje de éxito antes de redirigir
            messages.success(request, "Nueva tarea agregada.")
            return redirect('project_detail', pk=pk)
        
        # Si alguno de los campos está vacío, no crear la tarea
        messages.error(request, "Todos los campos son obligatorios.")
        return redirect('project_detail', pk=pk)
    
    return render(request, 'create_task.html', {'project_name': project.name})
# Actualizar estado de tarea
def toggle_task_completion(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed = request.POST.get('completed') == 'true'

        try:
            task = Task.objects.get(id=task_id)
            task.completed = completed
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tarea no encontrada.'})

# Editar proyecto
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        description = request.POST.get('description', '')
        deadline = request.POST.get('deadline', '')

        if name and description and deadline:
            project.name = name
            project.description = description
            project.deadline = deadline
            project.save()
            
            return redirect('project_list')
        

        return render(request, 'edit_project.html', {'project': project, 'error': 'Todos los campos son obligatorios.'})
    
    return render(request, 'edit_project.html', {'project': project})



# Eliminar proyecto
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    # Mensaje de éxito al eliminar
    messages.success(request, '¡Proyecto eliminado con éxito!')
    return redirect('project_list')

