from modelos.contrato import Contrato

class Posicao:
    _id = -1

    def __init__(self):
        self._id += 1
        self._qtd_contratos = 0
        self._preco_medio = 0.0
        self._precos = []
        self._resultado = 0.0
        self._historico = []
        self._tipo = ''
        self._ativo = ''
        self._contratos = []



    def entrada(self, qtd_contrato, contrato: Contrato):
        self._historico.append({
            'preco_medio': self._preco_medio,
            'qtd_contratos': self._qtd_contratos,
            'resultado': self._resultado
        })
        self._ativo = contrato._ativo

        if self._qtd_contratos == 0:
            self._preco_medio = contrato._preco
            self._qtd_contratos += qtd_contrato
            self._precos.append(contrato._preco)
        else:
            self.calcular_preco_medio(qtd_contrato, contrato)

    
        if contrato._tipo_operacao.lower() == "comprado":
            self._tipo = "comprado"
        elif contrato._tipo_operacao.lower() == "vendido":
            self._tipo = "vendido"

        self._contratos.append(
            {'Posição ID' : self._id,
            'Ativo' :  self._ativo,
            'Quantidade contratos' : qtd_contrato,
            'Tipo': self._tipo,
            'Direção' :  contrato._tipo_acao,
            'Preço' : contrato._preco}
        )



    def desfazer(self):
        """Restaura o último estado antes da alteração"""
        if not self._historico:
            print("Nenhuma ação para desfazer.")
            return

        ultimo_estado = self._historico.pop()
        self._preco_medio = ultimo_estado['preco_medio']
        self._qtd_contratos = ultimo_estado['qtd_contratos']
        self._resultado = ultimo_estado['resultado']
        self._contratos.pop()
        print("Ação desfeita com sucesso.")



    def calcular_preco_medio(self, qtd_contrato, contrato: Contrato):
        total_antigo = self._preco_medio * self._qtd_contratos
        total_novo = contrato._preco * qtd_contrato
        self._preco_medio = (total_antigo + total_novo) / (self._qtd_contratos + qtd_contrato)
        self._qtd_contratos += qtd_contrato
    

    def saida(self, qtd_contrato, contrato : Contrato):

        if contrato._ativo.lower() == "dólar" : 
            if qtd_contrato > self._qtd_contratos:
                print("Quantidade de contratos maior que a quantidade posicionada!")
            else:
                self._qtd_contratos -= qtd_contrato
                if contrato._tipo_operacao.lower() == "comprado" and contrato._tipo_acao.lower() == "saída":
                    self.saida_comprado_dolar(qtd_contrato,contrato)
                elif contrato._tipo_operacao.lower() == "vendido" and contrato._tipo_acao.lower() == "saída":
                    self.saida_vendido_dolar(qtd_contrato,contrato)
                else:
                    print("Erro")

        elif contrato._ativo.lower() == "índice":
            if qtd_contrato > self._qtd_contratos:
                print("Quantidade de contratos maior que a quantidade posicionada!")

            else:
                self._qtd_contratos -= qtd_contrato
                if contrato._tipo_operacao.lower() == "comprado" and contrato._tipo_acao.lower() == "saída":
                    self.saida_comprado_indice(qtd_contrato,contrato)
                elif contrato._tipo_operacao.lower() == "vendido" and contrato._tipo_acao.lower() == "saída":
                    self.saida_vendido_indice(qtd_contrato,contrato)
                else:
                    print("Erro")




    def saida_comprado_dolar(self, qtd_contrato, contrato : Contrato):
            self._resultado = ((contrato._preco - self._preco_medio) * 10000) * qtd_contrato
    
    def saida_vendido_dolar(self, qtd_contrato, contrato : Contrato):
            self._resultado = ((self._preco_medio - contrato._preco) * 10000) * qtd_contrato


    def saida_comprado_indice(self, qtd_contrato, contrato : Contrato):
            self._resultado = ((contrato._preco - self._preco_medio) * 0.2) * qtd_contrato
    
    def saida_vendido_indice(self, qtd_contrato, contrato : Contrato):
            self._resultado = ((self._preco_medio - contrato._preco) * 0.2) * qtd_contrato


        

    def __str__(self):
        return f'Posição id : {self._id} | Quantidade de contratos : {self._qtd_contratos} \
                Preço médio : {self._preco_medio} | Lucro/Prejuízo  : {round(self._resultado,2)}'

        
    def listar_contratos(self):
        return self._contratos