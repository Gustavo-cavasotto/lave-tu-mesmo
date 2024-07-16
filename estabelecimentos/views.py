from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from estabelecimentos.forms import EstabelecimentoForm
from estabelecimentos.models import Estabelecimento
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

# def admin_required(user):
#     return user.is_authenticated and user.is_staff

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Você não tem permissão para acessar esta página.')
            return redirect('home')  # Redireciona para a home page
    return _wrapped_view

@admin_required
def lista_estabelecimentos(request):
    object_list = Estabelecimento.objects.all()
    search_value = request.GET.get('search_value')
    search_field = ''
    
    if search_value:
        search_field = request.GET['searchField']

        if search_field == u"nome":
            object_list = object_list.filter(nome__icontains=search_value)
        elif search_field == u"cidade":
            object_list = object_list.filter(cidade__icontains=search_value)
        elif search_field == u"telefone":
            object_list = object_list.filter(telefone__icontains=search_value)
        
    paginator = Paginator(object_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'search_field': search_field,
        'name': 'Estabelecimentos',
        'operacao': 'Listagem'
    }
    
    return render(request, 'estabelecimentos/templates/lista.html', context)

@admin_required
def criar_estabelecimento(request):
    if request.method == 'POST': 
            form = EstabelecimentoForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    estabelecimento = form.save()  # Salva o objeto e retorna a instância do modelo Pessoa
                    messages.success(request, 'Inclusão efetuada')
                    return redirect('editar_estabelecimento', id=estabelecimento.id)
                except:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Erro no campo {form.fields[field].label}: {error}")
                    return redirect('criar_estabelecimento')
        
    else: #Se o método não for POST, exibimos o formulário vazio.
        form = EstabelecimentoForm()
    
    context = {
        'form': form,
        'operacao': 'Incluindo',
        'name': 'Estabelecimento'
    }
    
    return render(request, 'estabelecimentos/templates/form.html', context)

@admin_required
def editar(request, id):
    estabelecimento = Estabelecimento.objects.get(id=id)
    if request.method == 'POST':
        form = EstabelecimentoForm(request.POST, request.FILES, instance=estabelecimento)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Alteração efetuada')
                return redirect('editar_estabelecimento', id=id)
            except:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Erro no campo {form.fields[field].label}: {error}")
                return redirect('editar_estabelecimento', id=id)
    else:
        form = EstabelecimentoForm(instance=estabelecimento)
    
    context = {
        'form': form,
        'operacao': 'Editando',
        'estabelecimento': estabelecimento,
        'name': 'Estabelecimento'
    }
    
    return render(request, 'estabelecimentos/templates/form.html', context)

@admin_required
def excluir(request, id):
    estabelecimento = Estabelecimento.objects.get(id=id)
    estabelecimento.delete()
    messages.success(request, 'Exclusão efetuada')
    return redirect('lista_estabelecimentos')