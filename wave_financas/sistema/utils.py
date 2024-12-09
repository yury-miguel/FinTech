import base64
from .models import Usuario
from django.shortcuts import get_object_or_404

# Função global que retorna dados do usuario para todos os módulos
def retorna_dados_usuario(id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

    contexto = {
        "nome": usuario.nome,
        "email": usuario.email,
        "telefone": usuario.telefone,
        "foto_base64": base64.b64encode(usuario.foto).decode('utf-8') if usuario.foto else None
    }
    return contexto