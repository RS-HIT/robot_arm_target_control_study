# 简历项目描述

## 1. 简历短版

基于 Python 搭建 2D 二连杆机械臂运动学控制与轨迹规划实验项目，实现正/逆运动学、雅可比伪逆控制、阻尼最小二乘和 resolved-rate 轨迹跟踪。

项目支持参数扫描、关节空间/笛卡尔空间轨迹对比、速度/加速度约束分析，并输出 CSV、曲线图和 pytest 测试结果。

## 2. 简历详细版

完成一个面向机器人算法入门的 2D 二连杆机械臂控制实验项目，使用 Python、NumPy、Matplotlib 和 pytest 实现正运动学、解析逆运动学、雅可比伪逆迭代控制、阻尼伪逆控制和 resolved-rate 轨迹跟踪。

项目通过参数敏感性实验分析 `gain`、`max_step`、`damping` 对目标点收敛、误差曲线和关节角平滑性的影响；对比关节空间轨迹与笛卡尔空间轨迹在末端路径、关节速度和关节加速度上的差异；进一步通过 `total_time` 重定时实验观察速度/加速度约束 violation 的变化。

项目包含命令行实验脚本、CSV 指标输出、Matplotlib 可视化图像和 pytest 自动测试，适合作为机器人运动学、数值 IK 和基础轨迹规划的学习展示项目。

## 3. 面试讲解版本

我做这个项目的目的是把机器人控制里比较抽象的概念变成一个能运行、能画图、能解释数据流的小实验。项目输入通常是目标点、轨迹类型或轨迹参数，程序先用正运动学计算当前末端位置，再根据解析逆运动学、雅可比伪逆或阻尼伪逆计算关节更新；在轨迹实验中，会先生成期望末端轨迹或关节轨迹，再用 resolved-rate 控制跟踪，并记录误差、关节角、速度、加速度和约束 violation。

通过实验我观察到，目标点控制不能只看最终误差，还要看误差曲线和关节角曲线；普通伪逆在奇异位形附近可能出现较大关节更新，阻尼伪逆能提高稳定性；关节空间轨迹通常关节运动更平滑，但末端路径不一定是直线；笛卡尔空间轨迹能更好控制末端路径，但可能带来更复杂的关节速度和加速度。当前项目仍然是 2D 运动学层面的学习实验，没有包含动力学、力矩、电机、摩擦、真实机械臂或 ROS/MuJoCo 仿真。

## 4. 技术关键词

- 中文：二连杆机械臂、正运动学、解析逆运动学、雅可比矩阵、雅可比伪逆、阻尼最小二乘、奇异位形、轨迹跟踪、轨迹规划、关节空间轨迹、笛卡尔空间轨迹、速度约束、加速度约束、参数敏感性实验。
- English: two-link planar robot arm, forward kinematics, inverse kinematics, Jacobian matrix, Jacobian pseudoinverse, damped least squares, singularity, resolved-rate control, trajectory tracking, trajectory planning, joint-space trajectory, Cartesian-space trajectory, velocity constraint, acceleration constraint, parameter sweep.
