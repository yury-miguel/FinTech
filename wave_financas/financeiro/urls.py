from . import views
from django.urls import path

urlpatterns = [
    path('fluxo_financeiro/', views.fluxo_financeiro, name='fluxo_financeiro'),
    path('portifolio/', views.portifolio, name='portifolio'),
    path('gestao_portifolio/', views.gestao_portifolio, name='gestao_portifolio'),
    path('gestao_projetos/', views.gestao_projetos, name='gestao_projetos'),
    path('gestao_ativos/', views.gestao_ativos, name='gestao_ativos'),
    path('gestao_daytrade/', views.gestao_daytrade, name='gestao_daytrade'),
    path('gestao_observacoes_daytrade/', views.gestao_observacoes_daytrade, name='gestao_observacoes_daytrade'),
    path('total_receitas/', views.total_receitas, name='total_receitas'),
    path('total_despesas/', views.total_despesas, name='total_despesas'),
    path('saldo/', views.saldo, name='saldo'),
    path('cadastrar_observacao_daytrade/', views.cadastrar_observacao_daytrade, name='cadastrar_observacao_daytrade'),
    path('cadastrar_projeto/', views.cadastrar_projeto, name='cadastrar_projeto'),
    path('cadastrar_ativo/', views.cadastrar_ativo, name='cadastrar_ativo'),
    path('cadastrar_daytrade/', views.cadastrar_daytrade, name='cadastrar_daytrade'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('extrato_financeiro/', views.extrato_financeiro, name='extrato_financeiro'),
]