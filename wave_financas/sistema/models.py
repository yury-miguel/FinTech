from django.db import models
from usuarios.models import Usuario

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100)
    cep = models.CharField(max_length=15, null=True, blank=True)
    rua = models.CharField(max_length=500, null=True, blank=True)
    cidade = models.CharField(max_length=500, null=True, blank=True)
    bairro = models.CharField(max_length=500, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)
    contato = models.TextField()
    descricao = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    def __str__(self):
        return self.nome_cliente

    class Meta:
        db_table = 'cliente'

class Meta(models.Model):
    id_meta = models.AutoField(primary_key=True)
    descricao = models.TextField()
    status = models.BooleanField(default=False)
    observacao = models.TextField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'metas'

class Nota(models.Model):
    id_nota = models.AutoField(primary_key=True)
    nota = models.BinaryField()
    descricao = models.CharField(max_length=700)
    tipo = models.CharField(max_length=255)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')

    class Meta:
        db_table = 'notas'