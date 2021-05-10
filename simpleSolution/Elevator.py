from Global import *
from Status import Status
from Task import Task


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
        except:
            raise Exception("Add Stop Task failure!")

    def step(self):
        if self.status.is_Run == False:
            # 停止状态
            pass
        elif self.status.state == 0:
            self.layer += 1


if __name__ == '__main__':
    print(2 | 1 << 1)
