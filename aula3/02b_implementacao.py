# importação de bibliotecas
from flask import Flask
from gpiozero import LED
from time import sleep
from gpiozero import Button
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD
from py_irsend.irsend import send_once
import threading

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/power")
@app.route("/power/<int:x>") 
def liga(x = None):
    if x is None:
        send_once("aquario", ["KEY_POWER"])
    threading.Timer(x, send_once("aquario", ["KEY_POWER"]))
    return "Ligou!"

@app.route("/aumentar_volume")
def aumenta():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return "Aumentou!"

@app.route("/abaixa_volume")
def abaixa():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return "Abaixou!"
    
@app.route("/mudo") 
def mudo():
    send_once("aquario", ["KEY_MUTE"])
    return "Mutou!"

@app.route("/canal/<string:x>")
def canal(x):
    lista = []
    for i in x:
        lista.append("KEY_"+i)
    send_once("aquario", lista)
    return "Canal"

# rode o servidor
if __name__ == "__main__": 
    app.run(port = 5000, debug=True) 