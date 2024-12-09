from django.contrib import admin
from .models import Cliente, Meta, Nota

# REGISTRA OS DADOS PARA GERENCIAR FACILMENTE
admin.site.register(Cliente)
admin.site.register(Meta)
admin.site.register(Nota)
