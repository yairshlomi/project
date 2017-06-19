//Send.ino

#include<SPI.h>
#include<RF24.h>
#include "DHT.h"

#define DHTPIN 2
#define PIRPIN 3
#define FLAMEPIN A0
#define SMOKEPIN A1
#define LPGPIN A2
#define BUZZER 4


#define DHTTYPE DHT22

// ce, csn pins
RF24 radio(9, 10);
DHT dht(DHTPIN, DHTTYPE);

int id;
int count;
const int datasize = 28;
bool fire_alarm = false;
bool fire_temp = false;
bool fire_lpg = false;
bool fire_smoke = false;

struct payload {
  int id;
  int temp;
  bool pir;
  int flame;
  int smoke;
  int lpg;

};

payload sample = {0,0,0,0,0,0};

void setup(void){

  id = 1;
  //while (!Serial);
  //delay(5000);
  Serial.begin(9600);

  pinMode(PIRPIN, INPUT);

  Serial.println("DHTxx test!");

  dht.begin();
  delay(5000);


  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);

  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe (1, pipe);

  radio.enableDynamicPayloads();
  radio.powerUp();


   radio.startListening();
   Serial.println("starting loop, radio on.");

}

void loop(void){

   char receiveMessage[32] = {0};
   count = 0;


   if(radio.available()) {
    radio.read(receiveMessage, sizeof(receiveMessage));
    Serial.println(receiveMessage);
    Serial.println("Turning off the radio");
    radio.stopListening();

    String stringMessage(receiveMessage);

    Serial.println(stringMessage);

    if(stringMessage == "SAMPLE") {
      Serial.println("Looks like they want to sample the sensors!");

      sample_sensors(&sample, id);

      char message[32];
      convert_to_string(&sample, message);


      Serial.print("the second message is");
      while (count < 32) {
      Serial.print(message[count]);
      count++;
     }
      count = 0;

    Serial.println();


      radio.write(message,sizeof(message));
      Serial.println("we sent our message");

    }

    else {
      int 1_counet = 0, 2_counet = 0,3_counet = 0, 4_counet = 0;
      for (int j = 0; stringMessage[i] != '0'; j++)
            swtich (stringMessage[i]) {
                case '1':
                {
                    flame_alarm = true;
                    1_counet++;
                    break;
                }
                case '2':
                {
                    lpg_alarm= true;
                    2_counet++;
                    break;
                  }
                case '3':
                {
                    smoke_alarm = true;
                    3_counet++;
                    break;
                }
                case '5':
                {
                    temp_alarm = true;
                    5_counet++;
                break;
                }
                default:
                  break;

      }
        if (1_counet == 0)
          flame_alarm = false;
        if (2_counet == 0)
            lpg_alarm = false;
        if (3_counet == 0)
            smoke_alarm = false;
        if (5_counet == 0)
            temp_alarm = false;

    }


    if(sample.temp > 5000 && !temp_alarm || sample.flame > 400 && !flame_alarm|| sample.smoke > 800 && !smoke_alarm|| sample.lpg > 800&& !lpg_alarm) {
      Serial.println("Emergency!");
      tone (BUZZER, 1000, 15000);
    }



     //stringMessage.remove(0);




   Serial.print("the temprature is: ");
   Serial.println(sample.temp);
   Serial.print("the PIR value is: ");
   Serial.println(sample.pir);
   Serial.print("the flame value is: ");
   Serial.println(sample.flame);
   Serial.print("the smoke value is: ");
   Serial.println(sample.smoke);
   Serial.print("the lpg value is: ");
   Serial.println(sample.lpg);

   }
   radio.startListening();
   Serial.println("waiting for signal");
   delay(50);


}

void sample_sensors(payload *sample, int id) {


   sample->id = id;
   float floattemp = dht.readTemperature();
   floattemp *=100;
   int temp = (int) floattemp;
   sample->temp = temp;
   bool pir = digitalRead(PIRPIN);
   sample->pir = pir;
   int flame = analogRead(FLAMEPIN);
   sample->flame = flame;
   int smoke = analogRead(SMOKEPIN);
   sample->smoke = smoke;
   int lpg = analogRead(LPGPIN);
   sample->lpg = lpg;



}


void convert_to_string(payload *sample, char* message) {

  char data [32];
  for (int j = 0; j < 32; j++)
    data[j] = '\0';
  int data_counter = 0;
  int i = 0;
  int temp;
  char digits [] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ' };
  int zero = 0;


  data [data_counter] = digits[(sample->id)];
  data_counter++;

  data [data_counter] = digits[10];
  data_counter++;

  temp = sample->temp;



  if (temp % 10 == 0) {
    zero = zeros(temp);


  }

    temp = reverse(temp);
  while (temp > 0) {
    data [data_counter] = digits[temp % 10];
    temp /= 10;
    data_counter++;

  }

   if (zero != 0)
    for (i = 0; i < zero; i++)  {
      data [data_counter] = digits[0];
      data_counter++;

  }
  zero = 0;


  data [data_counter] = digits[10];
  data_counter++;

  data [data_counter] = digits[(sample->pir)];
  data_counter++;

  data [data_counter] = digits[10];
  data_counter++;

  temp = sample->flame;

  if (temp % 10 == 0) {
    zero = zeros(temp);


  }

  temp = reverse(temp);
  while (temp > 0) {
    data [data_counter] = digits[temp % 10];
    temp /= 10;
    data_counter++;

  }

   if (zero != 0)
    for (i = 0; i < zero; i++)  {
      data [data_counter] = digits[0];
      data_counter++;

  }

    zero = 0;


  data [data_counter] = digits[10];
  data_counter++;

  temp = sample->smoke;

  if (temp % 10 == 0) {
    zero = zeros(temp);

  }

  temp = reverse(temp);
  while (temp > 0) {
    data [data_counter] = digits[temp % 10];
    temp /= 10;
    data_counter++;

  }

   if (zero != 0)
    for (i = 0; i < zero; i++)  {
      data [data_counter] = digits[0];
      data_counter++;

  }

    zero = 0;


 data [data_counter] = digits[10];
  data_counter++;

  temp = sample->lpg;
if (temp % 10 == 0) {
    zero = zeros(temp);

  }
  temp = reverse(temp);
  while (temp > 0) {
    data [data_counter] = digits[temp % 10];
    temp /= 10;
    data_counter++;

  }

   if (zero != 0)
    for (i = 0; i < zero; i++)  {
      data [data_counter] = digits[0];
      data_counter++;

  }

    zero = 0;

  data [data_counter] = digits[10];
  data_counter++;





  int count = 0;



  Serial.println();

  Serial.println("the data counter is");
  Serial.println(data_counter);

    for (int j = data_counter; j < 32; j++)
    data[j] = '0';


    Serial.print("the first message is ");
    while (count < 32) {
    Serial.print(data[count]);
    count++;
     }

    Serial.println();


  count = 0;
  while (count < 32) {
    message [count] = data[count];
    count++;
     }


}

int reverse(int num) {

  int rev = 0;
  int i = 0;
  int digit[5] = {10000,10000,10000,10000,10000};
  int count = 0;



  while (num > 0) {
    digit [count++] = num % 10;
    num /= 10;

  }
  i = 0;
  while (digit[i] != 10000) {
    rev += digit[i];
    i++;
    if (digit[i] != 10000)
      rev *=10;

  }

  return rev;


}


int zeros(int num) {

  int count = 0;
  if (num % 10 == 0)
    count++;

  if (num % 100 == 0)
    count++;

 if (num % 1000 == 0)
    count++;

  return count;

}
