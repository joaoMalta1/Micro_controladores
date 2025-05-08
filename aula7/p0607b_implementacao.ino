#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
RotaryEncoder encoder(20, 21);

int posicaoAnterior = 0;
int campainhaPassiva = 5;
int terra = A5;
int globalTime = 0;
int currentTime = 0;
int emAndamento = 0; // False
int num = 0;

GFButton botao(A1);

unsigned long instanteAnteriorDeDeteccao = 0;

int frequencia = 440;
int duracaoEmMs = 1000;

void mudaEstado()
{
  if (emAndamento == 0)
  {
    emAndamento = 1;
  }
}

void setup()
{
  Serial.begin(9600);
  int origem1 = digitalPinToInterrupt(20);
  attachInterrupt(origem1, tickDoEncoder, CHANGE);
  int origem2 = digitalPinToInterrupt(21);
  attachInterrupt(origem2, tickDoEncoder, CHANGE);
  botao.setPressHandler(mudaEstado);
  pinMode(campainhaPassiva, OUTPUT);
  pinMode(terra, OUTPUT);
}

void tickDoEncoder()
{
  encoder.tick();
}

void toca()
{
  tone(campainhaPassiva, frequencia, duracaoEmMs);
  emAndamento = 0;
}

void loop()
{
  botao.process();
  int posicao = encoder.getPosition();
  if (globalTime == 0 && emAndamento == 1)
  {
    toca();
  }

  if (posicao > posicaoAnterior)
  {
    globalTime += 15;
    Serial.println(globalTime);
  }

  else if (posicao < posicaoAnterior)
  {
    if (globalTime - 15 < 0)
    {
      globalTime = 0;
    }
    else
    {
      globalTime -= 15;
    }
    Serial.println(globalTime);
  }

  posicaoAnterior = posicao;
  if ((millis() > currentTime + 1000) && emAndamento == 1)
  {
    if (globalTime - 1 < 0)
    {
      globalTime = 0;
    }
    else
    {
      globalTime--;
      currentTime = millis();
    }
  }
  num = int((globalTime / 60) * 100) + globalTime % 60;
  display.set(num, 0, true);
  display.changeDot(1, true);
  display.update();
}
