from os import X_OK
import pygame
from pygame import cursors

from Elevator import Elevator
from Global import *
from Elevator_Group import Elevator_Group
from Building import Building
from Request import Request


#######################################################################
#######################################################################
# 电梯组的显示
#######################################################################
#######################################################################
def Elevator_Group_Render(elevator_Number=default_Elevator_Number,
                          Layer_Number=max_Layer):
    pygame.init()
    pygame.font.init()

    #######################################################################
    # 设置屏幕
    #######################################################################
    screen_Width = elevator_Number * (
        display_Elevator_Group_Elevator_Width +
        (display_Elevator_Group_Elevator_Button_Hmargin +
         display_Elevator_Group_Elevator_Button_Width) * 3 +
        display_Elevator_Group_Elevator_Button_Group_Hmargin
    ) + display_Elevator_Group_Floor_Width + 100
    screen_Height = Layer_Number * display_Elevator_Group_Elevator_Height

    screen = pygame.display.set_mode((screen_Width, screen_Height))
    pygame.display.set_caption("Elevator Group")

    #######################################################################
    # 图片导入
    #######################################################################
    def load_img(path, size=None):
        img = pygame.image.load(path)
        if size == None:
            return img
        elif isinstance(size, tuple):
            return pygame.transform.scale(img, (size[0], size[1]))
        else:
            raise Exception("Invalid input!")

    icon = load_img(r'./img/smiling.png')
    elevatorImg = load_img(r'./img/elevator.png',
                           (display_Elevator_Group_Elevator_Width,
                            display_Elevator_Group_Elevator_Height))
    openedElevatorImg = load_img(r'./img/opened_Elevator.png',
                                 (display_Elevator_Group_Elevator_Width,
                                  display_Elevator_Group_Elevator_Height))

    pygame.display.set_icon(icon)

    #######################################################################
    # 文字导入
    #######################################################################
    def show_Text(content, x, y, fc, bc, w, h, size=30, font='Comic Sans MS'):
        myfont = pygame.font.SysFont(font, size)
        text = myfont.render(content, False, fc)
        text_surface = pygame.Surface((w, h))
        text_surface.fill(bc)
        startX = (w - text.get_size()[0]) / 2
        startY = (h - text.get_size()[1]) / 2
        text_surface.blit(text, (startX, startY))
        screen.blit(text_surface, (x, y))

    #######################################################################
    # 计算每个电梯的起始位置
    #######################################################################
    def calElevatorXstart(index):
        return display_Elevator_Group_Elevator_Width * index

    def calElevatorYstart(l):
        return screen_Height - (l * display_Elevator_Group_Elevator_Height)

    elevator_Pos_List = [(calElevatorXstart(i), calElevatorYstart(1))
                         for i in range(elevator_Number)]

    #######################################################################
    # 计算每个电梯的按钮的位置
    #######################################################################
    def calButtonGroupStartPos(x, y, index):
        return (x + index *
                ((display_Elevator_Group_Elevator_Button_Width +
                  display_Elevator_Group_Elevator_Button_Hmargin) * 3 +
                 display_Elevator_Group_Elevator_Button_Group_Hmargin), y)

    def calButtonPos(x, y, num):
        return (x + (num % 3) *
                (display_Elevator_Group_Elevator_Button_Width +
                 display_Elevator_Group_Elevator_Button_Hmargin), y -
                (num // 3) * (display_Elevator_Group_Elevator_Button_Width +
                              display_Elevator_Group_Elevator_Button_Hmargin))

    def calButtonGroupPos(x, y, index, totolNum):
        pos = list()
        (Xstart, Ystart) = calButtonGroupStartPos(x, y, index)
        for i in range(totolNum):
            pos.append(calButtonPos(Xstart, Ystart, i))
        return pos

    def calAllButtonGroupPos(x, y, totolNum):
        PosGroup = list()
        for i in range(elevator_Number):
            PosGroup.append(calButtonGroupPos(x, y, i, totolNum))
        return PosGroup

    def calOneAuxiliaryButtonGroupPos(x, y, index):
        pos = list()
        (Xstart, Ystart) = calButtonGroupStartPos(x, y, index)
        for i in range(3):
            pos.append(calButtonPos(Xstart, Ystart, i))
        return pos

    def calAuxiliaryButtonGroupPos(x, y):
        PosGroup = list()
        for i in range(elevator_Number):
            PosGroup.append(calOneAuxiliaryButtonGroupPos(x, y, i))
        return PosGroup

    ButtonStartX = display_Elevator_Group_Elevator_Width * \
        elevator_Number + display_Elevator_Group_Floor_Width + 50

    # 所有按钮的位置信息
    allNButtonGroupPos = calAllButtonGroupPos(
        ButtonStartX,
        screen_Height - (display_Elevator_Group_Elevator_Button_Height +
                         display_Elevator_Group_Elevator_Button_Vmargin) * 2,
        Layer_Number)

    auxiliaryButtonGroupPos = calAuxiliaryButtonGroupPos(
        ButtonStartX,
        screen_Height - display_Elevator_Group_Elevator_Button_Height -
        display_Elevator_Group_Elevator_Button_Vmargin)

    #######################################################################
    # 显示每个电梯的按钮的函数
    #######################################################################
    def showButton(content, x, y, is_Active):
        myfont = pygame.font.SysFont(display_Elevator_Button_Font,
                                     display_Elevator_Button_Font_Size)

        if is_Active:
            text = myfont.render(
                content, False,
                display_Elevator_Group_Elevator_Button_Fcolor_Active)
        else:
            text = myfont.render(
                content, False, display_Elevator_Group_Elevator_Button_Fcolor)
        text_surface = pygame.Surface(
            (display_Elevator_Group_Elevator_Button_Width,
             display_Elevator_Group_Elevator_Button_Height))

        text_surface.fill(display_Elevator_Group_Elevator_Button_Bcolor)

        startX = (display_Elevator_Group_Elevator_Button_Width -
                  text.get_size()[0]) / 2
        startY = (display_Elevator_Group_Elevator_Button_Height -
                  text.get_size()[1]) / 2
        text_surface.blit(text, (startX, startY))
        screen.blit(text_surface, (x, y))

    def showAuxiliaryButtonGroup():
        for groupPos in auxiliaryButtonGroupPos:
            showButton("><", groupPos[0][0], groupPos[0][1], False)
            showButton("<>", groupPos[1][0], groupPos[1][1], False)
            showButton("!", groupPos[2][0], groupPos[2][1], False)

    def showNumberButtonGroup(state):
        for i in range(elevator_Number):
            for j in range(Layer_Number):
                showButton(str(j + 1), allNButtonGroupPos[i][j][0],
                           allNButtonGroupPos[i][j][1], state[i][j])

    def showAllKindsOfButtonGroup(state):
        showAuxiliaryButtonGroup()
        showNumberButtonGroup(state)

    #######################################################################
    # 显示电梯
    #######################################################################
    elevatorGroupX = [
        i * display_Elevator_Group_Elevator_Width
        for i in range(elevator_Number)
    ]
    elevatorGroupY = [
        screen_Height - display_Elevator_Group_Elevator_Height
        for i in range(elevator_Number)
    ]

    def show_Elevator(x, y, state):
        if state == 0 or state == 1:
            screen.blit(elevatorImg, (x, y))
        else:
            screen.blit(openedElevatorImg, (x, y))

    def show_Elevator_Group(status_List):
        for i in range(elevator_Number):
            layer = status_List[i][0]
            state = status_List[i][1]
            direction = status_List[i][2]
            time = status_List[i][3]
            if state == 1:
                if direction == 1:
                    elevatorGroupY[i] = screen_Height - (
                        layer + (velocity - time) /
                        velocity) * display_Elevator_Group_Elevator_Height
                elif direction == 2:
                    elevatorGroupY[i] = screen_Height - (
                        layer - (velocity - time) /
                        velocity) * display_Elevator_Group_Elevator_Height
            show_Elevator(elevatorGroupX[i], elevatorGroupY[i], state)

    #######################################################################
    # 显示楼层
    #######################################################################
    def show_Floor():
        for i in range(Layer_Number):
            Xstart = elevator_Number * display_Elevator_Group_Elevator_Width
            Ystart = screen_Height - (
                i + 1) * display_Elevator_Group_Elevator_Height
            pygame.draw.line(
                screen, (0, 0, 0), (Xstart, Ystart),
                (Xstart + display_Elevator_Group_Floor_Width, Ystart))
            show_Text(str(i + 1),
                      Xstart + display_Elevator_Group_Floor_Width / 4,
                      Ystart + display_Elevator_Group_Floor_Height / 4,
                      (255, 255, 255), (0, 0, 0),
                      display_Elevator_Group_Floor_Width / 2,
                      display_Elevator_Group_Floor_Height / 2, 15)

    #######################################################################
    # run
    #######################################################################
    elevatorGroupHandle = Elevator_Group(Layer_Number, elevator_Number)
    running = True
    while running:
        screen.fill(display_Elevator_Group_Bcolor)
        elevatorGroupHandle.step()

        show_Elevator_Group([[
            elevatorHandle.layer, elevatorHandle.status.state,
            elevatorHandle.operation_Direction,
            elevatorHandle.status.remaining_Time
        ] for elevatorHandle in elevatorGroupHandle.list])
        showAllKindsOfButtonGroup([
            elevatorGroupHandle.list[i].get_Button_State()
            for i in range(elevator_Number)
        ])
        show_Floor()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursorsPos = event.pos

                def ifClickButton(cx, cy, bx, by):
                    if cx >= bx and cx <= bx + display_Elevator_Group_Elevator_Button_Width and cy >= by and cy <= by + display_Elevator_Group_Elevator_Button_Height:
                        return True
                    else:
                        return False

                for i in range(elevator_Number):
                    flag = 0
                    for j in range(Layer_Number):
                        if ifClickButton(cursorsPos[0], cursorsPos[1],
                                         allNButtonGroupPos[i][j][0],
                                         allNButtonGroupPos[i][j][1]):
                            elevatorGroupHandle.list[i].button_Click(j + 1)
                            flag = 1
                            break
                    if flag == 0:
                        if ifClickButton(cursorsPos[0], cursorsPos[1],
                                         auxiliaryButtonGroupPos[i][0][0],
                                         auxiliaryButtonGroupPos[i][0][1]):
                            elevatorGroupHandle.list[i].close_Click()
                            flag = 1
                        elif ifClickButton(cursorsPos[0], cursorsPos[1],
                                           auxiliaryButtonGroupPos[i][1][0],
                                           auxiliaryButtonGroupPos[i][1][1]):
                            elevatorGroupHandle.list[i].open_Click()
                            flag = 1
                        elif ifClickButton(cursorsPos[0], cursorsPos[1],
                                           auxiliaryButtonGroupPos[i][1][0],
                                           auxiliaryButtonGroupPos[i][1][1]):
                            elevatorGroupHandle.list[i].alarm_Click()
                            flag = 1
                    if flag == 1:
                        break

        pygame.display.update()


if __name__ == '__main__':
    Elevator_Group_Render()
