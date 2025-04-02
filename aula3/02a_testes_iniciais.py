# importação de bibliotecas
from gpiozero import LED
from time import sleep
from gpiozero import Button
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD

# definição de funções


# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]

def liga():
    for i in leds:
        i.on()
def desliga():
    for i in leds:
        i.off()

botao1 = Button(11)
botao2 = Button(12)



botao1.when_pressed = liga
botao2.when_pressed = desliga

init("aula", blocking=False)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

lista_apertado = ["KEY_1"]

# loop infinito
while True:
    lista = nextcode()
    
    if lista != []:
        codigo = lista[0]
        num_led = codigo[-1]
        if num_led >= "1" and num_led <= "5":
            lcd.clear()
            lcd.message(str("LED " + num_led +"\nselecionado"))
            lista_apertado.append(codigo)
            print("Primeiro")
        if codigo == "KEY_UP":
            if lista_apertado[-1][-1] < "5":
                lcd.clear()
                print("Segundo")
                lista_apertado.append("KEY_" + str(int(lista_apertado[-1][-1])+1))
                lcd.message(str("LED " + lista_apertado[-1][-1] +"\nselecionado"))
        if codigo == "KEY_DOWN":
            if lista_apertado[-1][-1] > "1" and lista_apertado[-1][-1] < "6":
                lcd.clear()
                print("Terceiro")
                lista_apertado.append("KEY_" + str(int(lista_apertado[-1][-1])-1))
                lcd.message(str("LED " + lista_apertado[-1][-1] +"\nselecionado"))
        if codigo == "KEY_OK" and len(lista_apertado) > 0:
            leds[int(lista_apertado[-1][-1])-1].toggle()

        
            
        print(codigo)
    sleep(0.2)
