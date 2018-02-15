from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Avg, Max, Sum, Count, ProtectedError, DateTimeField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Trunc, ExtractHour
from django.utils import timezone

from .models import Cadastro, Recibo
from .forms import CadastroForm, ReciboForm
from .exportexcel import QuerysetToWorkbook

def index(request):
    qtd_cadastro = Cadastro.objects.count()
    total_vendas = Recibo.objects.all().aggregate(Sum('total'))
    media_vendas = Recibo.objects.all().aggregate(Avg('total'))

    hoje = timezone.now()
    dt_inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_final = hoje.replace(hour=23, minute=59, second=59, microsecond=0)

    cad_por_hora =  Cadastro.objects.filter(data_hora__range=(dt_inicio, dt_final)) \
        .annotate(hora=ExtractHour('data_hora')) \
        .values('hora') \
        .order_by('hora') \
        .annotate(qtd=Count('id')) \
        .values('hora', 'qtd')

    vendas_por_dia = Recibo.objects.annotate(dia=Trunc('data_hora', 'day', output_field=DateTimeField())) \
        .values('dia') \
        .order_by('dia') \
        .annotate(qtd=Count('id')) \
        .annotate(total=Sum('total')) \
        .values('dia', 'qtd', 'total')

    return render(request,
                  'index.html',
                  {
                      'qtd_cadastro': qtd_cadastro,
                      'total_vendas': total_vendas,
                      'media_vendas': media_vendas,
                      'vendas_por_dia': vendas_por_dia,
                      'cad_por_hora': cad_por_hora
                  })

def cadastro(request):
    max_senha = Cadastro.objects.all().aggregate(Max('senha'))
    if max_senha['senha__max']:
        nova_senha = max_senha['senha__max'] + 1
    else:
        nova_senha = 1

    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            novo = form.save()
            messages.success(request, 'Cadastro adicionado com sucesso.')
            return HttpResponseRedirect(reverse('cadastro'))
    else:
        form = CadastroForm()

    cadastro_lista = Cadastro.objects.order_by('-senha')
    paginator = Paginator(cadastro_lista, 25)

    page = request.GET.get('page')
    cadastros = paginator.get_page(page)
    return render(request,
                  'cadastro.html',
                  {
                      'cadastros': cadastros,
                      'form': form,
                      'nova_senha': nova_senha
                  }
    )


def cadastro_delete(request, cadastro_id):
    try:
        cadastro = Cadastro.objects.get(pk=cadastro_id)
        try:
            cadastro.delete()
        except ProtectedError:
            messages.warning(request, 'Cadastro {} já possui recibo e não pode ser deletado.'.format(cadastro_id))
            return HttpResponseRedirect(reverse('cadastro'))
        messages.success(request, 'Cadastro {} deletado com sucesso.'.format(cadastro_id))
        return HttpResponseRedirect(reverse('cadastro'))
    except Cadastro.DoesNotExist:
        messages.warning(request, 'Cadastro {} não encontrado.'.format(cadastro_id))
        return HttpResponseRedirect(reverse('cadastro'))


def recibo_lista(request):
    recibos = Recibo.objects.order_by('-id')[:5]
    return render(request,
                  'recibo_lista.html',
                  {
                      'recibos': recibos
                  })


def recibo_novo(request, senha):
    try:
        cadastro = Cadastro.objects.get(senha=senha)
    except Cadastro.DoesNotExist:
        messages.warning(request, 'Cadastro com a senha {} não encontrado.'.format(senha))
        return HttpResponseRedirect(reverse('recibo_lista'))

    existe_rec = Recibo.objects.filter(cadastro=cadastro)
    if len(existe_rec) > 0:
        messages.warning(request, 'Cadastro com a senha {} já possui o recibo {}.'.format(senha, existe_rec[0].id))
        return HttpResponseRedirect(reverse('recibo_lista'))

    soma_compras = Recibo.objects.filter(cadastro__cpf=cadastro.cpf).aggregate(total_compras=Sum('total'))

    if soma_compras['total_compras']:
        if soma_compras['total_compras'] > 700:
            cor_alerta = 'red'
        else:
            cor_alerta = 'black'
    else:
        cor_alerta = 'black'

    if request.method == 'POST':
        form = ReciboForm(request.POST)
        if form.is_valid():
            novo = form.save(commit=False)
            novo.cadastro = cadastro
            novo.total = novo.brinquedo_vl+novo.bazar_vl+novo.eletro_vl+novo.relogio_vl+novo.musical_vl+novo.vestuario_vl+novo.perfume_vl
            novo.save()
            messages.success(request, 'Recibo adicionado com sucesso.')
            return HttpResponseRedirect(reverse('recibo_lista'))
    else:
        form = ReciboForm()

    return render(request,
                  'recibo_novo.html',
                  {
                      'form': form,
                      'cadastro': cadastro,
                      'soma_compras': soma_compras,
                      'cor_alerta': cor_alerta
                  }
    )


def recibo_delete(request, recibo_id):
    try:
        recibo = Recibo.objects.get(pk=recibo_id)
        recibo.delete()
        messages.success(request, 'Recibo {} deletado com sucesso.'.format(recibo_id))
        return HttpResponseRedirect(reverse('recibo_lista'))
    except Cadastro.DoesNotExist:
        messages.warning(request, 'Recibo {} não encontrado.'.format(recibo_id))
        return HttpResponseRedirect(reverse('recibo_lista'))


def recibo_imprimir(request, recibo_id):
    try:
        recibo = Recibo.objects.get(pk=recibo_id)
    except Recibo.DoesNotExist:
        messages.warning(request, 'Recibo {} não encontrado.'.format(recibo_id))
        return HttpResponseRedirect(reverse('recibo_lista'))

    return render(request,
                  'recibo_imprimir.html',
                  {
                      'rec': recibo
                  })


def export_excel(request):
    qs = Recibo.objects.all()

    columns = [
        ("Recibo", 10, 'id'),
        ("Data/Hora", 20, 'data_hora'),
        ("Senha", 10, 'cadastro.senha'),
        ("CPF", 20, 'cadastro.cpf'),
        ("Nome", 35, 'cadastro.nome'),
        ("E-mail", 30, 'cadastro.email'),
        ("Qt Brinquedo", 10, 'brinquedo_qt'),
        ("Vl Brinquedo", 10, 'brinquedo_vl'),
        ("Qt Bazar", 10, 'bazar_qt'),
        ("Vl Bazar", 10, 'bazar_vl'),
        ("Qt Eletro", 10, 'eletro_qt'),
        ("Vl Eletro", 10, 'eletro_vl'),
        ("Qt Relogio", 10, 'relogio_qt'),
        ("Vl Relogio", 10, 'relogio_vl'),
        ("Qt Musical", 10, 'musical_qt'),
        ("Vl Musical", 10, 'musical_vl'),
        ("Qt Vestuario", 10, 'vestuario_qt'),
        ("Vl Vestuario", 10, 'vestuario_vl'),
        ("Qt Perfume", 10, 'perfume_qt'),
        ("Vl Perfume", 10, 'perfume_vl'),
        ("Vl Total", 10, 'total')
    ]

    qtw = QuerysetToWorkbook(qs, columns, filename='Recibos')
    qtw.build_workbook()
    return qtw.response()
