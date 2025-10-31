import copy
from modelos.contrato import Contrato # Assumindo que esta importação está correta

class Posicao:
    # Variável de classe para gerar IDs únicos.
    _contador_id = 0

    def __init__(self):
        # 💡 Correção: Atribui um ID único e incrementa o contador de classe.
        self._id = Posicao._contador_id
        Posicao._contador_id += 1 

        self._qtd_contratos = 0
        self._preco_medio = 0.0
        self._resultado = 0.0 # Resultado acumulado da posição
        self._historico = [] # Para o método desfazer
        self._tipo = ''      # 'comprado' ou 'vendido'
        self._ativo = ''     # 'dólar' ou 'índice'
        self._contratos = [] # Histórico detalhado de entradas/saídas

    def entrada(self, qtd_contrato, contrato: Contrato):
        # 1. Salva o estado atual ANTES de modificar, para o 'desfazer'
        self._salvar_estado_historico()

        # 2. Validações iniciais (Impede trocar ativo/tipo)
        if self._qtd_contratos > 0:
            if contrato._ativo.lower() != self._ativo.lower():
                # Reverte o histórico (operação não permitida)
                self._historico.pop() 
                return f"Erro: já existe posição aberta em {self._ativo.title()}, não é possível operar {contrato._ativo.title()}."
            if contrato._tipo_operacao.lower() != self._tipo.lower():
                # Reverte o histórico (operação não permitida)
                self._historico.pop() 
                return f"Erro: a posição atual é '{self._tipo}', não é possível adicionar contratos '{contrato._tipo_operacao.lower()}'."
            
        self._ativo = contrato._ativo.lower() # Garante que o ativo está em minúsculas
        self._tipo = contrato._tipo_operacao.lower() # Garante o tipo em minúsculas

        # 3. Lógica de Preço Médio e Quantidade
        if self._qtd_contratos == 0:
            # Primeira entrada
            self._preco_medio = contrato._preco
            self._qtd_contratos = qtd_contrato
        else:
            # Entrada adicional (recalcula preço médio)
            self._calcular_novo_preco_medio(qtd_contrato, contrato)

        # 4. Adiciona o novo contrato ao histórico de operações
        self._contratos.append({
            'Posição ID': self._id,
            'Ativo': self._ativo,
            'Quantidade contratos': qtd_contrato,
            'Tipo': self._tipo,
            'Direção': contrato._tipo_acao, # 'Entrada'
            'Preço': contrato._preco
        })
        
        # 5. O estado final da operação JÁ foi salvo no início, antes de qualquer alteração

    def saida(self, qtd_contrato, contrato: Contrato):
        # 1. Salva o estado atual ANTES de modificar
        self._salvar_estado_historico()

        # 2. Valida quantidade
        if qtd_contrato > self._qtd_contratos:
            self._historico.pop() # Remove o estado salvo se a operação for inválida
            print("Quantidade de contratos maior que a quantidade posicionada!")
            return

        # 3. Calcula o resultado financeiro da saída
        if self._ativo == "dólar":
            if self._tipo == "comprado":
                self._calcular_saida_dolar_comprado(qtd_contrato, contrato)
            elif self._tipo == "vendido":
                self._calcular_saida_dolar_vendido(qtd_contrato, contrato)
        
        elif self._ativo == "índice":
            if self._tipo == "comprado":
                self._calcular_saida_indice_comprado(qtd_contrato, contrato)
            elif self._tipo == "vendido":
                self._calcular_saida_indice_vendido(qtd_contrato, contrato)
        
        # 4. Atualiza a quantidade de contratos
        self._qtd_contratos -= qtd_contrato

        # 5. Adiciona o contrato de saída ao histórico
        self._contratos.append({
            'Posição ID': self._id,
            'Ativo': self._ativo,
            'Quantidade contratos': qtd_contrato * -1, # Usa negativo para representar saída
            'Tipo': self._tipo,
            'Direção': contrato._tipo_acao, # 'Saída'
            'Preço': contrato._preco
        })

        # 6. 💡 Zerar a posição se a quantidade for zero
        if self._qtd_contratos == 0:
            self._ativo = ''
            self._tipo = ''
            self._preco_medio = 0.0 # Resultado é mantido em self._resultado

    def desfazer(self):
        if not self._historico:
            print("Nenhuma ação para desfazer.")
            return

        # Reverte o estado para o estado anterior ao último salvo
        ultimo_estado = self._historico.pop()
        self._preco_medio = ultimo_estado['preco_medio']
        self._qtd_contratos = ultimo_estado['qtd_contratos']
        self._resultado = ultimo_estado['resultado']
        self._ativo = ultimo_estado['ativo']
        self._tipo = ultimo_estado['tipo']
        self._contratos = copy.deepcopy(ultimo_estado['contratos'])

        print("Ação desfeita com sucesso.")

    # --------------------------
    # MÉTODOS INTERNOS (CÁLCULO)
    # --------------------------
    
    def _salvar_estado_historico(self):
        """Salva o estado atual da posição antes de uma nova operação."""
        self._historico.append({
            'preco_medio': self._preco_medio,
            'qtd_contratos': self._qtd_contratos,
            'resultado': self._resultado,
            'ativo': self._ativo,
            'tipo': self._tipo,
            'contratos': copy.deepcopy(self._contratos)
        })

    def _calcular_novo_preco_medio(self, qtd_contrato, contrato: Contrato):
        """Recalcula o preço médio ao adicionar mais contratos."""
        total_antigo = self._preco_medio * self._qtd_contratos
        total_novo = contrato._preco * qtd_contrato
        
        nova_qtd = self._qtd_contratos + qtd_contrato
        
        self._preco_medio = (total_antigo + total_novo) / nova_qtd
        self._qtd_contratos = nova_qtd
        
    def _calcular_saida_dolar_comprado(self, qtd_contrato, contrato: Contrato):
        """Calcula e acumula o resultado (Comprado no Dólar)."""
        # 💡 Correção: Usa += para ACUMULAR o resultado da saída
        self._resultado += ((contrato._preco - self._preco_medio) * 10000) * qtd_contrato

    def _calcular_saida_dolar_vendido(self, qtd_contrato, contrato: Contrato):
        """Calcula e acumula o resultado (Vendido no Dólar)."""
        # 💡 Correção: Usa += para ACUMULAR o resultado da saída
        self._resultado += ((self._preco_medio - contrato._preco) * 10000) * qtd_contrato

    def _calcular_saida_indice_comprado(self, qtd_contrato, contrato: Contrato):
        """Calcula e acumula o resultado (Comprado no Índice)."""
        # 💡 Correção: Usa += para ACUMULAR o resultado da saída
        self._resultado += ((contrato._preco - self._preco_medio) * 0.2) * qtd_contrato

    def _calcular_saida_indice_vendido(self, qtd_contrato, contrato: Contrato):
        """Calcula e acumula o resultado (Vendido no Índice)."""
        # 💡 Correção: Usa += para ACUMULAR o resultado da saída
        self._resultado += ((self._preco_medio - contrato._preco) * 0.2) * qtd_contrato
    
    # --------------------------
    # REPRESENTAÇÃO E LISTAGEM
    # --------------------------
    def __str__(self):
        status = f" ({self._tipo.upper()} em {self._ativo.title()})" if self._qtd_contratos > 0 else " (POSIÇÃO FECHADA)"
        return (
            f"Posição ID: {self._id}{status} | "
            f"Contratos: {self._qtd_contratos} | "
            f"Preço médio: {self._preco_medio:.2f} | "
            f"Lucro/Prejuízo Total: {self._resultado:.2f}"
        )

    def listar_contratos(self):
        return self._contratos