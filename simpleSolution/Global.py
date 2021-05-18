# 单位时间
unit_Interval = 1
# 几个单位时间移动一层
velocity = 20
# 在每个楼层停留多少单位时间
waiting_Time = 20
# 最大楼层数
max_Layer = 20
# 最小楼层数 暂时不用 默认从1楼开始
min_Layer = 1
# 默认电梯数
default_Elevator_Number = 5
# 运行时电梯可召唤最小距离 # 暂时不用
min_Running_Distance = 2

# scale 变成标准大小的1/scale
scale = 2

# display setting
# screen
display_Screen_Bcolor = (0, 0, 0)

# Elevator
display_Elevator_Button_Font = 'Comic Sans MS'
display_Elevator_Button_Font_Size = 30 // scale
display_Elevator_Button_Font_Color = (255, 255, 255)
display_Elevator_Button_Font_Color_Active = (255, 0, 0)

display_Elevator_Button_Bcolor = (0, 0, 0)

display_Elevator_Button_Xstart = 500 // scale
display_Elevator_Button_Ystart = 600 // scale

display_Elevator_Button_Width = 50 // scale
display_Elevator_Button_Height = 50 // scale

display_Elevator_Button_Vmargin = 20 // scale
display_Elevator_Button_Hmargin = 20 // scale

display_elevator_Width = 50 // scale
display_elevator_Height = 50 // scale

# Elevator_Group
display_Elevator_Group_Bcolor = (255, 255, 255)

display_Elevator_Group_Elevator_Width = display_elevator_Width
display_Elevator_Group_Elevator_Height = display_elevator_Height

display_Elevator_Group_Floor_Width = display_Elevator_Group_Elevator_Width * 2
display_Elevator_Group_Floor_Height = display_Elevator_Group_Elevator_Height

display_Elevator_Group_Elevator_Button_Width = display_Elevator_Button_Width
display_Elevator_Group_Elevator_Button_Height = display_Elevator_Button_Height

display_Elevator_Group_Elevator_Button_Fcolor = (255, 255, 255)
display_Elevator_Group_Elevator_Button_Fcolor_Active = (255, 0, 0)
display_Elevator_Group_Elevator_Button_Bcolor = (0, 0, 0)

display_Elevator_Group_Elevator_Button_Hmargin = 20 // scale
display_Elevator_Group_Elevator_Button_Vmargin = 20 // scale

display_Elevator_Group_Elevator_Button_Group_Hmargin = 20 // scale

# Floor
display_Floor_Button_Width = display_Elevator_Group_Floor_Height // 2
display_Floor_Button_Height = display_Elevator_Group_Floor_Height // 2

display_Floor_Button_Hmargin = 10 // scale
display_Floor_Button_Vmargin = 10 // scale
