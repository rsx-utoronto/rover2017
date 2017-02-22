// spoof lidar readings 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); 
}

int generateNoise() { 
  // approximate gaussian noise with the sum of uniforms
  float sum = 0; 
  for(int i=0; i<20; i++) {
    sum += Math.random() - 0.5; 
  }
  return (int) sum; 
}

int pos1, pos2 = 90; 

void loop() {
  // put your main code here, to run repeatedly:

  int pulse_width = pos1 + generateNoise(); 
  
  Serial.println(String(pulse_width) + "   " + String(pos1) + "   " + String(pos2));
  delay(10); 
}
