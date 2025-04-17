# importação de bibliotecas
from threading import Timer
from gpiozero import LED
from gpiozero import MotionSensor
from gpiozero import Button
import requests
from gpiozero import LightSensor
from gpiozero import DistanceSensor
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask, render_template



# criação do servidor
url = "https://cloud.activepieces.com/api/v1/webhooks/Q3RMCKNcpLb4ddO4gZmjM"
cliente = MongoClient("localhost", 27017)
banco = cliente["nome_cliente"]
colecao = banco["teste_micro"]


app = Flask(__name__)
@app.route("/led/<int:id>/<string:estado>")
def servidor(id, estado):
    print(id)
    print(type(id))
    print(estado)
    print(leds[id])
    if estado == 'on':
        atualiza_led(id, True)
    elif estado == 'off':
        atualiza_led(id, False)
    return "ok"

@app.route("/exibe")
def html():
    dicionario = {"led1": "", "led2": "", "led3": "", "led4": "", "led5": ""}
    documentos = colecao.find_one(busca,sort=ordenacao)
    for i,el in enumerate(documentos["estadoLed"]):
        if el == True:
            dicionario["led"+str(i+1)] = "Aceso"
        else:
            dicionario["led"+str(i+1)] = "Apagado"
    print("aqui")
    return render_template("pagina.html",dicionario=dicionario)


# definição de funções das páginas
def atualiza_led(indiceLed, novoEstado):
    led = leds[indiceLed]
    led.toggle()
    global timer
    if timer != None:
        timer.cancel()
        timer = None
    novoEstado = led.is_lit
    listaEstados = []
    for id in leds:
        listaEstados.append(id.is_lit)
    data = {"data": datetime.now(), "estadoLed": listaEstados}
    x = colecao.insert(data)

def apagaleds():
    global timer 
    timer = Timer(10, leds[0].off)
    timer.start()

def sensorM():
    atualiza_led(0, True)

def sensorL():
    atualiza_led(1, True)

def sensorL2():
    atualiza_led(1, False)

def botao1_pressionado():
    atualiza_led(0, True)



# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]

busca = {} 
ordenacao = [["data", DESCENDING]]
sensor = MotionSensor(27)
sensorLuz = LightSensor(8)
sensor.threshold = 0.6
timer = None
documentos = colecao.find_one(busca,sort=ordenacao) 

sensor.when_motion = sensorM
sensor.when_no_motion = apagaleds
sensorLuz.when_dark = sensorL
sensorLuz.when_light = sensorL2
botoes[0].when_pressed = botao1_pressionado

for i, el in enumerate(documentos["estadoLed"]):
    if el == True:
        leds[i].on()
    else:
        leds[i].off()

# rode o servidor
app.run(port=5000, debug=True)
