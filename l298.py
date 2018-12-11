# AutoTelescope by Aidan Taylor
# Move a telescope with 2 stepper motors
# Includes piCamera, Keypad Controls and LSM303 sensor for positioning
# Please note will run in Python 2 only

# include the following libraries

from picamera import PiCamera
import RPi.GPIO as GPIO
import Adafruit_LSM303
import time

# create Camera instance
camera = PiCamera() #activate the camera
camera.hflip = True

# create LSM303 instance

lsm303 = Adafruit_LSM303.LSM303()

#GPIO main setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Stepper GPIO
delay = 0.06 #sets how fast the steppers can sequence
steps = 100 #only used to test the steppers now

azCoilA1Pin = 11
azCoilA2Pin = 12
azCoilB1Pin = 13
azCoilB2Pin = 15

alCoilA1Pin = 16
alCoilA2Pin = 18
alCoilB1Pin = 19
alCoilB2Pin = 21

GPIO.setup(azCoilA1Pin, GPIO.OUT)
GPIO.setup(azCoilA2Pin, GPIO.OUT)
GPIO.setup(azCoilB1Pin, GPIO.OUT)
GPIO.setup(azCoilB2Pin, GPIO.OUT)

GPIO.setup(alCoilA1Pin, GPIO.OUT)
GPIO.setup(alCoilA2Pin, GPIO.OUT)
GPIO.setup(alCoilB1Pin, GPIO.OUT)
GPIO.setup(alCoilB2Pin, GPIO.OUT)

stepAzNum = 0
stepAlNum = 0

#Keypad GPIO
rowPins = [31,32,33,35]
colPins = [36,37,38,40]

GPIO.setup(40, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP)

digits = [["1","2","3","A"],
          ["4","5","6","B"],
          ["7","8","9","C"],
          ["*","0","#","D"]]

keyLatch = [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]

key = 0
lastKey = 0
keyMode = 0

#Controls to switch the stepper coils
def setAzStep(w1, w2, w3, w4):
    GPIO.output(azCoilA1Pin, w1)
    GPIO.output(azCoilA2Pin, w2)
    GPIO.output(azCoilB1Pin, w3)
    GPIO.output(azCoilB2Pin, w4)

def setAlStep(w1, w2, w3, w4):
    GPIO.output(alCoilA1Pin, w1)
    GPIO.output(alCoilA2Pin, w2)
    GPIO.output(alCoilB1Pin, w3)
    GPIO.output(alCoilB2Pin, w4)

#Controls to move the steppers backwards and forwards
def azForward():
    global stepAzNum

    stepAzNum = stepAzNum +1

    if(stepAzNum <= 3):
        if(stepAzNum == 1):
            setAzStep(0,0,1,0)
            time.sleep(delay)
        if(stepAzNum == 2):
            setAzStep(0,1,0,0)
            time.sleep(delay)
        if(stepAzNum == 3):
            setAzStep(0,0,0,1)
            time.sleep(delay)
    else:
        stepAzNum = 0
        setAzStep(1,0,0,0)
        time.sleep(delay)
    
def azBackward():
    global stepAzNum

    stepAzNum = stepAzNum -1

    if(stepAzNum >= 0):
        if(stepAzNum == 0):
            setAzStep(1,0,0,0)
            time.sleep(delay)
        if(stepAzNum == 1):
            setAzStep(0,0,1,0)
            time.sleep(delay)
        if(stepAzNum == 2):
            setAzStep(0,1,0,0)
            time.sleep(delay)
    else:
        stepAzNum = 3
        setAzStep(0,0,0,1)
        time.sleep(delay)

def alForward():
    global stepAlNum

    stepAlNum = stepAlNum +1

    if(stepAlNum <= 3):
        if(stepAlNum == 1):
            setAlStep(0,0,1,0)
            time.sleep(delay)
        if(stepAlNum == 2):
            setAlStep(0,1,0,0)
            time.sleep(delay)
        if(stepAlNum == 3):
            setAlStep(0,0,0,1)
            time.sleep(delay)
    else:
        stepAlNum = 0
        setAlStep(1,0,0,0)
        time.sleep(delay)
        
def alBackward():
    global stepAlNum

    stepAlNum = stepAlNum -1

    if(stepAlNum >= 0):
        if(stepAlNum == 0):
            setAlStep(1,0,0,0)
            time.sleep(delay)
        if(stepAlNum == 1):
            setAlStep(0,0,1,0)
            time.sleep(delay)
        if(stepAlNum == 2):
            setAlStep(0,1,0,0)
            time.sleep(delay)
    else:
        stepAlNum = 3
        setAlStep(0,0,0,1)
        time.sleep(delay)

