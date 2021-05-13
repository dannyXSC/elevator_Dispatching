from Request import Request
from Global import *
from Floor import Floor
from Elevator_Group import Elevator_Group


class Building():
    def __init__(self, layer_Number=max_Layer, n=default_Elevator_Number):
        self.layers = [Floor(i) for i in range(layer_Number)]
        self.elevators = Elevator_Group(layer_Number, n)
        self.solving_Request = list()

    def step(self):
        self.distribute()
        for elevator in self.elevators.list:
            request = elevator.step()
            if isinstance(request, Request):
                if request.is_Up == True:
                    self.layers[request.layer - 1].up_Button_State = False
                else:
                    self.layers[request.layer - 1].down_Button_State = False
                if request in self.solving_Request:
                    self.solving_Request.remove(request)
                else:
                    raise Exception("Error!")
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
            picked_Elevator = -1
            min_Distance = len(self.layers)+5
            # for elevator in self.elevators.list:
            for j in range(len(self.elevators.list)):
                if picked[i] == False and self.elevators.list[j].can_Add_Task(
                        layer, direction):
                    if min_Distance >= abs(self.elevators.list[j].layer-layer):
                        picked_Elevator = j
                        min_Distance = abs(self.elevators.list[j].layer-layer)
            if picked_Elevator != -1:
                if self.elevators.list[picked_Elevator].status.state == 0:
                    self.elevators.list[picked_Elevator].call(layer, True,
                                                              self.elevators.wait_Queue[i])
                else:
                    self.elevators.list[picked_Elevator].add_Stop_Task(layer, True,
                                                                       self.elevators.wait_Queue[i])
                complete_List.append(self.elevators.wait_Queue[i])
                self.solving_Request.append(self.elevators.wait_Queue[i])
                picked[i] = True

        try:
            for complete in complete_List:
                if complete in self.elevators.wait_Queue:
                    self.elevators.wait_Queue.remove(complete)
        except:
            raise Exception("Distribute error!")

    def add_Request(self, request):
        # 暂时的请求都按到来的顺序存在list中
        if request not in self.elevators.wait_Queue and request not in self.solving_Request:
            self.elevators.wait_Queue.append(request)
