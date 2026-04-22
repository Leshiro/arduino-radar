#include <Arduino.h>
#include <Servo.h>

Servo radarServo;

const int trigPin = 2;
const int echoPin = 3;

int pos = 90;
int direction = 1;

unsigned long lastMove = 0;
const int stepDelay = 20;

void setup() {
  Serial.begin(9600);
  radarServo.attach(9, 544, 2400);

  radarServo.write(pos);
  delay(1000);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

long getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);

  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000);
  return duration * 0.034 / 2;
}

void loop() {
  unsigned long now = millis();

  if (now - lastMove >= stepDelay) {
    lastMove = now;
    long distance = getDistance();

    Serial.print(pos);
    Serial.print(",");
    Serial.println(distance);

    radarServo.write(pos);
    pos += direction;

    if (pos >= 180 || pos <= 0) {
      direction = -direction;
    }
  }
}