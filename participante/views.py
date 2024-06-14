from django.shortcuts import render, redirect
from .models import Participante

# PARTICIPANTE
def participante(request):
    participantes = Participante.objects.all()
    return render(request, "participante/index.html", {"participantes": participantes})

def salvar_participante(request):
    codigo          = request.POST['codigo']
    nome            = request.POST['nome']
    sobrenome       = request.POST['sobrenome']
    dataNascimento  = request.POST['dataNascimento']
    sexo            = request.POST['sexo']
    imagem          = request.POST['imagem']

    # salvar no Db
    Participante.objects.create(codigo=codigo, nome=nome, sobrenome=sobrenome, dataNascimento=dataNascimento, sexo=sexo, imagem=imagem)
    participantes = Participante.objects.all()

    return redirect('participante')

def editar_participante(request, id):
    participante = Participante.objects.get(idParticipante=id)
    return render(request, 'participante/atualizar_participante.html', {'participante': participante})

def atualizar_participante(request, id):
    codigo          = request.POST.get('codigo')
    nome            = request.POST.get('nome')
    sobrenome       = request.POST.get('sobrenome')
    dataNascimento  = request.POST.get('dataNascimento')
    sexo            = request.POST.get('sexo')
    imagem          = request.POST.get('imagem')

    participante = Participante.objects.get(idParticipante=id)

    participante.codigo         = codigo
    participante.nome           = nome
    participante.sobrenome      = sobrenome
    participante.dataNascimento = dataNascimento
    participante.sexo           = sexo
    participante.imagem         = imagem

    participante.save()
    return redirect('participante')

def deletar_participante(request, id):
    participante = Participante.objects.get(idParticipante=id)
    participante.delete()
    return redirect('participante')