from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# LOGIN
def pagina_login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        # obtendo os dados inseridos nos campos ' usuario ' e ' senha '.
        usuario    = request.POST.get('usuario')
        senha       = request.POST.get('senha')

        usuario = authenticate(username=usuario, password=senha)

        if usuario:
            login(request, usuario)

            return HttpResponse('Autenticado.') # DESENVOLVER PÁG. PARA INDEX.HTML
        else:
            return HttpResponse('Email ou Senha inválidos.')

def pagina_cadastro(request):
    if request.method == 'GET':
        return render(request, 'login/cadastro.html')
    else:
        # pegando os dados da pág. cadastro
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # acessando o Db e filtrando o usuario, retornando o primeiro objeto
        usuario_cadastrado = User.objects.filter(username=usuario).first()

        if usuario_cadastrado:
            return HttpResponse('Já existe um usuário com o mesmo nome.')

        # criando um novo usuario
        usuario_novo = User.objects.create_user(
            username=usuario,
            email   =email,
            password=senha
        )
        usuario_novo.save()
        return HttpResponse('Usuário cadastrado com sucesso.')
