from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserApp


@login_required
def dashboard(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем список приложений для текущего пользователя
    user_apps = UserApp.objects.filter(user=user).first()
    if user_apps:
        apps = user_apps.app.all().order_by('name')
    else:
        apps = []

    context = {
        'apps': apps
    }
    return render(request, 'dashboard/dashboard.html', context)


