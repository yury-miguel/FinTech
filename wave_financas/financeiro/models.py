from django.db import models
from sistema.models import Cliente
from usuarios.models import Usuario

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=500)
    natureza = models.CharField(max_length=10, choices=[('receita', 'Receita'), ('despesa', 'Despesa')])
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'categoria'

class DayTrade(models.Model):
    id_daytrade = models.AutoField(primary_key=True)
    contratos = models.IntegerField()
    caixa_atual = models.TextField()
    gastos = models.DecimalField(max_digits=10, decimal_places=2)
    lucro_liquido = models.DecimalField(max_digits=10, decimal_places=2)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'daytrade'

class Ativo(models.Model):
    id_ativo = models.AutoField(primary_key=True)
    descricao = models.TextField()
    valor_investido = models.DecimalField(max_digits=10, decimal_places=2)
    data_investimento = models.DateField(null=True, blank=True)
    valor_retorno = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_retorno = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'ativos'

class Projeto(models.Model):
    id_projeto = models.AutoField(primary_key=True)
    nome_projeto = models.TextField()
    observacao = models.TextField()
    valor_cobrado = models.DecimalField(max_digits=10, decimal_places=2)
    valor_gasto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente', null=True, blank=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'projetos'

class ObservacoesDayTrade(models.Model):
    id_obs = models.AutoField(primary_key=True)
    detalhe = models.CharField(max_length=5000)
    status = models.CharField(max_length=10, choices=[('gain', 'Gain'), ('loss', 'Loss')])
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'obs_daytrade'