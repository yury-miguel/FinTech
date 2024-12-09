from . import views
from django.urls import path

urlpatterns = [
    path('cadastrar_receita/', views.cadastrar_receita, name='cadastrar_receita'),
    path('editar_receita/', views.editar_receita, name='editar_receita'),
    path('receitas_por_categoria/', views.receitas_por_categoria, name='receitas_por_categoria'),
]