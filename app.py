import RPi.GPIO as GPIO
import time
import picamera
from subprocess import call
import datetime
camera = picamera.PiCamera()
camera.resolution = (1600, 1200)
camera.sharpness = 100


GPIO.setmode(GPIO.BCM)

TRIG = 21
ECHO = 18

def takePicture():
    date_string = str(datetime.datetime.now())

    name = input("What is your name?")

    print("Name is " + name)
    time.sleep(3)
    camera.capture('image.jpg')
##    camera.close()
    call([" cp /home/pi/image.jpg " + "/home/pi/" + name], shell=True)

def checkDistance():
    print("Distance measurement in progress")

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)

    print("Waiting for sensor to settle")

    time.sleep(2)    

    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
        

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()


    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print("Distance: %.1f cm" % distance)

    return distance

if __name__ == '__main__':
    try:
        while True:
            returnDist = checkDistance()
            if returnDist < 40:
                takePicture()
            else:
                continue
    except KeyboardInterrupt:
        print ("Stopped measurement")
        camera.close()
        GPIO.cleanup()
