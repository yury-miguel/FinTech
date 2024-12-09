import json
from .models import Usuario
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Realiza autenticacao do usuario para entrar no sistema
@csrf_exempt
def login_usuario(request):
    if request.method == "POST":
        try:
            dados = json.loads(request.body)
            email = dados.get("email")
            senha = dados.get("senha")

            usuario = Usuario.objects.filter(email=email).first()
            if not usuario:
                return JsonResponse({"erro": "Usuário não encontrado"}, status=404)

            if senha == usuario.senha:
                request.session['usuario_id'] = usuario.id_usuario
                return JsonResponse({"mensagem": "Login realizado"}, status=200)

            return JsonResponse({"erro": "Senha incorreta"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Formato de JSON inválido.'}, status=400)

    elif request.method == "GET":
        return render(request, 'usuarios/login.html')

    return JsonResponse({'erro': 'Método não permitido.'}, status=405)