#Used to test the steppers
def stepTest():

    time.sleep(2)

    for i in range(0, steps):
        azForward()

    time.sleep(2)

    for i in range(0, steps):
        azBackward()

    time.sleep(2)

    for i in range(0, steps):
        alForward()

    time.sleep(2)

    for i in range(0, steps):
        alBackward()

    time.sleep(2)

#Scan the KeyPad
def controls():
    
    global keyLatch
    global key
    #For Loop polls columns to check pressed rows
    for col in range(0, 4):
        GPIO.output(colPins[col],0)
        time.sleep(0.001)
        for row in range(0, 4):
            inputState = GPIO.input(rowPins[row])
           # print("col: ",col, "row: ",row)
            if inputState == False and keyLatch[row][col] == False:
                keyLatch[row][col] = True
                key = (digits[row][col])
                #print(digits[row][col]) #uncomment to debug
                time.sleep(0.001)
            elif inputState == True and keyLatch[row][col] == True:
                keyLatch[row][col] = False
                key = "z"
        GPIO.output(colPins[col],1)
        time.sleep(0.001)

def freeMove():
    
    global keyLatch
    global key
    #For Loop polls columns to check pressed rows
    for col in range(0, 4):
        GPIO.output(colPins[col],0)
        time.sleep(0.001)
        for row in range(0, 4):
            inputState = GPIO.input(rowPins[row])
           # print("col: ",col, "row: ",row)
            if inputState == False:
                key = (digits[row][col])
                #print(digits[row][col]) #uncomment to debug
                time.sleep(0.001)
        GPIO.output(colPins[col],1)
        time.sleep(0.001)

# MAIN PROGRAM STARTS HERE
print("Program Starting")

#Unlock the steppers
setAzStep(0,0,0,0)
setAlStep(0,0,0,0)

print("Position telescope and press return/enter to start")
raw_input()
azForward()
alForward()
    
print("Press 2,6,8,4 to move, B and C for camera * to test, D to quit")

while True:

    accel, mag = lsm303.read()
    accel_x, accel_y, accel_z = accel
    mag_x, mag_z, mag_y = mag

    if keyMode == 1:
        camera.annotate_text = 'FREEMOVE Accel X={0}, Accel Y={1}, Accel Z={2}, Mag X={3}, Mag Y={4}, Mag Z={5}'.format(
                    accel_x, accel_y, accel_z, mag_x, mag_y, mag_z)
    else:
        camera.annotate_text = 'Accel X={0}, Accel Y={1}, Accel Z={2}, Mag X={3}, Mag Y={4}, Mag Z={5}'.format(
                    accel_x, accel_y, accel_z, mag_x, mag_y, mag_z)
    
    if keyMode == 0:
        controls()
        if key != lastKey:
            lastKey = key
            #print(key)
            if(key == "2"):
                alBackward()
            elif(key == "8"):
                alForward()
            elif(key == "4"):
                azForward()
            elif(key == "6"):
                azBackward()
            elif(key == "*"):
                stepTest()
            elif(key == "B"):
                camera.stop_preview()
                print("Camera Exit")
            elif(key == "C"):
                camera.start_preview()
                camera.vflip = True
                camera.crop = (0.25, 0.25, 0.5, 0.5) # This line crops the camera but reduces resolution
            elif(key == "#"):
                print('Accel X={0}, Accel Y={1}, Accel Z={2}, Mag X={3}, Mag Y={4}, Mag Z={5}'.format(
                    accel_x, accel_y, accel_z, mag_x, mag_y, mag_z))
            elif(key == "A"):
                print("Free Move")
                time.sleep(1)
                keyMode = 1
                key = "z"
            elif(key == "D"):
                camera.stop_preview()
                print("Now Quitting, support Telescope")
                time.sleep(5)
                setAlStep(0,0,0,0)
                setAzStep(0,0,0,0)
                print("Finished")
                break
    else:
        freeMove()
        if(key == "2"):
            alBackward()
            key = "z"
        elif(key == "8"):
            alForward()
            key = "z"
        elif(key == "4"):
            azForward()
            key = "z"
        elif(key == "6"):
            azBackward()
            key = "z"
        elif(key == "A"):
            print("Ending Free Move")
            time.sleep(1)
            keyMode = 0
