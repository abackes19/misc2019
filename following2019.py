from bsmLib import RPL
RPL.init()
import time, math
import post_to_web as PTW


x = "yes"

# motors
motorL = 0
motorR = 1

# analog sensors
fana = 0
bana = 1
lana = 2
bl_ana = 3
br_ana = 4
fdig = 5

# speeds
go = 1750
slowgo = 1650
back = 1250
slowback = 1350


# readings
#Fanalog = RPL.analogRead(fana)
#Banalog = RPL.analogRead(bana)
#Lanalog = RPL.analogRead(lana)
#fsensor = RPL.analogRead(fdig)

# distances
#straight = Fanalog - Banalog
fardist = 200
closedist = 500
gone = 50



def reverse():
    RPL.servoWrite(motorL,back)
    RPL.servoWrite(motorR,back)
def slow_reverse():
    RPL.servoWrite(motorL,slowback)
    RPL.servoWrite(motorR,slowback)

def forward():
    RPL.servoWrite(motorL,go)
    RPL.servoWrite(motorR,go)

def stop():
    RPL.servoWrite(motorL, 1500)
    RPL.servoWrite(motorR, 1500)

def hardL():
    RPL.servoWrite(motorL,slowback)#TURN LEFT TURN LEFT
    RPL.servoWrite(motorR,slowgo)
def slightL():
    RPL.servoWrite(motorL,slowgo)
    RPL.servoWrite(motorR,go)

def slightR():
    RPL.servoWrite(motorL,go)#TURN LEFT TURN LEFT
    RPL.servoWrite(motorR,slowgo)
def hardR():
    RPL.servoWrite(motorL,slowgo)#TURN RIGHT TURN RIGHT
    RPL.servoWrite(motorR,slowback)

while x != "no": # big loop

    while True: # forward
        Fanalog = RPL.analogRead(fana)
        Banalog = RPL.analogRead(bana)
        Lanalog = RPL.analogRead(lana)
        bl_analog = RPL.analogRead(bl_ana)
        br_analog = RPL.analogRead(br_ana)
        fsensor = RPL.analogRead(fdig)

        PTW.state['Fanalog'] = Fanalog
        PTW.state['Banalog'] = Banalog
        PTW.state['Lanalog'] = Lanalog
        PTW.state['fsensor'] = fsensor
        forward()



        if Banalog > gone: # getting backR
            if Fanalog > gone: # ... and frontR
                if fsensor > 150: # ... and front
                    if Lanalog <= gone: # but not left, at turn so turn left TURN TURN TURN
                        while fsensor > 50:
                            slow_reverse()
                        stop()
                        while math.abs(bl_analog - br_analog) > 50 and math.abs(Fanalog - Banalog) > 50:
                            hardL()
                        forward()
                    else: # ... and left, then at end
                        stop()
                        break # spin! spin!


                # centering if whole robot too close or far away
                elif Fanalog >= closedist or Banalog >= closedist: # too close
                    slightL()

                elif Fanalog <= fardist or Banalog <= fardist:
                    slightR()


            else: # no front or front right, but back right
                forward() # need to continue so doesn't turn too sharp, will turn when get front

        else: # back right gets nothing, turn right
            if fsensor > 50 and Lanalog > 50: #TURN RIGHT TURN RIGHT TURN RIGHT
                while fsensor > 50:
                    slow_reverse()
                stop()
                while math.abs(bl_analog - br_analog) > 50:
                    hardR()
                forward()
            else:
                forward()
        PTW.post()


    while True: # full spin
        hardR()
        if math.abs(bl_analog - br_analog) < 50 and fsensor < 50:
            stop()
            break
    stop()

    #####################################################

    x = input("continue? >")
