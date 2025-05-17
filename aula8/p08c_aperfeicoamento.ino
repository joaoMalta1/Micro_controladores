#include <GFButton.h>
#include <EEPROM.h>
#include <Servo.h>
#include <meArm.h>

GFButton botaoA(2);
GFButton botaoB(3);
GFButton botaoC(4);
GFButton botaoD(5);


bool taAberto = false;
bool taRelativo = false;
int x, y, z;
int eixoX = A0;
int eixoY = A1;
int valor_lidoX;
int valorFinalX;
int valor_lidoY;
int valorFinalY;
int potenciometro = A5;
int valor_lidoZ;
int valorFinalZ;
int incrementaX = 0;
int incrementaY = 0;
int endereco = 0;
int index = 0;
int matriz[4][4];


int base = 12, ombro = 11, cotovelo = 10, garra = 9;
meArm braco(
  180, 0, -pi / 2, pi / 2,      // ângulos da base
  135, 45, pi / 4, 3 * pi / 4,  // ângulos do ombro
  180, 90, 0, -pi / 2,          // ângulos do cotovelo
  30, 0, pi / 2, 0              // ângulos da garra
);

void salva() {
  Serial.println(index);
  matriz[index][0] = x;
  matriz[index][1] = y;
  matriz[index][2] = z;
  matriz[index][3] = taAberto;

  /*Serial.println(matriz[index][0]);
  Serial.println(matriz[index][1]);
  Serial.println(matriz[index][2]);
  Serial.println(matriz[index][3]);
*/

  EEPROM.put(endereco, matriz);
  if (index <= 3) {
    index++;
  } else {
    index = 0;
  }
}

void abre_fecha() {
  if (taAberto) {
    braco.closeGripper();
    taAberto = false;
  } else {
    braco.openGripper();
    taAberto = true;
  }
}

void mudaEstado() {
  if (taRelativo) {
    taRelativo = false;
    Serial.println("modo absoluto");
  } else {
    taRelativo = true;
    Serial.println("modo relativo");
  }
}

void aumenta_anguloX() {
  if (valorFinalX < 135) {
    valorFinalX = valorFinalX + 10;
  }
  delay(20);
}
void diminui_anguloX() {
  if (valorFinalX > 45) {
    valorFinalX = valorFinalX - 10;
  }
  delay(20);
}

void ler() {
  int aux [4][4];
  EEPROM.get(endereco, aux);
  for (int i = 0; i <=3; i++) 
  {
    taAberto = !aux[i][3];
    braco.goDirectlyTo(aux[i][0], aux[i][1], aux[i][2]);
    abre_fecha();
    delay(500);
  }
}

void setup() {
  Serial.begin(9600);
  braco.begin(base, ombro, cotovelo, garra);
  braco.gotoPoint(0, 130, 0);
  delay(30);
  braco.closeGripper();
  taAberto = false;
  botaoA.setPressHandler(abre_fecha);
  botaoB.setPressHandler(mudaEstado);
  botaoC.setPressHandler(salva);
  botaoD.setPressHandler(ler);
  pinMode(eixoX, INPUT);
  pinMode(eixoY, INPUT);
  pinMode(potenciometro, INPUT);
}

void loop() {
  botaoA.process();
  botaoB.process();
  botaoC.process();
  botaoD.process();

  valor_lidoX = analogRead(eixoX);
  valor_lidoY = analogRead(eixoY);
  valor_lidoZ = analogRead(potenciometro);
  valorFinalZ = map(valor_lidoZ, 0, 1023, -30, 100);

  if (taRelativo) {
    valorFinalX = map(valor_lidoX, 0, 1023, -10, 10);
    valorFinalY = map(valor_lidoY, 0, 1023, -10, 10);
    x = x + valorFinalX + 1;
    y = y + valorFinalY + 1;
    z = valorFinalZ;

    if (x < -150) {
      x = -150;
    }
    if (x > 150) {
      x = 150;
    }
    if (y < 100) {
      y = 100;
    }
    if (y > 200) {
      y = 200;
    }
    //Serial.println(x);
    //Serial.println(y);

    braco.goDirectlyTo(x, y, z);
    delay(40);


  } else {
    valorFinalX = map(valor_lidoX, 0, 1023, -150, 150);
    valorFinalY = map(valor_lidoY, 0, 1023, 100, 200);
    x = valorFinalX;
    y = valorFinalY;
    z = valorFinalZ;

  }
}
