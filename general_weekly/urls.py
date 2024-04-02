from django.urls import path
from .views import general_weekly


urlpatterns = [
    path('', general_weekly, name='general_weekly'),  # Маршрут по умолчанию
]