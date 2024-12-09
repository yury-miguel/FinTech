from datetime import datetime
from mimetypes import guess_type
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from sistema.utils import retorna_dados_usuario
from .models import Cliente, Meta, Nota, Usuario
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, Http404


# Cadastra um cliente
@login_required
def cadastrar_cliente(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        nome = request.POST.get('nome')
        contato = request.POST.get('contato')
        descricao = request.POST.get('descricao')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        cidade = request.POST.get('cidade')
        bairro = request.POST.get('bairro')
        uf = request.POST.get('uf')

        Cliente.objects.create(
            nome_cliente=nome,
            contato=contato,
            descricao=descricao,
            cep=cep,
            rua=rua,
            cidade=cidade,
            bairro=bairro,
            uf=uf,
            id_usuario=id_usuario
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Cliente cadastrado com sucesso!'})

    contexto = retorna_dados_usuario(id_usuario)
    return render(request, 'sistema/clientes.html', contexto)


# Retorna um relatório de clientes
@login_required
def relatorio_clientes(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    clientes = Cliente.objects.filter(id_usuario=id_usuario)

    total_clientes = clientes.count()
    clientes_novos_mes = clientes.filter(data_cadastro__month=timezone.now().month).count()
    cidades = clientes.values_list('cidade', flat=True).distinct()
    estados = clientes.values_list('uf', flat=True).distinct()

    estados_count = clientes.values('uf').annotate(count=Count('uf'))
    estados_labels = [item['uf'] for item in estados_count]
    estados_data = [item['count'] for item in estados_count]

    crescimento = clientes.annotate(mes=TruncMonth('data_cadastro')).values('mes').annotate(count=Count('id_cliente')).order_by('mes')
    crescimento_labels = [item['mes'].strftime('%b %Y') for item in crescimento]
    crescimento_data = [item['count'] for item in crescimento]

    dados_clientes = {
        'total_clientes': total_clientes,
        'clientes_novos_mes': clientes_novos_mes,
        'total_cidades': len(cidades),
        'total_estados': len(estados),
        'lista_clientes': clientes,
        'estados_labels': estados_labels,
        'estados_data': estados_data,
        'crescimento_labels': crescimento_labels,
        'crescimento_data': crescimento_data,
    }

    contexto = retorna_dados_usuario(id_usuario)
    contexto['dados_clientes'] = dados_clientes

    return render(request, 'sistema/clientes_relatorio.html', contexto)



# Edita um cliente especifico
@login_required
def editar_cliente(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        id_cliente = request.POST.get('id_cliente')
        cliente = get_object_or_404(Cliente, id_cliente=id_cliente, id_usuario=id_usuario)

        cliente.nome_cliente = request.POST.get('nome')
        cliente.contato = request.POST.get('contato')
        cliente.cep = request.POST.get('cep')
        cliente.cidade = request.POST.get('cidade')
        cliente.uf = request.POST.get('uf')
        cliente.bairro = request.POST.get('bairro')
        cliente.rua = request.POST.get('rua')
        cliente.save()

        return JsonResponse({'success': True, 'message': 'Cliente Editado'})

    clientes = Cliente.objects.filter(id_usuario=id_usuario).order_by('-data_cadastro')
    contexto = retorna_dados_usuario(id_usuario)
    contexto["clientes"] = clientes
    return render(request, 'sistema/editar_cliente.html', contexto)


# Realiza exclusão de um cliente especifico
@login_required
def excluir_cliente(request, id_cliente):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente, id_usuario=id_usuario)
    cliente.delete()
    return redirect('editar_cliente')


# Cadastra metas
@login_required
def gerenciar_meta(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

        if 'editar_meta' in request.POST:
            meta_id = request.POST.get('meta_id')
            descricao = request.POST.get('descricao')
            status = request.POST.get('status') == 'on'
            observacao = request.POST.get('observacao')
            data_conclusao = request.POST.get('data_conclusao') if request.POST.get('data_conclusao') != '' else None

            meta = get_object_or_404(Meta, id_meta=meta_id, id_usuario=id_usuario)
            meta.descricao = descricao
            meta.status = status
            meta.observacao = observacao
            meta.data_conclusao = data_conclusao
            meta.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': meta.id_meta,
                    'descricao': meta.descricao,
                    'status': 'Concluída' if meta.status else 'Pendente',
                    'observacao': meta.observacao,
                    'data_conclusao': meta.data_conclusao if meta.data_conclusao else None
                })

        elif 'excluir_meta' in request.POST:
            meta_id = request.POST.get('meta_id')
            meta = get_object_or_404(Meta, id_meta=meta_id, id_usuario=id_usuario)
            meta.delete()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'id': meta_id})

        else:
            descricao = request.POST.get('descricao')
            status = request.POST.get('status') == 'on'
            observacao = request.POST.get('observacao')
            data_conclusao = request.POST.get('data_conclusao') if request.POST.get('data_conclusao') != '' else None

            meta = Meta.objects.create(
                descricao=descricao,
                status=status,
                observacao=observacao,
                data_conclusao=data_conclusao,
                id_usuario=id_usuario
            )

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': meta.id_meta,
                    'descricao': meta.descricao,
                    'status': 'Concluída' if meta.status else 'Pendente',
                    'observacao': meta.observacao,
                    'data_conclusao': meta.data_conclusao if meta.data_conclusao else None
                })

    metas = Meta.objects.filter(id_usuario=id_usuario).order_by('-data_cadastro')
    contexto = retorna_dados_usuario(id_usuario)
    contexto["metas"] = metas
    return render(request, 'sistema/daytrade.html', contexto)


