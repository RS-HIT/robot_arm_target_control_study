# 第四阶段学习指示：轨迹跟踪与 PD 控制思想

## 1. 本阶段学习目标

本阶段目标是从“控制机械臂到达一个目标点”升级到“控制机械臂沿一条轨迹运动”，并理解简化任务空间 P / PD 控制的基本思想。

完成后你应该能解释：

- 目标点控制和轨迹跟踪有什么区别。
- P 项和 D 项分别在控制中起什么作用。
- 为什么本阶段的 PD 控制仍然是运动学层面的简化控制。

## 2. 目标点控制和轨迹跟踪的区别

目标点控制只关心末端最后是否接近某一个点。

轨迹跟踪关心一串连续的期望点，要求机械臂末端在整个过程中都尽量贴近期望路径。

可以简单理解为：

```text
目标点控制：到达一个点
轨迹跟踪：沿着一串点移动
```

## 3. P 控制、PD 控制、PID 控制的关系

- P 控制：根据当前位置误差进行修正。
- PD 控制：在 P 控制基础上加入误差变化速度，用来抑制过快变化和震荡趋势。
- PID 控制：在 PD 基础上加入 I 项，用累计误差处理长期偏差。

## 4. 为什么本阶段先学 PD，不直接学 PID

当前项目没有动力学模型，也没有真实电机、摩擦和外部扰动。直接加入 I 项会增加调参复杂度，还可能引入积分累积问题。

因此本阶段先理解 P 和 D：

- P 项让末端向期望位置靠近。
- D 项观察误差变化趋势，让控制更稳。

## 5. 本阶段新增文件

- `src/robot_arm_target_control_study/trajectory.py`
- `src/robot_arm_target_control_study/tracking_controller.py`
- `scripts/run_trajectory_tracking_demo.py`
- `tests/test_trajectory.py`
- `docs/09_stage4_trajectory_tracking_guide.md`
- `docs/10_pd_control_notes.md`

## 6. 必须看懂的函数

- `generate_line_trajectory()`
- `generate_circle_trajectory()`
- `compute_trajectory_velocity()`
- `compute_task_space_p_control_step()`
- `compute_task_space_pd_control_step()`
- `compute_resolved_rate_p_step()`
- `compute_resolved_rate_pd_step()`
- `simulate_trajectory_tracking()`
- `plot_trajectory_tracking()`
- `plot_tracking_error()`
- `plot_tracking_joint_angles()`

## 7. 推荐阅读顺序

1. 先读 `trajectory.py`，理解轨迹点从哪里来。
2. 再读 `tracking_controller.py`，理解 P 和 PD 如何产生关节角更新。
3. 读 `simulation.py` 中的 `simulate_trajectory_tracking()`，理解逐点跟踪流程。
4. 运行 `scripts/run_trajectory_tracking_demo.py`。
5. 最后看输出图像，并对比 P 和 PD 的误差曲线。

## 8. 验收命令

```bash
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller p_ff
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller pd
python scripts/run_trajectory_tracking_demo.py --trajectory circle --controller p_ff
python scripts/run_trajectory_tracking_demo.py --trajectory circle --controller pd
pytest
```

## 9. 如何看轨迹跟踪图

`trajectory_tracking_path.png`：

- 期望轨迹和实际轨迹越接近，说明跟踪越好。
- 如果实际轨迹明显滞后或偏离，说明控制参数或初始姿态还需要调整。

`trajectory_tracking_error.png`：

- 误差整体较小，说明跟踪效果较好。
- 误差尖峰表示某些轨迹点跟踪困难。
- PD 相比 P 如果误差更平滑，说明 D 项起到了抑制变化的作用。

`trajectory_tracking_joint_angles.png`：

- 关节角平滑变化，说明动作更自然。
- 关节角突变或锯齿明显，说明控制可能过激进。

## 10. 本次修复说明

### 10.1 为什么轨迹跟踪要从轨迹起点初始化？

如果初始关节角对应的末端位置离轨迹起点很远，机械臂一开始会先“追到轨迹上”，而不是沿轨迹运动。这样画出来的实际轨迹会从远处绕过来，无法真实反映轨迹跟踪控制器本身的效果。

因此 demo 默认使用 `init_mode=ik_start`：先对期望轨迹第一个点做解析逆运动学，把机械臂放到轨迹起点附近。

### 10.2 为什么 resolved-rate 控制中要用速度命令？

轨迹跟踪不是静止目标点控制。期望点本身在移动，所以控制器不仅要知道“现在差多少”，还要知道“轨迹希望往哪里走”。

resolved-rate 控制先生成末端速度命令：

```text
x_dot_cmd = desired_velocity + kp * position_error
```

再用雅可比伪逆把末端速度转换成关节速度。

### 10.3 为什么 q_dot 更新关节角时必须乘 dt？

`q_dot` 是关节速度，单位可以理解为“弧度/秒”。关节角更新量应该是：

```text
delta_theta = q_dot * dt
```

如果不乘 `dt`，就等于把速度直接当成角度增量，会导致每一步动作过大，出现跳动或锯齿。

### 10.4 为什么 error_derivative = (error - prev_error) / dt 容易导致震荡？

离散轨迹点之间可能有跳变，误差也会因为目标点移动而快速变化。直接对误差做差分，容易产生 derivative kick，也就是 D 项突然变得很大。

修复后的 PD 使用速度误差：

```text
velocity_error = desired_velocity - actual_velocity
```

这更符合轨迹跟踪直觉：比较“希望末端怎么动”和“实际末端怎么动”。

### 10.5 p、p_ff、pd 三种控制器有什么区别？

- `p`：只使用 `kp * position_error`，适合观察纯位置误差修正。
- `p_ff`：使用 `desired_velocity + kp * position_error`，适合轨迹跟踪入门，通常比纯 P 滞后更少。
- `pd`：使用 `desired_velocity + kp * position_error + kd * velocity_error`，适合观察速度误差对平滑性的影响。

### 10.6 为什么先推荐 p_ff，而不是直接使用 pd？

`p_ff` 已经利用了轨迹速度信息，逻辑清楚，参数少，通常能得到稳定的轨迹跟踪结果。

`pd` 多了 `kd`，如果 `kd` 太大，仍可能放大速度估计噪声或造成震荡。因此建议先看 `p_ff`，再用较小的 `kd` 观察 PD 的影响。

## 11. 如何调试 PD 参数

建议按下面顺序调试：

1. 先用 `controller=p_ff` 验证轨迹生成、IK 初始化和速度前馈是否正常。
2. 如果 `p_ff` 稳定，再测试 `controller=pd`。
3. `kd` 建议从 `0.0`、`0.02`、`0.05`、`0.1` 逐步尝试。
4. 如果关节角曲线出现高频锯齿，说明 `kd` 可能过大，或者实际速度估计太敏感。
5. 如果误差曲线变得更平滑，说明 `kd` 可能起到了抑制震荡的作用。
6. 如果 `pd` 比 `p_ff` 更差，不代表 PD 概念错误，可能是当前简化运动学模型中速度估计不稳定。

示例：

```bash
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller pd --kd 0.02
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller pd --kd 0.05
```

## 12. 下一阶段学习建议

- 比较不同 `kp` 和 `kd` 的轨迹跟踪效果。
- 增加更复杂但仍然二维的轨迹，例如 S 形轨迹。
- 尝试在轨迹上标出时间或关键点。
- 后续再学习速度级控制、动力学控制或更真实的仿真环境。
