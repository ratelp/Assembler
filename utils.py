def binario(numero, quantidadeBit):
    # Caso seja passado algum tipo de texto
    if type(numero) == str: 
        try: 
            # Tenta inicialmente transformar em decimal 
            # (para o caso de que seja passado numero binario em texto)
            numero = int(numero,2)
        except:
            # Caso falhar (já é decimal) prossegue com type cast normal para inteiro
            numero = int(numero)

    # Caso seja numero negativo, irá executar o complemento de 2 
    if numero < 0:
        numero = (1 << quantidadeBit) + numero
    # Retorna com a quantidade de numeros necessários preenchidos
    return format(numero, f'0{quantidadeBit}b')


def localizadorDeLabels(nomeArquivo, endereco):
    
    # Acessa arquivo e separa linhas
    arquivo = open(nomeArquivo)
    arquivoLinhas = arquivo.read().split('\n')
    arquivo.close()

    # Irá retirar os caracteres '#' e o que vier após eles de cada linha do arquivo
    listaLinhas = [linha.split('#')[0].strip() for linha in arquivoLinhas]

    # Retirando linhas vazias
    listaLinhas = [linha for linha in listaLinhas if linha]

    # Inicializa lista e contador
    linhaLabel = []
    contador = 0

    # Verifica em cada linha os caracteres, ao localizar ':' guarda o valor da linha
    for linha in listaLinhas:
        contador += 1
        for caractere in linha:
            if caractere == ':':
                # Guardando informações da label na lista
                linhaLabel.append({
                    'label' : linha.split(':')[0],
                    'numLinha' : contador,
                    'endereco' : endereco + (contador-1)*4
                })
                # Caso não tenha instruções na linha da label, irá subtrair 1 para que a linha não seja contada em futuros labels e para que label atual aponte para próxima instrução
                if not any(inst in linha for inst in formato_instrucoes):
                    contador -= 1  
    return linhaLabel

# Função para localizar linha de uma determinada instrução
def localizaLinhaInstrucao(nomeArquivo, instrucao): 
 
   # Acessa arquivo e separa linhas
   arquivo = open(nomeArquivo)
   arquivoLinhas = arquivo.read().split('\n')
   arquivo.close()

   # Irá retirar os caracteres '#' e o que vier após eles de cada linha do arquivo
   listaLinhas = [linha.split('#')[0].strip() for linha in arquivoLinhas]

   # Verifica se em alguma das linhas, possui alguma que não possui nenhuma instrução
   listaLinhas = [linha for linha in listaLinhas if any(inst in linha for inst in formato_instrucoes)]

   # Lista onde ficará o resultado se possui ou não a instrução na linha determinada
   listaValidadora = []

   for i in range(len(listaLinhas)):
      if listaLinhas[i].find(instrucao) != -1:
         listaValidadora.append(1)
      else:
         listaValidadora.append(0)

   # Guarda número da linha de todas as instruções solicitadas
   listaRetorno = []

   for i in range(len(listaValidadora)):
      if listaValidadora[i] == 1:
         listaRetorno.append(i+1)

   return listaRetorno
    
