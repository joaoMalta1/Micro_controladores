# importação de bibliotecas
from threading import Timer
from gpiozero import LED
from gpiozero import MotionSensor
from gpiozero import Button
import requests
from gpiozero import LightSensor
from gpiozero import DistanceSensor

# definição de funções

def ola():
    print("ola")
    timer = Timer(2.0, ola)
    timer.start()

def acende_leds():
    led1.on()
    led2.on()
    global timer
    if timer != None:
        timer.cancel()
        timer = None

def apagaleds():
    global timer 
    led1.off()
    timer = Timer(8, apagar_led2)
    timer.start()

def apagar_led2():
    print("led2")
    led2.off()
    
def manda_email():
    data = {"luz": int(sensorluz.value*100), "distancia": int(sensorDistancia.distance*100)}
    print(data)
    x = requests.post(url, params = data)
    print(x)

# criação de componentes
url = "https://cloud.activepieces.com/api/v1/webhooks/hdp3xhq227yOEBQqnyiAv"
sensor = MotionSensor(27)
led1 = LED(21)
led2 = LED(22)
botao1 = Button(11)
sensorluz = LightSensor(8)
sensorDistancia = DistanceSensor(trigger=17, echo=18)

botao1.when_pressed = manda_email
sensor.when_motion = acende_leds
sensor.when_no_motion = apagaleds
timer = Timer(2, ola)
timer.start() 
