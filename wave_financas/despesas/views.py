from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from sistema.utils import retorna_dados_usuario
from .models import Despesa, Categoria, Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


# Permite cadastrar uma nova receita
@login_required
def cadastrar_despesa(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        paga = request.POST.get('paga') == 'paga'
        data_pagamento = request.POST.get('data_despesa') if request.POST.get('data_despesa') != '' else None
        id_categoria = request.POST.get('categoria')
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        id_categoria = get_object_or_404(Categoria, id_categoria=id_categoria)

        try:
            Despesa.objects.create(
                descricao=descricao,
                valor=valor,
                paga=paga,
                data_pagamento=data_pagamento,
                id_usuario=id_usuario,
                id_categoria=id_categoria
            )
            return JsonResponse({'message': 'Despesa cadastrada com sucesso!'}, status=201)

        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)

    categorias = Categoria.objects.filter(id_usuario=id_usuario, natureza='despesa')
    contexto = retorna_dados_usuario(id_usuario)
    contexto['categorias'] = categorias
    return render(request, 'despesas/despesa.html', contexto)


# Realiza edições em uma receita especifica quando for necessário
@login_required
def editar_despesa(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST' and request.POST.get('acao') == 'editar':
        try:
            id_despesa = request.POST.get('despesa_id')
            despesa = get_object_or_404(Despesa, id_despesa=id_despesa, id_usuario=id_usuario)

            despesa.descricao = request.POST.get('descricao')
            despesa.valor = request.POST.get('valor')
            despesa.paga = request.POST.get('paga') == 'paga'
            despesa.data_pagamento = request.POST.get('data_despesa') if request.POST.get('data_despesa') != '' else None
            despesa.id_categoria = get_object_or_404(Categoria, id_categoria=request.POST.get('categoria'))
            despesa.save()

            return JsonResponse({'message': 'Despesa atualizada com sucesso!'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)

    elif request.POST.get('acao') == 'deletar':
        try:
            id_despesa = request.POST.get('despesa_id')
            despesa = get_object_or_404(Despesa, id_despesa=id_despesa, id_usuario=id_usuario)
            despesa.delete()

            return JsonResponse({'message': 'Despesa excluída com sucesso!'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)

    despesas = Despesa.objects.filter(id_usuario=id_usuario).select_related('id_categoria')
    categorias = Categoria.objects.filter(id_usuario=id_usuario, natureza='despesa')

    contexto = retorna_dados_usuario(id_usuario)
    contexto['categorias'] = categorias
    contexto['despesas'] = despesas

    return render(request, 'despesas/gestao.html', contexto)


# Retorna receita por categoria para o gráfico de análises
@login_required
def despesas_por_categoria(request):
    if request.method == "GET":
        id_usuario = request.session.get('usuario_id')
        if not id_usuario:
            return redirect('/usuarios/login/')

        total_despesas = Despesa.objects.filter(id_usuario=id_usuario, paga=True).aggregate(Sum('valor'))['valor__sum'] or 0

        despesas = (Despesa.objects.filter(id_usuario=id_usuario, paga=True).values('id_categoria__descricao')
                    .annotate(valor__sum=Sum('valor')))

        despesas_por_categoria = [
            {"categoria": d["id_categoria__descricao"], "valor__sum": float(d["valor__sum"])}
            for d in despesas
        ]

        contexto = retorna_dados_usuario(id_usuario)
        contexto['total_despesas'] = total_despesas
        contexto['despesas_por_categoria'] = despesas_por_categoria
        return render(request, 'despesas/analise.html', contexto)