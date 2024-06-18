from django.contrib import admin
from django.urls import path, include
from .views import participante, salvar_participante, editar_participante, atualizar_participante, deletar_participante, analisar_participante

urlpatterns = [
    # CADASTRO PARTICIPANTES
    path('',                                participante,               name='participante'),
    path('salvar_participante/',            salvar_participante,        name='salvar_participante'),
    path('editar_participante/<int:id>',    editar_participante,        name='editar_participante'),
    path('atualizar_participante/<int:id>', atualizar_participante,     name='atualizar_participante'),
    path('deletar_participante/<int:id>',   deletar_participante,       name='deletar_participante'),
    path('analisar_participante/<int:id>',  analisar_participante,      name='analisar_participante')
]