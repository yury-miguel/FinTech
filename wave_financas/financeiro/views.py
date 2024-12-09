import json
from .models import *
from datetime import datetime
from calendar import monthrange
from django.db.models import Sum
from collections import defaultdict
from receitas.models import Receita
from despesas.models import Despesa
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from sistema.utils import retorna_dados_usuario
from django.contrib.auth.decorators import login_required


# Renderiza a página principal 'Fluxo' além de enviar os dados e controlar o gráfico e filtro de lançamentos.
def fluxo_financeiro(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    tipo_lancamento = request.GET.get('tipo-lancamento', 'saldo')
    periodo_inicial = request.GET.get('periodo-inicial')
    periodo_final = request.GET.get('periodo-final')

    data_inicio = datetime.strptime(periodo_inicial, '%Y-%m-%d') if periodo_inicial else None
    data_fim = datetime.strptime(periodo_final, '%Y-%m-%d') if periodo_final else None

    receitas = Receita.objects.filter(id_usuario=id_usuario, recebida=True)
    despesas = Despesa.objects.filter(id_usuario=id_usuario, paga=True)

    if data_inicio and data_fim:
        receitas = receitas.filter(data_recebimento__range=(data_inicio, data_fim))
        despesas = despesas.filter(data_pagamento__range=(data_inicio, data_fim))

    receitas_por_mes = defaultdict(float)
    despesas_por_mes = defaultdict(float)

    for receita in receitas:
        mes = receita.data_recebimento.strftime('%Y-%m')
        receitas_por_mes[mes] += float(receita.valor)

    for despesa in despesas:
        mes = despesa.data_pagamento.strftime('%Y-%m')
        despesas_por_mes[mes] += float(despesa.valor)

    meses = sorted(set(receitas_por_mes.keys()).union(set(despesas_por_mes.keys())))
    fluxo_mensal = []
    entradas_mes = []

    for mes in meses:
        receita_mes = receitas_por_mes.get(mes, 0)
        despesa_mes = despesas_por_mes.get(mes, 0)

        if tipo_lancamento == 'entrada':
            fluxo = receita_mes
        elif tipo_lancamento == 'saida':
            fluxo = -despesa_mes
        else:
            fluxo = receita_mes - despesa_mes

        fluxo_mensal.append({'mes': mes, 'fluxo': fluxo})

    for fluxo in fluxo_mensal:
        mes = fluxo['mes']
        ano, mes_num = map(int, mes.split('-'))
        dia = monthrange(ano, mes_num)[1]
        data_formatada = f"{mes}-{dia:02d}"
        entradas_mes.append({'data': data_formatada, 'total': fluxo['fluxo']})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'entradas_mes': entradas_mes}, status=200)

    contexto = retorna_dados_usuario(id_usuario)
    contexto['entradas_mes'] = entradas_mes
    return render(request, "financeiro/fluxo.html", contexto)


