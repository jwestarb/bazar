from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Avg, Max, Sum, ProtectedError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Cadastro, Recibo
from .forms import CadastroForm, ReciboForm

def index(request):
    qtd_cadastro = Cadastro.objects.count()
    total_vendas = Recibo.objects.all().aggregate(Sum('total'))
    media_vendas = Recibo.objects.all().aggregate(Avg('total'))
    return render(request,
                  'index.html',
                  {
                      'qtd_cadastro': qtd_cadastro,
                      'total_vendas': total_vendas,
                      'media_vendas': media_vendas

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
                      'cadastro': cadastro
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