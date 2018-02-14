import datetime
from django import forms
from localflavor.br.forms import BRCPFField
from core.models import Cadastro, Recibo


class CadastroForm(forms.ModelForm):
    cpf = BRCPFField(max_length=11, min_length=11)

    class Meta:
        model = Cadastro
        fields = [
            'senha',
            'nome',
            'cpf',
            'email'
        ]


class ReciboForm(forms.ModelForm):
    brinquedo_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    bazar_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    eletro_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    relogio_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    musical_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    vestuario_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)
    perfume_vl = forms.DecimalField(max_digits=10, decimal_places=2, localize=True)

    class Meta:
        model = Recibo
        fields = [
            'brinquedo_qt',
            'brinquedo_vl',
            'bazar_qt',
            'bazar_vl',
            'eletro_qt',
            'eletro_vl',
            'relogio_qt',
            'relogio_vl',
            'musical_qt',
            'musical_vl',
            'vestuario_qt',
            'vestuario_vl',
            'perfume_qt',
            'perfume_vl'
        ]