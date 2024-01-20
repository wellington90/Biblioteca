from usuarios.models import Usuario
from django import forms
from django.db.models import fields
from .models import Livros, Categoria
from django.db import models    
from datetime import date

class CadastroLivro(forms.ModelForm):
    """
    Formulário para cadastro de livros.

    Utiliza o modelo Livros e exibe todos os campos disponíveis.
    O campo 'usuario' é oculto no formulário.

    Attributes:
    - model: Classe do modelo utilizado no formulário (Livros).
    - fields: Lista de campos a serem exibidos no formulário (todos os campos do modelo).
    """

    class Meta:
        model = Livros
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        """
        Inicializador do formulário.

        Oculta o campo 'usuario' no formulário.

        Parameters:
        - args: Argumentos posicionais.
        - kwargs: Argumentos de palavra-chave.
        """
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput()

class CategoriaLivro(forms.Form):
    """
    Formulário para cadastro de categorias de livros.

    Contém os campos 'nome' e 'descricao', este último exibido como uma área de texto.

    Attributes:
    - nome: Campo para inserção do nome da categoria (CharField).
    - descricao: Campo para inserção da descrição da categoria (CharField com widget Textarea).
    """

    nome = forms.CharField(max_length=30)
    descricao = forms.CharField(max_length=60)

    def __init__(self, *args, **kwargs):
        """
        Inicializador do formulário.

        Converte o campo 'descricao' em uma área de texto.

        Parameters:
        - args: Argumentos posicionais.
        - kwargs: Argumentos de palavra-chave.
        """
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget = forms.Textarea()
