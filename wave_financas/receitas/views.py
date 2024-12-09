from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from sistema.utils import retorna_dados_usuario
from .models import Receita, Categoria, Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required


# Permite cadastrar uma nova receita
@login_required
def cadastrar_receita(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        recebida = request.POST.get('efetuada') == 'efetuada'
        data_recebimento = request.POST.get('data_receita') if request.POST.get('data_receita') != '' else None
        id_categoria = request.POST.get('categoria')
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        id_categoria = get_object_or_404(Categoria, id_categoria=id_categoria)

        try:
            Receita.objects.create(
                descricao=descricao,
                valor=valor,
                recebida=recebida,
                data_recebimento=data_recebimento,
                id_usuario=id_usuario,
                id_categoria=id_categoria
            )

            return JsonResponse({'message': 'Receita cadastrada com sucesso!'}, status=201)

        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)

    categorias = Categoria.objects.filter(id_usuario=id_usuario, natureza='receita')
    contexto = retorna_dados_usuario(id_usuario)
    contexto['categorias'] = categorias
    return render(request, 'receitas/receita.html', contexto)


# Realiza edições em uma receita especifica quando for necessário
@login_required
def editar_receita(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST' and request.POST.get('acao') == 'editar':
        try:
            id_receita = request.POST.get('receita_id')
            receita = get_object_or_404(Receita, id_receita=id_receita, id_usuario=id_usuario)

            receita.descricao = request.POST.get('descricao')
            receita.valor = request.POST.get('valor')
            receita.recebida = request.POST.get('efetuada') == 'efetuada'
            receita.data_recebimento = request.POST.get('data_receita') if request.POST.get('data_receita') != '' else None
            receita.id_categoria = get_object_or_404(Categoria, id_categoria=request.POST.get('categoria'))
            receita.save()

            return JsonResponse({'message': 'receita atualizada com sucesso!'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)

    elif request.POST.get('acao') == 'deletar':
        try:
            id_receita = request.POST.get('receita_id')
            receita = get_object_or_404(Receita, id_despesa=id_receita, id_usuario=id_usuario)
            receita.delete()

            return JsonResponse({'message': 'receita excluída com sucesso!'}, status=200)

        except ValidationError as e:
            return JsonResponse({'message': str(e)}, status=400)

    receitas = Receita.objects.filter(id_usuario=id_usuario).select_related('id_categoria')
    categorias = Categoria.objects.filter(id_usuario=id_usuario, natureza='receita')

    contexto = retorna_dados_usuario(id_usuario)
    contexto['categorias'] = categorias
    contexto['receitas'] = receitas

    return render(request, 'receitas/gestao.html', contexto)


# Retorna receita por categoria para o gráfico de análises
@login_required
def receitas_por_categoria(request):
    if request.method == "GET":
        id_usuario = request.session.get('usuario_id')
        if not id_usuario:
            return redirect('/usuarios/login/')

        total_receitas = Receita.objects.filter(id_usuario=id_usuario, recebida=True).aggregate(Sum('valor'))['valor__sum'] or 0

        receitas = (Receita.objects.filter(id_usuario=id_usuario, recebida=True).values('id_categoria__descricao')
                    .annotate(valor__sum=Sum('valor')))

        receitas_por_categoria = [
            {"categoria": d["id_categoria__descricao"], "valor__sum": float(d["valor__sum"])}
            for d in receitas
        ]

        contexto = retorna_dados_usuario(id_usuario)
        contexto['total_receitas'] = total_receitas
        contexto['receitas_por_categoria'] = receitas_por_categoria
        return render(request, 'receitas/analise.html', contexto)