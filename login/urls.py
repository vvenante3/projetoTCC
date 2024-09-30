from django.contrib import admin
from django.urls import path, include
from .views import pagina_login, pagina_cadastro, editar_usuario

urlpatterns = [
    # LOGIN
    path('',            pagina_login,       name='pagina_login'),

    # CADASTRO
    path('cadastro/',   pagina_cadastro,    name='pagina_cadastro'),

    # EDITAR CADASTRO
    path('editar_usuario/', editar_usuario, name='editar_usuario'),
]