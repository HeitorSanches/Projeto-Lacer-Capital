import math
import numpy as np
import plotly.express as px
from scipy.interpolate import make_interp_spline


def gauss(qtd_contratos):
    um_centavo = math.ceil(qtd_contratos * 0.15)
    dois_centavos = math.ceil(qtd_contratos * 0.70)
    tres_ou_mais_centavos = math.ceil(qtd_contratos * 0.15)

    soma = um_centavo + dois_centavos + tres_ou_mais_centavos
    if soma > qtd_contratos:
        excesso = soma - qtd_contratos
        dois_centavos -= excesso

    print(f'Liquidar com 1 centavo: {um_centavo}')
    print(f'Liquidar com 2 centavos: {dois_centavos}')
    print(f'Liquidar com 3 ou mais centavos: {tres_ou_mais_centavos}')

    x = np.array([1, 2, 3])
    y = np.array([um_centavo, dois_centavos, tres_ou_mais_centavos])

    x_suave = np.linspace(x.min(), x.max(), 200)
    spl = make_interp_spline(x, y, k=2)
    y_suave = spl(x_suave) * 1.5  

    fig = px.line(
        x=x_suave, y=y_suave,
        title='Distribuição Suavizada por Centavos',
        labels={'x': 'Centavos', 'y': 'Quantidade'}
    )

    fig.update_traces(fill='tozeroy', line=dict(width=4))

    fig.add_scatter(
        x=x,
        y=y * 1.5,
        mode='markers+text',
        text=[f"{int(valor)}" for valor in y],
        textposition='top center',
        marker=dict(size=8, color='red'),
        name='Valores'
    )

    fig.update_layout(height=600, width=900, yaxis_range=[0, max(y_suave) * 1.1])
    fig.show()
        


def main():
    while True:
        try:
            qtd_contratos = int(input("Digite a quantidade de contratos (mínimo 3): "))
            if qtd_contratos >= 3:
                gauss(qtd_contratos)
                break  # Sai do loop após executar gauss()
            else:
                print("Quantidade menor que 3! Digite novamente.")
        except ValueError:
            print("Erro: digite um número inteiro válido.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

main()