# Cadastra notas
@login_required
def cadastrar_nota(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return redirect('/usuarios/login/')

    if request.method == 'POST':
        id_usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
        descricao = request.POST.get('descricao')
        tipo = request.POST.get('tipo')
        arquivo = request.FILES.get('nota')

        if arquivo.name.endswith(('pdf', 'txt', 'docx')):
            arquivo_binario = arquivo.read()

            nota = Nota.objects.create(
                descricao=descricao,
                tipo=tipo,
                nota=arquivo_binario,
                id_usuario=id_usuario
            )

            response_data = {
                'success': True,
                'nota': {
                    'descricao': nota.descricao,
                    'tipo': nota.tipo,
                    'data_cadastro': nota.data_cadastro.strftime("%d/%m/%Y %H:%M"),
                }
            }

            return JsonResponse(response_data)

        else:
            return JsonResponse({'success': False, 'error': 'Formato de arquivo não permitido'})

    notas = Nota.objects.filter(id_usuario=id_usuario).order_by('-data_cadastro')

    contexto = retorna_dados_usuario(id_usuario)
    contexto["notas"] = notas
    return render(request, 'sistema/notas.html', contexto)


# Função para retornar alguma nota filtrada por tipo ou data
@login_required
def filtrar_notas(request):
    id_usuario = request.session.get('usuario_id')
    if not id_usuario:
        return JsonResponse({'success': False, 'error': 'Usuário não autenticado'})

    filtro_data = request.GET.get('filtro_data', '')
    filtro_tipo = request.GET.get('filtro_tipo', '')

    notas = Nota.objects.filter(id_usuario=id_usuario).order_by('-data_cadastro')

    if filtro_data:
        try:
            data_formatada = datetime.strptime(filtro_data, '%Y-%m-%d').date()
            notas = notas.filter(data_cadastro__date=data_formatada)

        except ValueError:
            return JsonResponse({'success': False, 'error': 'Data inválida'})

    if filtro_tipo:
        notas = notas.filter(tipo__icontains=filtro_tipo)

    notas_data = [
        {
            'descricao': nota.descricao,
            'tipo': nota.tipo,
            'data_cadastro': nota.data_cadastro.strftime("%d/%m/%Y"),
            'id_nota': nota.id_nota,
        }
        for nota in notas
    ]

    return JsonResponse({'success': True, 'notas': notas_data})


# Baixa uma nota especifica salva pelo usuario
@login_required
def baixar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id_nota=nota_id, id_usuario=request.session.get('usuario_id'))

    if not nota.nota:
        raise Http404("Nota não encontrada ou não disponível.")

    file_mime_type, _ = guess_type(nota.tipo)
    response = HttpResponse(nota.nota, content_type=file_mime_type or 'application/octet-stream')

    response['Content-Disposition'] = f'attachment; filename="{nota.descricao}.pdf"'

    return response