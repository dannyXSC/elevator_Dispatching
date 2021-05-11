from Global import *
from Elevator import Elevator
from Request import Request


class Elevator_Group():
    def __init__(self, l=min_Layer, n=default_Elevator_Number):
        self.list = [Elevator(l) for x in range(n)]
        self.wait_Queue = list()

    def step(self):
        for elevator in self.list:
            state = elevator.step()

    def distribute(self):
        pass

    def add_Request(self, request):
        self.wait_Queue.append(request)


if __name__ == '__main__':

    def test():
        return 1, 2, 3, 4

    a = []
    a = test()
    print(a, type(a))
