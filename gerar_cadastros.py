# -*- coding: utf-8 -*-
import os, sys
import random
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bazar.settings")
import django
django.setup()

from core.models import Cadastro

def strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def randomDate(start, end, prop):
    return strTimeProp(start, end, '%Y-%m-%d %H:%M', prop)

def generate_cpf():
    cpf = [random.randint(0, 9) for x in range(9)]

    for _ in range(2):
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11
        cpf.append(11 - val if val > 1 else 0)

    return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)

for i in range(1, 1000 ):
    cad = Cadastro()
    cad.senha = i
    cad.cpf = generate_cpf()
    cad.nome = 'Teste {}'.format(i)
    cad.email = 'teste{}@teste.com'.format(i)
    cad.save()
