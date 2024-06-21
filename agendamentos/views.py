from django.shortcuts import render

# Create your views here.
def criar(request):
    if request.method == 'POST': 
            form = PessoaForm(request.POST)
            if form.is_valid():
                try:
                    pessoa = form.save()  # Salva o objeto e retorna a instância do modelo Pessoa
                    messages.success(request, 'Inclusão efetuada')
                    return redirect('editar_pessoa', id=pessoa.id)
                except:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"Erro no campo {form.fields[field].label}: {error}")
                    return redirect('criar_pessoa')
        
    else: #Se o método não for POST, exibimos o formulário vazio.
        form = PessoaForm()
    
    context = {
        'form': form,
        'operacao': 'Incluindo',
        'name': 'Pessoa'
    }
    
    return render(request, 'pessoas/templates/form.html', context)