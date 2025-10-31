from modelos.usuario import Usuario

class Analista(Usuario):
    def __init__(self, nome: str, email: str, data_nascimento: date,senha:str, area: str):
            super().__init__(nome, email, data_nascimento,senha)
            self._area = area 

    def __str__(self):
            return f"Analista: {self._nome} | Área: {self._area} | Email: {self._email}"