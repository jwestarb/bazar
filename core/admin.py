from django.contrib import admin
from .models import Cadastro, Recibo


@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    list_display = ['senha', 'data_hora', 'nome', 'cpf', 'email']

@admin.register(Recibo)
class CadastroAdmin(admin.ModelAdmin):

    list_display = ['id', 'data_hora', 'cadastro_senha', 'cadastro_cpf', 'cadastro_nome', 'total']

    def cadastro_senha(self, obj):
        return obj.cadastro.senha

    cadastro_senha.admin_order_field = 'cadastro__senha'
    cadastro_senha.short_description = 'Senha'

    def cadastro_cpf(self, obj):
        return obj.cadastro.cpf

    cadastro_cpf.admin_order_field = 'cadastro__cpf'
    cadastro_cpf.short_description = 'CPF'

    def cadastro_nome(self, obj):
        return obj.cadastro.nome

    cadastro_nome.admin_order_field = 'cadastro__nome'
    cadastro_nome.short_description = 'Nome'

