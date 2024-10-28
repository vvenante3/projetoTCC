from django.db import models
from django.contrib.auth.models import User

def faces_participantes_path(instance, filename):
    return f'faces_participantes/{filename}'

class Participante(models.Model):
    idParticipante  = models.AutoField(primary_key=True)
    codigo          = models.CharField(max_length=8)
    nome            = models.CharField(max_length=30)
    sobrenome       = models.CharField(max_length=30)
    dataNascimento  = models.DateField()
    sexo            = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    imagem          = models.ImageField(upload_to=faces_participantes_path)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participantes' )

    def __str__(self):
        return f'{self.idParticipante} - {self.codigo} - {self.nome} - {self.sobrenome} - {self.dataNascimento} - {self.sexo} - {self.imagem}'