import RoboPiLib as RPL
RPL.RoboPiInit("/dev/ttyAMA0",115200)
import time, math
import post_to_web as PTW

now = time.time()
future = now

x = "yes"

# motors
motorL = 0
motorR = 1

# analog sensors
fana = 3
bana = 4
lana = 1

# digital sensors
fdig = 20
bdig = 18

# speeds
go = 1750
slowgo = 1650
back = 1250
slowback = 1350


#250 = l max
#r = 500


# turning times
ninety = 1.5
backup = .7

# readings
#Fanalog = RPL.analogRead(fana)
#Banalog = RPL.analogRead(bana)
#Lanalog = RPL.analogRead(lana)
#fsensor = RPL.digitalRead(fdig)
#bsensor = RPL.digitalRead(bdig)

# distances
#straight = Fanalog - Banalog
tolerance = 50
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
    RPL.servoWrite(motorL,slowgo)#TURN LEFT TURN LEFT
    RPL.servoWrite(motorR,slowback)
def hardR():
    RPL.servoWrite(motorL,slowgo)#TURN RIGHT TURN RIGHT
    RPL.servoWrite(motorR,slowback)

while x != "no": # big loop

    while True: # forward
        Fanalog = RPL.analogRead(fana)
        Banalog = RPL.analogRead(bana)
        Lanalog = RPL.analogRead(lana)
        fsensor = RPL.digitalRead(fdig)
        bsensor = RPL.digitalRead(bdig)

        PTW.state['Fanalog'] = Fanalog
        PTW.state['Banalog'] = Banalog
        PTW.state['Lanalog'] = Lanalog
        PTW.state['fsensor'] = fsensor
        PTW.state['bsensor'] = bsensor
        PTW.state['straight'] = straight
        forward()



        if Banalog > gone: # getting backR
            if Fanalog > gone: # ... and frontR
                if fsensor > 150: # ... and front
                    if Lanalog <= gone: # but not left, at turn so turn left TURN TURN TURN
                        while fsensor > 50:
                            slow_reverse()
                        stop()
                        while math.abs(bl_ana - br_ana) > 50 and math.abs(Fanalog - Banalog) > 50:
                            hardL()
                        forward()
                    else: # ... and left, then at end
                        stop()
                        break # reverse! reverse!


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
                while math.abs(Fanalog - Banalog) > 50:
                    hardR()
                forward()
            else:
                forward()

    #####################################################
        PTW.post()

    x = input("continue? >")
