# robot_arm_target_control_study

这是一个面向机器人算法入门的 2D 平面二连杆机械臂目标点控制 demo。

第一阶段不使用 MuJoCo、ROS 或强化学习框架，只完成一个可以运行、可以测试、可以解释的小项目：用户输入目标点，程序通过正运动学、雅可比矩阵和雅可比伪逆迭代控制，让机械臂末端逐步靠近目标点。

## 功能特点

- 2D 平面二连杆机械臂建模。
- 使用正运动学计算基座、肘关节和末端执行器位置。
- 使用雅可比伪逆将末端误差转换为关节角更新量。
- 支持解析逆运动学与雅可比伪逆迭代控制对比。
- 支持参数扫描、阻尼雅可比控制和接近奇异位形实验。
- 支持命令行输入目标点。
- 自动输出最终姿态图、误差曲线、关节角变化曲线和实验对比曲线。
- 提供 pytest 测试，覆盖正运动学、解析逆运动学、可达目标收敛、阻尼控制和通用仿真历史。

## 示例结果

机械臂最终姿态：

![机械臂最终姿态](docs/assets/arm_pose.png)

末端误差曲线：

![末端误差曲线](docs/assets/error_curve.png)

关节角变化曲线：

![关节角变化曲线](docs/assets/joint_curve.png)

## 项目结构

```text
robot_arm_target_control_study/
├── README.md
├── requirements.txt
├── scripts/
│   ├── run_damped_jacobian_demo.py
│   ├── run_compare_methods.py
│   ├── run_parameter_sweep.py
│   ├── run_singularity_demo.py
│   ├── run_time_scaling_sweep.py
│   ├── run_trajectory_space_compare.py
│   ├── run_trajectory_tracking_demo.py
│   └── run_reach_demo.py
├── src/
│   └── robot_arm_target_control_study/
│       ├── controller.py
│       ├── kinematics.py
│       ├── plotting.py
│       ├── simulation.py
│       ├── tracking_controller.py
│       ├── trajectory.py
│       └── utils.py
├── tests/
│   ├── test_controller.py
│   ├── test_kinematics.py
│   ├── test_trajectory.py
│   └── test_trajectory_metrics.py
├── docs/
│   ├── assets/
│   ├── 01_code_reading_notes.md
│   ├── 02_code_reading_notes.md
│   ├── 02_interview_questions.md
│   ├── 05_stage2_learning_guide.md
│   ├── 06_stage3_experiment_guide.md
│   ├── 07_experiment_report_template.md
│   ├── 08_parameter_experiment_report.md
│   ├── 09_stage4_trajectory_tracking_guide.md
│   ├── 10_pd_control_notes.md
│   ├── 11_stage5_trajectory_planning_guide.md
│   ├── 12_trajectory_planning_notes.md
│   ├── 13_stage6_constraint_aware_trajectory_guide.md
│   └── 14_joint_vs_cartesian_summary.md
└── outputs/
```

## 安装依赖

建议在项目根目录运行：

```bash
pip install -r requirements.txt
```

依赖包括：

- `numpy`：做矩阵和向量计算。
- `matplotlib`：画机械臂姿态图和曲线图。
- `pytest`：运行测试。

