
#include <GFButton.h>
#include <EEPROM.h>
#include <Servo.h>

Servo servo;
Servo servo2;

GFButton botaoB(3);
GFButton botaoA(2);
GFButton botaoC(4);

int conta = 0;
int pinoDoServo = 12;
int pinoDoServo2 = 11;
int potenciometro = A5;
int valor_lido;
int valorFinal = 90;
int valorFinal2 = 90;

void soma_um() {
  conta++;
  EEPROM.put(0, conta);
  Serial.println(conta);
}

void aumenta_angulo() {
  if (valorFinal2 < 135) {
    valorFinal2 = valorFinal2 + 1;
  }
  delay(20);
}
void diminui_angulo() {
  if (valorFinal2 > 45) {
    valorFinal2 = valorFinal2 - 1;
  }
  delay(20);
}

void setup() {
  pinMode(potenciometro, INPUT);
  servo.attach(pinoDoServo);
  servo2.attach(pinoDoServo2);
  Serial.begin(9600);
  botaoB.setPressHandler(soma_um);
  EEPROM.get(0, conta);
}


void loop() {
  valor_lido = analogRead(potenciometro);
  valorFinal = map(valor_lido, 0, 1023, 0, 180);

  botaoA.process();
  botaoB.process();
  botaoC.process();

  if (botaoA.isPressed()) {
    diminui_angulo();
  }
  if (botaoC.isPressed()) {
    aumenta_angulo();
  }

  servo.write(valorFinal);
  servo2.write(valorFinal2);
  //Serial.println(valorFinal2);

  //Serial.println(conta);
  //delay(500);
}
