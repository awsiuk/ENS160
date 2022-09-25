from myENS160 import myENS160

obj=myENS160()
TVOC=obj.getTVOC()
AQI=obj.getAQI()
ECO2=obj.getECO2()
print(AQI)
print(TVOC)
print(ECO2)

