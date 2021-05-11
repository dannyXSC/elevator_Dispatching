from Global import *
from Status import Status
from Task import Task
from Request import Request


class Elevator():
    def __init__(self, l=min_Layer):
        self.layer = 1  # 初始在第一层
        self.operation_Direction = 0  # 无
        self.status = Status(0, 0)
        self.button = [False for x in range(max_Layer + 1)]
        self.stop_Task = dict()

    def add_Stop_Task(self, l, is_Out):
        if not isinstance(l, int) or not isinstance(is_Out, bool):
            raise Exception("Invalid input!")
        try:
            if l in self.stop_Task:
                if is_Out == True:
                    self.stop_Task[l] = self.stop_Task[l] | 1
                else:
                    self.stop_Task[l] = self.stop_Task[l] | (1 << 1)
            else:
                if is_Out == True:
                    self.stop_Task[l] = 1
                else:
                    self.stop_Task[l] = (1 << 1)
            self.status.state = 1
            self.status.remaining_Time = velocity
        except:
            raise Exception("Add Stop Task failure!")

    def call(self, l, is_Out):
        if not isinstance(l, int) or l < min_Layer or l > max_Layer:
            raise Exception("Invalid input!")
        try:
            if l == self.layer:
                self.status.state = 2
                self.status.remaining_Time = waiting_Time
                self.operation_Direction = 0
            elif l > self.layer:
                self.status.state = 1
                self.status.remaining_Time = velocity
                self.operation_Direction = 1
                self.add_Stop_Task(l, is_Out)
            else:
                self.status.state = 1
                self.status.remaining_Time = velocity
                self.operation_Direction = 2
                self.add_Stop_Task(l, is_Out)
        except:
            raise Exception("Call elevator failure!")

    def step(self):
        if self.status.state == 0:
            # 停止状态
            pass
        elif self.status.state == 1:
            # 运行状态
            self.status.remaining_Time -= 1
            if self.status.remaining_Time <= 0:
                if self.operation_Direction == 2:
                    self.layer -= 1
                elif self.operation_Direction == 1:
                    self.layer += 1
            #TODO: 更新状态 stop task   顶楼

        else:
            # 中停状态
            pass


if __name__ == '__main__':
    request = Request()
    print(isinstance(request, Request))