def tradutor(nomeArquivo, posicaoLabels, hexa):

    # Index para se utilizar na manipulação do endereço do formato i
    indexLabelI = 0

    # Coleta cada linha do arquivo enviado separando pelas linhas em uma lista
    arquivo = open(nomeArquivo)
    arquivoLinhas = arquivo.read().split('\n')
    arquivo.close()

    # Irá retirar os caracteres '#' e o que vier após eles de cada linha do arquivo
    listaLinhas = [linha.split('#')[0].strip() for linha in arquivoLinhas]

    # Irá separar cada palavra de cada linha em uma lista
    listaPalavra = [palavra for linha in listaLinhas for palavra in linha.split()]

    # Gerando nome do novo arquivo
    if hexa:
        nomeNovoArquivo = nomeArquivo.split('.')[0] + '.hex'
    else:
        nomeNovoArquivo = nomeArquivo.split('.')[0] + '.bin'
    
    # Abre arquivo para escrição
    arquivoEscrita = open(nomeNovoArquivo, 'w')

    # Caso seja o usuário tenha escolhido '-h' é inserido no arquivo v2.0 raw
    if hexa:
        arquivoEscrita.write('v2.0 raw' + '\n')

    # Para cada palavra em arquivoPalavras irá guardar na lista, retirando os caracteres ',' e '$'
    listaLimpa = [i.replace(',', '').replace('$', '').replace('(','') for i in listaPalavra]

    instrucoes = {}
    for index, palavra in enumerate(listaLimpa):
        bits = ''
        try:
            match palavra:
                
                # Para o FORMATO R ------------------------------------------------------------------------------------------
                # Quando utlizado formato_instrucoes[palavra][x] -> Quantidade de bits padrão para determinada instrução
                # Quando utilizado binario(regs[listaLimpa[index + x]],y) -> Quantidade dependerá do número ou do registrador x index a frente do atual e tera o tamanho de y bits
                
                case ('sll' | 'srl'):
                    bits = formato_instrucoes[palavra][1] + formato_instrucoes[palavra][2] + binario(regs[listaLimpa[index + 2]],5) + binario(regs[listaLimpa[index + 1]],5) + binario(regs[listaLimpa[index + 3]],5) + formato_instrucoes[palavra][6]

                case ('jr'):
                    bits = formato_instrucoes[palavra][1] + binario(regs[listaLimpa[index + 1]],5) + formato_instrucoes[palavra][3] + formato_instrucoes[palavra][4] + formato_instrucoes[palavra][5] + formato_instrucoes[palavra][6] 
                case ('mfhi' | 'mflo' ):
                    bits = formato_instrucoes[palavra][1] + formato_instrucoes[palavra][2]  + formato_instrucoes[palavra][3] + binario(regs[listaLimpa[index + 1]],5) + formato_instrucoes[palavra][5] + formato_instrucoes[palavra][6]
                case ('mult' | 'multu' | 'div' | 'divu'):
                    bits = formato_instrucoes[palavra][1] + binario(regs[listaLimpa[index + 1]],5)  + binario(regs[listaLimpa[index + 2]],5) + formato_instrucoes[palavra][4] + formato_instrucoes[palavra][5] + formato_instrucoes[palavra][6]
                case ('add' | 'addu' | 'sub' | 'subu' | 'and' | 'or' | 'slt' | 'sltu' | 'mul'):
                    bits = formato_instrucoes[palavra][1] + binario(regs[listaLimpa[index + 2]],5)  + binario(regs[listaLimpa[index + 3]],5) + binario(regs[listaLimpa[index + 1]],5) + formato_instrucoes[palavra][5] + formato_instrucoes[palavra][6]
                # Para o FORMATO R ------------------------------------------------------------------------------------------

                # Para o FORMATO I ------------------------------------------------------------------------------------------
                # Quando utlizado formato_instrucoes[palavra][x] -> Quantidade de bits padrão para determinada instrução
                # Quando utilizado binario(regs[listaLimpa[index + x]],y) -> Quantidade dependerá do número ou do registrador x index a frente do atual e tera o tamanho de y bits
                # Para beq e bne foi feito uma função com entitulação 'localizaLinhaInstrucao', com intuito de localizar linha
                # onde está a instrução e assim poder calcular a diferença da posição atual para posição da label

                case('beq' | 'bne'):
                    i = 0 
                    # selecionando linha em que está a label
                    while listaLimpa[index + 3] != posicaoLabels[i]['label']:
                        i += 1
                    bits = formato_instrucoes[palavra][1] + binario(regs[listaLimpa[index + 1]],5)  + binario(regs[listaLimpa[index + 2]],5) + binario((posicaoLabels[i]['numLinha'] - (localizaLinhaInstrucao(nomeArquivo,palavra)[indexLabelI] + 1)),16)
                    # Atualizando index
                    indexLabelI += 1

                case('addi' | 'addiu' | 'slti' | 'sltiu' | 'andi' | 'ori'):
                    bits = formato_instrucoes[palavra][1] + binario(regs[listaLimpa[index + 2]],5)  + binario(regs[listaLimpa[index + 1]],5) + binario(int(listaLimpa[index + 3]),16)
                    

                case('lui'):
                    bits = formato_instrucoes[palavra][1] + formato_instrucoes[palavra][2]  + binario(regs[listaLimpa[index + 1]],5) + binario(int(listaLimpa[index + 2]),16)


                case ('lw' | 'sw'):
                    # listaLimpa[index + 3].split(')')[0] o split é para separar o 9) ficando 9 e ) para poder utilizar forma separada
                    bits = formato_instrucoes[palavra][1] + binario(regs[listaLimpa[index + 3].split(')')[0]],5)  + binario(regs[listaLimpa[index + 1]],5) + binario(int(listaLimpa[index + 2]),16)
                # Para o FORMATO I ------------------------------------------------------------------------------------------


                # Para o FORMATO J ------------------------------------------------------------------------------------------
                # Utiliza do endereço na posicao do label
                case('j' | 'jal'):

                    i = 0 
                    # selecionando linha em que está a label
                    while listaLimpa[index + 1] != posicaoLabels[i]['label']:
                        i += 1
                    
                    valorDiv4 = posicaoLabels[i]['endereco'] >> 2
                    
                    bits = formato_instrucoes[palavra][1] + binario(valorDiv4,26)
                # Para o FORMATO J ------------------------------------------------------------------------------------------   
            
            if palavra in formato_instrucoes.keys():
                if palavra in instrucoes:
                    instrucoes[palavra] += 1
                else:
                    instrucoes[palavra] = 1
            
            if bits:
                if hexa:
                    bits = hex(int(bits,2))[2:].zfill(8)
                arquivoEscrita.write(bits + '\n')

        except KeyError:
            continue
        
    arquivoEscrita.close()

    return instrucoes

