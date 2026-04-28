# 代码阅读笔记：项目数据流

这份笔记适合在读完整体代码前快速建立项目运行流程的概念。

## 1. 总体数据流

```text
命令行输入目标点
-> 控制器迭代
-> 正运动学计算末端位置
-> 记录误差
-> 输出图像
```

对应到代码中：

- `scripts/run_reach_demo.py`：读取 `--target_x` 和 `--target_y`，把用户输入转换成目标点。
- `simulation.py`：运行迭代循环，保存每一步的关节角、末端位置和误差。
- `kinematics.py`：用正运动学计算当前机械臂的基座、肘关节和末端位置。
- `controller.py`：用雅可比伪逆根据末端误差计算关节角更新量。
- `plotting.py`：把最终姿态、误差曲线和关节角曲线保存为图片。

## 2. 一次迭代里发生什么

每一轮仿真主要做五件事：

1. 根据当前 `theta1`、`theta2` 调用正运动学，得到末端位置。
2. 计算目标点和末端点之间的误差。
3. 把当前关节角、末端位置和误差记录到 `history`。
4. 如果误差小于阈值，就认为已经到达目标附近。
5. 如果还没到，就用雅可比伪逆计算关节角更新量，并进入下一轮。

## 3. 推荐阅读顺序

建议按下面顺序读：

1. `scripts/run_reach_demo.py`：先看用户入口。
2. `src/robot_arm_target_control_study/simulation.py`：理解主循环。
3. `src/robot_arm_target_control_study/kinematics.py`：理解正运动学和雅可比矩阵。
4. `src/robot_arm_target_control_study/controller.py`：理解雅可比伪逆控制。
5. `src/robot_arm_target_control_study/plotting.py`：理解结果如何输出。
