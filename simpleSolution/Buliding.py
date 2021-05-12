from Global import *
from Floor import Floor
from Elevator_Group import Elevator_Group


class Building():
    def __init__(self, layer_Number=max_Layer, n=default_Elevator_Number):
        self.layers = [Floor(i) for i in range(layer_Number)]
        self.elevators = Elevator_Group(layer_Number, n)