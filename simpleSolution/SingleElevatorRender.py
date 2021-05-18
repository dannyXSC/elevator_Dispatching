from os import X_OK
import pygame
from pygame import cursors

from Elevator import Elevator
from Global import *
from Elevator_Group import Elevator_Group
from Building import Building
from Request import Request


def Single_Elevator_Render():
    pygame.init()
    pygame.font.init()

    screen_Width = 800
    screen_Height = max_Layer * display_elevator_Height
    screen = pygame.display.set_mode((screen_Width, screen_Height))
    pygame.display.set_caption("Elevator")
    icon = pygame.image.load(r'./img/smiling.png')
    pygame.display.set_icon(icon)

    elevatorImg = pygame.image.load(r'./img/elevator.png')
    openedElevatorImg = pygame.image.load(r'./img/opened_Elevator.png')
    elevatorImg = pygame.transform.scale(
        elevatorImg, (display_elevator_Width, display_elevator_Height))
    openedElevatorImg = pygame.transform.scale(
        openedElevatorImg, (display_elevator_Width, display_elevator_Height))

    elevatorHandle = Elevator()

    elevatorX = 0
    elevatorY = screen_Height - (
        display_elevator_Height +
        (elevatorHandle.layer - 1) * display_Elevator_Button_Height)

    def get_Button_Pos(num):
        pos = list()
        for i in range(num):
            tempX = display_Elevator_Button_Xstart + (
                i % 3) * (display_Elevator_Button_Width +
                          display_Elevator_Button_Hmargin)
            tempY = display_Elevator_Button_Ystart - (
                i // 3) * (display_Elevator_Button_Height +
                           display_Elevator_Button_Vmargin)
            pos.append((tempX, tempY))
        return pos

    def show_Elevator(x, y, state):
        if state == 0 or state == 1:
            screen.blit(elevatorImg, (x, y))
        else:
            screen.blit(openedElevatorImg, (x, y))

    def show_Text(content, x, y, fc, bc, w, h, size=30, font='Comic Sans MS'):
        myfont = pygame.font.SysFont(font, size)
        text = myfont.render(content, False, fc)
        text_surface = pygame.Surface((w, h))
        text_surface.fill(bc)
        startX = (w - text.get_size()[0]) / 2
        startY = (h - text.get_size()[1]) / 2
        text_surface.blit(text, (startX, startY))
        screen.blit(text_surface, (x, y))

    def show_Floor():
        for i in range(max_Layer):
            Y = screen_Height - (display_elevator_Height +
                                 i * display_elevator_Height)
            pygame.draw.line(screen, (0, 0, 0), (display_elevator_Width, Y),
                             (200, Y))
            show_Text(str(i + 1), display_elevator_Width * 2,
                      Y + display_elevator_Height / 4, (255, 255, 255),
                      (0, 0, 0), display_elevator_Height / 2,
                      display_elevator_Height / 2, 15)

    def show_Button(content, x, y, is_Active):
        myfont = pygame.font.SysFont(display_Elevator_Button_Font,
                                     display_Elevator_Button_Font_Size)
        if is_Active:
            text = myfont.render(content, False,
                                 display_Elevator_Button_Font_Color_Active)
        else:
            text = myfont.render(content, False,
                                 display_Elevator_Button_Font_Color)
        text_surface = pygame.Surface(
            (display_Elevator_Button_Width, display_Elevator_Button_Height))

        text_surface.fill(display_Elevator_Button_Bcolor)

        startX = (display_Elevator_Button_Width - text.get_size()[0]) / 2
        startY = (display_Elevator_Button_Height - text.get_size()[1]) / 2
        text_surface.blit(text, (startX, startY))
        screen.blit(text_surface, (x, y))

    def show_A_Button(x, y, state):
        show_Button("><", x, y, state[0])
        show_Button(
            "<>", x + display_Elevator_Button_Width +
            display_Elevator_Button_Hmargin, y, state[1])
        show_Button(
            "!", x + 2 *
            (display_Elevator_Button_Width + display_Elevator_Button_Hmargin),
            y, state[2])

    def show_Button_Group(state):
        if isinstance(state, list):
            num = len(state)
            for i in range(num):
                show_Button(str(i + 1), button_Pos[i][0], button_Pos[i][1],
                            state[i])

    button_Pos = get_Button_Pos(max_Layer)
    close_Button_Pos = (display_Elevator_Button_Xstart,
                        display_Elevator_Button_Ystart +
                        display_Elevator_Button_Height +
                        display_Elevator_Button_Vmargin)
    open_Button_Pos = (display_Elevator_Button_Xstart +
                       display_Elevator_Button_Width +
                       display_Elevator_Button_Hmargin,
                       display_Elevator_Button_Ystart +
                       display_Elevator_Button_Height +
                       display_Elevator_Button_Vmargin)
    alarm_Button_Pos = (
        display_Elevator_Button_Xstart +
        (display_Elevator_Button_Width + display_Elevator_Button_Hmargin) * 2,
        display_Elevator_Button_Ystart + display_Elevator_Button_Height +
        display_Elevator_Button_Vmargin)

    # run
    running = True
    while running:
        # screen
        screen.fill((255, 255, 255))

        elevatorHandle.step()

        if elevatorHandle.status.state == 1:
            if elevatorHandle.operation_Direction == 1:
                elevatorY = screen_Height - (
                    display_elevator_Height +
                    (elevatorHandle.layer - 1) * display_elevator_Height +
                    (display_elevator_Height *
                     (velocity - elevatorHandle.status.remaining_Time) /
                     velocity))
            elif elevatorHandle.operation_Direction == 2:
                elevatorY = screen_Height - (
                    display_elevator_Height +
                    (elevatorHandle.layer - 1) * display_elevator_Height -
                    (display_elevator_Height *
                     (velocity - elevatorHandle.status.remaining_Time) /
                     velocity))
        show_Elevator(elevatorX, elevatorY, elevatorHandle.status.state)
        show_Button_Group(
            [elevatorHandle.button[i] for i in range(1, max_Layer + 1)])
        show_A_Button(
            display_Elevator_Button_Xstart, display_Elevator_Button_Ystart +
            display_Elevator_Button_Vmargin + display_Elevator_Button_Height,
            [0, 0, 0])
        show_Floor()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursorPos = event.pos
                flag = 0
                for i in range(max_Layer):
                    if cursorPos[0] >= button_Pos[i][0] and cursorPos[
                            0] <= button_Pos[i][
                                0] + display_Elevator_Button_Width and cursorPos[
                                    1] >= button_Pos[i][1] and cursorPos[
                                        1] <= button_Pos[i][
                                            1] + display_Elevator_Button_Height:
                        elevatorHandle.button_Click(i + 1)
                        flag = 1
                        break
                if flag == 0:
                    if cursorPos[0] >= close_Button_Pos[0] and cursorPos[
                            0] <= close_Button_Pos[
                                0] + display_Elevator_Button_Width and cursorPos[
                                    1] >= close_Button_Pos[1] and cursorPos[
                                        1] <= close_Button_Pos[
                                            1] + display_Elevator_Button_Height:
                        elevatorHandle.close_Click()
                    elif cursorPos[0] >= open_Button_Pos[0] and cursorPos[
                            0] <= open_Button_Pos[
                                0] + display_Elevator_Button_Width and cursorPos[
                                    1] >= open_Button_Pos[1] and cursorPos[
                                        1] <= open_Button_Pos[
                                            1] + display_Elevator_Button_Height:
                        elevatorHandle.open_Click()
                    elif cursorPos[0] >= alarm_Button_Pos[0] and cursorPos[
                            0] <= alarm_Button_Pos[
                                0] + display_Elevator_Button_Width and cursorPos[
                                    1] >= alarm_Button_Pos[1] and cursorPos[
                                        1] <= alarm_Button_Pos[
                                            1] + display_Elevator_Button_Height:
                        elevatorHandle.alarm_Click()

        pygame.display.update()


if __name__ == '__main__':
    Single_Elevator_Render()
