from django.db import models

# Create your models here.
class Estabelecimento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    descricao = models.TextField()

    def __str__(self):
        return self.nome