#Feito por: Miguel Rodrigues Guimaraes de Oliveira
#Matricula: 201910339
#Curso: GCC108 - Teoria da Computacao
#Professor: Rafael S. Durelli
#

import sys

#estrutura para armazenar a maquina de turing
class estado:
    def __init__(self, valor):
        self.valor = valor
        self.__transicoes = []
    #adiciona(add) uma transicao
    def add_transicao(self, char_in, char_out, prox_estado, mov_fita):
        self.__transicoes.append({"char_in": char_in, 
                          "char_out": char_out,
                          "prox_estado": prox_estado,
                          "mov_fita": mov_fita  })
    #pega(get) um dado da transicao
    def get_dt(self, pos, string):
        return self.__transicoes[pos][string]
    #pega(get) a quantidade de transicoes que tem
    def get_qtdt(self):
        return len(self.__transicoes)

#retira da linha de alguns caracteres
def limpa(linha, vet_apaga):
    for caracter in vet_apaga:
        linha = linha.replace(caracter, '')
    return linha

#le os estados do arquivo e retorna a quantidade
def cria_estados(mt):
    linha = mt.readline() #"queimar" primeira linha que possui apenas um (
    linha = mt.readline() #recebe os estados
    qtd_estados = 0
    estados = []
    for c in linha:
        if(c == 'q'):
            estados.append( estado(qtd_estados) )
            qtd_estados += 1
    return estados

#recebe as transicoes e verifica se sao validas
def transicoes(estados, abc_fita, mt):
    linha = mt.readline();
    linha = mt.readline()
    linha = linha.replace('-',',')
    linha = limpa(linha, "\t ()>\n")
    linha = linha.split(',')

    while linha[0] != '}':
        pos_estado = int(linha[0].replace('q',''),10)
        pos_prox = int(linha[2].replace('q',''),10)

        tem_in = False
        tem_out = False
        for carac in abc_fita:
            if carac == linha[1]:
                tem_in = True
            if carac == linha[3]:
                tem_out = True

        l_ou_r = 1
        if linha[4] == 'L':
            l_ou_r = -1
        elif linha[4] == 'R':
            l_ou_r = 1
        else:
            raise Exception("Caracter invalido: na parte de movimentação é necessário usar apenas L ou R")
        if tem_in and tem_out :
            estados[pos_estado].add_transicao(linha[1], linha[3], pos_prox, l_ou_r)
        else:
            raise Exception("Houve algum problema na hora da criação da máquina")
        linha = mt.readline()
        linha = linha.replace('-',',')
        linha = limpa(linha, "\t ()>\n")
        linha = linha.split(',')

    return estados

#escreve o estado da fita com 
def escreve_saida(fita, estado_atual, saida):
    for a in range(len(fita)):
        if a == pos_fita:
            saida.write("{q"+str(estado_atual)+'}')
        saida.write(fita[a])
    saida.write('\n')

#caso tenha transicao, informa a posicao dela, caso nao tenha, retorna -1
def tem_transicao(e, pos_fita):
    for aux in range(e.get_qtdt()):
        if fita[pos_fita] == e.get_dt(aux, "char_in"):
            return aux 
    return -1




#inicio

#abre arquivos
try:
    mt = open(sys.argv[1], 'r') #arquivo que contem descricao da mt (maquina de turing)
except(e):
    raise Exception("Houve problema ao abrir o arquivo de entrada.")
    
    
#declaro variaveis
estados = [] #armazena estados e suas transicoes
abc_entrada = [] #alfabeto de entrada
abc_fita = [] #alfabeto da fita
estado_inicial = '' #estado inicial
fita = '' #entrada da fita
vet_apaga = "\t {},\n" #caracteres que devem ser apagados de algumas linhas

#atribuo valor as variaves
try:
    estados = cria_estados(mt)
    abc_entrada = limpa(mt.readline(), vet_apaga)
    abc_fita = limpa(mt.readline(), vet_apaga)
    estados = transicoes(estados, abc_fita, mt)
    estado_inicial = int(limpa(mt.readline(), vet_apaga + 'q'), 10)
    mt.readline()
    fita = limpa(mt.readline(), vet_apaga)
except(e):
    raise Exception("Houve problema ao criar os estados")
    
if abc_entrada[0] != "1":
    raise Exception("Alfabeto de entrada invalido. Alfabeto", abc_entrada)

mt.close()

try:
    saida = open(sys.argv[2], 'w') #arquivo onde sera escrito o processamento da mt
except(e):
    raise Exception("Houve problemas ao criar o arquivo de saida.")
#roda entrada na maquina
estado_atual = estado_inicial
pos_fita = 0
pos_transicao = 0


while pos_transicao != -1:
    try:
        e = estados[estado_atual]
        pos_transicao = tem_transicao(e, pos_fita)
        escreve_saida(fita, estado_atual, saida)
        
        if pos_transicao != -1:
            fita = fita[:pos_fita] + e.get_dt(pos_transicao, "char_out") + fita[pos_fita+1:]
            pos_fita = pos_fita + e.get_dt(pos_transicao, "mov_fita")
            if(pos_fita == len(fita)):
                fita = fita + "B"
            estado_atual = e.get_dt(pos_transicao, "prox_estado")
    except(e):
        raise Exception("Houve problema na execução da maquina\n: ", e)
    


saida.close()
#fim
