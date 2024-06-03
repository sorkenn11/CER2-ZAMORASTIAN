from django.urls import path
from . import views

urlpatterns= [
    path('',views.proyectos_anonimos),
    path('edicionCurso/<int:id>',views.edicionCurso,name="edicion_curso"),
    path('editarCursos/',views.editarCursos , name="editar_cursos"),
    path('crearProyecto/', views.crearProyecto, name='crear_proyecto'),
    path('student/', views.proyectos_estudiante, name='student'),
    path('student/edicionCurso/<int:id>',views.edicionCurso , name="edicion"),
    path('student/crearProyecto/',views.crearProyecto, name="crearEstudiante"),
    path('access-denied/', views.permission_denied_view, name='access_denied'),
    path('products/',views.products,name='products'),
    path('logout/',views.exit,name="exit"),
    path('teacher/', views.proyectos_profesor, name='teacher'),
    path('teacher/patrocinar/<int:proyecto_id>/',views.patrocinar_proyecto,name="patrocinar_proyecto"),
    path('login/', views.login_view, name='login'),
    path('login_redirect/', views.login_redirect, name='login_redirect'),

]