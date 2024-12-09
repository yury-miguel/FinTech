from django.db import models
from usuarios.models import Usuario
from financeiro.models import Categoria

class Despesa(models.Model):
    id_despesa = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=500)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    paga = models.BooleanField()
    data_pagamento = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, db_column='id_categoria')

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'despesa'