## 运行 demo

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
```

运行后终端会打印：

- 目标点坐标。
- 最终末端位置。
- 最终误差。
- 是否到达目标附近。
- 输出图片路径。

## 第二阶段：解析逆运动学与雅可比伪逆对比

第二阶段在第一阶段基础上增加“解析逆运动学 vs 雅可比伪逆迭代控制”对比实验。运行：

```bash
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
```

终端会输出：

- 目标点和可达性判断。
- 解析逆运动学计算出的 `theta1`、`theta2`。
- 解析逆运动学对应的最终末端位置和误差。
- 雅可比伪逆迭代控制的最终末端位置、误差和迭代步数。
- 两种方法的简短对比说明。

解析逆运动学适合结构简单、自由度较少、几何关系清楚的机械臂。它的特点是“直接求解”：只要目标点可达，通常可以直接算出关节角。

雅可比伪逆适合更容易推广到高自由度或复杂机械臂的场景。它的特点是“迭代逼近”：每一步根据末端误差计算关节角增量，逐步靠近目标点，但可能受到初始关节角、步长和奇异位形影响。

两者区别可以简单理解为：

- 解析逆运动学：目标点 -> 几何公式 -> 关节角。
- 雅可比伪逆控制：目标点 -> 当前误差 -> 关节角小步更新 -> 重复迭代。

第二阶段新增输出：

- `outputs/figures/workspace.png`：二连杆机械臂工作空间图，包含最远可达圆和最近不可达内圆。

## 第三阶段：参数敏感性与阻尼雅可比控制实验

第三阶段继续使用 2D 二连杆机械臂，不引入 MuJoCo、ROS、强化学习或复杂三维模型。重点是观察普通雅可比伪逆控制在不同参数、不同初始姿态和接近奇异位形时的表现，并加入阻尼最小二乘控制做对比。

为什么要做参数实验：

- `gain` 会影响每次朝目标移动的积极程度。太小可能收敛慢，太大可能振荡。
- `max_step` 会限制单次关节角变化。太小可能慢，太大可能动作跳跃。
- `damping` 是阻尼系数，会让接近奇异位形时的关节角更新更保守。

为什么不能只看 `final_error`：

- `final_error` 只告诉你最后停在哪里，看不出中间过程是否很慢、是否震荡、是否突然跳动。
- 两组参数可能最终误差都很小，但一组平滑下降，另一组来回摆动后才收敛。
- 控制算法不仅要“最后到达”，也要看过程是否稳定、动作是否自然。

为什么要看 error curve：

- 平滑下降：通常表示控制过程稳定。
- 下降很慢：参数可能过保守，例如 `gain` 或 `max_step` 太小。
- 上下波动：可能出现震荡，常见于参数过激进。
- 长时间不下降：可能接近奇异位形、目标不可达，或参数设置不合适。

为什么要看 joint angle curve：

- 关节角平滑变化：动作比较自然。
- 突然尖峰：可能单步更新量过大。
- 高频锯齿：可能控制在目标附近来回震荡。
- 某个关节变化特别大：说明主要运动压力集中在这个关节上。

和 PID 调参的类比：

- `gain` 类似 P 控制中的 `Kp`，决定误差反馈的修正力度。
- `max_step` 更像输出限幅或速度限制，不是 `Kp`，它限制每一步最多能改变多少关节角。
- `damping` 更像数值阻尼、正则化或刹车，用来抑制奇异位形附近的过大更新，不等同于 PID 的 D 项。

运行参数扫描：

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
```

运行普通伪逆和阻尼雅可比对比：

```bash
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
```

运行奇异位形实验：

```bash
python scripts/run_singularity_demo.py
```

普通伪逆和阻尼伪逆的区别：

- 普通伪逆直接使用雅可比矩阵的伪逆把末端误差转换成关节角更新。
- 阻尼伪逆在矩阵里加入 `damping^2 * I`，牺牲一点直接性，换取接近奇异位形时更平滑、更稳定的更新。

第三阶段新增输出：

