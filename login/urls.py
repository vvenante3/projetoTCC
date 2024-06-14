from django.contrib import admin
from django.urls import path, include
from .views import pagina_login

urlpatterns = [
    #     LOGIN
    path('', pagina_login, name='pagina_login'),
]