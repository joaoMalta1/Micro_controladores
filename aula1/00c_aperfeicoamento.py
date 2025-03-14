from json import load
from turtle import *


# Copie as funções que você fez na Implementação aqui embaixo
from turtle import *

speed(20)

def desenha_retangulo(x, y, comprimento, altura, cor):
    penup()
    goto(x,y)
    pendown()
    fillcolor(cor)
    begin_fill() 
    for i in range(2):
        forward(comprimento)
        right(90)
        forward(altura)
        right(90)
    end_fill() 
    return
    
    
def desenha_circulo(x, y, raio, cor):
    penup()
    goto(x +(raio/2)-6,y-(raio))
    pendown()
    fillcolor(cor)
    begin_fill() 
    circle(raio)
    end_fill() 
    return
    
    
def desenha_poligono(lista_pontos, cor):
    setheading(0)
    penup()
    fillcolor(cor)
    begin_fill()
    for i in lista_pontos:
        goto(i["x"], i["y"])
        pendown()
    i = lista_pontos[0]
    goto(i["x"], i["y"])
    penup()
    end_fill() 
    return
    
# Faça a primeira parte do Aperfeiçoamento aqui

def desenha_bandeira(dicionario_do_pais):
    el = dicionario_do_pais["elementos"]
    for i in el:
        if i["tipo"] == "retângulo":
            desenha_retangulo(i["x"],i["y"],i["comprimento"],i["altura"],i["cor"])
            
        elif i["tipo"] ==  "polígono":
           desenha_poligono(i["pontos"],i["cor"])
           
        elif i["tipo"] == "círculo":
            desenha_circulo(i["x"],i["y"],i["raio"],i["cor"])
    return


lista_de_paises = load(open('paises.json', encoding="UTF-8"))
desenha_bandeira(lista_de_paises[0])


# Faça a segunda parte do Aperfeiçoamento aqui

def input_func(x,y):
    pais = textinput("input", "text")
    for i in lista_de_paises:
        if pais == i["nome"]:
            desenha_bandeira(i)
    
onscreenclick(input_func)

# O desafio deve ser feito diretamente no JSON, não aqui!


# Mantém a janela do Turtle aberta
mainloop()