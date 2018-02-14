"""bazar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cadastro/delete/<int:cadastro_id>/', views.cadastro_delete, name='cadastro_delete'),
    path('recibo/', views.recibo_lista, name='recibo_lista'),
    path('recibo/novo/<int:senha>/', views.recibo_novo, name='recibo_novo'),
    path('recibo/imprimir/<int:recibo_id>/', views.recibo_imprimir, name='recibo_imprimir'),
    path('recibo/delete/<int:recibo_id>/', views.recibo_delete, name='recibo_delete'),
]
