from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuario
from hashlib import sha256

def login(request):
    """
    View para a página de login.

    Verifica se o usuário já está autenticado. Se estiver, redireciona para a página inicial.
    Caso contrário, exibe a página de login.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Resposta HTTP contendo a renderização da página de login.
    """
    if request.session.get('usuario'):
        return redirect('/livro/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})

def cadastro(request):
    """
    View para a página de cadastro de usuários.

    Verifica se o usuário já está autenticado. Se estiver, redireciona para a página inicial.
    Caso contrário, exibe a página de cadastro de usuários.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Resposta HTTP contendo a renderização da página de cadastro de usuários.
    """
    if request.session.get('usuario'):
        return redirect('/livro/home/')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status': status})

def valida_cadastro(request):
    """
    View para validar o formulário de cadastro de usuários.

    Realiza as validações necessárias, como verificar se o nome e e-mail são fornecidos, se a senha
    tem pelo menos 8 caracteres, e se o e-mail já está cadastrado. Em caso de sucesso, cadastra o
    usuário no banco de dados e redireciona para a página de cadastro com um status indicando o sucesso.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Redireciona para a página de cadastro com um status indicando o resultado do cadastro.
    """
    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    usuario = Usuario.objects.filter(email=email)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        return redirect('/auth/cadastro/?status=1')

    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if len(usuario) > 0:
        return redirect('/auth/cadastro/?status=3')

    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome=nome, senha=senha, email=email)
        usuario.save()

        return redirect('/auth/cadastro/?status=0')
    except:
        return redirect('/auth/cadastro/?status=4')

def validar_login(request):
    """
    View para validar o formulário de login.

    Verifica se o e-mail e senha fornecidos correspondem a um usuário cadastrado. Em caso de sucesso,
    cria uma sessão para o usuário e redireciona para a página inicial.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Redireciona para a página inicial em caso de sucesso ou exibe uma mensagem de erro.
    """
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email=email).filter(senha=senha)

    if len(usuario) == 0:
        return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect('/livro/home/')

    return HttpResponse(f"{email} {senha}")

def sair(request):
    """
    View para encerrar a sessão do usuário.

    Limpa a sessão do usuário e redireciona para a página de login.

    Parameters:
    - request: Objeto HttpRequest contendo os dados da requisição.

    Returns:
    - HttpResponse: Redireciona para a página de login.
    """
    request.session.flush()
    return redirect('/auth/login/')
