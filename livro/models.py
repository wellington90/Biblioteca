from django.db import models    
from datetime import date
from usuarios.models import Usuario

class Categoria(models.Model):
    """
    Modelo para representar categorias de livros.

    Attributes:
    - nome: Nome da categoria (CharField).
    - descricao: Descrição da categoria (TextField).
    - usuario: Usuário associado à categoria (ForeignKey para o modelo Usuario).
    """

    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        """
        Retorna uma representação em string do objeto Categoria.

        Returns:
        - str: Nome da categoria.
        """
        return self.nome


class Livros(models.Model):
    """
    Modelo para representar livros.

    Attributes:
    - nome: Nome do livro (CharField).
    - autor: Autor principal do livro (CharField).
    - co_autor: Co-autor do livro (CharField, opcional).
    - data_cadastro: Data de cadastro do livro (DateField, padrão para a data atual).
    - emprestado: Indica se o livro está emprestado (BooleanField, padrão False).
    - categoria: Categoria à qual o livro pertence (ForeignKey para o modelo Categoria).
    - usuario: Usuário associado ao livro (ForeignKey para o modelo Usuario).

    Meta:
    - verbose_name: Nome exibido nos metadados para o modelo.
    """

    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=30)
    co_autor = models.CharField(max_length=30, blank=True)
    data_cadastro = models.DateField(default=date.today)
    emprestado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        """
        Retorna uma representação em string do objeto Livro.

        Returns:
        - str: Nome do livro.
        """
        return self.nome

class Emprestimos(models.Model):
    """
    Modelo para representar empréstimos de livros.

    Attributes:
    - nome_emprestado: Usuário a quem o livro foi emprestado (ForeignKey para o modelo Usuario, opcional).
    - nome_emprestado_anonimo: Nome do destinatário do empréstimo, caso seja anônimo (CharField, opcional).
    - data_emprestimo: Data em que o livro foi emprestado (DateField, opcional).
    - data_devolucao: Data prevista para a devolução do livro (DateField, opcional).
    - livro: Livro associado ao empréstimo (ForeignKey para o modelo Livros).

    Methods:
    - __str__: Retorna uma representação em string do objeto Emprestimos.

    Returns:
    - str: Representação do empréstimo.
    """

    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    nome_emprestado_anonimo = models.CharField(max_length=30, blank=True, null=True)
    data_emprestimo = models.DateField(blank=True, null=True)
    data_devolucao = models.DateField(blank=True, null=True)
    livro = models.ForeignKey(Livros, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.nome_emprestado} | {self.livro}"
