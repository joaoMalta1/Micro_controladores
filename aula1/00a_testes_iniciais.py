from turtle import *

speed(15)
# Desenhe o que foi solicitado no enunciado do PDF aqui embaixo
def retangulo(x, y, comprimento, altura):
    penup()
    goto(x,y)
    pendown()
    for i in range(2):
        forward(comprimento)
        right(90)
        forward(altura)
        right(90)
    return

def triangulo(x, y, size):
    penup()
    goto(x,y)
    pendown()
    setheading(60)
    forward(size)
    setheading(-60)
    setheading(-60)
    forward(size)
    setheading(+60)
    setheading(-180)
    forward(size)
    return

def circulo(x, y, raio):
    penup()
    goto(x,y)
    pendown()
    circle(raio)
    return

def espiral(x, y, qtd,raio):
    penup()
    goto(x-raio,y)
    penup()
    #right(-10)
    forward(raio)
    pendown()
    for i in range(qtd): 
        circle(raio + i * 10, 120) 
    return

def coord(x,y):
    penup()
    goto(x,y)
    string = "coordenadas x:%d y:%d " %(x, y)
    return write(string)

retangulo(0,300,100,50)
triangulo(300,-150,100)
circulo(0,-200,50)
espiral(-400,-120, 8, 50)

onscreenclick(coord)



# Mantém a janela do Turtle aberta
mainloop()