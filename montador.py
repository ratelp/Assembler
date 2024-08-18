
from utils import binario, localizadorDeLabels, regs, instrucoes
import sys 

listArg = sys.argv # Coleta os argumentos
nomeArquivo = 0 # inicializa nomeArquivo
parametro = 0 # inicializa parametro
posicaoLabels = [] # inicializa lista que irá coletar a posição dos labels

if len(listArg) > 1:
    nomeArquivo = listArg[1] # Coleta o nome do arquivo a ser lido 
    parametro = listArg[2] # Coleta o parâmetro para ser utilizado

    posicaoLabels = localizadorDeLabels(nomeArquivo) # Localiza Labels e guarda as informações na lista


# Verifica se foi repassado parâmetro e encaminha para determinada opção escolhida
if parametro != 0:
    if parametro == "-b":
        print("-b")
    elif parametro == "-h":
        print("-h")
    else:
        print("Parâmetro inválido")

