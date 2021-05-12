from Global import *
from Floor import Floor
from Elevator_Group import Elevator_Group


class Building():
    def __init__(self, layer_Number=max_Layer, n=default_Elevator_Number):
        self.layers = [Floor(i) for i in range(layer_Number)]
        self.elevators = Elevator_Group(layer_Number, n)

    def step(self):
        self.distribute()
        for elevator in self.elevators.list:
            state = elevator.step()
            if state == True:
                if elevator.operation_Direction == 1:
                    self.layers[elevator.layer - 1].up_Button_State = False
                elif elevator.operation_Direction == 2:
                    self.layers[elevator.layer - 1].down_Button_State = False
                else:
                    # TODO: 如果在同一层按的按钮怎么办
                    pass

    def distribute(self):
        # 从所有的等待队列中，选出
        complete_List = list()
        size = len(self.elevators.wait_Queue)
        picked = [False for i in range(size)]
        for i in range(size):
            layer = self.elevators.wait_Queue[i].layer
            is_Up = self.elevators.wait_Queue[i].is_Up
            direction = 1 if is_Up == True else 2
            for elevator in self.elevators.list:
                if picked[i] == False and elevator.can_Add_Task(
                        layer, direction):
                    if elevator.status.state == 0:
                        elevator.call(layer, True)
                    else:
                        elevator.add_Stop_Task(layer, True)
                    complete_List.append(self.elevators.wait_Queue[i])
                    picked[i] = True

        try:
            for complete in complete_List:
                if complete in self.elevators.wait_Queue:
                    self.elevators.wait_Queue.remove(complete)
        except:
            raise Exception("Distribute error!")

    def add_Request(self, request):
        # 暂时的请求都按到来的顺序存在list中
        self.elevators.wait_Queue.append(request)