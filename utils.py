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


def localizadorDeLabels(nomeArquivo):
    
    # Acessa arquivo e separa linhas
    arquivo = open(nomeArquivo)
    arquivoPalavras = arquivo.read().split('\n')

    # Inicializa lista e contador
    linhaLabel = []
    contador = 0

    # Verifica em cada linha os caracteres, ao localizar ':' guarda o valor da linha
    for linha in arquivoPalavras:
        contador += 1
        for caractere in linha:
            if caractere == ':':
                # Guardando informações da label na lista
                linhaLabel.append({
                    'label' : linha.split(':')[0],
                    'numLinha' : contador,
                    'endereco' : 0x00400000 + (contador-1)*4
                })    

    return linhaLabel

# Dicionário de Registradores
regs = {
    'ze' : 0,  '0'  :  0,
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

instrucoes = {
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
    'sw'    : ['I','101100','','',''],

    'j'     : ['J','000010',''],
    'jal'   : ['J','000011',''],
}