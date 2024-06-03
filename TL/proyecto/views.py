from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import views as auth_views
from .models import Proyecto
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .decorators import student_required, teacher_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404



def edicionCurso(request,id):
    curso=Proyecto.objects.get(id=id)
    return render(request,"edicionCurso.html",{"cursos":curso})

@login_required
def editarCursos(request):
    id = request.POST['curso_id']
    nProfesor="-"
    nProyecto= request.POST['nProyecto']
    tematica = request.POST['tematica']


    curso= Proyecto.objects.get(id=id)
    curso.nombre_profesor=nProfesor
    curso.nombre_proyecto=nProyecto
    curso.tema=tematica
    curso.save()
    messages.success(request,'¡Proyecto Actualizado!')
    return redirect('/student')

@login_required
def crearProyecto(request):
    if request.method == 'POST':
        nProyecto = request.POST.get('nProyecto')
        tematica = request.POST.get('tematica')
        
        # Obtener el nombre del usuario autenticado
        nombre_estudiante = request.user.get_full_name()
        if not nombre_estudiante:  # Si el nombre completo no está configurado, usa el nombre de usuario
            nombre_estudiante = request.user.username

        nuevo_proyecto = Proyecto(
            nombre_estudiante=nombre_estudiante,
            nombre_proyecto=nProyecto,
            tema=tematica,
        )
        nuevo_proyecto.save()
        messages.success(request, '¡Proyecto Creado Exitosamente!')
        return redirect('/student')
    else:
        return render(request, 'crearProyecto.html')

#logeo

@login_required
def products(request):
    return redirect('/')

def exit(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login_redirect')
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'registration/login.html')




@login_required
def proyectos_estudiante(request):
    if not request.user.groups.filter(name='Estudiante').exists():
        return redirect('access_denied')  # Redirige si el usuario no es parte del grupo estudiantes

    proyectos = Proyecto.objects.all()

    return render(request, 'student.html', {
        'proyectos': proyectos,
        'usuario_actual': request.user
    })

@login_required
def proyectos_profesor(request):
    if not request.user.groups.filter(name='Profesor').exists():
        return redirect('access_denied')  # Redirige si el usuario no es parte del grupo profesores

    filtro = request.GET.get('filtro', 'todos')
    if filtro == 'sin_patrocinio':
        proyectos = Proyecto.objects.filter(nombre_profesor='-')
    else:
        proyectos = Proyecto.objects.all()

    return render(request, 'teacher.html', {'proyectos': proyectos, 'filtro': filtro})

@login_required
def teacher_view(request):
    user_groups = request.user.groups.all()
    is_teacher = any(group.name == 'Profesor' for group in user_groups)
    if not is_teacher:
        return HttpResponse("Permisos denegados para vista de profesores")
    return render(request, 'teacher.html', {'groups': user_groups})


def permission_denied_view(request):
    return render(request, '403.html', status=403)

@login_required
def students_view(request):
    proyectos = Proyecto.objects.filter(Estudiante=request.user)
    return render(request, "students.html", {"proyectos": proyectos}) 

@login_required
def teachers_view(request):
    proyectos = Proyecto.objects.filter(Profesor=request.user)
    return render(request, "teacher.html", {"proyectos": proyectos}) 

@login_required
def patrocinar_proyecto(request, proyecto_id):
    if not request.user.groups.filter(name='Profesor').exists():
        return redirect('access_denied')  # Redirige si el usuario no es parte del grupo profesores

    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.nombre_profesor = request.user.get_full_name()  # Asigna el nombre completo del usuario actual
    proyecto.save()

    return HttpResponseRedirect('/teacher/')

def proyectos_anonimos(request):
    tematica_seleccionada = request.GET.get('tematica', '')

    # Filtrar proyectos con patrocinio del profesor
    proyectos = Proyecto.objects.exclude(nombre_profesor='-')
    
    if tematica_seleccionada:
        proyectos = proyectos.filter(tema=tematica_seleccionada)

    # Obtener temáticas únicas de los proyectos patrocinados para el filtro
    tematicas = Proyecto.objects.exclude(nombre_profesor='-').values_list('tema', flat=True).distinct()

    return render(request, 'tabla.html', {
        'proyectos': proyectos,
        'tematicas': tematicas,
        'tematica_seleccionada': tematica_seleccionada,
    })


@login_required
def login_redirect(request):
    if request.user.groups.filter(name='Profesor').exists():
        return redirect('teacher')
    elif request.user.groups.filter(name='Estudiante').exists():
        return redirect('student')
    else:
        return redirect('access_denied')