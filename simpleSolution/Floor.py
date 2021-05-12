from Global import *


class Floor():
    def __init__(self, l=0, upState=False, downState=False):
        self.layer = l
        self.up_Button_State = upState
        self.down_Button_State = downState
