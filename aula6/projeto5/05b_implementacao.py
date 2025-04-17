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
from flask import Flask

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

# definição de funções das páginas
def atualiza_led(indiceLed, novoEstado):
    led = leds[indiceLed]
    led.toggle()
    novoEstado = led.is_lit
    print(novoEstado)
    listaEstados = []
    for id in leds:
        listaEstados.append(id.is_lit)
    data = {"data": datetime.now(), "estadoLed": listaEstados}
    print(data)
    x = colecao.insert(data)
    print(x)

def botao1_pressionado():
    atualiza_led(0, True)

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
botoes[0].when_pressed = botao1_pressionado
# rode o servidor
app.run(port=5000)