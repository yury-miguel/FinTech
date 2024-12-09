from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_usuario, name='login_usuario'),
]