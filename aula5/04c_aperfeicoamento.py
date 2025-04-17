# importação de bibliotecas
from os import system
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Button, Buzzer, DistanceSensor
from os import system
from subprocess import Popen
import time
import requests
from gpiozero import LED
from urllib.request import urlretrieve
from mplayer import Player
from datetime import datetime, timedelta


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

def manda_audio():
    parar_gravacao()
    data = {"chat_id": id_da_conversa}
    arquivo = {"voice": open("audio.ogg", "rb")}
    x = requests.post(endereco_base +"/sendVoice", data = data, files = arquivo)
    try:
        x
        print(x.text)
    except Exception as e:
        print(e)
    
    
def iniciar_gravacao():
    global aplicativo
    comando = ["arecord", "--duration", "30", "audio.wav"]
    aplicativo = Popen(comando) # executa em plano de fundo

def parar_gravacao():
    global aplicativo
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
    system("opusenc audio.wav audio.ogg")

def start_time():
    global time
    print("inicio contagem do tempo")
    time = datetime.now()
    print(time)

def alerta():
    print("saiu")
    global time
    if datetime.now()- time >= timedelta(seconds = 10):        
        data = {"chat_id": id_da_conversa , "text": "A pessoa saiu"}
        x = requests.post(endereco_base +"/sendMessage", json = data)
        try:
            x
            print(x.text)
        except Exception as e:
            print(e)

# criação de componentes
global aplicativo
aplicativo = None
time = 0

led1 = LED(21)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)
player = Player()

botao1.when_pressed = ligar
botao1.when_released = mensagem
botao2.when_pressed = led1.off
botao3.when_pressed = iniciar_gravacao
botao3.when_released = manda_audio
proximo_id_de_update = 0
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1
sensor.when_in_range = start_time
sensor.when_out_of_range = alerta

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
        elif "voice" in mensagem:
            id_do_arquivo = mensagem["voice"]["file_id"]
            endereco = endereco_base + "/getFile"
            dados = {"file_id": id_do_arquivo}
            resposta = requests.get(endereco, json=dados)
            dicionario = resposta.json()
            print(dicionario)
            final_do_link = dicionario["result"]["file_path"]
            link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link
            arquivo_de_destino = "meu_arquivo.ogg"
            urlretrieve(link_do_arquivo, arquivo_de_destino)
            player.loadfile(arquivo_de_destino)
            
        
        # depois baixa o arquivo e faz algo com ele
        proximo_id_de_update = resultado["update_id"] + 1