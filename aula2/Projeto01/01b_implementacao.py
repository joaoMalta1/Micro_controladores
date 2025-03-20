# importação de bibliotecas
from os import system
from time import sleep
from mplayer import Player
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import LED

# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")

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
        
# criação de componentes

led1 = LED(21)
'''led2 = LED(22)
led3 = LED(23)
led5 = LED(25)'''

botao3 = Button(13)
botao2 = Button(12)
botao1 = Button(11)


player = Player()
player.loadlist("playlist.txt")
botao2.when_pressed = Tocar_pausar

botao1.when_pressed = back
botao3.when_pressed  = next

lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)

# loop infinito
while True:
    lcd.clear()
    lcd.message(player.metadata['Title']) 
    sleep(0.2)
