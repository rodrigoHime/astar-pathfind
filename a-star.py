# -*- coding: utf-8 -*-

'''
Implementação do algoritmo de busca do caminho minimo A-Estrela (a*)
Autor/Aluno: Rodrigo Hime
Curso: Bacharelado em Sistemas de Informação - UFRPE
Cadeira: Heurísticas para problemas NP-Completos 
Prof.: Jones Albuquerque
'''

class Node:
    # -- tipo: bloco(-8), piso(11)
    def __init__(self, x = 0, y = 0, tipo = 1, pai = None):
        self.x = x
        self.y = y
        self.custoF = 0 # custo total (custoH + custoG) heuristica
        self.custoH = 0 # custo no atual para o no final(custo da heuristica no caso uma adaptação da manhattan)
        self.custoG = 0 # custo do no atual para o no inicial(custo do movimento)
        self.pai    = pai 
        self.noNorte = None
        self.noSul   = None        
        self.noLeste = None
        self.noOeste = None
        self.valorHeuristica = 1
        self.tipo = tipo

    def __eq__(self, outro):
        if self.x == outro.x and self.y == outro.y:
            return 1
        else:
            return 0

    def __ne__(self, outro):
        if self.x != outro.x or self.y != outro.y:
            return 1
        else:
            return 0

    def getPai(self):
        return self.pai

    # -- coordenadas
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # -- adjacentes
    def getNoNorte(self):
        return self.noNorte

    def setNoNorte(self, no = None):
        self.noNorte = no

    def getNoSul(self):
        return self.noSul

    def setNoSul(self, no = None):
        self.noSul = no

    def getNoLeste(self):
        return self.noLeste

    def setNoLeste(self, no = None):
        self.noLeste = no

    def getNoOeste(self):
        return self.noOeste

    def setNoOeste(self, no = None):
        self.noOeste = no

    # -- custos
    def setCustoF(self, value=0):
        self.custoF = value

    def setCustoH(self, value=0):
        self.custoH = value * self.valorHeuristica

    def setCustoG(self, value=0):
        self.custoG = value * self.valorHeuristica

    def calcCustoH(self, noDestino):
        if self.x > noDestino.x:
            if self.y > noDestino.y:
                self.setCustoH((self.x - noDestino.x) + (self.y - noDestino.y))
            elif self.y < noDestino.y:
                self.setCustoH((self.x - noDestino.x) + (noDestino.y - self.y))
        elif self.x < noDestino.x:
            if self.y > noDestino.y:
                self.setCustoH((noDestino.x - self.x) + (self.y - noDestino.y))
            elif self.y < noDestino.y:
                self.setCustoH((noDestino.x - self.x) + (noDestino.y - self.y))

    def calcCustoF(self, noDestino):

        self.calcCustoH(noDestino)
        self.calcCustoG()
        self.custoF = self.custoH + self.custoG

    def calcCustoG(self):
        no = self
        custo = 0
        while no.pai:
            no = no.pai
            custo += 1
        self.setCustoG(custo)

    def getCustoF(self):
        return self.custoF

