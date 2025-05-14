from django.db import models

# Create your models here.
class Estabelecimento(models.Model):
    class Meta:
        db_table = 'estabelecimentos'
        
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    foto = models.ImageField(upload_to='estabelecimentos', null=True, blank=True)
    instagram = models.CharField(max_length=40)

    def __str__(self):
        return self.nome