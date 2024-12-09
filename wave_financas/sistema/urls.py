from . import views
from django.urls import path

urlpatterns = [
    path('gerenciar_meta/', views.gerenciar_meta, name='gerenciar_meta'),
    path('cadastrar_nota/', views.cadastrar_nota, name='cadastrar_nota'),
    path('filtrar_notas/', views.filtrar_notas, name='filtrar_notas'),
    path('baixar_nota/<int:nota_id>/', views.baixar_nota, name='baixar_nota'),
    path('cadastrar_cliente/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('editar_cliente/', views.editar_cliente, name='editar_cliente'),
    path('excluir/<int:id_cliente>/', views.excluir_cliente, name='excluir_cliente'),
    path('relatorio_clientes/', views.relatorio_clientes, name='relatorio_clientes'),
]