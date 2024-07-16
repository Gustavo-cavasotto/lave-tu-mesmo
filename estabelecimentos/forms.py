from django import forms
from django.contrib.auth.models import User

from estabelecimentos.models import Estabelecimento

class EstabelecimentoForm(forms.ModelForm):
    class Meta:
        model = Estabelecimento
        fields = '__all__'
    