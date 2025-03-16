''' aprendendo led '''
from gpiozero import LED

led = LED(21)
led.on() #liga o led
led.is_lit() # true ou false se o led esta aceso
led.off() #desliga o led
led.toggle() #inverte o estado do led
led.blink(ont_time = 0.5, off_time = 0.2,n =4) #fica piscando o led, seguindo os parametros passados, o parametro n diz quantas vezes piscar

''' aprendendo botao '''
from gpiozero import Button

botao = (11) #diz a porta em que o botão está
botao.is_pressed() #verifica se botao está apertado (true ou false)
def acender_led():
    led.on()
def piscard_led():
    led.blink(n=2)
def apagar_led():
    led.off
    
botao.when_pressed = acender_led #usa um ponteiro para referenciar a funcao apertar o botao
botao.when_held = piscar_led 
botao.when_released = apagar_led

''' aprendendo display '''
from Adafruit_CharLCD import Adafruit_CharLCD

lcd = Adafruit_CharLCD(2,3,4,5,6,7,16,2)
lcd.message("teste") #exibe no display a string passada
lcd.message("teste2") #escreve ao lado da escrita anterior
lcd.clear() #limpa o display

''' aprendendo controle de midia '''
from mplayer import Player

player = Player()
player.loadfile("musica.mp3")
player.pause() #faz o toggle entre os estados 
player.paused() # true ou false se está tocando ou nao
player.stop() #para de fato  a musica
play.quit() #sai do player
playerlength # duração total do audio em segundos
player.time_pos # instante de tempo atual da musica
player.time_pos = 20 #vai para o instante 20 da musica
player.time_pos +=5 #avança 5 segundos da musica
player.metadata #retorna um dict com as informações
player.loadlist("lista_de_path.txt")
player.pt_step(1) #avança uma musica da lista 
player.pt_step(-1) #retorna para a musica anterior
player.volume = 5 #diz o volume da musica ou o altera  
player.speed = 2 #diz a speed da musica ou o altera  