from django.http import HttpResponse
from django.shortcuts import redirect, render
import json
from agendamentos.forms import AgendamentoForm
from django.contrib import messages
from django.core.paginator import Paginator
from agendamentos.models import Agendamentos
from estabelecimentos.models import Estabelecimento

#Create your views here.
def listar(request):
    object_list = Agendamentos.objects.filter(usuario=request.user)
    search_value = request.GET.get('search_value')
    search_field = ''
        
    paginator = Paginator(object_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'object_list': page_obj,
        'page_obj': page_obj,
        'search_field': search_field,
        'name': 'Agendamentos',
        'operacao': 'Listagem'
    }
    
    return render(request, 'agendamentos/templates/lista.html', context)

def criar(request):
    if request.method == 'POST': 
            form = AgendamentoForm(request.POST)
            if form.is_valid():
                try:
                    agendamento = form.save()  # Salva o objeto e retorna a instância do modelo Pessoa
                    messages.success(request, 'Inclusão efetuada')
                    return redirect('editar_agendamento', id=agendamento.id)
                except:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Erro no campo {form.fields[field].label}: {error}")
                    return redirect('criar_agendamento')
        
    else: #Se o método não for POST, exibimos o formulário vazio.
        form = AgendamentoForm(initial={'usuario': request.user})
    
    context = {
        'form': form,
        'operacao': 'Incluindo',
        'name': 'Agendamento'
    }
    
    return render(request, 'agendamentos/templates/form.html', context)

def criar_com_id(request, estabelecimento_id):
    estabelecimento = Estabelecimento.objects.get(id=estabelecimento_id)
    if request.method == 'POST': 
            form = AgendamentoForm(request.POST)
            if form.is_valid():
                try:
                    agendamento = form.save()  # Salva o objeto e retorna a instância do modelo Pessoa
                    messages.success(request, 'Inclusão efetuada')
                    return redirect('editar_agendamento', id=agendamento.id)
                except:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Erro no campo {form.fields[field].label}: {error}")
                    return redirect('criar_agendamento')
        
    else: #Se o método não for POST, exibimos o formulário vazio.  
        form = AgendamentoForm(initial={'usuario': request.user, 'estabelecimento': estabelecimento})
        
    
    context = {
        'form': form,
        'operacao': 'Incluindo',
        'name': 'Agendamento'
    }
    
    return render(request, 'agendamentos/templates/form.html', context)

def editar(request, id):
    agendamento = Agendamentos.objects.get(id=id)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Alteração efetuada')
                return redirect('editar_agendamento', id=id)
            except:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Erro no campo {form.fields[field].label}: {error}")
                return redirect('editar_agendamento', id=id)
    else:
        form = AgendamentoForm(instance=agendamento)
    
    context = {
        'form': form,
        'operacao': 'Editando',
        'agendamento': agendamento,
        'name': 'Agendamento'
    }
    
    return render(request, 'agendamentos/templates/form.html', context)

def excluir(request, id):
    agendamento = Agendamentos.objects.get(id=id)
    agendamento.delete()
    messages.success(request, 'Exclusão efetuada')
    return redirect('listar_agendamentos')

def verificar_disponibilidade(request):
    horario_agendamento = request.GET.get('data_hora')
    estabelecimento_id = request.GET.get('estabelecimento')
    print(horario_agendamento, estabelecimento_id)
    agendamentos = Agendamentos.objects.filter(estabelecimento=estabelecimento_id, data_hora=horario_agendamento)
    print(agendamentos)
    if agendamentos:
        retorno = {
                'mensagem': 'Horário indisponível para agendamento.',
                'status': 'ERRO'
        }
    else:
        retorno = {
                'mensagem': 'Horário está disponível !',
                'status': 'OK'
        }
    return HttpResponse(json.dumps(retorno), content_type='application/json')
    
        