
from utils import tradutor, localizadorDeLabels
from cpi import CalculadoraCPI
import sys 

listArg = sys.argv # Coleta os argumentos
nomeArquivo = 0 # inicializa nomeArquivo
parametro = 0 # inicializa parametro
posicaoLabels = [] # inicializa lista que irá coletar a posição dos labels
enderecoInicial = 0x00400000 # inicializa endereço inicial

if len(listArg) > 1:
    nomeArquivo = listArg[1] # Coleta o nome do arquivo a ser lido 
    parametro = listArg[2] # Coleta o parâmetro para ser utilizado

    posicaoLabels = localizadorDeLabels(nomeArquivo, enderecoInicial) # Localiza Labels e guarda as informações na lista


calculadora_cpi = CalculadoraCPI('ciclos.csv') # Inicializa calculadora de CPI

# Verifica se foi repassado parâmetro e encaminha para determinada opção escolhida
if parametro != 0:
    if parametro == "-b":
        instrucoes = tradutor(nomeArquivo,posicaoLabels, False)

        if instrucoes:     
            print('Quantidades por tipo de instruções:')
            for i, qt in instrucoes.items():
                print(f'{i}: {qt}')

            print()
            print(f'CPI Médio: {calculadora_cpi.calcular(instrucoes)}')

    elif parametro == "-h":
        instrucoes = tradutor(nomeArquivo,posicaoLabels, True)
        if instrucoes:
            print('Quantidades por tipo de instruções:')
            for i, qt in instrucoes.items():
                print(f'{i}: {qt}')

            print() # Pular linha
            print(f'CPI Médio: {calculadora_cpi.calcular(instrucoes)}')

    else:
        print("Parâmetro inválido")

