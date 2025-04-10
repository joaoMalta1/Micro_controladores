# importação de bibliotecas
from Adafruit_CharLCD import Adafruit_CharLCD
from gpiozero import Button
from os import system
from subprocess import Popen
import time
import requests
from gpiozero import LED

# parâmetros iniciais do Telegram
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

chave = "7695750620:AAEZgi2RXfmW1B__B-_VhBD8FM35Favtp78"
id_da_conversa = "6244360043"
endereco_base = "https://api.telegram.org/bot" + chave

def exibe_texto():
    lcd.clear()
    lcd.message("Gravando...")
    system("arecord --duration 5 --format cd audio.wav")
    lcd.clear()

def foto():
    for i in range(5):
        system("fswebcam --resolution 640x480 --skip 10 foto"+str(i)+".jpg")
        led1.blink(n = 1 ,on_time = 0.1)
        time.sleep(2)
    print("foi")

def mensagem():
    data = {"chat_id": id_da_conversa , "text": "la vai"}
    x = requests.post(endereco_base +"/sendMessage", json = data)
    try:
        x
        print(x.text)
    except Exception as e:
        print(e)
        

led1 = LED(21)
botao1 = Button(11)
botao1.when_pressed = exibe_texto
botao2 = Button(12)
botao2.when_pressed = foto
botao3 = Button(13)
botao3.when_pressed = mensagem

# definição de funções


# criação de componentes

