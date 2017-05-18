# coding:utf-8

import RPi.GPIO as GPIO
import os
from time import sleep
import codecs
import subprocess

LCDLocation = '3e'

sleep(10)

class ActiveComp:
    def startComp_LineTracer(self):

        #Run Component
        ret = subprocess.call("sudo python /home/pi/Desktop/RTC/Zumo-comp.py &",shell=True)
        self.writeLCD("Zumo",ret)
        ret = subprocess.call("sudo python /home/pi/Desktop/RTC/LineTracer-comp.py &",shell=True)
        self.writeLCD("LineTracer",ret)

        #Wait time
        sleep(0.5)

    def startComp_LCD(self):
        os.system("sudo python /home/pi/Desktop/RTC/ReadingLog.py &")
        os.system("sudo python /home/pi/Desktop/RTC/TwoLinesLCD.py &")
        sleep(0.5)

    def rtshell_LineTracer(self):
        #RTShell Command
        os.system("rtcon /localhost/raspberrypi.host_cxt/Zumo0.rtc:VelocityIn /localhost/raspberrypi.host_cxt/LineTracer0.rtc:Velocity")#Connect Component
        os.system("rtcon /localhost/raspberrypi.host_cxt/Zumo0.rtc:LineSensors /localhost/raspberrypi.host_cxt/LineTracer0.rtc:LineSensors")#Connect Component
        os.system("rtconf /localhost/raspberrypi.host_cxt/Zumo0.rtc set Port /dev/ttyACM0")#Change Config
        print "Setting Complete"

        #Wait Time
        sleep(0.5)

    def rtshell_LCD(self):
        #RTShell Command
        os.system("rtcon /localhost/raspberrypi.host_cxt/ReadingLog0.rtc:Output /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc:Input")
        os.system("rtconf /localhost/raspberrypi.host_cxt/ReadingLog0.rtc set ErrorLog /home/pi/Desktop/RTC/ErrorLog.txt")
        os.system("rtconf /localhost/raspberrypi.host_cxt/ReadingLog0.rtc set SuccessLog /home/pi/Desktop/RTC/SuccessLog.txt")

    def ActiveComp(self):
        #Active component
        os.system("rtact /localhost/raspberrypi.host_cxt/ReadingLog0.rtc /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc /localhost/raspberrypi.host_cxt/Zumo0.rtc /localhost/raspberrypi.host_cxt/LineTracer0.rtc")

    def writeLCD(self,name,state):#make log
        if state == 0:
            f = open('/home/pi/Desktop/RTC/SuccessLog.txt','a')
            ret = subprocess.check_output('date')
            ret = ret.split(" ")
            f.write(ret[2] + " " + ret[1] + " " + ret[3] +"\n")
            f.write(name + "Active\n")
            f.close()
        else:
            f = open('/home/pi/Desktop/RTC/ErrorLog.txt','a')
            ret = subprocess.check_output('date')
            ret = ret.split(" ")
            f.write(ret[2] + " " + ret[1] + " " + ret[3] +"\n")
            f.write(name + "False\n")
            f.close()


class DeactiveComp:
    def Deactive_Comp(self):
        #Deact Component
        print "Stop start"
        os.system("rtdeact /localhost/raspberrypi.host_cxt/Zumo0.rtc /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
        os.system("rtdeact /localhost/raspberrypi.host_cxt/ReadingLog0.rtc /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc")

        #Wait time
        sleep(0.5)

    def exit_Comp(self):
        #Component Exit
        os.system("rtexit /localhost/raspberrypi.host_cxt/Zumo0.rtc")
        print "Zumo0.rtc exit"
        os.system("rtexit /localhost/raspberrypi.host_cxt/LineTracer0.rtc")
        print "LineTracer0.rtc exit"
        sleep(3)
        os.system("rtexit /localhost/raspberrypi.host_cxt/ReadingLog0.rtc")
        os.system("rtexit /localhost/raspberrypi.host_cxt/TwoLinesLCD0.rtc")
        print "All Components exit"

   
class check:
    def stateUpdate(self):
        
        os.system('bash /home/pi/checkName.sh')
    
    def ActivateCheck(self):
        #Check status is Active
        state_file = open('/home/pi/stateComp.txt','r')
        return state_file.read() == 'Active'
    
    def ActivateState(self):
        os.system('echo -n "Active"> /home/pi/stateComp.txt')

    def DeactivateState(self):
        os.system('echo -n "Deactive"> /home/pi/stateComp.txt')

class LED:
    def turnOn(self):
        GPIO.output(10,True)
        
    def turnOff(self):
        GPIO.output(10,False)

class writeLog:
    def LogMake(self):
        os.system('echo -n  > /home/pi/Desktop/RTC/ErrorLog.txt')
        os.system('echo -n  > /home/pi/Desktop/RTC/SuccessLog.txt')


GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN)
GPIO.setup(15,GPIO.IN)
GPIO.setup(10,GPIO.OUT)
os.system("echo y | rtm-naming")
LED = LED()
LED.turnOff()
check = check()
writeLog = writeLog()
check.stateUpdate()
check.DeactivateState()


try:
	while True:
		if GPIO.input(14) == 1:
                   if check.ActivateCheck() == False:
                       LED.turnOn()
                       state = ActiveComp()
                       writeLog.LogMake()
                       state.startComp_LCD()
                       state.rtshell_LCD()   
                       state.startComp_LineTracer()
                       state.rtshell_LineTracer()
                       state.ActiveComp()
                       check.ActivateState()
                   

                if GPIO.input(15) == 1:
                    if check.ActivateCheck() == True:
                        LED.turnOff()
                        state = DeactiveComp()
                        state.Deactive_Comp()
                        state.exit_Comp()
                        check.DeactivateState()

                    
except KeyboardInterrupt:
    pass

GPIO.cleanup() #GPIO close
    
