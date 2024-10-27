from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Participante
from datetime import date
from django.contrib.auth.decorators import login_required

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

    participante.codigo         = codigo
    participante.nome           = nome
    participante.sobrenome      = sobrenome
    participante.dataNascimento = dataNascimento
    participante.sexo           = sexo

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