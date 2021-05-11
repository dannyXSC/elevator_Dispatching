from Global import *
from Floor import Floor
from Elevator_Group import Elevator_Group


class Building():
    def __init__(self,
                 minL=min_Layer,
                 maxL=max_Layer,
                 n=default_Elevator_Number):
        self.layers = [Floor(i) for i in range(minL, maxL + 1)]
        self.elevators = Elevator_Group(minL, n)

    def run():
        pass