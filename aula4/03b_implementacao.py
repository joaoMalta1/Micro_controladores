# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
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
                texto = texto + codigo[-1]
            elif codigo[-1] == "K":
                return texto

# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
init("aula", blocking=False)
print(retornar_nome_do_morador("101","101001"))

# loop infinito
while True:
    apto = coletar_digitos("Digite o apto:\n")
    logico = validar_apartamento(apto)
    if logico == True:
        lcd.clear()
        senha = coletar_digitos("Digite a senha:\n")
        nome = retornar_nome_do_morador(apto,senha)
        if nome == None:
            lcd.clear()
            lcd.message("Acesso negado!\n")
            time.sleep(1)
        else:
            lcd.clear()
            lcd.message("Bem-vindo(a)\n%s" %(nome))
            time.sleep(1)
    else:
        lcd.clear()
        lcd.message("Apartamento\ninvalido!\n")
        time.sleep(1)
