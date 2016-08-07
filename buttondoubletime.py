#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import thread

SDI   = 11
RCLK  = 12
SRCLK = 13
SDIB = 15
RCLKB = 16
SRCLKB = 18
BTN = 22

segCode = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71,0x40,0x80]


#code0=0x3f
#code1=0x06
#code2=0x5b
#code3=0x4f
#code4=0x66
#code5=0x6d
#code6=0x7d
#code7=0x07
#code8=0x7f
#code9=0x6f
#codeA=0x77
#codeB=0x7c
#codeC=0x39
#codeD=0x5e
#codeE=0x79
#codeF=0x71
codeDash=0x40
#codeDot=0x80

timerStarted = False

class InterruptExecution (Exception):
        pass

def print_msg():
        print 'Program is running...'
        print 'Please press Ctrl+C to end the program...'

def setup():
        GPIO.setmode(GPIO.BOARD)    #Number GPIOs by its physical location
        GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(SDI, GPIO.OUT)
        GPIO.setup(RCLK, GPIO.OUT)
        GPIO.setup(SRCLK, GPIO.OUT)
        GPIO.output(SDI, GPIO.LOW)
        GPIO.output(RCLK, GPIO.LOW)
        GPIO.output(SRCLK, GPIO.LOW)
        GPIO.setup(SDIB, GPIO.OUT)
        GPIO.setup(RCLKB, GPIO.OUT)
        GPIO.setup(SRCLKB, GPIO.OUT)
        GPIO.output(SDIB, GPIO.LOW)
        GPIO.output(RCLKB, GPIO.LOW)
        GPIO.output(SRCLKB, GPIO.LOW)        

def my_callback(channel): 
        if GPIO.input(BTN):
                doButton()

def doButton():
        global timerStarted
        print "Timer status on button press: " + str(timerStarted)
        if timerStarted == True:
                timerStarted = False
                hc595_shiftTens(codeDash)
                hc595_shiftOnes(codeDash)
        else:
                timerStarted = True
                thread.start_new_thread( countDown, ("counterdown",1,) )
        print "Timer status post button press: " + str(timerStarted)        

def hc595_shiftTens(dat):
        for bit in xrange(0, 8):
                GPIO.output(SDI, 0x80 & (dat << bit))
                GPIO.output(SRCLK, GPIO.HIGH)              
                time.sleep(0.001)
                GPIO.output(SRCLK, GPIO.LOW)
        GPIO.output(RCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(RCLK, GPIO.LOW)


def hc595_shiftOnes(dat):
        for bit in xrange(0, 8):
                GPIO.output(SDIB, 0x80 & (dat << bit))
                GPIO.output(SRCLKB, GPIO.HIGH)                
                time.sleep(0.001)
                GPIO.output(SRCLKB, GPIO.LOW)
        GPIO.output(RCLKB, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(RCLKB, GPIO.LOW)        

def countDown(threadName, delay):
        global timerStarted
        while timerStarted:
                try:
                        for i in xrange(12,0,-1):
                                print "i = " + str(i)
                                if i > 9:
                                        firstNum=str(i)[0]
                                        print "i > 9"
                                        secondNum=str(i)[1]
                                else:
                                        firstNum=0
                                        secondNum=i
                                print "firstNum is " + str(firstNum)
                                print "secondNum is " + str(secondNum)
                                print "before tens"
                                hc595_shiftTens(segCode[int(firstNum)])
                                print "before ones"
                                hc595_shiftOnes(segCode[int(secondNum)])
                                time.sleep(1)
                        hc595_shiftTens(codeDash)
                        hc595_shiftOnes(codeDash)
                        timerStarted = False
                except InterruptExecution:
                        print "Interrupted"
                        hc595_shiftTens(codeDash)
                        hc595_shiftOnes(codeDash)


def mainLoop():
        while True:
                pass

def destroy():   #When program ending, the function is executed.
        GPIO.cleanup()

if __name__ == '__main__': #Program starting from here
        print_msg()
        setup()
        try:
                GPIO.add_event_detect(BTN, GPIO.FALLING, callback=my_callback)  
                hc595_shiftTens(codeDash)
                hc595_shiftOnes(codeDash)
                #timerStarted=1
                #thread.start_new_thread( countDown, ("counterdown",1,) )
                mainLoop()

        except KeyboardInterrupt:
                destroy()

