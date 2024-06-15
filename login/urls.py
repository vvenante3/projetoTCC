from django.contrib import admin
from django.urls import path, include
from .views import pagina_login, pagina_cadastro

urlpatterns = [
    # LOGIN
    path('',            pagina_login,       name='pagina_login'),

    # CADASTRO
    path('cadastro/',   pagina_cadastro,    name='pagina_cadastro'),

]