# 第六阶段学习指示：约束感知轨迹与轨迹重定时

## 1. 本阶段学习目标

本阶段目标是把第五阶段的轨迹空间对比升级为“约束感知”的分析：不仅看末端路径，还要看关节速度、关节加速度、是否违反限制，以及 total_time 对平滑性的影响。

## 2. 为什么关节速度和加速度重要

真实机械臂的关节不能无限快地转动，也不能瞬间产生很大的加速度。

- 速度过大：关节可能跟不上。
- 加速度过大：动作突然，可能对电机和结构不友好。

## 3. 为什么不能只看末端路径

末端路径看起来很好，不代表关节运动合理。

有些笛卡尔轨迹能让末端走直线，但关节速度和加速度可能波动更大。因此必须同时观察末端路径和关节约束。

## 4. 真实时间轴和轨迹点序号的区别

轨迹点序号只表示第几个采样点，不表示真实时间。

如果笛卡尔跟踪使用 `inner_steps`，它会产生更多内部控制点。用点序号比较会不公平，所以第六阶段统一使用“时间 / s”作为横轴。

## 5. 什么是 total_time

`total_time` 表示整条轨迹希望用多少秒执行完。

脚本中：

```text
dt = total_time / (num_points - 1)
dt_inner = dt / inner_steps
```

## 6. 为什么走慢一点通常更平滑

同样的位移，如果用更长时间完成，每秒需要移动的距离更小，关节速度通常会降低。

速度降低后，加速度也通常会变小，所以轨迹更平滑、更容易执行。

## 7. 什么是速度约束 violation

如果某个关节速度绝对值超过 `joint_velocity_limit`，就记为一次速度约束 violation。

`velocity_violation_count` 越大，说明轨迹越可能超出关节速度能力。

## 8. 什么是加速度约束 violation

如果某个关节加速度绝对值超过 `joint_acceleration_limit`，就记为一次加速度约束 violation。

`acceleration_violation_count` 越大，说明动作越突然，轨迹越不平滑。

## 9. 关节空间轨迹和笛卡尔空间轨迹的取舍

关节空间轨迹：

- 优点：关节角、速度、加速度更容易设计得平滑。
- 缺点：末端路径不一定是直线。

笛卡尔空间轨迹：

- 优点：末端路径更直观，适合需要末端沿直线或指定路径运动的任务。
- 缺点：对应到关节空间后，速度和加速度可能更复杂。

## 10. 本阶段新增文件

- `src/robot_arm_target_control_study/utils.py`
- `scripts/run_time_scaling_sweep.py`
- `docs/13_stage6_constraint_aware_trajectory_guide.md`
- `docs/14_joint_vs_cartesian_summary.md`
- `tests/test_trajectory_metrics.py`

本阶段还扩展了：

- `scripts/run_trajectory_space_compare.py`
- `src/robot_arm_target_control_study/plotting.py`
- `src/robot_arm_target_control_study/simulation.py`

## 11. 推荐阅读顺序

1. 读 `utils.py`，理解路径偏差和约束 violation。
2. 读 `run_trajectory_space_compare.py`，理解单次对比实验。
3. 读 `run_time_scaling_sweep.py`，理解 total_time 扫描。
4. 运行脚本并查看 CSV。
5. 打开速度、加速度和 summary 图。

## 12. 验收命令

```bash
python scripts/run_trajectory_space_compare.py --total_time 5.0
python scripts/run_trajectory_space_compare.py --method linear --total_time 5.0
python scripts/run_trajectory_space_compare.py --method quintic --total_time 5.0
python scripts/run_time_scaling_sweep.py
pytest
```

## 13. 本阶段可写进简历的内容

可以写：

> 在 2D 二连杆机械臂项目中实现约束感知轨迹对比和轨迹重定时分析，支持关节速度/加速度 violation 统计、路径偏差指标、total_time 扫描和可视化评估。
