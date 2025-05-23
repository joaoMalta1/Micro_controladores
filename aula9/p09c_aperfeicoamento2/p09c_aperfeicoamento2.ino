
// NÃO COPIE O IMPLEMENTAÇÃO 1 PARA CÁ NÃO!
// ESSE É UM CÓDIGO SEPARADO DA PRIMEIRA PARTE!

// ESTE É O ARQUIVO DO ARDUINO SÓ COM O SHIELD MULTIFUNÇÃO.
// NÃO TEM MOTOR E SENSOR ÓTICO.

#include <GFButton.h>
#include <ShiftDisplay.h>

GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);
int cont = 0;
String comandos[] = { "frente", "tras", "esquerda", "direita" };
ShiftDisplay display(4, 7, 8, COMMON_CATHODE, 4, true);
int led1 = 13;
int led2 = 12;
bool automatico = false;
unsigned long tempo = 0;


void setup() {
  Serial.begin(9600);
  botao1.setPressHandler(aperta);
  botao3.setPressHandler(aperta3);
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  Serial1.begin(115200);
  Serial1.setTimeout(10);
}

void loop() {
  botao1.process();
  botao2.process();
  botao3.process();


  if (automatico) {
    display.set("automatico");
    display.update();
    if (millis() > tempo + 50) {
      tempo = millis();
      Serial1.println("auto");
    }
  } else {
    display.set(comandos[cont]);
    display.update();
    if (botao2.isPressed()) {
      if (millis() > tempo + 50) {
        tempo = millis();
        Serial1.println(comandos[cont]);
      }
    } else {
      if (millis() > tempo + 50) {
        tempo = millis();
        Serial1.println("parar");
      }
    }
  }

  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();  // remove quebra de linha
    if (texto.startsWith("1")) {
      digitalWrite(led1, HIGH);
    } else if (texto.startsWith("0")) {
      digitalWrite(led1, LOW);
    }
    if (texto.substring(2) == "1") {
      digitalWrite(led2, HIGH);
    } else if (texto.substring(2) == "0") {
      digitalWrite(led2, LOW);
    }
  }
}



void aperta() {
  cont++;
  if (cont > 3) {
    cont = 0;
  }
}
void aperta3() {

  if (automatico) {
    automatico = false;
  } else {
    automatico = true;
  }
}
