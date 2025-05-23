
// ESTE É O ARQUIVO DO ARDUINO COM OS MOTORES E OS SENSORES ÓTICOS.
// NÃO TEM BOTÃO, NEM LED E NEM DISPLAY AQUI.
#include <AFMotor.h>
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
int vel = 160;
int sensor1 = A11;
int sensor2 = A12;
unsigned long tempo = 0;


void setup() {
  Serial.begin(9600);
  motor3.setSpeed(vel);
  motor4.setSpeed(vel);
  Serial.println("Digite direcao:");
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  Serial1.begin(9600);
  Serial1.setTimeout(10);
}

void loop() {
  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();  // remove quebra de linha
    if (texto.startsWith("frente")) {
      frente();
    } else if (texto.startsWith("tras")) {
      tras();
    } else if (texto.startsWith("esquerda")) {
      esq();
    } else if (texto.startsWith("direita")) {
      dir();
    } else if (texto.startsWith("parar")) {
      parar();
    } else {
      Serial.println("incorreta!");
    }
  }
  if (millis() > tempo + 100) {
    tempo = millis();
    int val1 = digitalRead(sensor1);
    int val2 = digitalRead(sensor2);
    String texto1 = String(val1) + "," + String(val2);
    Serial1.println(texto1);
  }
}

void frente() {
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void tras() {
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void esq() {
  motor4.run(FORWARD);
  motor3.run(BACKWARD);
}

void dir() {
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}
void parar() {
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}
