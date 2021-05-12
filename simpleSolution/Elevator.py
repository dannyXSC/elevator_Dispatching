import time

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
        is_Arrive = False
        if self.status.state == 0:
            # 停止状态
            return self.status
        elif self.status.state == 1:
            # 运行状态
            self.status.remaining_Time -= 1
            if self.status.remaining_Time < 0:
                if self.operation_Direction == 2:
                    self.layer -= 1
                elif self.operation_Direction == 1:
                    self.layer += 1
                else:
                    raise Exception("Status error!")
                self.status.remaining_Time = velocity
                if self.layer in self.stop_Task:
                    if self.stop_Task[self.layer] & (1 << 1) != 0:
                        self.button[self.layer] = False
                    if self.stop_Task[self.layer] & 1 != 0:
                        is_Arrive = True
                    del self.stop_Task[self.layer]
                    self.status.state = 2
                    self.status.remaining_Time = waiting_Time
                    # operation_Direction不变
            else:
                # 如果时间没有流完，就什么都不干
                pass
        else:
            # 中停状态
            if self.layer in self.stop_Task:
                if self.stop_Task[self.layer] & (1 << 1) != 0:
                    self.button[self.layer] = False
                if self.stop_Task[self.layer] & 1 != 0:
                    is_Arrive = True
                del self.stop_Task[self.layer]
                self.status.state = 2
                self.status.remaining_Time = waiting_Time
            else:
                self.status.remaining_Time -= 1
                if self.status.remaining_Time < 0:
                    if self.can_Stop() == True:
                        # 进入停止状态
                        # 复位
                        self.status.state = 0
                        self.status.remaining_Time = 0
                        self.operation_Direction = 0
                        self.button_Restoration()
                        self.stop_Task = dict()
                    else:
                        # 进入运行状态
                        self.status.state = 1
                        self.status.remaining_Time = velocity
                else:
                    # 如果时间没有流完，就什么都不干
                    pass
        return is_Arrive

    def button_Restoration(self):
        size = len(self.button)
        for i in range(size):
            self.button[i] = False

    def can_Stop(self):
        if self.status.state == 0:
            return True
        elif self.status.state == 1:
            return False
        else:
            if self.operation_Direction == 0:
                return True
            elif self.operation_Direction == 1:
                if self.layer > max_Layer:
                    raise Exception("Layer error!")
                elif self.layer == max_Layer:
                    return True
                else:
                    for l in self.stop_Task:
                        if l >= self.layer:
                            return False
                    return True
            else:
                if self.layer < min_Layer:
                    raise Exception("Layer error!")
                elif self.layer == min_Layer:
                    return True
                else:
                    for l in self.stop_Task:
                        if l <= self.layer:
                            return False
                    return True

    def open_Click(self):
        if self.status.state == 1:
            # 如果正在运行，就什么都不干
            pass
        else:
            # 如果停止状态
            self.status.state = 2
            self.status.remaining_Time = waiting_Time

    def close_Click(self):
        if self.status.state == 1 or self.status.state == 0:
            # 如果正在运行，就什么都不干
            pass
        else:
            # 如果中停状态
            self.status.remaining_Time = 0

    def button_Click(self, l):
        if not isinstance(l, int) or l < min_Layer or l > max_Layer:
            raise Exception("Invalid input!")
        else:
            self.button[l] = True
            if self.status.state == 0:
                self.call(l, False)
            elif self.can_Add_Task(l):
                self.add_Stop_Task(l, False)
            else:
                pass

    def alarm_Click(self):
        pass

    def can_Add_Task(self, l, direction=None):
        if direction == None:
            if not isinstance(l, int) or l < min_Layer or l > max_Layer:
                raise Exception("Invalid input!")
            if l in self.stop_Task:
                return False
            if self.status.state == 0:
                return True
            elif self.status.state == 2:
                if self.operation_Direction == 0 or (
                        self.operation_Direction == 1
                        and l >= self.layer) or (self.operation_Direction == 2
                                                 and l <= self.layer):
                    return True
                else:
                    return False
            else:
                if self.operation_Direction == 1:
                    if l >= self.layer + min_Running_Distance:
                        return True
                    else:
                        return False
                elif self.operation_Direction == 2:
                    if l <= self.layer - min_Running_Distance:
                        return True
                    else:
                        return False
                else:
                    # When operation_Direction == 0, self.status.state == 0
                    raise Exception("Error!")
        else:
            # direction 1 向上 2向下
            if not isinstance(l, int) or l < min_Layer or l > max_Layer:
                raise Exception("Invalid input!")
            if self.status.state == 0:
                return True
            elif self.status.state == 2:
                if self.operation_Direction == 0 or (
                        self.operation_Direction == 1 and l >= self.layer
                        and direction == 1) or (self.operation_Direction == 2
                                                and l <= self.layer
                                                and direction == 2):
                    return True
                else:
                    return False
            else:
                if self.operation_Direction == 1 and direction == 1:
                    if l >= self.layer + min_Running_Distance:
                        return True
                    else:
                        return False
                elif self.operation_Direction == 2 and direction == 2:
                    if l <= self.layer - min_Running_Distance:
                        return True
                    else:
                        return False
                else:
                    return False

    def get_Button_State(self):
        return self.button[1:]


if __name__ == '__main__':
    import time
    elevator = Elevator()
    elevator.button_Click(5)
    for i in range(20):
        if i == 10:
            elevator.button_Click(1)
        if i == 5:
            elevator.close_Click()
        elevator.step()
        print(elevator.layer, elevator.status.state)
        time.sleep(unit_Interval)
