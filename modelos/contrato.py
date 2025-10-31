class Contrato:
    _id = -1


    def __init__(self, tipo_operacao : str , tipo_acao : str, preco : float , ativo : str):
        self._id += 1
        self._tipo_operacao = tipo_operacao
        self._preco = preco
        self._tipo_acao = tipo_acao
        self._ativo = ativo
    
    
    def __repr__(self):
        return f"{self._ativo} | {self._tipo_operacao} |  Preço: {self._preco:.2f}"