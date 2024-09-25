#include <ESP8266WiFi.h>
#include<WiFiClientSecure.h>
#include<ESP8266HTTPClient.h>
#include <ESPSupabase.h>
#define button 16

const char *ssid = "MANI SURYA TEJA's S23";
const char *password = "kkkkkkkk";
const char *url = "https://tgyzaqrrxsjqwlkanrqh.supabase.co/";
const char *key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRneXphcXJyeHNqcXdsa2FucnFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY3MDI1NzIsImV4cCI6MjA0MjI3ODU3Mn0.gkOxXIxUR0axX5syhUhQlOBCTqodeMVkSu5YP_sUjJw";
const char *name = "status";
WiFiClient client;

Supabase db;

void setup() {
  Serial.begin(115200);
  pinMode(button,INPUT);
  connect();
}

void connect() {
  Serial.println();
  Serial.println("Connecting to wifi..");

  int retry = 0;
  WiFi.begin(ssid, password);

  // Retry for a maximum of 15 times or until connection is successful
  while ((WiFi.status() != WL_CONNECTED) && (retry < 15)) {
    retry += 1;
    Serial.print(".");
    delay(1000); // Small delay between retries
  }
  delay(3000);
  // Check if successfully connected
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nConnectivity Failed");
  }
  db.begin(url,key);


}

void loop() {
  // Print the IP address every second
  if(digitalRead(Button)){
  db.urlQuery_reset();
  String json="[{\"ready\":1}]";
  db.update("status").eq("id", "1").doUpdate(json);
  db.urlQuery_reset();
  String json="[{\"result\":""}]";
  db.update("status").eq("id", "1").doUpdate(json);
  delay(1000);
  }
}
