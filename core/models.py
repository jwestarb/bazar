from django.db import models
from django.contrib.auth.models import User


class CreatedUpdatedModel(models.Model):
    criado_em = models.DateTimeField(u'Criado em', auto_now_add=True, editable=False)
    criado_por = models.ForeignKey(User,
                                   related_name="created_%(app_label)s_%(class)s_set",
                                   null=True, editable=False, on_delete=models.SET_NULL)
    atualizado_em = models.DateTimeField(u'Atualizado em', auto_now=True, editable=False)
    atualizado_por = models.ForeignKey(User,
                                       related_name="modified_%(app_label)s_%(class)s_set",
                                       null=True, editable=False, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class Cadastro(CreatedUpdatedModel):
    data_hora = models.DateTimeField('Data/Hora', auto_now_add=True)
    senha = models.IntegerField('Senha', unique=True)
    nome = models.CharField('Nome', max_length=200)
    cpf = models.CharField('CPF', max_length=11)
    email = models.EmailField('E-mail', null=True, blank=True)

    def cpf_format(self):
        return "{}.{}.{}-{}".format(self.cpf[0:3], self.cpf[3:6], self.cpf[6:9], self.cpf[9:11])

    class Meta:
        ordering = ['-senha']

    def __str__(self):
        return self.nome


class Recibo(CreatedUpdatedModel):
    cadastro = models.ForeignKey(Cadastro, verbose_name='Cadastro', on_delete=models.PROTECT)
    data_hora = models.DateTimeField('Data/Hora', auto_now_add=True)
    brinquedo_qt = models.PositiveIntegerField('Brinquedos Qtd', default=0)
    brinquedo_vl = models.DecimalField('Brinquedos Valor', max_digits=10, decimal_places=2, default=0)
    bazar_qt = models.PositiveIntegerField('Artigos de Bazar Qtd', default=0)
    bazar_vl = models.DecimalField('Artigos de Bazar Valor', max_digits=10, decimal_places=2, default=0)
    eletro_qt = models.PositiveIntegerField('Equipamentos Eletrônicos Qtd', default=0)
    eletro_vl = models.DecimalField('Equipamentos Eletrônicos Valor', max_digits=10, decimal_places=2, default=0)
    relogio_qt = models.PositiveIntegerField('Relógios Qtd', default=0)
    relogio_vl = models.DecimalField('Relógios Vlr', max_digits=10, decimal_places=2, default=0)
    musical_qt = models.PositiveIntegerField('Instrumentos Musicais, Mesas e Módulos Qtd', default=0)
    musical_vl = models.DecimalField('Instrumentos Musicais, Mesas e Módulos Valor', max_digits=10, decimal_places=2, default=0)
    vestuario_qt = models.PositiveIntegerField('Vestuário Qtd', default=0)
    vestuario_vl = models.DecimalField('Vestuário Valor', max_digits=10, decimal_places=2, default=0)
    perfume_qt = models.PositiveIntegerField('Higiene Pessoal, Perfumes e Cosméticos Qtd', default=0)
    perfume_vl = models.DecimalField('Higiene Pessoal, Perfumes e Cosméticos Valor', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Valor Total', editable=False, max_digits=12, decimal_places=2, default=0)


    class Meta:
        ordering = ['-data_hora']

    def __str__(self):
        return self.cadastro.nome
