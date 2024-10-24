from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Participante
from datetime import date
from django.contrib.auth.decorators import login_required

import os
import cv2
from django.conf import settings
from django.core.files.storage import default_storage

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
def realizar_analise(request):
    if request.method == 'POST' and request.FILES['imagem_participante']:
        imagem = request.FILES['imagem_participante']

        imagem_path = os.path.join(settings.MEDIA_ROOT, 'temp', imagem.name)
        default_storage.save(imagem_path, imagem)

        img = cv2.imread(imagem_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        resultado = "Neutro"

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]

            if w > 100:
                resultado = "Feliz"
            elif w < 80:
                resultado = "Triste"

        default_storage.delete(imagem_path)

        return render(request, 'analisar_participante.html', {resultado: resultado})

    return render(request, 'analisar_participante.html')