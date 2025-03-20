# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO
# DEPOIS FAÇA OS NOVOS RECURSOS
# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from os import system
from time import sleep
from mplayer import Player
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import LED
import random

# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")

def desafio_random():
    f = open("playlist.txt",'r')
    new = open("newlist.txt",'w')
    texto = f.read()
    lista = texto.split('\n')
    lista.remove('')
    while lista:
        element = random.choice(lista)
        print(element)
        new.write(element+'\n')
        lista.remove(element)
    return 'newlist.txt' 

# definição de funções
def Tocar_pausar():
    global player
    player.pause()
    if player.paused:
        led1.blink()
    else:
        led1.on()
        
def next():
    player.pt_step(1)

    
def back():
    if player.time_pos > 2:
        player.time_pos = 0
    else:
        player.pt_step(-1)
        
def solta():
    if player.speed == 2:
        player.speed = 1
    else:
        next()
        
def acelera():
    player.speed = 2
# criação de componentes

led1 = LED(21)

botao3 = Button(13)
botao2 = Button(12)
botao1 = Button(11)


player = Player()
player.loadlist(desafio_random())
botao2.when_pressed = Tocar_pausar

botao1.when_pressed = back
botao3.when_held = acelera
botao3.when_released  = solta




# 
lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)
inicio = 0
fim = 16
# loop infinito
while True:
    lcd.clear()
    if player.metadata != None:
        size = len(player.metadata['Title'])
        lcd.message((player.metadata['Title'])[inicio:fim])
        inicio +=1
        fim +=1
        if fim >= size:
            inicio = 0
            fim = 16
            
        if player.time_pos:
            time_total = player.length
            time_current = player.time_pos
            min_tot = time_total //60
            sec_tot = time_total % 60
            time_current = player.time_pos
            min_current =int(time_current //60)
            sec_current = time_current %60
            mensagem = '\n{:02d}:{:02d} de {:02d}:{:02d}'
            lcd.message(mensagem.format(int(min_current),int(sec_current),int(min_tot), int(sec_tot)))
    sleep(0.2)



