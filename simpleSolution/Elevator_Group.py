from Global import *
from Elevator import Elevator
from Request import Request


class Elevator_Group():
    def __init__(self, l=max_Layer, n=default_Elevator_Number):
        self.list = [Elevator(l) for x in range(n)]
        self.wait_Queue = list()

    def step(self):
        for elevator in self.list:
            state = elevator.step()


if __name__ == '__main__':
    r1 = Request(2, True)
    r2 = Request(1, True)
    myList = [r1, r2]
    print(myList)
    myList.remove(r1)
    print(myList)
