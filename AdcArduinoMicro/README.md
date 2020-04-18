# ADC converter for Raspberry Pi using an Arduino

## Description

Raspberry pi doesn't have any analog input but Arduino does. I just did a simple code on Arduino to do ADC aquisition and send them by I2C to a Raspberry Pi.

## Use

Upload the arduino code in your favorite arduino micro from the folder analogI2C.
Wire your arduino to your raspberry pi (5V, GND, SDA, SCL). 

If you wired everything correctly you should detect the arduino with ``` i2cdetect -y 1 ``` at the address 0x08. 

To try to get the ADC value of the channel 0 you can use ```i2cget -y 1 0x08 0x00 w```. 

Now you can test the python driver like so:

```

from adc_Arduino_Micro import Adc_Arduino_Micro


adc = Adc_Arduino_Micro()

adc.read_raw(0) # will read ADC0 and return value between 0 and 1023 

adc.read_voltage(0) # will read ADC0 and return value between 0 and 5 (V)

adc.read_voltage(0, 3.3) # will read ADC0 and return value between 0 and 3.3 (V) 


``` 

## Fix your arduino to your Raspberry

I did a little support to 3D print available as stl file: ArduinoFix v1.stl