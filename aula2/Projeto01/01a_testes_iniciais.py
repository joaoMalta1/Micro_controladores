# importação de bibliotecas
from gpiozero import LED
from time import sleep
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD

# definição de funções
def blink4():
    global conta
    conta += 1
    led3.blink(n=4)
    lcd.clear()
    lcd.message(str(conta))

# criação de componentes
led = LED(21)
led2 = LED(22)
led3 = LED(23)
led5 = LED(25)
botao3 = Button(13)
botao2 = Button(12)
botao1 = Button(11)
conta = 0
lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)

led.blink(on_time = 1,off_time = 3)
botao2.when_pressed = led2.toggle
botao3.when_pressed = blink4




# loop infinito
while True:
    if led.is_lit and botao1.is_pressed:
        led5.on()
    else:
        led5.off()
    
    sleep(0.2)