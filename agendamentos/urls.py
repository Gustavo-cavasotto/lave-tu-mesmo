from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('listar/', login_required(views.listar), name='listar_agendamentos'),
    path('criar/', login_required(views.criar), name='criar_agendamento'),
    path('criar_id/<int:estabelecimento_id>/', login_required(views.criar_com_id), name='criar_agendamento_com_id'),
    path('editar/<int:id>/', login_required(views.editar), name='editar_agendamento'),
    path('excluir/<int:id>/', login_required(views.excluir), name='excluir_agendamento'),
    path('verificar_disponibilidade/', login_required(views.verificar_disponibilidade), name='verificar_disponibilidade'),
]