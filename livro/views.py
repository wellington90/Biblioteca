from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Emprestimos, Livros, Categoria
from .forms import CadastroLivro, CategoriaLivro
from django import forms

def home(request):
    """
    View para a página inicial (home) do sistema.

    Verifica se o usuário está autenticado. Se estiver, exibe a lista de livros, o formulário
    de cadastro de livros e o formulário de cadastro de categorias. Caso contrário, redireciona
    para a página de login.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Resposta HTTP contendo a renderização da página home.
    """
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id=request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livros.objects.filter(usuario=usuario)
        form = CadastroLivro()
        form.fields['usuario'].initial = request.session['usuario']
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

        form_categoria = CategoriaLivro()

        return render(request, 'home.html', {'livros': livros,
                                             'usuario_logado': request.session.get('usuario'),
                                             'form': form,
                                             'status_categoria': status_categoria,
                                             'form_categoria': form_categoria})
    else:
        return redirect('/auth/login/?status=2')


def ver_livros(request, id):
    """
    View para visualização detalhada de um livro específico.

    Verifica se o usuário está autenticado e se o livro pertence a ele. Se sim, exibe informações
    detalhadas sobre o livro, suas categorias e empréstimos associados. Caso contrário, exibe uma
    mensagem indicando que o livro não pertence ao usuário.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.
    - id: Identificador único do livro a ser visualizado.

    Returns:
    - HttpResponse: Resposta HTTP contendo a renderização da página de visualização do livro.
    """
    if request.session.get('usuario'):
        livros = Livros.objects.get(id=id)
        if request.session.get('usuario') == livros.usuario.id:
            usuario = Usuario.objects.get(id=request.session['usuario'])
            categoria_livro = Categoria.objects.filter(usuario=request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro=livros)
            form = CadastroLivro()
            form.fields['usuario'].initial = request.session['usuario']
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario=usuario)

            form_categoria = CategoriaLivro()

            return render(request, 'ver_livro.html', {'livro': livros,
                                                      'categoria_livro': categoria_livro,
                                                      'emprestimos': emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form': form,
                                                      'id_livro': id,
                                                      'form_categoria': form_categoria})
        else:
            return HttpResponse('Esse livro não é seu')
    return redirect('/auth/login/?status=2')


def cadastrar_livro(request):
    """
    View para o cadastro de livros.

    Processa o formulário de cadastro de livros. Se os dados forem válidos, salva o livro no
    banco de dados e redireciona para a página inicial. Caso contrário, exibe uma mensagem de erro.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Redireciona para a página home em caso de sucesso ou exibe uma mensagem de erro.
    """
    if request.method == 'POST':
        form = CadastroLivro(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/livro/home')
        else:
            return HttpResponse('DADOS INVÁLIDOS')


def excluir_livro(request, id):
    """
    View para a exclusão de livros.

    Exclui o livro com o ID fornecido do banco de dados e redireciona para a página inicial.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.
    - id: Identificador único do livro a ser excluído.

    Returns:
    - HttpResponse: Redireciona para a página home após a exclusão.
    """
    Livros.objects.get(id=id).delete()
    return redirect('/livro/home')


def cadastrar_categoria(request):
    """
    View para o cadastro de categorias.

    Processa o formulário de cadastro de categorias. Se os dados forem válidos, salva a categoria no
    banco de dados e redireciona para a página inicial com um parâmetro indicando o sucesso. Caso
    contrário, exibe uma mensagem de erro.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Redireciona para a página home com um parâmetro indicando o sucesso ou exibe uma mensagem de erro.
    """
    form = CategoriaLivro(request.POST)
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')
    if int(id_usuario) == int(request.session.get('usuario')):
        user = Usuario.objects.get(id=id_usuario)
        categoria = Categoria(nome=nome, descricao=descricao, usuario=user)
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse('Pare de ser um usuário malandrinho. Não foi desta vez.')
