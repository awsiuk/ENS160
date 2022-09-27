import machine
import time

ENS160_ADDR = 0x53

## ENS160 chip version
ENS160_PART_ID = 0x160

# ENS160 Register address
## This 2-byte register contains the part number in little endian of the ENS160.
ENS160_PART_ID_REG = 0x00
## This 1-byte register sets the Operating Mode of the ENS160.
ENS160_OPMODE_REG = 0x10
## This 1-byte register configures the action of the INTn pin.
ENS160_CONFIG_REG = 0x11
## This 1-byte register allows some additional commands to be executed on the ENS160.
ENS160_COMMAND_REG = 0x12
## This 2-byte register allows the host system to write ambient temperature data to ENS160 for compensation.
ENS160_TEMP_IN_REG = 0x13
## This 2-byte register allows the host system to write relative humidity data to ENS160 for compensation.
ENS160_RH_IN_REG = 0x15
## This 1-byte register indicates the current STATUS of the ENS160.
ENS160_DATA_STATUS_REG = 0x20
## This 1-byte register reports the calculated Air Quality Index according to the UBA.
ENS160_DATA_AQI_REG = 0x21
## This 2-byte register reports the calculated TVOC concentration in ppb.
ENS160_DATA_TVOC_REG = 0x22
## This 2-byte register reports the calculated equivalent CO2-concentration in ppm, based on the detected VOCs and hydrogen.
ENS160_DATA_ECO2_REG = 0x24
## This 2-byte register reports the calculated ethanol concentration in ppb.
ENS160_DATA_ETOH_REG = 0x22
## This 2-byte register reports the temperature used in its calculations (taken from TEMP_IN, if supplied).
ENS160_DATA_T_REG = 0x30
## This 2-byte register reports the relative humidity used in its calculations (taken from RH_IN if supplied).
ENS160_DATA_RH_REG = 0x32
## This 1-byte register reports the calculated checksum of the previous DATA_ read transaction (of n-bytes).
ENS160_DATA_MISR_REG = 0x38
## This 8-byte register is used by several functions for the Host System to pass data to the ENS160.
ENS160_GPR_WRITE_REG = 0x40
## This 8-byte register is used by several functions for the ENS160 to pass data to the Host System.
ENS160_GPR_READ_REG = 0x48

# OPMODE(Address 0x10) register mode
## DEEP SLEEP mode (low power standby).
ENS160_SLEEP_MODE  = 0x00
## IDLE mode (low-power).
ENS160_IDLE_MODE = 0x01
## STANDARD Gas Sensing Modes.
ENS160_STANDARD_MODE = 0x02

# CMD(0x12) register command
## reserved. No command.
ENS160_COMMAND_NOP = 0x00
## Get FW Version Command.
ENS160_COMMAND_GET_APPVER = 0x0E
## Clears GPR Read Registers Command.
ENS160_COMMAND_CLRGPR = 0xCC


class myENS160:
    def calibrate_temp(self, _temp):
        buf = bytearray(2)
        buf[0] = _temp & 0xFF
        buf[1] = (_temp & 0xFF00) >> 8
        self.i2c.writeto_mem(ENS160_ADDR, ENS160_TEMP_IN_REG, buf)
        time.sleep(0.2)
        
    def calibrate_hum(self, _rh):
        buf = bytearray(2)
        buf[0] = _rh & 0xFF
        buf[1] = (_rh & 0xFF00) >> 8
        self.i2c.writeto_mem(ENS160_ADDR, ENS160_RH_IN_REG, buf)
        time.sleep(0.2)
        
    def __init__(self):
        SCL_PIN=machine.Pin(1)
        SDA_PIN=machine.Pin(0)
        print("initialize i2c")
        self.i2c=machine.I2C(0,scl=SCL_PIN, sda=SDA_PIN,freq=400000)
        print("setting OPMODE")
        buf=bytearray(1)
        buf[0]=ENS160_STANDARD_MODE
        self.i2c.writeto_mem(ENS160_ADDR, ENS160_OPMODE_REG, buf)
        time.sleep(0.2)
        #print("initial calibration")
        self.calibrate_temp(25)
        self.calibrate_hum(50)
        
    def getAQI(self):
        buf=self.i2c.readfrom_mem(ENS160_ADDR,ENS160_DATA_AQI_REG,1)
        return (buf[0])
  
    def getTVOC(self):
        buf=self.i2c.readfrom_mem(ENS160_ADDR,ENS160_DATA_TVOC_REG,2)
        return (buf[1]<<8 | buf[0])
    
    def getECO2(self):
        buf=self.i2c.readfrom_mem(ENS160_ADDR,ENS160_DATA_ECO2_REG,2)
        return (buf[1]<<8 | buf[0])
