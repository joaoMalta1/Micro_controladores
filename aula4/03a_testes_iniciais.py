# importação de bibliotecas
from gpiozero import Buzzer
from gpiozero import Button
from gpiozero import LED
from gpiozero import DistanceSensor
from Adafruit_CharLCD import Adafruit_CharLCD
from pymongo import MongoClient
from datetime import datetime



# definição de funções

def toca ():
    buzzer.beep(n = 1, on_time = 0.5)
    
def pisca():
    led1.blink(n=2)

def calcula_distancia():
    lcd.clear()
    lcd.message("%.1fcm" %(sensor.distance * 100))
    banco = cliente["infoaa"]
    colecao = banco["testes"]
    dados = {"time": datetime.now(), "distance": (sensor.distance * 100)}
    colecao.insert(dados) 

# criação de componentes
cliente = MongoClient("localhost", 27017)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2) 
botao1 = Button(11)
botao2 = Button(12)
buzzer = Buzzer(16)
led1 = LED(21)

sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1
sensor.when_in_range = pisca
sensor.when_out_of_range = pisca
botao1.when_pressed = toca
botao2.when_pressed = calcula_distancia


    