#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);
RotaryEncoder encoder(20, 21);

int posicaoAnterior = 0;

int campainhaPassiva = 5;
int terra = A5;

GFButton botao(A2);
GFButton botao3(A3);
unsigned long instanteAnteriorDeDeteccao = 0;

int frequencia = 440;
int frequencia2 = 220;

int duracaoEmMs = 50;

int led = 13;
int led2 = 12;
int ligado = 0;
int n = 0;

void setup()
{
  Serial.begin(9600);
  int origem1 = digitalPinToInterrupt(20);
  attachInterrupt(origem1, tickDoEncoder, CHANGE);
  int origem2 = digitalPinToInterrupt(21);
  attachInterrupt(origem2, tickDoEncoder, CHANGE);

  botao.setPressHandler(botaoPressionado);

  botao3.setPressHandler(exibe3);
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(campainhaPassiva, OUTPUT);
  pinMode(terra, OUTPUT);

  digitalWrite(led, LOW);
  digitalWrite(led2, HIGH);
  digitalWrite(terra, LOW);
}

void tickDoEncoder()
{
  encoder.tick();
}

void loop()
{
  int posicao = encoder.getPosition();
  if (posicao > posicaoAnterior)
  {
    tone(campainhaPassiva, frequencia, duracaoEmMs);
    Serial.println(posicao);
  }
  else if (posicao < posicaoAnterior)
  {
    tone(campainhaPassiva, frequencia2, duracaoEmMs);
    Serial.println(posicao);
  }
  posicaoAnterior = posicao;

  // put your main code here, to run repeatedly:
  botao.process();
  botao3.process();

  display.set(n);
  display.update();

  if (instanteAnteriorDeDeteccao + 2000 < millis())
  {
    printa();
    instanteAnteriorDeDeteccao = millis();
  }
}

int exibe3()
{
  n++;
}

void printa()
{
  Serial.println(n);
}

void botaoPressionado()
{

  if (digitalRead(led2) == 1)
  {
    digitalWrite(led2, LOW);
  }
  else
  {
    digitalWrite(led2, HIGH);
  }
}
