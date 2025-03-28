from myENS160 import myENS160
import machine

#I2C init for sensors readout
#pin 11 & 12 is SDL  & SCA for ESP32-s3-nano
SCL_PIN=machine.Pin(11)
SDA_PIN=machine.Pin(12)
i2c=machine.I2C(0,scl=SCL_PIN, sda=SDA_PIN,freq=400000)

#init ENS160 sensor on the i2c bus
ens=myENS160(i2c)

# get data
TVOC=ens.getTVOC()
AQI=ens.getAQI()
ECO2=ens.getECO2()

#print data
print(AQI)
print(TVOC)
print(ECO2)

