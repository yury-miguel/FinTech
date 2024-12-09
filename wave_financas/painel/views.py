import json
from sistema.models import *
from itertools import groupby
from receitas.models import *
from despesas.models import *
from datetime import datetime
from financeiro.models import *
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from sistema.utils import retorna_dados_usuario
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear


# Obtém os dados para preencher o dashboard de insights sobre financeiro
def painel_financeiro(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    # Totais de Receitas e Despesas
    receitas = Receita.objects.filter(id_usuario=id_usuario, recebida=True).annotate(month=TruncMonth('data_recebimento'))
    despesas = Despesa.objects.filter(id_usuario=id_usuario, paga=True).annotate(month=TruncMonth('data_pagamento'))

    total_receitas = receitas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_despesas = despesas.aggregate(Sum('valor'))['valor__sum'] or 0

    receitas_fluxo = receitas.values('month').annotate(receitas=Sum('valor'))
    despesas_fluxo = despesas.values('month').annotate(despesas=Sum('valor'))
    meses_fluxo = sorted(list(receitas_fluxo) + list(despesas_fluxo), key=lambda x: x['month'])
    fluxo_mensal = []

    # Linha do tempo (Receitas x Despesas por mês)
    for month, group in groupby(meses_fluxo, key=lambda x: x['month']):
        item = {'month': month, 'receitas': 0, 'despesas': 0}
        for g in group:
            item['receitas'] += g.get('receitas', 0)
            item['despesas'] += g.get('despesas', 0)
        fluxo_mensal.append(item)

    # Maiores receitas e despesas
    maior_receita = receitas.order_by('-valor').first()
    maior_despesa = despesas.order_by('-valor').first()

    # Total ganho com Day Trade
    day_trade = DayTrade.objects.filter(id_usuario=id_usuario)
    lucro_day_trade = day_trade.aggregate(Sum('lucro_liquido'))['lucro_liquido__sum'] or 0

    # Total ganho com Projetos
    projetos = Projeto.objects.filter(id_usuario=id_usuario)
    lucro_projetos = projetos.aggregate(
        total_lucro=Sum(F('valor_cobrado') - F('valor_gasto'))
    )['total_lucro'] or 0

    # Total ganho com Ativos
    ativos = Ativo.objects.filter(id_usuario=id_usuario, valor_retorno__isnull=False)
    lucro_ativos = ativos.aggregate(
        total_retorno=Sum(F('valor_retorno') - F('valor_investido'))
    )['total_retorno'] or 0

    dados = {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'fluxo_mensal': json.dumps(fluxo_mensal, cls=DjangoJSONEncoder),
        'maior_receita': maior_receita,
        'maior_despesa': maior_despesa,
        'lucro_day_trade': lucro_day_trade,
        'lucro_projetos': lucro_projetos,
        'lucro_ativos': lucro_ativos,
    }

    dados_cartoes = [
        {"titulo": "Total Receitas", "valor": dados["total_receitas"], "cor": "bg-light border-success"},
        {"titulo": "Total Despesas", "valor": dados["total_despesas"], "cor": "bg-light border-danger"},
        {"titulo": "Lucro Day Trade", "valor": dados["lucro_day_trade"], "cor": "bg-light border-primary"},
        {"titulo": "Lucro Projetos", "valor": dados["lucro_projetos"], "cor": "bg-light border-warning"},
    ]

    contexto = retorna_dados_usuario(id_usuario)
    contexto['dados'] = dados
    contexto['dados_cartoes'] = dados_cartoes
    return render(request, 'painel/financeiros.html', contexto)


# Obtém os dados para preencher o dashboard de insights sobre projetos
def painel_projetos(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        contexto = retorna_dados_usuario(id_usuario)
        return render(request, 'painel/projetos.html', contexto)


# Obtém os dados para preencher o dashboard de insights sobre cliente
def painel_clientes(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        contexto = retorna_dados_usuario(id_usuario)
        return render(request, 'painel/clientes.html', contexto)


# Obtém os dados para preencher o dashboard de insights sobre investimentos
def painel_investimentos(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        contexto = retorna_dados_usuario(id_usuario)
        return render(request, 'painel/investimentos.html', contexto)


# Obtém os dados para preencher o dashboard de insights sobre daytrade
def painel_daytrade(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        contexto = retorna_dados_usuario(id_usuario)
        return render(request, 'painel/daytrade.html', contexto)