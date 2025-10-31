from flask import Flask, render_template, request, redirect, url_for
from modelos.contrato import Contrato
from modelos.posicao import Posicao

app = Flask(__name__)

posicao = Posicao()

@app.route("/")
def index():
    contratos = posicao.listar_contratos()
    return render_template("index.html", posicao=posicao)

@app.route("/entrada", methods=["POST"])
def entrada():
    ativo = request.form["ativo"]
    tipo_operacao = request.form["tipo_operacao"]
    preco = float(request.form["preco"])
    qtd = int(request.form["qtd"])
    
    # Cria o objeto Contrato
    contrato = Contrato(tipo_operacao, "Entrada", preco, ativo)
    
    # 💡 CORREÇÃO: Chama o método APENAS UMA VEZ.
    # O método 'entrada' retorna uma string de erro OU None (se for bem-sucedido).
    erro = posicao.entrada(qtd, contrato) 

    if erro:
        # Se retornar uma string de erro (ex: "não é possível operar outro ativo")
        # o histórico já foi desfeito dentro do método 'entrada' da classe Posicao.
        return render_template('index.html', posicao=posicao, erro=erro)
    else:
        # Se for None, significa sucesso
        return redirect(url_for("index"))

@app.route("/saida", methods=["POST"])
def saida():
    ativo = posicao._ativo
    preco = float(request.form["preco"])
    qtd = int(request.form["qtd"])

    if posicao._tipo.lower() == "comprado":
        contrato = Contrato("comprado", "Saída", preco,ativo)
        posicao.saida(qtd, contrato)
    elif posicao._tipo.lower() == "vendido":
        contrato = Contrato("vendido", "Saída", preco,ativo)
        posicao.saida(qtd, contrato)

    return redirect(url_for("index"))

        

@app.route("/desfazer", methods=["POST"])
def desfazer():
    posicao.desfazer()
    return redirect(url_for("index"))

@app.route("/listar_contratos", methods=["POST"])
def listar_contratos():
    contratos = posicao.listar_contratos()  # retorna uma lista
    return render_template("index.html", posicao=posicao, contratos=contratos)


if __name__ == "__main__":
    app.run(debug=True)
