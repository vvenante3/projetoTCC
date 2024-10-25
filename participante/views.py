from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Participante
from datetime import date
from django.contrib.auth.decorators import login_required

import os
import cv2
import urllib.request
from django.conf import settings
from deepface import DeepFace
import matplotlib.pyplot as plt
import numpy as np

# PARTICIPANTE
@login_required(login_url='pagina_login')
def participante(request):
    # Verifica o login de Autenticação
    if request.user.is_authenticated:

        # Traz os dados que estão cadastrados em nosso Db
        participantes = Participante.objects.all()
        return render(request, "participante/index.html", {"participantes": participantes})
    return HttpResponse('Você precisa estar logado.')

def salvar_participante(request):
    if request.method == "POST":
        codigo          = request.POST['codigo']
        nome            = request.POST['nome']
        sobrenome       = request.POST['sobrenome']
        dataNascimento  = request.POST['dataNascimento']
        sexo            = request.POST['sexo']
        imagem          = request.FILES['imagem']

        # salvar no Db
        Participante.objects.create(codigo=codigo, nome=nome, sobrenome=sobrenome, dataNascimento=dataNascimento, sexo=sexo, imagem=imagem)
        participantes = Participante.objects.all()

    return redirect('participante')

def editar_participante(request, id):
    participante = Participante.objects.get(idParticipante=id)
    return render(request, 'participante/atualizar_participante.html', {'participante': participante})

def atualizar_participante(request, id):
    participante = Participante.objects.get(idParticipante=id)

    codigo          = request.POST.get('codigo')
    nome            = request.POST.get('nome')
    sobrenome       = request.POST.get('sobrenome')
    dataNascimento  = request.POST.get('dataNascimento')
    sexo            = request.POST.get('sexo')

    participante.codigo = codigo
    participante.nome = nome
    participante.sobrenome = sobrenome
    participante.dataNascimento = dataNascimento
    participante.sexo = sexo

    if 'imagem' in request.FILES:
        participante.imagem = request.FILES['imagem']

    participante.save()
    return redirect('participante')

def deletar_participante(request, id):
    participante = Participante.objects.get(idParticipante=id)
    participante.delete()
    return redirect('participante')

def analisar_participante(request, id):
    participante = Participante.objects.get(idParticipante=id)
    return render(request, 'participante/analisar_participante.html', {'participante': participante})

def relatorios(request):
    participantes = Participante.objects.all()

    quantidade_participantes = participantes.count()

    hoje = date.today()
    idades = [
        hoje.year - p.dataNascimento.year - ((hoje.month, hoje.day) < (p.dataNascimento.month, p.dataNascimento.day))
        for p in participantes
    ]

    idade_media = sum(idades) / quantidade_participantes if quantidade_participantes > 0 else 0

    masculino_count = participantes.filter(sexo='M').count()
    feminino_count = participantes.filter(sexo='F').count()

    context = {
        'quantidade_participantes': quantidade_participantes,
        'idade_media': idade_media,
        'masculino_count': masculino_count,
        'feminino_count': feminino_count,
    }

    return render(request, 'participante/relatorios.html', context)


# Desenvolvimento da analise facial
def realizar_analise(request,):
    resultado = None

    if request.method == 'POST' and 'imagem_url' in request.POST:
        imagem_url = request.POST['imagem_url']

        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        imagem_path = os.path.join(temp_dir, 'imagem_participante.jpg')
        urllib.request.urlretrieve(imagem_url, imagem_path)

        img = cv2.imread(imagem_path)
        img = cv2.resize(img, (640, 480))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            resultado = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
            if resultado:
                dominant_emotion = resultado[0]['dominant_emotion']
                emocoes = resultado[0]['emotion']
                plot_emocoes(emocoes)
            else:
                resultado = "Nenhuma face detectada."
        except Exception as e:
            resultado = f"Erro na análise: {str(e)}"

        os.remove(imagem_path)

    return render(request, 'analisar_participante.html', {'resultado': resultado, 'participante': participante})

def plot_emocoes(emocoes):
    x = list(emocoes.values())
    y = list(emocoes.keys())
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(y, x, color='skyblue')
    ax.set_xlabel('Intensidade')
    ax.set_title('Análise de Emoções')
    plt.show()