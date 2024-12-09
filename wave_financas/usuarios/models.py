from django.db import models

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=256)
    telefone = models.CharField(max_length=15)
    senha = models.CharField(max_length=255)
    foto = models.BinaryField(null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'usuario'