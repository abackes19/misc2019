# using arrow keys! also multiple angles! sideview and topview
# notes: can use continuously, but use one key at a time in an orderly fashion

# able to change z coordinate, and see change on topview.
# z is a plane, w is a dummy plane
# elbow is working
# don't cross y axis

# now integrating grasper movement too

# 0 = True, 1 = False

multiplier = 3
d_one = 23 * multiplier # the distance from shoulder to elbow
d_two = 23 * multiplier # distance from elbow to wrist
robot_height = 8 * multiplier
robot_length = 28 * multiplier
long_end = 22 * multiplier
holder_height = 2 * multiplier
robot_width = 16 * multiplier

#the files needed to run the code
import pygame, math, time, socket, pickle
from pygame.locals import *

#enters Pygame
pygame.init()

#define the colors for the display
white = (255,255,255); black = (0,0,0)
red = (255,0,0); green = (127, 232, 134)
blue = (102, 136, 214); pink = (232, 13, 119)
grey = (203, 206, 214)

#dimentions of Pygame screen
display_width = 800
display_height = 450
screen = pygame.display.set_mode((display_width,display_height))
screen.fill(white)

#set the size of the step each input takes
step = 2

#set the origin of the side view
originx = 225
originy = 250

#set the origin of the top view
toriginz = 575
toriginw = 250

#defining variables so no error occurs
x, y, z, w = d_two, d_one, 0, d_two
xo, yo = x, y
x_change = y_change = z_change = 0

#setting up socket connection
s = socket.socket()
port = 2187
xyz = [x, y, z]

gopen = gclose = 1
#gopen = gclose = False

#set up kill commands
done = False
connect = True

def ik(x, y, z): # here is where we do math
    arm_reach = math.sqrt(y ** 2 + x ** 2)# determining distance from shoulder to wrist
    if arm_reach < d_one + d_two and arm_reach > d_one - d_two and y > -robot_height * multiplier:

        a_shoulder = math.acos((arm_reach ** 2 + d_one ** 2 - d_two ** 2) / (2 * d_one * arm_reach)) + math.atan2(y, x) #angle of shoulder

        xe = d_one * math.cos(a_shoulder)
        ye = d_one * math.sin(a_shoulder)

        ############################MAKE CHANGES HERE?######################
        try:
            ze = xe * z / x
        except:
            ze = 0
        ####################################################################

        return xe, ye, ze

    else:
        return False

    #update the screen
    pygame.display.flip()

def pos(x, y, z):
    x_change = y_change = z_change = 0
    gopen = gclose = 1
    #gopen = gclose = False

    if event.type == pygame.KEYDOWN:
        # what key are they pressing? move accordingly
        if event.key == pygame.K_ESCAPE:
            done = True
            return done

        elif event.key == pygame.K_a:
            x_change = -step

        elif event.key == pygame.K_d:
            x_change = step

        elif event.key == pygame.K_w:
            y_change = step

        elif event.key == pygame.K_s:
            y_change = -step

        elif event.key == pygame.K_q:
            z_change = -step

        elif event.key == pygame.K_e:
            z_change = step

        elif event.key == pygame.K_j:
            gopen = 0
            #gopen = False
        elif event.key == pygame.K_l:
            gclose = 0
            #gclose = False

    return x_change, y_change, z_change, gopen, gclose

# s.connect(('127.0.0.1', port))
# tests if you can connect
try:
    s.connect(('192.168.21.135', port))
    print("connection successful")
except:
    print("No connection")
    connect = False

#check for inputs
clock = pygame.time.Clock()

