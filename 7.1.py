import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time


list = []
leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = 8
TroykaMoudle = 17
comparator = 4
levels = 2**bits
maxVOLTAGE = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(TroykaMoudle, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)

def decimal2binary(i):
    return [int(elem) for elem in bin(i)[2:].zfill(bits)]
def bin2dac(i): 
     signal = decimal2binary(i)
     GPIO.output(dac, signal)
     return signal
def adc():
    value = 0
    for i in range(7, -1, -1):
        bin2dac(value + 2 ** i)
        time.sleep(0.008)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            value += 2 ** i
    return value

try:
    check = 1
    GPIO.output(17,1) 
    start = time.time() 
    print('Зарядка началась.')
    while True:
        value = adc()
        GPIO.output(leds, decimal2binary(value)) 
        if value >= 60 and check == 1: 
            GPIO.output(17, 0)
            print('Разрядка началась.')
            check = 0
        if check == 0 and value <= 5:
            end = time.time()
            T = (end - start)/(len(list)-1)
            print("Общее время = {:.2f}". format(end-start))
            nu = 1/T 
            dV = maxVOLTAGE / levels 
            list.append(value) 
            break
        list.append(value) 
        voltage = maxVOLTAGE / levels * value
        print("digital value = {:^3}, anallog VOLTAGE = {:.2f}". format(value, voltage)) 
    plt.plot(list)
    with open('data.txt', 'w') as outputfile1:
        for i in range(len(list)):
            outputfile1.write(str(list[i])+ '\n')
    with open('settings.txt', 'w') as outputfile2:
            outputfile2.write('T = '+ str(T) + '\n')
            outputfile2.write('dV = ' + str(dV))
    plt.show() 
    
finally:
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")