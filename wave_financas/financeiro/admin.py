from django.contrib import admin
from .models import Categoria, DayTrade, Ativo, Projeto, ObservacoesDayTrade

# REGISTRA OS DADOS PARA GERENCIAR FACILMENTE
admin.site.register(Categoria)
admin.site.register(DayTrade)
admin.site.register(Ativo)
admin.site.register(Projeto)
admin.site.register(ObservacoesDayTrade)