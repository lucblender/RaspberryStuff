import smbus
import logging

class Adc_Arduino_Micro:

    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.addr = 0x08

    def read_raw(self, channel):
        if channel in range(0,12):
            return self.bus.read_word_data(self.addr, channel)
        else:
            logging.error("ADC channel must be go from 0 to 11, not "+str(channel))
            return 0

    def read_voltage(self, channel, v_ref = 5):
        return v_ref*self.read_raw(channel)/1023

