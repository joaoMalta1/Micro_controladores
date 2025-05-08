#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
RotaryEncoder encoder(20, 21);

int campainhaPassiva = 5;
int terra = A5;
unsigned long currentTime[] = {0, 0, 0, 0};

int num = 0;

int led1 = 13;
int led2 = 12;
int led3 = 11;
int led4 = 10;

int indiceAtual = 0;

int listaGlobal[] = {0, 0, 0, 30};
int listaAndamento[] = {0, 0, 0, 0};
int listaPosicao = 0;

GFButton botao(A1);
GFButton botao2(A2);

unsigned long instanteAnteriorDeDeteccao = 0;

int frequencia = 440;
int duracaoEmMs = 1000;

void mudaEstado()
{
  if (listaAndamento[indiceAtual] == 0)
  {
    listaAndamento[indiceAtual] = 1;
  }
}

void setup()
{
  Serial.begin(9600);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);

  int origem1 = digitalPinToInterrupt(20);
  attachInterrupt(origem1, tickDoEncoder, CHANGE);
  int origem2 = digitalPinToInterrupt(21);
  attachInterrupt(origem2, tickDoEncoder, CHANGE);
  botao.setPressHandler(mudaEstado);
  botao2.setPressHandler(somaIndice);

  digitalWrite(led1, LOW);
  digitalWrite(led2, HIGH);
  digitalWrite(led3, HIGH);
  digitalWrite(led4, HIGH);

  pinMode(campainhaPassiva, OUTPUT);
  pinMode(terra, OUTPUT);
}

void tickDoEncoder()
{
  encoder.tick();
}

void toca(int i)
{
  tone(campainhaPassiva, frequencia, duracaoEmMs);
  listaAndamento[i] = 0;
}

void loop()
{
  botao.process();
  botao2.process();

  int posicao = encoder.getPosition();

  if (posicao > listaPosicao)
  {
    (listaGlobal[indiceAtual]) += 15;
    Serial.println(listaGlobal[indiceAtual]);
  }

  else if (posicao < listaPosicao)
  {
    if ((listaGlobal[indiceAtual] - 15) < 0)
    {
      (listaGlobal[indiceAtual]) = 0;
    }
    else
    {
      (listaGlobal[indiceAtual]) -= 15;
    }
    Serial.println(listaGlobal[indiceAtual]);
  }

  listaPosicao = posicao;
  for (int i = 0; i < 4; i++)
  {
    if ((millis() > currentTime[i] + 1000) && listaAndamento[i] == 1)
    {
      if (listaGlobal[i] - 1 < 0)
      {
        listaGlobal[i] = 0;
      }
      else
      {
        listaGlobal[i]--;
      }
      currentTime[i] = millis();
    }

    if (listaGlobal[i] == 0 && listaAndamento[i] == 1)
    {
      toca(i);
    }
  }

  num = int((listaGlobal[indiceAtual] / 60) * 100) + listaGlobal[indiceAtual] % 60;
  display.set(num, 0, true);
  display.changeDot(1, true);
  display.update();

  if (indiceAtual == 0)
  {
    digitalWrite(led1, LOW);
    digitalWrite(led4, HIGH);
  }
  else if (indiceAtual == 1)
  {
    digitalWrite(led2, LOW);
    digitalWrite(led1, HIGH);
  }
  else if (indiceAtual == 2)
  {
    digitalWrite(led3, LOW);
    digitalWrite(led2, HIGH);
  }
  else if (indiceAtual == 3)
  {
    digitalWrite(led4, LOW);
    digitalWrite(led3, HIGH);
  }
}

void somaIndice()
{
  Serial.println(indiceAtual);
  if (indiceAtual + 1 > 3)
  {
    indiceAtual = 0;
  }
  else
  {
    indiceAtual++;
  }
}
