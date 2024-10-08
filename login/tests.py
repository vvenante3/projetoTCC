from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from login.models import Usuario
from django.contrib.auth import authenticate


class PaginaCadastro(TestCase):
    def test_cadastro_usuario_existente(self):
        User.objects.create_user(username='usuario_existente', email='existente@email.com', password='123456')

        response = self.client.post(reverse('pagina_cadastro'), {
            'usuario'   : 'usuario_existente',
            'crp'       : '123456',
            'email'     : 'existente@email.com',
            'senha'     : '123456'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Já existe um usuário com o mesmo nome.')

    def test_cadastro_usuario_novo(self):
        response = self.client.post(reverse('pagina_cadastro'), {
            'usuario'   : 'novo_usuario',
            'crp'       : '654321',
            'email'     : 'novo@email.com',
            'senha'     : 'novasenha123'
        })

        # Verificando se o usuário foi criado corretamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário cadastrado com sucesso.')

        # Verificando se o usuário foi salvo no banco de dados
        usuario_novo = User.objects.filter(username='novo_usuario').first()
        self.assertIsNotNone(usuario_novo)

        # Verificando se o registro de CRP foi salvo
        usuario_registro = Usuario.objects.filter(user=usuario_novo, crp='654321').first()
        self.assertIsNotNone(usuario_registro)

class PaginaLogin(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='usuario_teste', password='senha_teste')

    def test_login_sucesso(self):
        response = self.client.post(reverse('pagina_login'), {
            'usuario'   : 'usuario_teste',
            'senha'     : 'senha_teste'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Autenticado.')

    def test_login_invalido(self):
        response = self.client.post(reverse('pagina_login'), {
            'usuario'   : 'usuario_teste',
            'senha'     : 'senha_errada'
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email ou Senha inválidos.')

