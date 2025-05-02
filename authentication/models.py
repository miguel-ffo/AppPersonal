from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ROLE = [
    ('aluno', 'Aluno'),
    ('personal', 'Personal Trainer')
    ]

    role = models.CharField(max_length=20, choices=ROLE)

    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)


class Aluno(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    objetivo = models.CharField(null=True, blank=True, max_length=255)
    idade = models.IntegerField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)

    personal = models.ForeignKey('Personal', on_delete=models.CASCADE, related_name='alunos')



class Personal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    cref = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=255)
    experiencia = models.IntegerField(null=True, help_text="Tempo de experiência")
    biografia = models.TextField(blank=True)






