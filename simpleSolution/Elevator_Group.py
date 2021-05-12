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
        # 从所有的等待队列中，选出
        complete_List = list()
        for request in self.wait_Queue:
            layer = request.layer
            is_Up = request.is_Up
            direction = 1 if is_Up == True else 2
            for elevator in self.list:
                if elevator.can_Add_Task(layer, direction):
                    if elevator.status.state == 0:
                        elevator.call(layer, True)
                    else:
                        elevator.add_Stop_Task(layer, True)
                    complete_List.append(request)
        try:
            for complete in complete_List:
                self.wait_Queue.remove(complete)
        except:
            raise Exception("Distribute error!")

    def add_Request(self, request):
        # 暂时的请求都按到来的顺序存在list中
        self.wait_Queue.append(request)


if __name__ == '__main__':
    r1 = Request(2, True)
    r2 = Request(1, True)
    myList = [r1, r2]
    print(myList)
    myList.remove(r1)
    print(myList)
