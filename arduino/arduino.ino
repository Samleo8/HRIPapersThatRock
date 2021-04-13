#define ROCK_BUTTON 2
#define PAPER_BUTTON 3
#define SCISSORS_BUTTON 4
#define WIN_BUTTON 5
#define LOSE_BUTTON 6
#define TIE_BUTTON 7
#define START_ROUND 8

void setup() {
  pinMode(ROCK_BUTTON, INPUT_PULLUP);
  pinMode(PAPER_BUTTON, INPUT_PULLUP);
  pinMode(SCISSORS_BUTTON, INPUT_PULLUP);
  pinMode(WIN_BUTTON, INPUT_PULLUP);
  pinMode(LOSE_BUTTON, INPUT_PULLUP);
  pinMode(TIE_BUTTON, INPUT_PULLUP);
  pinMode(START_ROUND, INPUT_PULLUP);

  Serial.begin(9600);
}

void waitUntilLow(int pin) {
  while (digitalRead(pin) == LOW) delay(50);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(ROCK_BUTTON) == LOW) {
    Serial.println("ROCK");
    waitUntilLow(ROCK_BUTTON);
  } else if (digitalRead(PAPER_BUTTON) == LOW) {
    Serial.println("PAPER");
    waitUntilLow(PAPER_BUTTON);
  } else if (digitalRead(SCISSORS_BUTTON) == LOW) {
    Serial.println("SCISSORS");
    waitUntilLow(SCISSORS_BUTTON);
  } else if (digitalRead(START_ROUND) == LOW) {
    Serial.println("START");
    waitUntilLow(START_ROUND);
  } else if (digitalRead(WIN_BUTTON) == LOW) {
    Serial.println("WIN");
    waitUntilLow(WIN_BUTTON);
  } else if (digitalRead(LOSE_BUTTON) == LOW) {
    Serial.println("LOSE");
    waitUntilLow(LOSE_BUTTON);
  } else if (digitalRead(TIE_BUTTON) == LOW) {
    Serial.println("TIE");
    waitUntilLow(TIE_BUTTON);
  }
  
  //Wait until buttons back to normal
  delay(10);
}