- `outputs/logs/parameter_sweep.csv`：参数扫描实验结果表。
- `outputs/figures/gain_error_comparison.png`：固定 `max_step=0.08` 时，不同 `gain` 的误差曲线。
- `outputs/figures/gain_theta1_comparison.png`：固定 `max_step=0.08` 时，不同 `gain` 的 theta1 曲线。
- `outputs/figures/gain_theta2_comparison.png`：固定 `max_step=0.08` 时，不同 `gain` 的 theta2 曲线。
- `outputs/figures/max_step_error_comparison.png`：固定 `gain=0.8` 时，不同 `max_step` 的误差曲线。
- `outputs/figures/max_step_theta1_comparison.png`：固定 `gain=0.8` 时，不同 `max_step` 的 theta1 曲线。
- `outputs/figures/max_step_theta2_comparison.png`：固定 `gain=0.8` 时，不同 `max_step` 的 theta2 曲线。
- `outputs/figures/damping_error_comparison.png`：不同 `damping` 的阻尼雅可比误差曲线。
- `outputs/figures/damping_theta1_comparison.png`：不同 `damping` 的 theta1 曲线。
- `outputs/figures/damping_theta2_comparison.png`：不同 `damping` 的 theta2 曲线。
- `outputs/figures/pinv_vs_damped_error.png`：普通伪逆和阻尼雅可比误差曲线对比。
- `outputs/figures/pinv_vs_damped_joint_angles.png`：普通伪逆和阻尼雅可比关节角曲线对比。
- `outputs/figures/singularity_error.png`：接近伸直边界时的误差曲线。
- `outputs/figures/singularity_joint_angles.png`：接近伸直边界时的关节角曲线。

## 第四阶段：轨迹跟踪与 PD 控制思想

第四阶段从“到达一个目标点”升级到“沿着一串目标点运动”。目标点控制只关心末端最后能不能靠近某个点，轨迹跟踪还要关心整个运动过程中实际路径是否贴近期望路径。

本阶段仍然是简化运动学控制，不是完整动力学控制：没有质量、惯量、力矩、电机模型，也不引入 MuJoCo、ROS 或强化学习。

P 控制和 PD 控制的区别：

- P 控制只根据当前位置误差修正：误差越大，修正越大。
- P + 前馈（`p_ff`）在 P 控制基础上加入期望轨迹速度，更适合入门轨迹跟踪，通常比纯 P 更少滞后。
- PD 控制在 P + 前馈基础上加入速度误差项，观察实际末端速度和期望速度的差异，用来抑制过快变化和震荡趋势。
- 本阶段先学 PD，不直接学 PID，是因为 I 项主要用于长期稳态误差补偿，容易引入积分累积和调参复杂度；当前项目先把“误差”和“误差变化速度”理解清楚。

第四阶段修复后的轨迹跟踪使用 resolved-rate 控制：控制器先生成末端速度命令 `x_dot_cmd`，再通过阻尼雅可比伪逆求关节速度 `q_dot`，最后用 `theta = theta + q_dot * dt` 更新关节角。这样避免把速度命令误当成角度增量。

默认 `init_mode=ik_start` 会先用解析逆运动学把机械臂初始化到轨迹起点附近，避免实际轨迹从远处追赶期望轨迹。

运行轨迹跟踪 demo：

```bash
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller p_ff
python scripts/run_trajectory_tracking_demo.py --trajectory circle --controller p_ff
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller pd --kd 0.02
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller pd --kp 3.0 --kd 0.05 --damping 0.05 --max_joint_speed 1.5
python scripts/run_trajectory_tracking_demo.py --trajectory circle --controller pd
```

如果需要研究 PD 参数影响，可以通过 `--kd` 修改速度误差增益。建议先确认 `p_ff` 稳定，再尝试 `--kd 0.0`、`--kd 0.02`、`--kd 0.05`、`--kd 0.1`。

第四阶段输出图片：

- `outputs/figures/trajectory_tracking_path.png`：期望末端轨迹和实际末端轨迹对比。
- `outputs/figures/trajectory_tracking_error.png`：轨迹跟踪误差随轨迹点变化的曲线。
- `outputs/figures/trajectory_tracking_joint_angles.png`：跟踪过程中两个关节角的变化曲线。

## 第五阶段：关节空间轨迹与笛卡尔空间轨迹对比

第五阶段区分两个概念：

- 轨迹规划：先生成一串希望执行的位置、速度或关节角序列。
- 轨迹跟踪：控制机械臂尽量沿着规划好的轨迹运动。

