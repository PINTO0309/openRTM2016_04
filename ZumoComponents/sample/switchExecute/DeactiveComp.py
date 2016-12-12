# coding:utf-8

import RPi.GPIO as GPIO
import os
from time import sleep

sleep(5)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN)

try:
	while True:
		if GPIO.input(14) == 1:
                        print "Stop start"
                        os.system("rtdeact /localhost/raspberrypi.host_cxt/Zumo0.rtc /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
                        sleep(0.5)
                        os.system("rtexit /localhost/raspberrypi.host_cxt/Zumo0.rtc")
                        print "Zumo0.rtc exit"
                        os.system("rtexit /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
                        print "LineTracer0.rtc exit"

                                
			
except KeyboardInterrupt:
    pass

GPIO.cleanup() 
