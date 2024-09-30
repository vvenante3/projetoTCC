from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Usuario

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
        crp     = request.POST.get('crp'    )
        email   = request.POST.get('email'  )
        senha   = request.POST.get('senha'  )

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

        Usuario.objects.create(user=usuario_novo, crp=crp)

        return HttpResponse('Usuário cadastrado com sucesso.')

@login_required
def editar_usuario(request):
    if request.method == 'GET':
        return render(request, 'login/editar_usuario.html', {
            'usuario': request.user.username,
            'email': request.user.email,
            'crp': request.user.usuario.crp
        })
    else:
        usuario_novo     = request.POST.get('usuario')
        email_novo       = request.POST.get('email')
        crp_novo         = request.POST.get('crp')
        senha_nova       = request.POST.get('senha')

        request.user.username = usuario_novo
        request.user.email = email_novo
        request.user.crp = crp_novo

        request.user.save()
        request.user.usuario.save()

        if senha_nova:
            request.user.set_password(senha_nova)
            request.user.save()

            update_session_auth_hash(request, request.user)

        return HttpResponse('Usuário atualizado com sucesso.')