关节空间轨迹是在 `theta1/theta2` 上直接插值，优点是关节角变化容易设计得平滑；缺点是末端路径不一定是直线。

笛卡尔空间轨迹是在末端 `x/y` 空间中规划路径，例如让末端沿直线走；优点是末端路径直观，缺点是对应到关节空间后，关节速度和加速度可能更复杂。

速度和加速度很重要，因为真实机械臂不能只接收一串位置点。速度过大表示关节可能跟不上，加速度过大表示动作可能突然、对电机和结构不友好。

运行对比脚本：

```bash
python scripts/run_trajectory_space_compare.py
python scripts/run_trajectory_space_compare.py --start_x 0.8 --start_y 0.4 --goal_x 1.2 --goal_y 0.6 --method quintic
```

第五阶段输出：

- `outputs/figures/trajectory_space_path_compare.png`：期望直线、关节空间末端路径、笛卡尔跟踪路径对比。
- `outputs/figures/trajectory_space_theta_compare.png`：两种方法下的关节角变化对比。
- `outputs/figures/trajectory_space_velocity_compare.png`：两种方法下的关节速度对比。
- `outputs/figures/trajectory_space_acceleration_compare.png`：两种方法下的关节加速度对比。
- `outputs/logs/trajectory_space_compare.csv`：路径长度、最大关节速度、最大关节加速度、RMS 指标和最终误差。

## 第六阶段：约束感知轨迹对比与轨迹重定时

第六阶段在第五阶段基础上加入真实时间轴、速度/加速度约束检查和轨迹重定时。

为什么速度和加速度约束重要：

- 关节速度过大，说明机械臂可能跟不上轨迹。
- 关节加速度过大，说明动作变化太突然，对电机和结构不友好。
- 即使末端路径看起来正确，关节层面的速度和加速度也可能不适合执行。

为什么要用真实时间轴：

- 只用轨迹点序号时，关节空间轨迹和带 `inner_steps` 的笛卡尔跟踪点数不同，比较不公平。
- 使用时间 / s 作为横轴后，可以比较同一段真实运动时间内的关节角、速度和加速度。

`total_time` 表示整条轨迹希望用多少秒完成。通常 `total_time` 越大，轨迹走得越慢，关节速度和加速度越低，动作也更平滑。

运行命令：

```bash
python scripts/run_trajectory_space_compare.py --total_time 5.0
python scripts/run_time_scaling_sweep.py
python scripts/run_time_scaling_sweep.py --total_times 3 5 8 10
```

CSV 指标说明：

- `max_joint_velocity`：最大关节速度。
- `max_joint_acceleration`：最大关节加速度。
- `velocity_violation_count`：超过速度限制的采样数量。
- `acceleration_violation_count`：超过加速度限制的采样数量。
- `mean_path_deviation` / `max_path_deviation`：末端路径相对起点-终点直线的平均/最大偏差。

当前阶段仍然只是运动学层面分析，不是完整动力学仿真；它帮助建立“轨迹是否平滑、是否可能执行”的直觉。

## 运行测试

```bash
pytest
```

测试重点：

- 正运动学是否正确。
- 目标点 `(1.2, 0.6)` 是否能收敛。
- 不可达目标点是否不会导致程序崩溃。
- 解析逆运动学是否能回代到目标点。
- 阻尼雅可比控制输出是否合理，并能降低误差。
- 通用迭代仿真是否能返回完整历史记录。
- 轨迹生成、轨迹速度估计和轨迹跟踪 history 是否正确。
- 时间缩放、关节空间轨迹、离散速度和轨迹空间对比指标是否正确。
- 约束检查、路径偏差、真实时间轴和 total_time 扫描是否正确。

## 输出结果说明

demo 运行后会把图片保存到 `outputs/`：

