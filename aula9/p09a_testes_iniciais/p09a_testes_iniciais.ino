#include <AFMotor.h>

AF_DCMotor motor3(3);
int cont2 = 0;
int sensor1 = A11;
int sensor2 = A12;
unsigned long tempo = 0;
int valAux = analogRead(sensor2);

void setup() {
  Serial.begin(9600);
  motor3.setSpeed(0);  // valor entre 0 e 255
  Serial.println("Digite direcao e velocidade:");
  Serial.setTimeout(10);
  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim();  // remove quebra de linha
    if (texto.startsWith("frente")) {

      String vel1 = texto.substring(7);  //frente
      motor3.setSpeed(vel1.toInt());
      motor3.run(FORWARD);
    } else if (texto.startsWith("tras")) {

      String vel2 = texto.substring(5);  //tras
      motor3.setSpeed(vel2.toInt());
      motor3.run(BACKWARD);
    } else {
      Serial.println("incorreta!");
    }
  }
  if (millis() > tempo + 500) {
    tempo = millis();
    int val1 = analogRead(sensor1);
    int val2 = analogRead(sensor2);
    String texto1 = String(val1) + "," + String(val2);
    Serial.println(texto1);
    if (valAux < 800 && val2 > 800){
      cont2++;
      Serial.println("Contagem " + String(cont2));
    }
    valAux = val2;
  }
}
