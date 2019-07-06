from bsmLib import RPL
RPL.init()
import post_to_web as PTW

RPL.pinMode(1, RPL.INPUT)
RPL.analogRead(1)

frana = 1
rfana = 2
rbana = 3
brana = 4
blana = 5
lbana = 6
lfana = 7
flana = 8

while True:

    PTW.state['FRanalog'] = FRanalog
    PTW.state['BRanalog'] = BRanalog
    PTW.state['LFanalog'] = LFanalog
    PTW.state['FLanalog'] = FLanalog
    PTW.state['RFanalog'] = RFanalog
    PTW.state['BLanalog'] = BLanalog
    PTW.state['LBanalog'] = LBanalog
    PTW.state['RBanalog'] = RBanalog
    PTW.post()
