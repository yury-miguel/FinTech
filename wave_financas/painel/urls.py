from django.urls import path
from . import views

urlpatterns = [
    path('painel_financeiro/', views.painel_financeiro, name='painel_financeiro'),
    path('painel_projetos/', views.painel_projetos, name='painel_projetos'),
    path('painel_clientes/', views.painel_clientes, name='painel_clientes'),
    path('painel_investimentos/', views.painel_investimentos, name='painel_investimentos'),
    path('painel_daytrade/', views.painel_daytrade, name='painel_daytrade'),
]