class AStar:

    def __init__(self, mapa, inicio_x, inicio_y, dest_x, dest_y):
        self.mapa = mapa
        self.inicio_x = inicio_x
        self.inicio_y = inicio_y
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.listaAberta = []
        self.listaFechada = []

        self.noDestino = Node(self.dest_x, self.dest_y, mapa[dest_x][dest_y])
        self.noInicial = Node(self.inicio_x, self.inicio_y, mapa[inicio_x][inicio_y])
        self.noAtual   = self.noInicial

        self.iniciaBusca()

    def getCaminho(self, no):
        caminho = []
        caminho.append([no.getX(),no.getY()])
        while no.getPai():
            no = no.getPai()
            caminho.append([no.getX(),no.getY()])
        self.novoMapa(caminho)

    def showMapa(self, mapa):
        for j in mapa:
            print j


    def novoMapa(self, caminho):
        self.showMapa(self.mapa)
        print "\n ---------------------//--------------------- \n"
        mapa = self.mapa
        for x in range(0,len(self.mapa)):
            for y in range(0,len(self.mapa[x])):
                if [x,y] in caminho:
                    mapa[x][y] = 10

        self.showMapa(mapa) 

    def verificaFim(self):
        if self.noAtual is not None:
            if self.noAtual == self.noDestino:
                print "\n -- achou -- \n"
                self.getCaminho(self.noAtual)
                return True
            else:
                return False
        else:
            print " -- não achou -- "
            return True

    def iniciaBusca(self):
        self.listaFechada.append(self.noAtual)

        while not self.verificaFim():
            self.noAtual = self.getAdjacenteMenorValor()

    def detectaAdjacentes(self):

        x = self.noAtual.getX()
        y = self.noAtual.getY()

        # -- north
        if (self.mapa[x - 1][y] and self.mapa[x - 1][y] > 0):
            noNorte = Node(x - 1, y, self.mapa[x - 1][y], self.noAtual)
            if noNorte not in self.listaFechada:
                if noNorte not in self.listaAberta:
                    self.listaAberta.append(noNorte)
                    self.noAtual.setNoNorte(noNorte)
                    self.noAtual.getNoNorte().calcCustoF(self.noDestino);

        # -- south
        if (self.mapa[x + 1][y] and self.mapa[x + 1][y] > 0):
            noSul = Node(x + 1, y, self.mapa[x + 1][y], self.noAtual)
            if noSul not in self.listaFechada:
                if noSul not in self.listaAberta:
                    self.listaAberta.append(noSul)
                    self.noAtual.setNoSul(noSul)
                    self.noAtual.getNoSul().calcCustoF(self.noDestino); 

        # -- east 
        if (self.mapa[x][y + 1] and self.mapa[x][y + 1] > 0):
            noLeste = Node(x, y + 1, self.mapa[x][y + 1], self.noAtual)
            if noLeste not in self.listaFechada:
                if noLeste not in self.listaAberta:
                    self.listaAberta.append(noLeste)
                    self.noAtual.setNoLeste(noLeste)
                    self.noAtual.getNoLeste().calcCustoF(self.noDestino);
 
        # -- west
        if (self.mapa[x][y - 1] and self.mapa[x][y - 1] > 0):
            noOeste = Node(x, y - 1, self.mapa[x][y - 1], self.noAtual)
            if noOeste not in self.listaFechada:
                if noOeste not in self.listaFechada:
                    self.listaAberta.append(noOeste)
                    self.noAtual.setNoOeste(noOeste)
                    self.noAtual.getNoOeste().calcCustoF(self.noDestino); 


    def getAdjacenteMenorValor(self):
        
        self.detectaAdjacentes()

        menor = None
        for x in self.listaAberta:
            if menor:
                if x.getCustoF() < menor.getCustoF():
                    menor = x
            else:
                menor = x

        self.listaAberta = [s for s in self.listaAberta  if s != menor] # remove o menor da lista aberta 
        self.listaFechada.append(menor) # coloca o menor na lista fechada
        
        return menor

    def calcCustoF(self, no, noDestino):
        if no.x > noDestino.x:
            if no.y > noDestino.y:
                return ((no.x - noDestino.x) + (no.y - noDestino.y))
            elif no.y < noDestino.y:
                return ((no.x - noDestino.x) + (noDestino.y - no.y))
        elif no.x < noDestino.x:
            if no.y > noDestino.y:
                return ((noDestino.x - no.x) + (no.y - noDestino.y))
            elif no.y < noDestino.y:
                return ((noDestino.x - no.x) + (noDestino.y - no.y))
        


if __name__ == '__main__':

    # -- tipo: bloco(-8), piso(11)
    #         y  y  y  y  y  y  y  y  y  y  y  y  y  y  y  y
    mapa = [[-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8], # x
            [-8,11,11,-8,11,11,11,11,-8,11,11,11,11,11,11,-8], # x
            [-8,11,11,-8,11,11,11,11,-8,11,11,11,11,11,11,-8], # x
            [-8,11,-8,-8,11,-8,11,11,11,11,11,11,11,-8,11,-8], # x
            [-8,11,11,-8,11,11,11,11,11,11,11,11,11,11,11,-8], # x
            [-8,11,11,-8,-8,11,-8,11,11,11,11,11,-8,11,11,-8], # x
            [-8,11,-8,11,11,11,11,-8,11,11,11,11,-8,11,-8,-8], # x
            [-8,11,11,11,11,-8,11,11,-8,-8,-8,-8,-8,11,11,-8], # x
            [-8,11,11,11,11,11,-8,11,11,11,-8,11,11,11,11,-8], # x
            [-8,11,11,11,11,11,11,-8,11,11,-8,11,11,11,11,-8], # x
            [-8,11,11,11,11,11,11,-8,11,11,11,11,11,11,11,-8], # x
            [-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8]] # x    

    AStar(mapa, 1, 1, 10, 14)






