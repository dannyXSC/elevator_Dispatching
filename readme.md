# Read Me

1. 运行方式
```
cd simpleSolution
python Render.py
```


2. 代码功能概括
   > Render.py
   > 图形化界面

   > Global.py
   > 存全局变量的部分
   > ==可能在1k屏上我设置的大小有点大，请根据需求调Global.py中的scale参数==
   > 可通过调整velocity来改变电梯移动速度
   > 可通过调整waiting_Time来改变电梯
   > 可通过调整max_Layer来改变楼层数
   > 可通过调整default_Elevator_Number来改变电梯数量

3. 调度逻辑
   > 暂时实现的是比较简单的调度方法，即每次给每个任务分配离他最近的电梯
   > 未来有机会想通过中断方式设计更好的调度方法，但是最近比较忙，就算了，做一个比较简单的调度吧