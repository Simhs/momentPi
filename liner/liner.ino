// Run a A4998 Stepstick from an Arduino UNO.
// Paul Hurley Aug 2015
int x; 
int pushButton = 2;
int endButton = 3;

int sensorValue =0;
#define BAUD (9600)

void setup() 
{
  
  // make the pushbutton's pin an input:
  pinMode(pushButton, INPUT);
  pinMode(endButton, INPUT);
  pinMode(13, OUTPUT);
  Serial.begin(BAUD);
  pinMode(6,OUTPUT); // Enable
  pinMode(5,OUTPUT); // Step
  pinMode(4,OUTPUT); // Dir
  digitalWrite(6,LOW); // Set Enable low
  
}
void init_pos()
{
  while(1){
    int endButtonState = digitalRead(endButton);
    if (endButtonState == HIGH) {
      digitalWrite(4,HIGH); // Set Dir high  
      digitalWrite(5,HIGH); // Output high
      delay(1); // Wait 
      digitalWrite(5,LOW); // Output low
      delay(1); // Wait 
      
    
    } else {
      digitalWrite(4,LOW); // Set Dir high  
      for(x = 0; x < 30; x++) // Loop 200 times
      {
        digitalWrite(5,HIGH); // Output high
        delay(1); // Wait 
        digitalWrite(5,LOW); // Output low
      }
      break;
    }
  }
}

void button_pooling()
{
  while(1){
    int buttonState = digitalRead(pushButton);
    if (buttonState == HIGH) {
      delay(300);
      break;
    }
  }
}

void Starting(){
  sensorValue = analogRead(A0);
  sensorValue = 1023 - sensorValue;
  sensorValue = map(sensorValue,0,1023,1,300);
  digitalWrite(4,LOW); // Set Dir high
  for(x = 0; x < 800; x++) // Loop 200 times
  {
      digitalWrite(5,HIGH); // Output high
      delay(sensorValue); // Wait
      digitalWrite(5,LOW); // Output low
      int buttonState = digitalRead(pushButton);
      if (buttonState == HIGH) {
        delay(300);
        break;
      }
  }

}


void loop() 
{
  init_pos();
  button_pooling();
  Starting();
  
  delay(10); // pause one second

  
}
