from .models import Usuario
from django.contrib import admin
from django.contrib.auth.hashers import make_password

# REGISTRA OS DADOS PARA GERENCIAR FACILMENTE
admin.site.register(Usuario)


# Exemplo de cadastro do usuario
# usuario = Usuario(
#     nome='Exemplo',
#     email='exemplo@email.com',
#     telefone='123456789',
#     senha=make_password('senha123')
# )
# usuario.save()