#loop to run and update the screen
while not done:
    clock.tick(60)
    # determine where want to be
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        else: # did something other than close
            try:
                x_change, y_change, z_change, gopen, gclose = pos(x, y, z) # figure out the change
            except:
                done = True

    # move the change amount
    x += x_change
    y += y_change
    z += z_change

    if z_change == 0:
        w = math.sqrt(abs(x ** 2 - z ** 2))
        if x < z:
            w = -w

    elif z_change != 0:
        if x < 0:
            x = -math.sqrt(w ** 2 + z ** 2)
        else:
            x = math.sqrt(w ** 2 + z ** 2)

    #set the screen circle's colorings depending on position
    if gopen == 0:
    #if gopen == False
        pygame.draw.circle(screen, red, (int(display_width / 2), 20), 10, 0)
    elif gclose == 0:
    #elif gclose == False
        pygame.draw.circle(screen, green, (int(display_width / 2), 20), 10, 0)
    else:
        pygame.draw.circle(screen, black, (int(display_width / 2), 20), 10, 0)

    if ik(x, y, z) != False:
        # determine elbow point
        xe, ye, ze = ik(x, y, z)

        we = math.sqrt(abs(xe ** 2 - ze ** 2))
        if xe < ze:
            we = -we
        ################CHANGE HERE###################

        #so Pygame can move and not reset the origins
        xo = x + originx; yo = originy - y; zo = toriginz + z
        xe = xe + originx; ye = originy - ye; ze = toriginz + ze

        # draw lines
######################################################
        pygame.draw.rect(screen, green, [originx - long_end * multiplier / 2, originy + holder_height * multiplier, robot_length * multiplier * abs(w / x) / 2, (robot_height - holder_height) * multiplier])
        pygame.draw.rect(screen, blue, [robot_length * multiplier * abs(w / x) / 2 + originx - long_end * multiplier / 2, originy + holder_height * multiplier, robot_width * multiplier * abs(z / x), (robot_height - holder_height) * multiplier])
        pygame.draw.rect(screen, green, [toriginz - robot_width * multiplier / 4, toriginw - (robot_length - long_end) * multiplier / 2, robot_width * multiplier / 2, robot_length * multiplier / 2])

        #pygame.draw.lines(screen, blue, False, [[originx,originy], [xe, ye], [xo, yo]], 5) # sideview
        pygame.draw.line(screen, blue, (xe, ye), [(xo), (yo)], 5)
        pygame.draw.line(screen, pink, (originx, originy), (xe, ye), 5)

        pygame.draw.line(screen, blue, (toriginz, toriginw), (zo, toriginw - w), 5)
        pygame.draw.line(screen, pink, (toriginz, toriginw), (ze, toriginw - we), 5)

    else: # if out of range
        pygame.draw.lines(screen, black, False, [[originx, originy], [xe, ye], [xo, yo]], 5)
        pygame.draw.line(screen, black, (toriginz, toriginw), (zo, toriginw - w), 5)
        #change the color of the robot to show it's hit
        pygame.draw.rect(screen, black, [originx - long_end * multiplier / 2, originy + holder_height * multiplier, robot_length * multiplier * abs(w / x) / 2, (robot_height - holder_height) * multiplier])
        pygame.draw.rect(screen, black, [robot_length * multiplier * abs(w / x) / 2 + originx - long_end * multiplier / 2, originy + holder_height * multiplier, robot_width * multiplier * abs(z / x), (robot_height - holder_height) * multiplier])
        pygame.draw.rect(screen, black, [toriginz - robot_width * multiplier / 4, toriginw - (robot_length - long_end) * multiplier / 2, robot_width * multiplier / 2, robot_length * multiplier / 2])
        #show where you are out of range
        pygame.draw.circle(screen, pink, (int(originx + x), int(originy - y)), 5, 0)
        pygame.draw.circle(screen, blue, (int(toriginz + z), int(toriginw - w)), 5, 0)
        #so the arm can't go out of range
        x -= x_change
        y -= y_change
        z -= z_change

    if connect == True:
        xyz = [x, y, z, gopen, gclose]
        data = pickle.dumps(xyz, protocol = 2)
        #output = 'Thank you for connecting'
        s.sendall(data)

    #s.send(xyz)

    # Be IDLE friendly
    pygame.display.update()
    screen.fill(grey)
    pygame.draw.circle(screen, white, (originx, originy), (d_one + d_two), 0)
    pygame.draw.circle(screen, grey, (originx, originy), (d_one - d_two), 0)
    # topview
    pygame.draw.circle(screen, white, (toriginz, toriginw), (d_one + d_two), 0)
    pygame.draw.circle(screen, grey, (toriginz, toriginw), (d_one - d_two), 0)
    pygame.draw.rect(screen, grey, [0, (originy + robot_height * multiplier), display_width / 2, display_width / 2])

#closes the imported files
s.close()
pygame.quit()
