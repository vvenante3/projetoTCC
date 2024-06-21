from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from participante.models import Participante
from django.contrib.auth.models import User

class TesteSalvarParticipante(TestCase):
    def test_salvar_participante(self):
        codigo          = '12342024'
        nome            = 'nomeTeste'
        sobrenome       = 'sobrenomeTeste'
        dataNascimento  = datetime.strptime('2024-10-01', '%Y-%m-%d').date()
        sexo            = 'M'
        imagem          = 'imagem.jpg'

        response = self.client.post(reverse('salvar_participante'), {
            'codigo'        : codigo,
            'nome'          : nome,
            'sobrenome'     : sobrenome,
            'dataNascimento': dataNascimento,
            'sexo'          : sexo,
            'imagem'        : imagem
        })

        self.assertEqual(response.status_code, 302)
        while response.status_code == 302:
            response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        # self.assertRedirects(response, reverse('participante'))

        participante = Participante.objects.filter(codigo=codigo)
        self.assertEqual(participante.count(),1)
        participante = participante.first()
        self.assertEqual(participante.codigo, codigo)
        self.assertEqual(participante.nome, nome)
        self.assertEqual(participante.sobrenome, sobrenome)
        self.assertEqual(participante.dataNascimento, dataNascimento)
        self.assertEqual(participante.sexo, sexo)
        self.assertEqual(participante.imagem, imagem)

class TesteEditarParticipante(TestCase):
    def setUp(self):
        self.participante = Participante.objects.create(
            codigo          = '12342024',
            nome            = 'nomeTeste',
            sobrenome       = 'sobrenomeTeste',
            dataNascimento  = '2024-10-01',
            sexo            = 'M',
            imagem          = 'imagem.jpg'
    )

    def test_editar_participante(self):
        url = reverse('editar_participante', kwargs={'id': self.participante.idParticipante})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'participante/atualizar_participante.html')
        self.assertEqual(response.context['participante'], self.participante)

class TesteDeletarParticipante(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.participante = Participante.objects.create(
            codigo          = '12342024',
            nome            = 'nomeTeste',
            sobrenome       = 'sobrenomeTeste',
            dataNascimento  = '2024-10-01',
            sexo            = 'M',
            imagem          = 'imagem.jpg'
        )

    def test_deletar_participante(self):
        response = self.client.get(reverse('deletar_participante', args=[self.participante.idParticipante]))

        self.assertFalse(Participante.objects.filter(idParticipante=self.participante.idParticipante).exists())
        self.assertRedirects(response, reverse('participante'), status_code=302)