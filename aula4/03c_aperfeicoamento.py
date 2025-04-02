# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS
# importação de bibliotecas
from gpiozero import Buzzer
from gpiozero import Button
from gpiozero import LED
from gpiozero import DistanceSensor
from datetime import datetime
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, ASCENDING, DESCENDING 
from Adafruit_CharLCD import Adafruit_CharLCD
from lirc import init, nextcode
import time
# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]


# definição de funções

def validar_apartamento(num):
    busca = {"apartamento": num}
    if colecao.find_one(busca):
        return True
    return False 


def retornar_nome_do_morador(num,senha):
    busca = {"apartamento": num, "senha": senha}
    if colecao.find_one(busca):
        return colecao.find_one(busca)["nome"]
    return None

def coletar_digitos(string):
    lcd.clear()
    lcd.message(string)
    texto = ""
    while True:
        lista = nextcode()
        if lista != []:
            codigo = lista[0]
            if codigo[-1]>="0" and codigo[-1]<="9":
                lcd.message("*")
                buzzer.beep(n = 1, on_time = 0.2)
                texto = texto + codigo[-1]
            elif codigo[-1] == "K":
                return texto
        
def executa():
    apto = coletar_digitos("Digite o apto:\n")
    logico = validar_apartamento(apto)    
    if logico == True:
        lcd.clear()
        senha = coletar_digitos("Digite a senha:\n")
        nome = retornar_nome_do_morador(apto,senha)
        if nome == None: #
            lcd.clear()
            lcd.message("Acesso negado!\n")
            busca2 = {"apto":apto}
            data = {"date_time":datetime.now(),"apto":apto}
            colecao2.insert(data)
            
            buzzer.beep(n = 3, on_time = 0.5)
            time.sleep(1)
        else:
            lcd.clear()
            lcd.message("Bem-vindo(a)\n%s" %(nome))
            data = {"nome":nome, "date_time":datetime.now(),"apto":apto}
            colecao2.insert(data)
            time.sleep(1)
    else:
        lcd.clear()
        lcd.message("Apartamento\ninvalido!\n")
        time.sleep(1)

def busca_banco():
    apto = coletar_digitos("Digite o apto:\n")
    busca = {"apto":apto}
    ordenacao = [ ["date_time", DESCENDING] ]
    documentos = list(colecao2.find(busca, sort=ordenacao))
    #print(documentos)
    for i in documentos:
        if "nome" in  i:
            print(i["date_time"].strftime("%d/%m (%H:%M)") + ": "+ i["nome"]+"\n")
        else:
            print(i["date_time"].strftime("%d/%m (%H:%M)") + ": SENHA INCORRETA\n")

            
# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
buzzer = Buzzer(16)
botao2 = Button(12)
botao1 = Button(11)
botao1.when_pressed = busca_banco
botao2.when_pressed = executa

colecao2 = banco["invalido"]
init("aula", blocking=False)
print(retornar_nome_do_morador("101","101001"))
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1

#coletar_digitos("string")

#print(coletar_digitos("string"))

# loop infinito
#sensor.when_in_range = executa
       