# Dicionário de Registradores
regs = {
    'zero' : 0,'0'  :  0,
    'at' : 1,  '1'  :  1,
    'v0' : 2,  '2'  :  2,
    'v1' : 3,  '3'  :  3,
    'a0' : 4,  '4'  :  4,
    'a1' : 5,  '5'  :  5,
    'a2' : 6,  '6'  :  6,
    'a3' : 7,  '7'  :  7,
    't0' : 8,  '8'  :  8,
    't1' : 9,  '9'  :  9,
    't2' : 10, '10' : 10,
    't3' : 11, '11' : 11,
    't4' : 12, '12' : 12,
    't5' : 13, '13' : 13,
    't6' : 14, '14' : 14,
    't7' : 15, '15' : 15,
    's0' : 16, '16' : 16,
    's1' : 17, '17' : 17,
    's2' : 18, '18' : 18,
    's3' : 19, '19' : 19,
    's4' : 20, '20' : 20,
    's5' : 21, '21' : 21,
    's6' : 22, '22' : 22,
    's7' : 23, '23' : 23,
    't8' : 24, '24' : 24,
    't9' : 25, '25' : 25,
    'k0' : 26, '26' : 26,
    'k1' : 27, '27' : 27,
    'gp' : 28, '28' : 28,
    'sp' : 29, '29' : 29,
    'fp' : 30, '30' : 30,
    'ra' : 31, '31' : 31
}

# Dicionário de Instruções

formato_instrucoes = {
    'sll'   : ['R','000000','00000','','','','000000'],
    'srl'   : ['R','000000','00000','','','','000010'],
    'jr'    : ['R','000000','','00000','00000','00000','001000'],
    'mfhi'  : ['R','000000','00000','00000','','00000','010000'],
    'mflo'  : ['R','000000','00000','00000','','00000','010010'],
    'mult'  : ['R','000000','','','00000','00000','011000'],
    'multu' : ['R','000000','','','00000','00000','011001'],
    'div'   : ['R','000000','','','00000','00000','011010'],
    'divu'  : ['R','000000','','','00000','00000','011011'],
    'add'   : ['R','000000','','','','00000','100000'],
    'addu'  : ['R','000000','','','','00000','100001'],
    'sub'   : ['R','000000','','','','00000','100010'],
    'subu'  : ['R','000000','','','','00000','100011'],
    'and'   : ['R','000000','','','','00000','100100'],
    'or'    : ['R','000000','','','','00000','100101'],
    'slt'   : ['R','000000','','','','00000','101010'],
    'sltu'  : ['R','000000','','','','00000','101011'],
    'mul'   : ['R','011100','','','','00000','000010'],

    'beq'   : ['I','000100','','',''],
    'bne'   : ['I','000101','','',''],
    'addi'  : ['I','001000','','',''],
    'addiu' : ['I','001001','','',''],
    'slti'  : ['I','001010','','',''],
    'sltiu' : ['I','001011','','',''],
    'andi'  : ['I','001100','','',''],
    'ori'   : ['I','001101','','',''],
    'lui'   : ['I','001111','00000','',''],
    'lw'    : ['I','100011','','',''],
    'sw'    : ['I','101011','','',''],

    'j'     : ['J','000010',''],
    'jal'   : ['J','000011','']
}