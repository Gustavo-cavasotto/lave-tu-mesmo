from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from estabelecimentos.models import Estabelecimento

def lista_estabelecimentos(request):
    estabelecimentos = Estabelecimento.objects.all()
    return render(request, 'estabelecimentos/templates/lista.html', {'estabelecimentos': estabelecimentos})

def criar_estabelecimento(request):
    if request.method == 'POST':
        print('POST', request.POST)
        nome = request.POST.get('nome')
        cidade = request.POST.get('cidade')
        endereco = request.POST.get('endereco')
        telefone = request.POST.get('telefone')
        descricao = request.POST.get('descricao')
        
        estabelecimento = Estabelecimento(
            nome=nome,
            cidade=cidade,
            endereco=endereco,
            telefone=telefone,
            descricao=descricao,
        )
        
        try:
            estabelecimento.save()
            sucesso = "Estabelecimento criado com sucesso."
        except Exception as e:
            erro = "Este estabelecimento é inválido, revise os dados."
        
        # Recarregar a lista de estabelecimentos após a criação
        estabelecimentos = Estabelecimento.objects.all()
        context = {
            'estabelecimentos': estabelecimentos, 
            'erro': erro if 'erro' in locals() else '',
            'sucesso': sucesso if 'sucesso' in locals() else ''
        }
        return render(request, 'estabelecimentos/templates/lista_dados.html', context)
    return render(request, 'estabelecimentos/templates/form.html')


@csrf_exempt
@require_http_methods(["DELETE"])
def excluir_estabelecimento(request, id):
    estabelecimento = Estabelecimento.objects.get(id=id)
    estabelecimento.delete()
    
    # Recarregar a lista de dependentes após a exclusão
    estabelecimentos = Estabelecimento.objects.all()
    sucesso = "Estabelecimento excluído com sucesso."
    context = {
        'estabelecimentos': estabelecimentos,
        'sucesso': sucesso if 'sucesso' in locals() else '',
    }
    return render(request, 'estabelecimentos/templates/lista_dados.html', context)
    