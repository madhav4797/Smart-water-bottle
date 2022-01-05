import RPi.GPIO as GPIO
import time
import math
import drivers

GPIO.setmode(GPIO.BCM)

LEDAlarm = 4
TRIG = 23
ECHO = 24

def CalculateNewDistance():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    print("waiting for sensor to settle")
    time.sleep(5)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while(GPIO.input(ECHO)==0):
        pulse_start = time.time()
    
    while(GPIO.input(ECHO)==1):
        pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration*17150
    distance = round(distance, 2)
    return distance

def TurnOnLight():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDAlarm, GPIO.OUT)
    GPIO.output(LEDAlarm, GPIO.HIGH)

def TurnOffLight():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LEDAlarm, GPIO.OUT)
    GPIO.setup(LEDAlarm, GPIO.LOW)
    GPIO.cleanup()

def LCDdisplay(x, y):
    display = drivers.Lcd()
    display.lcd_clear()
    display.lcd_display_string(x, 1)
    display.lcd_display_string(y, 2)

print("Fill the water to the fullest and then input the value\n")

LCDdisplay("Water Quantity", "in ml")
DrinkingAmount = int(input("How much water do you wish to drink(in ml): "))

LCDdisplay("Frequency", "in min")
DrinkingFrequency = int(input("In how many minutes you wish to drink the water: "))*60

LCDdisplay(str(DrinkingAmount)+"ml", str(DrinkingFrequency/60)+"min")
NoOfTimes = math.floor(1000/DrinkingAmount)

Distance = (16.5)*(float(DrinkingAmount)/1000)
DistanceInitial = 3.41
print(Distance, NoOfTimes, DrinkingAmount)


for i in range(0, int(NoOfTimes)):
    print("start checking")
    time.sleep(DrinkingFrequency)
    TurnOnLight()
    check = 1
    while(check == 1):
        DistanceFinal = CalculateNewDistance()
        if(DistanceFinal-DistanceInitial>=Distance):
            DistanceInitial = DistanceFinal
            TurnOffLight()
            check = 0
            print(DistanceInitial)
            print(DistanceFinal)
            WaterLeft = ((16.5-DistanceFinal+3.41)/16.5)*1000
            LCDdisplay(str(WaterLeft)+"ml water","left to drink") 
        else:
            LCDdisplay("Please Drink", "some water")
            time.sleep(60)
            TurnOnLight()