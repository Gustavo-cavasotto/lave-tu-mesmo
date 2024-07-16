from django import forms
from agendamentos.models import Agendamentos
from django.contrib.auth.models import User

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamentos
        fields = '__all__'
    
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.HiddenInput())
    
    dia = forms.DateField(
        label = 'Data',
        required=False,
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    