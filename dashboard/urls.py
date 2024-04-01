from django.urls import path, include
from .views import dashboard
from django.shortcuts import redirect

urlpatterns = [
    path('', dashboard, name='dashboard'),
]