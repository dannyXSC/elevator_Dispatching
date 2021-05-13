from Request import Request
from Global import *
from Floor import Floor
from Elevator_Group import Elevator_Group


class Building():
    def __init__(self, layer_Number=max_Layer, n=default_Elevator_Number):
        self.elevator_Number = n
        self.layers = [Floor(i) for i in range(layer_Number)]
        self.elevators = Elevator_Group(layer_Number, n)
        self.qualification = dict()
        # self.rigister = dict()

    def step(self):
        self.distribute()
        for elevator in self.elevators.list:
            request = elevator.step()
            if isinstance(request, Request):
                if request.is_Up == True:
                    self.layers[request.layer - 1].up_Button_State = False
                else:
                    self.layers[request.layer - 1].down_Button_State = False
                # if elevator.operation_Direction == 1:
                #     self.layers[elevator.layer - 1].up_Button_State = False
                # elif elevator.operation_Direction == 2:
                #     self.layers[elevator.layer - 1].down_Button_State = False
                # else:
                #     #
                #     pass

    def distribute(self):
        # 从所有的等待队列中，选出
        complete_List = list()
        size = len(self.elevators.wait_Queue)
        picked = [False for i in range(size)]
        for i in range(size):
            layer = self.elevators.wait_Queue[i].layer
            is_Up = self.elevators.wait_Queue[i].is_Up
            direction = 1 if is_Up == True else 2
            for j in range(self.elevator_Number):
                if self.elevators.list[j].can_Add_Task(layer, direction):
                    if i not in self.qualification:
                        self.qualification[i] = [j]
                    else:
                        self.qualification[i].append(j)
        for request in self.qualification:
            request_Layer = self.elevators.wait_Queue[request].layer
            minDistance = len(self.layers)+5
            pick_Elevator = -1
            for j in range(self.elevator_Number):
                if abs(request_Layer-self.elevators.list[j].layer) < minDistance:
                    minDistance = abs(
                        request_Layer-self.elevators.list[j].layer)
                    pick_Elevator = j
            if pick_Elevator < 0:
                raise Exception("Error!")
            complete_List.append(self.elevators.wait_Queue[request])
            # self.rigister[self.elevators.wait_Queue[request]] = pick_Elevator
            if self.elevators.list[pick_Elevator].status.state == 0:
                self.elevators.list[pick_Elevator].call(layer, True,
                                                        self.elevators.wait_Queue[request])
            else:
                self.elevators.list[pick_Elevator].add_Stop_Task(layer, True,
                                                                 self.elevators.wait_Queue[request])
        self.qualification = dict()
        try:
            for complete in complete_List:
                if complete in self.elevators.wait_Queue:
                    self.elevators.wait_Queue.remove(complete)
        except:
            raise Exception("Distribute error!")

    def add_Request(self, request):
        # 暂时的请求都按到来的顺序存在list中
        if request not in self.elevators.wait_Queue:
            self.elevators.wait_Queue.append(request)
