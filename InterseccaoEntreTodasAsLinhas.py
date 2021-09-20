# **********************************************************************
# PUCRS/FACIN
# COMPUTAÇÃO GRÁFICA
#
# Teste de colisão em OpenGL
#       
# Marcio Sarroglia Pinho
# pinho@inf.pucrs.br
# **********************************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
from Celula import Celula
import collections
import math
import time
import numpy as np

N_LINHAS = 500
MAX_X = 100

ContadorInt = 0
ContChamadas = 0
interAltura = 0
interLargura = 0
linhas = []
subdivisoesAltura = 2
subdivisoesLargura = 2
matriz = [[]]
#matriz = np.empty((subdivisoesAltura, subdivisoesLargura), Celula()) 
#matriz = np.full((subdivisoesAltura, subdivisoesLargura), Celuloa())
#matriz = [[Celula() for i in range(subdivisoesAltura)] for j in range(subdivisoesLargura)]
#matriz = np.full((subdivisoesAltura, subdivisoesLargura), [])

# **********************************************************************
#  init()
#  Inicializa os parâmetros globais de OpenGL
#/ **********************************************************************
def init():
    global linhas
    global matriz
    GeraSubdivisoes()

    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    linhas = [Linha() for i in range(N_LINHAS)]
    #matriz = [[Celula() for i in range(subdivisoesAltura)] for j in range(subdivisoesLargura)]
    matriz = [[list() for i in range(subdivisoesAltura+1)] for j in range(subdivisoesLargura+1)]

    for indice, linha in enumerate(linhas):
        linha.geraLinha(MAX_X, 10)
        CadastraLinhaNasSubdivisoes(indice, linha)

# **********************************************************************
# CadastraLinhaNasSubdivisoes(indice: int, linha :Linha)
# armazena a linha na posição 'indice' da matriz 
# **********************************************************************
def CadastraLinhaNasSubdivisoes(indice: int, linha: Linha):
    global matriz
    linha.miny = 0 if linha.miny < 0 else linha.miny
    linha.minx = 0 if linha.minx < 0 else linha.minx
    linha.maxy = 0 if linha.maxy < 0 else linha.maxy
    linha.maxx = 0 if linha.maxx < 0 else linha.maxx
    linha.miny = 100 if linha.miny > 100 else linha.miny
    linha.minx = 100 if linha.minx > 100 else linha.minx
    linha.maxy = 100 if linha.maxy > 100 else linha.maxy
    linha.maxx = 100 if linha.maxx > 100 else linha.maxx

    yMin = math.floor(linha.miny / interAltura)
    xMin = math.floor(linha.minx / interLargura)
    yMax = math.floor(linha.maxy / interAltura)
    xMax = math.floor(linha.maxx / interLargura)
    #print(yMin, yMax)
    #print(xMin, xMax)
    if yMin == yMax and xMin == xMax:
        matriz[yMin][xMin].append(indice)
    elif yMin != yMax and xMin == xMax:
        for y in range(yMin, yMax):
            matriz[y][xMin].append(indice)
    elif yMin == yMax and xMin != xMax:
        for x in range(xMin, xMax):
            matriz[yMin][x].append(indice)
    elif yMin != yMax and xMin != xMax:
        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                matriz[y][x].append(indice)

        #for y in range (yMin, yMax):
            #if xMin != xMax:
                #for x in range(xMin, xMax):
                    #matriz[y][x].append(indice)
            #else:
                    #matriz[y][x].append(indice)
    #else: 
        #for x in range(xMin, xMax):
            #matriz[yMin][x].append(indice)



# **********************************************************************
#  GeraSubdivisoes( )
#  Subdivide a janela em linhas e colunas
#
# **********************************************************************
def GeraSubdivisoes():
    global subdivisoesAltura
    global subdivisoesLargura
    global interAltura 
    global interLargura 
    interLargura = 100 / subdivisoesLargura
    interAltura = 100 / subdivisoesAltura



# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    # Reseta coordenadas do sistema antes the modificala
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Define os limites lógicos da área OpenGL dentro da Janela
    glOrtho(0, 100, 0, 100, 0, 1)

    # Define a área a ser ocupada pela área OpenGL dentro da Janela
    glViewport(0, 0, w, h)

    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ********************************************************************** */
