from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from estabelecimentos.models import Estabelecimento

@login_required(login_url='login')
def home(request):
    object_list = Estabelecimento.objects.all()
    search_value = request.GET.get('search_value')
    search_field = ''
    
    if search_value:
        object_list = object_list.filter(nome__icontains=search_value)
        
    paginator = Paginator(object_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'search_field': search_field,
        'name': 'Página Inicial',
        'operacao': 'Mostrando Estabelecimentos:'
    }
    
    return render(request, 'home/templates/home.html', context)