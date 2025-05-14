from django.db import models
from django.contrib.auth.models import User
from estabelecimentos.models import Estabelecimento
from datetime import date
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey

HORARIOS = (
        ("1", "07:00 ás 08:00"),
        ("2", "08:00 ás 09:00"),
        ("3", "09:00 ás 10:00"),
        ("4", "10:00 ás 11:00"),
        ("5", "11:00 ás 12:00"),
        ("6", "12:00 ás 13:00"),
        ("7", "13:00 ás 14:00"),
        ("8", "14:00 ás 15:00"),
        ("9", "15:00 ás 16:00"),
        ("10", "16:00 ás 17:00"),
        ("11", "17:00 ás 18:00"),
        ("12", "18:00 ás 19:00"),
        ("13", "19:00 ás 20:00"),
        ("14", "20:00 ás 21:00"),
        ("15", "21:00 ás 22:00"),
        ("16", "22:00 ás 23:00"),
        ("17", "23:00 ás 00:00"),
)


class Agendamentos(models.Model):
    class Meta:
        db_table = 'agendamentos'
        
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.CASCADE)
    dia = models.DateField(help_text="Insira uma data para agenda")
    horario = models.CharField(max_length=10, choices=HORARIOS)
    
    def clean(self):
        # Verifica se já existe um agendamento no mesmo dia e horário
        if Agendamentos.objects.filter(dia=self.dia, horario=self.horario, estabelecimento=self.estabelecimento).exists():
            raise ValidationError('Já existe um agendamento para este dia e horário.')

    def save(self, *args, **kwargs):
        self.clean()  # Chama a validação personalizada antes de salvar
        super().save(*args, **kwargs)