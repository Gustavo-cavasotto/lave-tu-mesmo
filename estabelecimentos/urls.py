from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('lista/', login_required(views.lista_estabelecimentos), name='lista_estabelecimentos'),
    path('criar/', login_required(views.criar_estabelecimento), name='criar_estabelecimento'),
    path('excluir/<int:id>', login_required(views.excluir_estabelecimento), name='excluir_estabelecimento'),
]
