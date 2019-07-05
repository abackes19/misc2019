from bsmLib import RPL
RPL.init()

import sys, tty, termios, signal

motor = 7
r_turn = 1000
l_turn = 2000

try:
  RPL.pinMode(motor,RPL.SERVO)
  RPL.servoWrite(motor,0)
except:
  pass

def stopAll():
  try:
    RPL.servoWrite(motor,0)
  except:
    print "error except"
    pass

def right():
  RPL.servoWrite(motor,r_turn)

def left():
  RPL.servoWrite(motor,l_turn)

fd = sys.stdin.fileno() # I don't know what this does
old_settings = termios.tcgetattr(fd) # this records the existing console settings that are later changed with the tty.setraw... line so that they can be replaced when the loop ends

def interrupted(signum, frame): # this is the method called at the end of the alarm
  stopAll()

signal.signal(signal.SIGALRM, interrupted) # this calls the 'interrupted' method when the alarm goes off
tty.setraw(sys.stdin.fileno()) # this sets the style of the input

print "Ready To Drive! Press * to quit.\r"
## the SHORT_TIMEOUT needs to be greater than the press delay on your keyboard
## on your computer, set the delay to 250 ms with `xset r rate 250 20`
SHORT_TIMEOUT = 0.255 # number of seconds your want for timeout
while True:
  signal.setitimer(signal.ITIMER_REAL,SHORT_TIMEOUT) # this sets the alarm
  ch = sys.stdin.read(1) # this reads one character of input without requiring an enter keypress
  signal.setitimer(signal.ITIMER_REAL,0) # this turns off the alarm
  if ch == '*': # pressing the asterisk key kills the process
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # this resets the console settings
    break # this ends the loop
  else:
    if ch == 'a':
      left()
    elif ch == "d":
      right()
    else:
      stopAll()
