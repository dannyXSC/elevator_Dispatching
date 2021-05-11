import pygame
from pygame import cursors

from Elevator import Elevator
from Global import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Elevator")
icon = pygame.image.load(
    r'D:\Project\elevator_Dispatching\test\pygame\img\smiling.png')
pygame.display.set_icon(icon)

elevatorImg = pygame.image.load(
    r'D:\Project\elevator_Dispatching\test\pygame\img\elevator.png')
openedElevatorImg = pygame.image.load(
    r'D:\Project\elevator_Dispatching\test\pygame\img\opened_Elevator.png')
elevator_Width = 50
elevator_Height = 50
elevatorImg = pygame.transform.scale(elevatorImg,
                                     (elevator_Width, elevator_Height))
openedElevatorImg = pygame.transform.scale(openedElevatorImg,
                                           (elevator_Width, elevator_Height))

elevatorHandle = Elevator()

elevatorX = 0
elevatorY = (elevatorHandle.layer - 1) * 20


def get_Button_Pos(num):
    pos = list()
    for i in range(num):
        tempX = display_Elevator_Button_Xstart + (i % 3) * (
            display_Elevator_Button_Width + display_Elevator_Button_Hmargin)
        tempY = display_Elevator_Button_Ystart - (i // 3) * (
            display_Elevator_Button_Height + display_Elevator_Button_Vmargin)
        pos.append((tempX, tempY))
    return pos


button_Pos = get_Button_Pos(max_Layer)


def show_Elevator(x, y):
    screen.blit(elevatorImg, (x, y))


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


def show_Button_Group(state):
    if isinstance(state, list):
        num = len(state)
        for i in range(num):
            show_Button(str(i + 1), button_Pos[i][0], button_Pos[i][1],
                        state[i])


# run
running = True
while running:
    # screen
    screen.fill((255, 255, 255))

    elevatorHandle.step()
    print(elevatorHandle.layer, elevatorHandle.status.state)

    if elevatorHandle.status.state == 1:
        if elevatorHandle.operation_Direction == 1:
            elevatorY = (elevatorHandle.layer - 1) * 20 + (
                20 *
                (velocity - elevatorHandle.status.remaining_Time) / velocity)
        elif elevatorHandle.operation_Direction == 2:
            elevatorY = (elevatorHandle.layer - 1) * 20 - (
                20 *
                (velocity - elevatorHandle.status.remaining_Time) / velocity)
    show_Elevator(elevatorX, elevatorY)
    show_Button_Group(
        [elevatorHandle.button[i] for i in range(1, max_Layer + 1)])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cursorPos = event.pos
            for i in range(max_Layer):
                if cursorPos[0] >= button_Pos[i][0] and cursorPos[
                        0] <= button_Pos[i][
                            0] + display_Elevator_Button_Width and cursorPos[
                                1] >= button_Pos[i][1] and cursorPos[
                                    1] <= button_Pos[i][
                                        1] + display_Elevator_Button_Height:
                    elevatorHandle.button_Click(i + 1)

    pygame.display.update()