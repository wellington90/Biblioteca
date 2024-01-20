from django.db import models

class Usuario(models.Model):
    """
    Modelo para representar usuários no sistema.

    Attributes:
    - nome: Nome do usuário (CharField).
    - email: Endereço de e-mail do usuário (EmailField).
    - senha: Senha do usuário (CharField).
    - ativo: Indica se o usuário está ativo (BooleanField, padrão False).

    Methods:
    - __str__: Retorna uma representação em string do objeto Usuario.

    Returns:
    - str: Nome do usuário.
    """

    nome = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=64)
    ativo = models.BooleanField(default=False)

    def __str__(self) -> str:
        """
        Retorna uma representação em string do objeto Usuario.

        Returns:
        - str: Nome do usuário.
        """
        return self.nome
