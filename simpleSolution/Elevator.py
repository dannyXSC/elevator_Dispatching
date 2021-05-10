from Global import *
from Status import Status


class Elevator():
    def __init__(self):
        self.layer = 1  # 初始在第一层
        self.target_Layer = 0  # 无
        self.status = Status(0, 0, 0)
        self.stop_Queue = list()

    def step(self):
        if self.status.is_Run == False:
            # 停止状态
            pass
        elif self.status.state == 0:
            self.layer += 1