#                                                                        */
#  Calcula a interseccao entre 2 retas (no plano "XY" Z = 0)             */
#                                                                        */
# k : ponto inicial da reta 1                                            */
# l : ponto final da reta 1                                              */
# m : ponto inicial da reta 2                                            */
# n : ponto final da reta 2                                              */
# 
# Retorna:
# 0, se não houver interseccao ou 1, caso haja                                                                       */
# int, valor do parâmetro no ponto de interseção (sobre a reta KL)       */
# int, valor do parâmetro no ponto de interseção (sobre a reta MN)       */
#                                                                        */
# ********************************************************************** */
def intersec2d(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> (int, float, float):
    det = (n.x - m.x) * (l.y - k.y)  -  (n.y - m.y) * (l.x - k.x)

    if (det == 0.0):
        return 0, None, None # não há intersecção

    s = ((n.x - m.x) * (m.y - k.y) - (n.y - m.y) * (m.x - k.x))/ det
    t = ((l.x - k.x) * (m.y - k.y) - (l.y - k.y) * (m.x - k.x))/ det

    return 1, s, t # há intersecção

# **********************************************************************
# HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto)
# Detecta interseccao entre os pontos
#
# **********************************************************************
def HaInterseccao(k: Ponto, l: Ponto, m: Ponto, n: Ponto) -> bool:
    ret, s, t = intersec2d( k,  l,  m,  n)

    if not ret: return False

    return s>=0.0 and s <=1.0 and t>=0.0 and t<=1.0


# **********************************************************************
# HaInterseccaoAABB(E1: Linha, E2: Linha)
# Detecta interseccao entre duas AABB
#
# **********************************************************************
def HaInterseccaoAABB(E1: Linha, E2: Linha) -> bool:
    if (abs(E1.centro[0] - E2.centro[0]) > E1.meiaLarg + E2.meiaLarg):
        return False
    if (abs(E1.centro[1] - E2.centro[1]) > E1.meiaAltura + E2.meiaAltura):
        return False
    return True



# **********************************************************************
# DesenhaLinhas()
# Desenha as linha na tela
#
# **********************************************************************
def DesenhaLinhas():
    global linhas

    glColor3f(0,0,0)

    for linha in linhas:
        linha.desenhaLinha()

# **********************************************************************
# DesenhaCenario()
# Desenha o cenario
#
# **********************************************************************
def DesenhaCenario():
    global ContChamadas, ContadorInt, matriz

    PA, PB, PC, PD, = Ponto(), Ponto(), Ponto(), Ponto() 
    ContChamadas, ContadorInt = 0, 0
    
    # Desenha as linhas do cenário
    glLineWidth(1)
    glColor3f(1,0,0)
    
    for i in range(N_LINHAS):
        PA.set(linhas[i].x1, linhas[i].y1)
        PB.set(linhas[i].x2, linhas[i].y2)
        vetCandidatas = GeraCandidatasAColisao(linhas[i])
        for j in vetCandidatas:  
                PC.set(j.x1, j.y1)
                PD.set(j.x2, j.y2)
                if HaInterseccaoAABB(linhas[i], j):
                    ContChamadas += 1
                    if HaInterseccao(PA, PB, PC, PD):
                        ContadorInt += 1
                        linhas[i].desenhaLinha()
                        j.desenhaLinha()
                else:
                    pass
            
# **********************************************************************
# GeraCandidatasAColisao(index: int) -> List[Linha()]
# Função que gera uma lista de linhas candidatas, baseada na subdivisão do espaço,
# à colisão com uma determinada linha.`
#
# **********************************************************************

def GeraCandidatasAColisao(linha: Linha()) -> list[Linha()]:
    global matriz, linhas
    candidatas = []
    linha.miny = 0 if linha.miny < 0 else linha.miny
    linha.minx = 0 if linha.minx < 0 else linha.minx
    linha.maxy = 0 if linha.maxy < 0 else linha.maxy
    linha.maxx = 0 if linha.maxx < 0 else linha.maxx
    linha.miny = 100 if linha.miny > 100 else linha.miny
    linha.minx = 100 if linha.minx > 100 else linha.minx
    linha.maxy = 100 if linha.maxy > 100 else linha.maxy
    linha.maxx = 100 if linha.maxx > 100 else linha.maxx


    yMin = math.floor(linha.miny / interAltura)
    xMin = math.floor(linha.minx / interLargura)
    yMax = math.floor(linha.maxy / interAltura)
    xMax = math.floor(linha.maxx / interLargura)

    if yMin == yMax and xMin == xMax:
        for indiceLinha in matriz[yMin][xMin]:
            candidatas.append(linhas[indiceLinha])
    elif yMin != yMax and xMin == xMax:
        for y in range(yMin, yMax):
            for indiceLinha in matriz[y][xMin]:
                candidatas.append(linhas[indiceLinha])
    elif yMin == yMax and xMin != xMax:
        for x in range(xMin, xMax):
            for indiceLinha in matriz[yMin][x]:
                candidatas.append(linhas[indiceLinha])
    elif yMin != yMax and xMin != xMax:
        for y in range(yMin, yMax):
            for x in range(xMin, xMax):
                for indiceLinha in matriz[y][x]:
                    candidatas.append(linhas[indiceLinha])

    return candidatas



# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    DesenhaLinhas()
    DesenhaCenario()
    
    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualização da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()

    if TempoTotal > 5.0:
        print(f'Tempo Acumulado: {TempoTotal} segundos.')
        print(f'Nros de Frames sem desenho: {int(nFrames)}')
        print(f'FPS(sem desenho): {int(nFrames/TempoTotal)}')
        
        TempoTotal = 0
        nFrames = 0
        
        print(f'Contador de Intersecoes Existentes: {ContadorInt/2.0}')
        print(f'Contador de Chamadas: {ContChamadas}')

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        init()

    # Força o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
#
#
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        pass

    glutPostRedisplay()


def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de título da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Algorimos de Cálculo de Colisão")

# executa algumas inicializações
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# será chamada automaticamente quando
# for necessário redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# será chamada automaticamente quando
# o usuário alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# será chamada automaticamente sempre
# o usuário pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" será chamada
# automaticamente sempre o usuário
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)

try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
