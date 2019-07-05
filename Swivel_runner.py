from bsmLib import RPL
RPL.init()
import curses, time

screen = curses.initscr()
curses.noecho()
curses.halfdelay(1)

swivel_pin = 1
key = ''
key_hit = time.time()

while key != ord('1'):
  key = screen.getch()
  screen.clear()
  if key == ord('q'):
    screen.addstr('Moving swivel clockwise')
    RPL.servoWrite(swivel_pin, 2000)
    key_hit = True
  if key == ord('e'):
    screen.addstr('Moving swivel counterclockwise')
    RPL.servoWrite(swivel_pin, 1000)
    key_hit = True
  if time.time() - key_hit > 0.5:
    screen.addstr('Stopped')
    RPL.servoWrite(swivel_pin, 0)
  if key == ord('1'):
    RPL.servoWrite(swivel_pin, 0)
    curses.endwin()
