from django.db import models

def faces_participantes_path(instance, filename):
    return f'faces_participantes/{filename}'

# Classe Participante
class Participante(models.Model):
    idParticipante  = models.AutoField(primary_key=True)
    codigo          = models.CharField(max_length=8)
    nome            = models.CharField(max_length=30)
    sobrenome       = models.CharField(max_length=30)
    dataNascimento  = models.DateField()
    sexo            = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino')])
    imagem          = models.ImageField(upload_to=faces_participantes_path)

    def __str__(self):
        return f'{self.idParticipante} - {self.codigo} - {self.nome} - {self.sobrenome} - {self.dataNascimento} - {self.sexo} - {self.imagem}'