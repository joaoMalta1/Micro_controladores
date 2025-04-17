# importação de bibliotecas
from os import system
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Button, Buzzer
from os import system
from subprocess import Popen
import time
import requests
from gpiozero import LED


# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")


# parâmetros iniciais do Telegram
chave = "7695750620:AAEZgi2RXfmW1B__B-_VhBD8FM35Favtp78"
id_da_conversa = "6244360043"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções
def ligar():
    buzzer.on()
    
def foto():
    system("fswebcam --resolution 640x480 --skip 10 foto.jpg")
    print("foi")
    
def mensagem():
    buzzer.off()
    foto()
    data = {"chat_id": id_da_conversa , "text": "Tem alguem na porta"}
    arquivo = {"photo": open("foto.jpg", "rb")}
    x = requests.post(endereco_base +"/sendMessage", json = data)
    y = requests.post(endereco_base +"/sendPhoto", data = data, files = arquivo)
    try:
        x
        print(x.text)
    except Exception as e:
        print(e)


# criação de componentes
led1 = LED(21)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)

botao1.when_pressed = ligar
botao1.when_released = mensagem
botao2.when_pressed = led1.off

proximo_id_de_update = 0

# loop infinito
while True:
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update}
    resposta = requests.get(endereco, json=dados)
    dicionario_da_resposta = resposta.json()
    for resultado in dicionario_da_resposta["result"]:
        mensagem = resultado["message"]
        if "text" in mensagem:
            texto = mensagem["text"]
            if texto == "Abrir":
                led1.on()
            elif texto == "Soar Alarme":
                buzzer.beep(n=5, on_time = 0.2)
        proximo_id_de_update = resultado["update_id"] + 1
    time.sleep(1)
