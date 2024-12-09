from . import views
from django.urls import path

urlpatterns = [
    path('cadastrar_despesa/', views.cadastrar_despesa, name='cadastrar_despesa'),
    path('editar_despesa/', views.editar_despesa, name='editar_despesa'),
    path('despesas_por_categoria/', views.despesas_por_categoria, name='despesas_por_categoria'),
]
