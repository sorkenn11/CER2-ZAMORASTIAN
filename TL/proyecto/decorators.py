from django.core.exceptions import PermissionDenied
from functools import wraps

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if any(group.name == group_name for group in request.user.groups.all()):
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator

student_required = group_required('Estudiantes')
teacher_required = group_required('Profesores')


