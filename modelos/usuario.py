import hashlib
from datetime import date

class Usuario:
    def __init__(self, nome: str, email: str,  data_nascimento: date,senha : str):
        self._nome = nome.title()
        self._email = email
        self._data_nascimento = data_nascimento
        self._senha = senha  
        self._ativo = False

    @property
    def ativar(self):
        self._ativo = True
        
    @property
    def desativar(self):
        self._ativo = False

    def __str__(self):
        return f"{self._nome} ({self._email})"
