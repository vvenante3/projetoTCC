from django.contrib import admin
from django.urls import path, include
from .views import pagina_login, pagina_logout, pagina_cadastro, editar_usuario, enviar_codigo_email

urlpatterns = [
    # LOGIN
    path('',                pagina_login,       name='pagina_login'),

    # DESLOGAR
    path('logout/',         pagina_logout,      name='deslogar_usuario'),

    # CADASTRO
    path('cadastro/',       pagina_cadastro,    name='pagina_cadastro'),

    # EDITAR CADASTRO
    path('editar_usuario/', editar_usuario,     name='editar_usuario'),

    # ESQUECI MINHA SENHA
    path('codigo_email/',   enviar_codigo_email, name='codigo_email'),

]