# API para retornar total de receitas recebidas
def total_receitas(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    # Receitas padrão
    receitas = Receita.objects.filter(id_usuario=id_usuario, recebida=True).aggregate(Sum('valor'))[
                   'valor__sum'] or 0

    # DayTrade
    daytrade_lucro = DayTrade.objects.filter(id_usuario=id_usuario).aggregate(Sum('lucro_liquido'))[
                         'lucro_liquido__sum'] or 0

    # Ativos
    ativos_retorno = \
    Ativo.objects.filter(id_usuario=id_usuario, valor_retorno__isnull=False).aggregate(Sum('valor_retorno'))[
        'valor_retorno__sum'] or 0

    # Projetos
    projetos_cobrado = Projeto.objects.filter(id_usuario=id_usuario).aggregate(Sum('valor_cobrado'))[
                           'valor_cobrado__sum'] or 0

    total = receitas + daytrade_lucro + ativos_retorno + projetos_cobrado

    return JsonResponse({'total_receitas': total}, status=200)


# API para retornar o total de despesas pagas
def total_despesas(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    # Despesas padrão
    despesas = Despesa.objects.filter(id_usuario=id_usuario, paga=True).aggregate(Sum('valor'))['valor__sum'] or 0

    # DayTrade
    daytrade_gastos = DayTrade.objects.filter(id_usuario=id_usuario).aggregate(Sum('gastos'))['gastos__sum'] or 0

    # Ativos
    ativos_investido = Ativo.objects.filter(id_usuario=id_usuario).aggregate(Sum('valor_investido'))[
                           'valor_investido__sum'] or 0

    # Projetos
    projetos_gasto = \
    Projeto.objects.filter(id_usuario=id_usuario, valor_gasto__isnull=False).aggregate(Sum('valor_gasto'))[
        'valor_gasto__sum'] or 0

    # Soma total das despesas
    total = despesas + daytrade_gastos + ativos_investido + projetos_gasto

    return JsonResponse({'total_despesas': total}, status=200)


# API para retornar saldo total
def saldo(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    # Calcula total de receitas
    total_receitas = Receita.objects.filter(id_usuario=id_usuario, recebida=True).aggregate(Sum('valor'))['valor__sum'] or 0
    daytrade_lucro = DayTrade.objects.filter(id_usuario=id_usuario).aggregate(Sum('lucro_liquido'))['lucro_liquido__sum'] or 0
    ativos_retorno = Ativo.objects.filter(id_usuario=id_usuario, valor_retorno__isnull=False).aggregate(Sum('valor_retorno'))['valor_retorno__sum'] or 0
    projetos_cobrado = Projeto.objects.filter(id_usuario=id_usuario).aggregate(Sum('valor_cobrado'))['valor_cobrado__sum'] or 0
    total_receitas += daytrade_lucro + ativos_retorno + projetos_cobrado

    # Calcula total de despesas
    total_despesas = Despesa.objects.filter(id_usuario=id_usuario, paga=True).aggregate(Sum('valor'))['valor__sum'] or 0
    daytrade_gastos = DayTrade.objects.filter(id_usuario=id_usuario).aggregate(Sum('gastos'))['gastos__sum'] or 0
    ativos_investido = Ativo.objects.filter(id_usuario=id_usuario).aggregate(Sum('valor_investido'))['valor_investido__sum'] or 0
    projetos_gasto = Projeto.objects.filter(id_usuario=id_usuario, valor_gasto__isnull=False).aggregate(Sum('valor_gasto'))['valor_gasto__sum'] or 0
    total_despesas += daytrade_gastos + ativos_investido + projetos_gasto

    # Calcula saldo
    saldo = total_receitas - total_despesas

    return JsonResponse({'saldo': saldo}, status=200)


# Recebe os dados do usuário logado e renderiza a pagina portifolio
def portifolio(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')
    
    clientes = Cliente.objects.filter(id_usuario=id_usuario).order_by('-data_cadastro')
    contexto = retorna_dados_usuario(id_usuario)
    contexto["clientes"] = clientes
    return render(request, "financeiro/portifolio.html", contexto)


# Recebe os dados do usuário logado e renderiza a pagina de gestão do portifolio
def gestao_portifolio(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    clientes = Cliente.objects.filter(id_usuario=id_usuario).order_by('-data_cadastro')
    contexto = retorna_dados_usuario(id_usuario)
    contexto["clientes"] = clientes
    return render(request, "financeiro/gestao_portifolio.html", contexto)


# Retorna separadamente os dadod entre receita e despesa o extrato financeiro
@login_required
def extrato_financeiro(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == "GET":
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')

        receitas = Receita.objects.filter(id_usuario=id_usuario).select_related('id_categoria')
        despesas = Despesa.objects.filter(id_usuario=id_usuario).select_related('id_categoria')

        if data_inicio or data_fim:
            try:
                if data_inicio:
                    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
                    receitas = receitas.filter(data_recebimento__gte=data_inicio)
                    despesas = despesas.filter(data_pagamento__gte=data_inicio)
                if data_fim:
                    data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
                    receitas = receitas.filter(data_recebimento__lte=data_fim)
                    despesas = despesas.filter(data_pagamento__lte=data_fim)
            except ValueError:
                pass

        extrato = {'receitas': [], 'despesas': []}

        for receita in receitas:
            extrato['receitas'].append({
                'descricao': receita.descricao,
                'categoria': receita.id_categoria.descricao,
                'valor': receita.valor,
                'status': 'A receber' if not receita.recebida else 'Recebida',
                'data_vencimento': receita.data_recebimento if receita.data_recebimento else 'Não informada',
                'data_recebimento': receita.data_recebimento if receita.recebida else 'Não recebida'
            })

        for despesa in despesas:
            extrato['despesas'].append({
                'descricao': despesa.descricao,
                'categoria': despesa.id_categoria.descricao,
                'valor': despesa.valor,
                'status': 'A pagar' if not despesa.paga else 'Paga',
                'data_vencimento': despesa.data_pagamento if despesa.data_pagamento else 'Não informada',
                'data_pagamento': despesa.data_pagamento if despesa.paga else 'Não paga'
            })

        contexto = retorna_dados_usuario(id_usuario)
        contexto['extrato'] = extrato
        return render(request, 'financeiro/extrato.html', contexto)


# Cadastra uma nova categoria de receita ou despesa
@login_required
def cadastrar_categoria(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        descricao = request.POST.get('descricao')
        natureza = request.POST.get('natureza')

        Categoria.objects.create(
            descricao=descricao,
            natureza=natureza,
            id_usuario=id_usuario
        )

        return JsonResponse({'message': 'Categoria cadastrada com sucesso!'}, status=201)


# Cadastra dados mensal de operações no daytrade
@login_required
def cadastrar_daytrade(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        contratos = request.POST.get('contratos')
        caixa_atual = request.POST.get('caixa_atual')
        gastos = request.POST.get('gastos')
        lucro_liquido = request.POST.get('lucro_liquido')
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

        DayTrade.objects.create(
            contratos=contratos,
            caixa_atual=caixa_atual,
            gastos=gastos,
            lucro_liquido=lucro_liquido,
            id_usuario=id_usuario
        )

        return JsonResponse({"success": "Resultados DayTrade cadastrado com sucesso!"}, status=201)


# Cadastra um ativo
@login_required
def cadastrar_ativo(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor_investido = request.POST.get('valor_investido')
        valor_retorno = request.POST.get('valor_retorno') or None
        data_investimento = request.POST.get('data_investimento')
        data_retorno = request.POST.get('data_retorno') or None
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

        Ativo.objects.create(
            descricao=descricao,
            valor_investido=valor_investido,
            valor_retorno=valor_retorno,
            data_investimento=data_investimento,
            data_retorno=data_retorno,
            id_usuario=id_usuario
        )

        return JsonResponse({"success": "Ativo cadastrado com sucesso!"}, status=201)


# Cadastra um projeto
@login_required
def cadastrar_projeto(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        nome_projeto = request.POST.get('nome_projeto')
        observacao = request.POST.get('observacao')
        valor_cobrado = request.POST.get('valor_cobrado')
        valor_gasto = request.POST.get('valor_gasto') or None
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim') or None
        id_cliente = request.POST.get('id_cliente') or None
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

        if id_cliente is not None:
            id_cliente = get_object_or_404(Cliente, id_cliente=id_cliente)
            Projeto.objects.create(
                nome_projeto = nome_projeto,
                observacao=observacao,
                valor_cobrado=valor_cobrado,
                valor_gasto=valor_gasto,
                data_inicio=data_inicio,
                data_fim=data_fim,
                id_cliente=id_cliente,
                id_usuario=id_usuario
            )
        else:
            Projeto.objects.create(
                observacao=observacao,
                valor_cobrado=valor_cobrado,
                valor_gasto=valor_gasto,
                data_inicio=data_inicio,
                data_fim=data_fim,
                id_usuario=id_usuario
            )

        return JsonResponse({"success": "Projeto cadastrado com sucesso!"}, status=201)


# Cadastra uma observacao relacionada ao daytrade
@login_required
def cadastrar_observacao_daytrade(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        detalhe = request.POST.get('detalhe')
        status = request.POST.get('status')
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

        ObservacoesDayTrade.objects.create(
            detalhe=detalhe,
            status=status,
            id_usuario=id_usuario
        )

        return JsonResponse({"success": "Operação cadastrada com sucesso!"}, status=201)


# Edita e exibe dados mensal de operações no daytrade
@login_required
def gestao_daytrade(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'GET':
        daytrade = DayTrade.objects.filter(id_usuario=id_usuario).values(
            'id_daytrade', 'contratos', 'caixa_atual', 'gastos', 'lucro_liquido'
        )

        return JsonResponse({'daytrade': list(daytrade)})

    elif request.method == 'POST':
        id_daytrade = request.POST.get('id_daytrade')
        daytrade = DayTrade.objects.get(id_daytrade=id_daytrade, id_usuario=id_usuario)

        daytrade.contratos = request.POST.get('contratos')
        daytrade.caixa_atual = request.POST.get('caixa_atual')
        daytrade.gastos = request.POST.get('gastos')
        daytrade.lucro_liquido = request.POST.get('lucro_liquido')
        daytrade.save()

        return JsonResponse({"success": "DayTrade Mensal editado com sucesso!"}, status=201)

    elif request.method == 'DELETE':
        body = json.loads(request.body)
        id_daytrade = body.get('id_daytrade')
        daytrade = DayTrade.objects.filter(id_daytrade=id_daytrade, id_usuario=id_usuario).first()

        if daytrade:
            daytrade.delete()
            return JsonResponse({"success": "DayTrade excluído com sucesso!"}, status=200)
        else:
            return JsonResponse({"error": "DayTrade não encontrado."}, status=404)


# Edita e exibe todos ativos
@login_required
def gestao_ativos(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'GET':
        ativos = Ativo.objects.filter(id_usuario=id_usuario).values(
            'id_ativo', 'descricao', 'valor_investido', 'valor_retorno', 'data_investimento', 'data_retorno'
        )

        return JsonResponse({'ativos': list(ativos)})

    elif request.method == 'POST':
        id_ativo = request.POST.get('id_ativo')
        ativo = Ativo.objects.get(id_ativo=id_ativo, id_usuario=id_usuario)

        ativo.descricao = request.POST.get('descricao')
        ativo.valor_investido = request.POST.get('valor_investido')
        ativo.valor_retorno = request.POST.get('valor_retorno') or None
        ativo.data_investimento = request.POST.get('data_investimento')
        ativo.data_retorno = request.POST.get('data_retorno') or None
        ativo.save()

        return JsonResponse({"success": "Ativo editado com sucesso!"}, status=201)

    elif request.method == 'DELETE':
        body = json.loads(request.body)
        id_ativo = body.get('id_ativo')
        ativo = Ativo.objects.filter(id_ativo=id_ativo, id_usuario=id_usuario).first()

        if ativo:
            ativo.delete()
            return JsonResponse({"success": "Ativo excluído com sucesso!"}, status=200)
        else:
            return JsonResponse({"error": "Ativo não encontrado."}, status=404)


# Edita e exibe todos os projeto
@login_required
def gestao_projetos(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'GET':
        projetos = Projeto.objects.filter(id_usuario=id_usuario).values(
            'id_projeto', 'nome_projeto', 'observacao', 'valor_cobrado', 'valor_gasto', 'data_inicio', 'data_fim', 'id_cliente'
        )
        return JsonResponse({'projetos': list(projetos)})

    elif request.method == 'POST':
        id_projeto = request.POST.get('id_projeto')
        projeto = Projeto.objects.get(id_projeto=id_projeto, id_usuario=id_usuario)

        projeto.nome_projeto = request.POST.get('nome_projeto')
        projeto.observacao = request.POST.get('observacao')
        projeto.valor_cobrado = request.POST.get('valor_cobrado')
        projeto.valor_gasto = request.POST.get('valor_gasto') or None
        projeto.data_inicio = request.POST.get('data_inicio')
        projeto.data_fim =request.POST.get('data_fim') or None
        projeto.save()

        return JsonResponse({"success": "Projeto atualizado com sucesso!"}, status=201)

    elif request.method == 'DELETE':
        body = json.loads(request.body)
        id_projeto = body.get('id')
        projeto = Projeto.objects.filter(id_projeto=id_projeto, id_usuario=id_usuario).first()

        if projeto:
            projeto.delete()
            return JsonResponse({"success": "Projeto excluído com sucesso!"}, status=200)
        else:
            return JsonResponse({"error": "Projeto não encontrado."}, status=404)


# Edita e exibe observacoes relacionada ao daytrade
@login_required
def gestao_observacoes_daytrade(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'GET':
       obs_daytrade = ObservacoesDayTrade.objects.filter(id_usuario=id_usuario).values(
            'id_obs', 'detalhe', 'status', 'data_cadastro'
        )
       return JsonResponse({'obs': list(obs_daytrade)})

    elif request.method == 'POST':
        id_obs = request.POST.get('id_obs')
        observacao = ObservacoesDayTrade.objects.get(id_obs=id_obs, id_usuario=id_usuario)

        observacao.detalhe = request.POST.get('detalhe')
        observacao.status = request.POST.get('status')
        observacao.save()

        return JsonResponse({"success": "Operação editada com sucesso!"}, status=201)

    elif request.method == 'DELETE':
        body = json.loads(request.body)
        id_obs = body.get('id_obs')
        observacao = ObservacoesDayTrade.objects.filter(id_obs=id_obs, id_usuario=id_usuario).first()

        if observacao:
            observacao.delete()
            return JsonResponse({"success": "Operação excluída com sucesso!"}, status=200)
        else:
            return JsonResponse({"error": "Operação não encontrado."}, status=404)