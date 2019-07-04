from bsmLib import RPL
RPL.init()
import curses, time

screen = curses.initscr()
curses.noecho()
curses.halfdelay(1)

motor_pin = 2
key = ''
key_down = time.time()

while key != ord('q'):
    key = screen.getch()
    screen.clear()
    screen.addstr(0, 0, 'Hit "q" to quit, and "a" or "d" to turn')
    screen.addstr(1, 0, 'Current movement state:')

    if key == ord('a'):
        RPL.servoWrite(motor_pin, 1400)
        key_down = time.time()
        screen.addstr(1, 24, 'Counterclockwise')
    if key == ord('d'):
        RPL.servoWrite(motor_pin, 1600)
        key_down = time.time()
        screen.addstr(1, 24, 'Clockwise')
    if time.time() - key_down > 0.5:
        RPL.servoWrite(motor_pin, 0)
        screen.addstr(1, 24, 'Stopped')
    if key == ord('q'):
        RPL.servoWrite(motor_pin, 0)
        curses.endwin()
    RPL.servoWrite(motor_pin, 0)
