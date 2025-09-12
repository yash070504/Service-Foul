#define transmit 6 // Laser transmitter module pin
#define ldr A0     // LDR input pin
#define irPin A1   // IR sensor input pin
#define buzzer 7   // Buzzer pin

void setup()
{
    Serial.begin(9600);
    pinMode(transmit, OUTPUT);
    pinMode(ldr, INPUT);
    pinMode(irPin, INPUT);
    pinMode(buzzer, OUTPUT);
    digitalWrite(transmit, HIGH); // Laser always ON
}

void loop()
{
    int ldrval = analogRead(ldr);
    int irval = analogRead(irPin);

    Serial.print("ldr: ");
    Serial.print(ldrval);
    Serial.print(" ir: ");
    Serial.println(irval);

    int threshold_ldr = 210;
    int threshold_ir = 1000;

    if (ldrval > threshold_ldr || irval > threshold_ir)
    {
        digitalWrite(buzzer, HIGH);
    }
    else
    {
        digitalWrite(buzzer, LOW);
    }

    delay(1000);
}
