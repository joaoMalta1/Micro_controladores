# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS# importação de bibliotecas
from flask import Flask, render_template, redirect 
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
@app.route("/power_insta")
def liga_insta():
    send_once("aquario", ["KEY_POWER"])
    return redirect("/")

@app.route("/power/<int:x>") 
def liga(x):
    timer = threading.Timer(x, liga_insta)
    timer.start()
    return redirect("/")

@app.route("/aumentar_volume")
def aumenta():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return redirect("/")

@app.route("/abaixa_volume")
def abaixa():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return redirect("/")
    
@app.route("/mudo") 
def mudo():
    send_once("aquario", ["KEY_MUTE"])
    return redirect("/")

@app.route("/canal/<string:x>")
def canal(x):
    lista = []
    for i in x:
        lista.append("KEY_"+i)
    send_once("aquario", lista)
    return redirect("/")

@app.route("/")
def lista():
    return render_template("pagina.html")
# rode o servidor
if __name__ == "__main__": 
    app.run(port = 5000, debug=True) 
