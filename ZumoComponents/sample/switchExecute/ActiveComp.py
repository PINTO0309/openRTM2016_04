# coding:utf-8

import RPi.GPIO as GPIO
import os
from time import sleep

sleep(5)
GPIO.setmode(GPIO.BCM)
GPIO.setup(25,GPIO.IN)

try:
	while True:
		if GPIO.input(25) == 1:
                        print "start"
                        os.system("echo y | rtm-naming")
                        os.system("sudo python /home/pi/Desktop/RTC/Zumo-comp.py &")
                        print "Start Zumo-comp.py"
                        os.system("sudo python /home/pi/Desktop/RTC/LineTracer-comp.py &")
                        print "Start LineTracer-comp.py"
                        sleep(0.5)
                        os.system("rtcon /localhost/raspberrypi.host_cxt/Zumo0.rtc:VelocityIn /localhost/raspberrypi.host_cxt/LineTracer0.rtc:Velocity")
                        os.system("rtcon /localhost/raspberrypi.host_cxt/Zumo0.rtc:LineSensors /localhost/raspberrypi.host_cxt/LineTracer0.rtc:LineSensors")
                        os.system("rtconf /localhost/raspberrypi.host_cxt/Zumo0.rtc set Port /dev/ttyACM0")
                        print "Setting Complete"
                        sleep(0.5)
                        print "start"
                        os.system("rtact /localhost/raspberrypi.host_cxt/Zumo0.rtc /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
                
                                
			
except KeyboardInterrupt:
    pass

GPIO.cleanup() 
