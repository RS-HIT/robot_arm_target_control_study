# 第五阶段学习指示：轨迹规划、时间缩放与轨迹空间对比

## 1. 本阶段学习目标

本阶段目标是理解“轨迹规划”和“轨迹跟踪”的区别，并比较关节空间轨迹与笛卡尔空间轨迹的不同表现。

学完后你应该能解释：

- 为什么关节空间插值时，末端不一定走直线。
- 为什么末端走直线时，关节速度和加速度可能更复杂。
- 为什么真实机械臂不仅需要位置点，还要关心速度和加速度。

## 2. 轨迹规划和轨迹跟踪的区别

轨迹规划是先设计一条希望执行的轨迹，例如一串关节角或一串末端位置。

轨迹跟踪是用控制器让机械臂尽量沿着这条轨迹运动。

可以简单理解为：

```text
轨迹规划：先想好路
轨迹跟踪：沿着路走
```

## 3. 关节空间轨迹是什么

关节空间轨迹直接在 `theta1`、`theta2` 上规划。

例如从：

```text
start_theta -> goal_theta
```

用 linear、cubic 或 quintic 方法插值，得到一串关节角。

优点是关节角曲线容易做得平滑。缺点是末端路径由正运动学间接决定，不一定是直线。

## 4. 笛卡尔空间轨迹是什么

笛卡尔空间轨迹直接在末端坐标 `x/y` 上规划。

例如从：

```text
start_xy -> goal_xy
```

生成一条末端直线，再用 resolved-rate 控制跟踪它。

优点是末端路径更直观。缺点是为了让末端走直线，关节可能需要做更复杂的速度和加速度变化。

## 5. 为什么关节空间插值时末端不一定走直线

机械臂正运动学是非线性的。即使 `theta1` 和 `theta2` 平滑变化，末端 `x/y` 位置也不一定沿直线变化。

这就是为什么关节空间轨迹看起来关节很平滑，但末端路径可能弯曲。

## 6. 为什么笛卡尔空间轨迹可能导致关节运动更复杂

如果要求末端严格沿直线运动，控制器需要不断调整两个关节配合。某些位置附近，关节角可能变化更快，速度和加速度也可能更大。

所以笛卡尔空间轨迹更关注末端效果，但不一定让关节运动最简单。

## 7. 什么是时间缩放 s(t)

`s(t)` 可以理解为从 0 到 1 的进度条。

```text
theta(t) = start_theta + s(t) * (goal_theta - start_theta)
```

当 `s=0` 时在起点，当 `s=1` 时在终点。不同的 `s(t)` 会决定中间运动是否平滑。

## 8. linear、cubic、quintic 的区别

- `linear`：匀速插值，简单，但起点和终点速度会突然变化。
- `cubic`：三次时间缩放，起点和终点速度为 0。
- `quintic`：五次时间缩放，起点和终点速度、加速度都更平滑。

## 9. 为什么速度和加速度曲线很重要

真实机械臂不能只看位置点。

- 速度过大：关节可能跟不上。
- 加速度过大：动作突然，可能对电机和结构不友好。
- 加速度 RMS 较大：整体运动可能更“费劲”或更不平滑。

因此第五阶段不仅看路径，还看关节速度和关节加速度。

## 10. 本阶段新增文件

- `scripts/run_trajectory_space_compare.py`
- `docs/11_stage5_trajectory_planning_guide.md`
- `docs/12_trajectory_planning_notes.md`

本阶段还扩展了：

- `src/robot_arm_target_control_study/trajectory.py`
- `src/robot_arm_target_control_study/plotting.py`
- `tests/test_trajectory.py`

## 11. 推荐阅读顺序

1. 读 `trajectory.py` 中的时间缩放和关节空间轨迹函数。
2. 读 `scripts/run_trajectory_space_compare.py`。
3. 运行对比脚本，查看终端指标和 CSV。
4. 打开四张对比图，比较路径、关节角、速度和加速度。
5. 再读 `docs/12_trajectory_planning_notes.md`。

## 12. 验收命令

```bash
python scripts/run_trajectory_space_compare.py
python scripts/run_trajectory_space_compare.py --method linear
python scripts/run_trajectory_space_compare.py --method cubic
python scripts/run_trajectory_space_compare.py --method quintic
pytest
```

## 13. 本阶段可以写进简历的内容

可以写：

> 在 2D 二连杆机械臂项目中实现关节空间轨迹规划、linear/cubic/quintic 时间缩放、笛卡尔空间轨迹跟踪对比，并分析关节速度、加速度和路径误差指标。
