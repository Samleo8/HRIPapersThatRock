#define ROCK_BUTTON 2
#define PAPER_BUTTON 3
#define SCISSORS_BUTTON 4

void setup() {
  pinMode(ROCK_BUTTON, INPUT_PULLUP);
  pinMode(PAPER_BUTTON, INPUT_PULLUP);
  pinMode(SCISSORS_BUTTON, INPUT_PULLUP);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (digitalRead(ROCK_BUTTON) == LOW) {
    Serial.println("ROCK");
    while (digitalRead(ROCK_BUTTON) == LOW) delay(10);
  } else if (digitalRead(PAPER_BUTTON) == LOW) {
    Serial.println("PAPER");
    while (digitalRead(PAPER_BUTTON) == LOW) delay(10);
  } else if (digitalRead(SCISSORS_BUTTON) == LOW) {
    Serial.println("SCISSORS");
    while (digitalRead(SCISSORS_BUTTON) == LOW) delay(10);
  }
  
  //Wait until buttons back to normal
  delay(10);
}
