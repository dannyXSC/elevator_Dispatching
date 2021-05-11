from Global import *
from Elevator import Elevator
from Request import Request


class Elevator_Group():
    def __init__(self, l=min_Layer, n=default_Elevator_Number):
        self.list = [Elevator(l) for x in range(n)]
        self.wait_Queue = list()

    def step(self):
        pass

    def distribute(self):
        pass

    def add_Request(self):
        pass


if __name__ == '__main__':
    print(default_Elevator_Number)
