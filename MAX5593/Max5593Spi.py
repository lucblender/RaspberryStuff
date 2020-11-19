import spidev

bus = 0
device = 0

spi = spidev.SpiDev()
spi.open(bus, device)
spi.mode = 0b00

def send_value(value):
    value_1 = (value & 0xF00)>>8
    value_2 = (value & 0xFF)
    for i in range (0,8):
        data_1 = (value_1 | i << 4)
        spi.xfer([data_1, value_2])
    
    spi.xfer([0x8F, 0xFF])
