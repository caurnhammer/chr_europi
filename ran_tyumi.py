# Christoph Aurnhammer, 2023
# MIT License
# Send trigger to analogue input to get 6 random voltages (0 - 10 Volt).
# Global range can be controlled via knob 1 (minimum) and knob 2 (maximum).
# Press button 2 to hold voltages.
# Press button 1 while holding button 2 to trigger manually.

from europi import *
from europi_script import EuroPiScript
from random import uniform
from machine import freq

class OledWrapper:
    def __init__(self):
        oled.fill(0)
        self.is_inverted = False
        
    def toggle_invert(self):
        if self.is_inverted == False:
            oled.invert(1)
            self.is_inverted = True
        else:
            oled.invert(0)
            self.is_inverted = False

    def han_tyumi(self):
        oled.contrast(0)
        # Neck
        oled.vline(60, 29, 2, 1)
        oled.vline(66, 29, 2, 1)
        # Mouth
        oled.rect(54, 22, 19, 7, 1)
        oled.hline(54, 24, 19, 1)
        oled.hline(54, 26, 19, 1)
        # Head
        oled.rect(33, 13, 60, 10, 1)
        # Eyes
        oled.rect(53-8, 15, 8, 4, 1)
        oled.rect(73, 15, 8, 4, 1)
        # Brain
        ## Hemisphere cut
        oled.vline(62, 1, 13, 1)
        oled.vline(64, 1, 13, 1) 
        # Top lines
        oled.hline(53, 1, 9, 1)
        oled.hline(65, 1, 8, 1)
        oled.vline(53, 1, 5, 1)
        oled.vline(65+8, 1, 5, 1)
        # mid lines
        oled.hline(55-9, 5, 8, 1)
        oled.hline(65+8, 5, 8, 1)
        oled.vline(55-10, 5, 5, 1)
        oled.vline(65+16, 5, 5, 1)
        # low line
        oled.hline(55-18, 9, 8, 1)
        oled.hline(65+16, 9, 8, 1)
        oled.vline(55-18, 9, 5, 1)
        oled.vline(65+24, 9, 5, 1)
         
        oled.show()

class RanTyumi(EuroPiScript):
    def __init__(self):
        self.my_oled = OledWrapper()

    def step(self, volt, state):
        if (state == 0) & (volt >= 0.4): # new rising edge: new values
            [cv.voltage(uniform(k1.read_position()/10, k2.read_position()/10)) for cv in cvs]
            self.my_oled.toggle_invert()
            return 1
        elif (state == 1) & (volt < 0.4): # new falling edge
            return 0
        else:
            return state

    def main(self):
        freq(250_000_000)
    
        self.my_oled.han_tyumi()
        
        state = 0
        while True:
            if b2.value() == 1:
                state = self.step(b1.value(), state)
            else:
                state = self.step(ain.read_voltage() / 10, state)

if __name__ == "__main__":
    rantyumi = RanTyumi()
    rantyumi.main()
