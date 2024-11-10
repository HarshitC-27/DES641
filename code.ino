// Define pins for ultrasonic sensors and LEDs
#define TRIG_PIN_1 2
#define ECHO_PIN_1 3
#define TRIG_PIN_2 4
#define ECHO_PIN_2 5

#define RED_LED_1 10
#define GREEN_LED_1 11
#define RED_LED_2 12
#define GREEN_LED_2 13

// Threshold distance to detect the car (in centimeters)
const int distanceThreshold = 10;

void setup() {
  // Set up pins for ultrasonic sensors
  pinMode(TRIG_PIN_1, OUTPUT);
  pinMode(ECHO_PIN_1, INPUT);
  pinMode(TRIG_PIN_2, OUTPUT);
  pinMode(ECHO_PIN_2, INPUT);

  // Set up pins for LEDs
  pinMode(RED_LED_1, OUTPUT);
  pinMode(GREEN_LED_1, OUTPUT);
  pinMode(RED_LED_2, OUTPUT);
  pinMode(GREEN_LED_2, OUTPUT);

  Serial.begin(9600); // Start serial communication for debugging
}

void loop() {
  checkSpace(TRIG_PIN_1, ECHO_PIN_1, RED_LED_1, GREEN_LED_1, 1);
  checkSpace(TRIG_PIN_2, ECHO_PIN_2, RED_LED_2, GREEN_LED_2, 2);
  delay(500);  // Delay to avoid excessive polling
}

void checkSpace(int trigPin, int echoPin, int redLed, int greenLed, int spaceNumber) {
  long duration, distance;
  
  // Send a pulse to trigger the sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the time it takes for the echo to return
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; // Convert the duration to distance in cm

  // Check if a car is present based on the threshold
  if (distance <= distanceThreshold) {
    digitalWrite(redLed, HIGH);    // Turn on red LED (occupied)
    digitalWrite(greenLed, LOW);   // Turn off green LED (unoccupied)
    Serial.print("Space ");
    Serial.print(spaceNumber);
    Serial.println(" is Occupied");
  } else {
    digitalWrite(redLed, LOW);     // Turn off red LED (not occupied)
    digitalWrite(greenLed, HIGH);  // Turn on green LED (unoccupied)
    Serial.print("Space ");
    Serial.print(spaceNumber);
    Serial.println(" is Unoccupied");
  }
}
