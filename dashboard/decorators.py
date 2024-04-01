from django.shortcuts import redirect
from functools import wraps
from .models import UserApp


def access_control_required(allowed_apps):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_apps = UserApp.objects.filter(user=request.user)
                user_app_names = [user_app.app.name for user_app in user_apps]
                # Проверяем, есть ли у пользователя доступ к приложению
                if set(allowed_apps).intersection(user_app_names):
                    return view_func(request, *args, **kwargs)
            return redirect('access_denied')
        return wrapper
    return decorator
