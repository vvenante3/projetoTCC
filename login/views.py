from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Usuario
from participante.models import Participante
from django.contrib import messages

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password


# LOGIN
def pagina_login(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')
    else:
        usuario     = request.POST.get('usuario')
        senha       = request.POST.get('senha')

        usuario = authenticate(username=usuario, password=senha)

        if usuario:
            login(request, usuario)
            participantes = Participante.objects.all()
            return render(request, "participante/index.html", {"participantes": participantes})
        else:
            return HttpResponse('Email ou Senha inválidos.')

def pagina_logout(request):
    logout(request)
    return redirect('pagina_login')

def enviar_email_personalizado(destinatario, assunto, mensagem):
    remetente       = "vitor.venante@hotmail.com"
    senha           = "senha123"
    servidor_smtp   = "smtp.office365.com"
    porta           = 587

    msg = MIMEMultipart()
    msg['From']     = remetente
    msg['To']       = destinatario
    msg['Subject']  = assunto
    msg.attach(MIMEText(mensagem, 'plain'))

    try:
        with smtplib.SMTP(servidor_smtp, porta) as server:
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def enviar_codigo_email(request):
    if request.method == 'POST':
        email   = request.POST.get('email')
        user    = User.objects.filter(email=email).first()

        if user:
            uid     = urlsafe_base64_encode(force_bytes(user.pk))
            token   = default_token_generator.make_token(user)
            link_redefinir_senha = request.build_absolute_uri(f"/redefinir-senha/{uid}/{token}/")

            mensagem = f"Olá, use o link abaixo para redefinir sua senha:\n{link_redefinir_senha}"
            assunto = "Redefinição de senha"
            enviar_email_personalizado(email, assunto, mensagem)

            return render(request, 'login/restaurarSenha_2_pag_confirmacao_email.html')
        else:
            return render(request, 'login/restaurarSenha_1_email_recuperacao.html', {
                "error": "E-mail não encontrado"
            })

    return render(request, 'login/restaurarSenha_1_email_recuperacao.html')

def redefinir_senha(request, uidb64, token):
    try:
        uid     = force_str(urlsafe_base64_decode(uidb64))
        user    = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            nova_senha      = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')

            if nova_senha and nova_senha == confirmar_senha:
                user.password = make_password(nova_senha)
                user.save()
                messages.success(request, "Senha alterada com sucesso!")
                return render(request, 'login/restaurarSenha_4_pag_confirmacao_alteracao_senha.html')
            else:
                messages.error(request, "As senhas não coincidem.")
                return render(request, 'login/restaurarSenha_3_form_nova_senha.html',
                              {'uidb64': uidb64, 'token': token})

        return render(request, 'login/restaurarSenha_3_form_nova_senha.html', {'uidb64': uidb64, 'token': token})

    messages.error(request, "O link para redefinição de senha é inválido ou expirou.")
    return redirect('pagina_login')


def pagina_cadastro(request):
    if request.method == 'GET':
        return render(request, 'login/cadastro.html')
    else:
        usuario = request.POST.get('usuario')
        crp     = request.POST.get('crp'    )
        email   = request.POST.get('email'  )
        senha   = request.POST.get('senha'  )

        usuario_cadastrado = User.objects.filter(username=usuario).first()

        if usuario_cadastrado:
            return HttpResponse('Já existe um usuário com o mesmo nome.')

        usuario_novo = User.objects.create_user(
            username    =usuario,
            email       =email,
            password    =senha
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

        request.user.username   = usuario_novo
        request.user.email      = email_novo
        request.user.crp        = crp_novo

        if senha_nova:
            request.user.set_password(senha_nova)
            request.user.save()
            update_session_auth_hash(request, request.user)
        else:
            request.user.save()
            request.user.usuario.save()

        messages.success(request, 'Dados atualizados com sucesso!')

        participantes = Participante.objects.all()
        return render(request, "participante/index.html", {"participantes": participantes})