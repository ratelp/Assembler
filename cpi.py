import pandas as pd

class CalculadoraCPI:
    """
    Calcula o CPI do programa com base em um arquivo .csv
    """

    valores = {}
    def __init__(self, filename):
        # Lê arquivo fornecido e salva informações em 'valores'
        # Formato de 'valores': {'instrucao': qt_ciclos}
        for v in pd.read_csv(filename).values:
            self.valores[v[0]] = v[1]
    
    def calcular(self, instrucoes):
        """
        Calcula CPI médio do conjunto de instruções fornecidas
        """
        total_ciclos = 0

        for i, qt in instrucoes.items():
            total_ciclos += self.valores[i] * qt

        return total_ciclos / sum(instrucoes.values())