- `arm_pose.png`：机械臂最终姿态图，包含目标点和末端点。
- `error_curve.png`：末端误差随迭代次数变化的曲线。
- `joint_curve.png`：两个关节角随迭代次数变化的曲线。
- `figures/workspace.png`：工作空间图，展示目标点是否可能落在机械臂可达范围内。
- `logs/parameter_sweep.csv`：不同 `gain` 和 `max_step` 参数组合的实验表格。
- `figures/pinv_vs_damped_error.png`：普通伪逆和阻尼雅可比的误差对比。
- `figures/pinv_vs_damped_joint_angles.png`：普通伪逆和阻尼雅可比的关节角对比。
- `figures/gain_*_comparison.png`：固定 `max_step` 后比较不同 `gain`。
- `figures/max_step_*_comparison.png`：固定 `gain` 后比较不同 `max_step`。
- `figures/damping_*_comparison.png`：比较不同阻尼系数。
- `figures/singularity_error.png`：奇异位形实验误差曲线。
- `figures/singularity_joint_angles.png`：奇异位形实验关节角曲线。
- `figures/trajectory_tracking_path.png`：期望轨迹和实际轨迹对比图。
- `figures/trajectory_tracking_error.png`：轨迹跟踪误差曲线。
- `figures/trajectory_tracking_joint_angles.png`：轨迹跟踪关节角曲线。
- `figures/trajectory_space_path_compare.png`：关节空间和笛卡尔空间路径对比。
- `figures/trajectory_space_theta_compare.png`：关节角轨迹对比。
- `figures/trajectory_space_velocity_compare.png`：关节速度对比。
- `figures/trajectory_space_acceleration_compare.png`：关节加速度对比。
- `logs/trajectory_space_compare.csv`：第五阶段轨迹空间对比指标。
- `logs/time_scaling_sweep.csv`：不同 `total_time` 下的约束和轨迹指标。
- `figures/time_scaling_velocity_compare.png`：不同 `total_time` 下最大关节速度对比。
- `figures/time_scaling_acceleration_compare.png`：不同 `total_time` 下最大关节加速度对比。
- `figures/time_scaling_metric_summary.png`：速度、加速度和加速度 RMS 汇总图。

README 中展示用的图片放在 `docs/assets/`，避免每次运行 demo 时覆盖首页展示图。

## 核心算法解释

二连杆机械臂有两个关节角：

- `theta1`：第一根连杆相对世界坐标系的角度。
- `theta2`：第二根连杆相对第一根连杆的角度。

正运动学回答的问题是：

> 已知关节角，末端在哪里？

雅可比矩阵回答的问题是：

> 关节角变化一点点，末端会往哪个方向动？

本项目使用雅可比伪逆控制：

```text
关节角更新量 = 雅可比伪逆 * 末端误差
```

也就是说，程序每一步都先计算“末端离目标还差多少”，再用雅可比矩阵的伪逆反推出“两个关节角应该怎么改一点点”。

项目数据流可以概括为：

```text
命令行输入目标点
-> 控制器迭代
-> 正运动学计算末端位置
-> 记录误差和关节角
-> 输出图像
```

## 当前阶段边界

当前仓库仍然只做：

- 2D 平面机械臂。
- 二连杆。
- 运动学层面的目标点控制。
- 解析逆运动学、雅可比伪逆、阻尼雅可比的教学实验。
- 参数扫描、误差曲线和关节角曲线输出。

暂时不做：

- 3D 机械臂。
- 障碍物避障。
- 动力学控制。
- MuJoCo / PyBullet。
- 强化学习。
- Sim2Real。
- 真实机械臂硬件控制。

## 后续计划

- 给参数扫描增加更多目标点和初始姿态组合。
- 支持命令行配置连杆长度、初始关节角和迭代参数。
- 将 `outputs/logs/parameter_sweep.csv` 中的结果整理成正式实验报告。
- 增加简单动画，展示机械臂逐步靠近目标点的过程。
- 学习并补充奇异值分解视角下的阻尼最小二乘解释。
- 在保持当前运动学 demo 清晰的基础上，后续再考虑 3D、动力学仿真或强化学习扩展。
