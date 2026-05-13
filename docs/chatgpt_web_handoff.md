# 项目上下文交接文档：给网页端 ChatGPT

> 本文档由 Codex 根据当前项目文件自动整理，用于交接给网页端 ChatGPT。内容可能需要用户进一步确认。

## 1. 项目基本信息

- 项目名称：`robot_arm_target_control_study`
- 项目类型：机器人算法学习项目 / 2D 平面二连杆机械臂控制实验项目
- 当前项目阶段：第六阶段，主题为“约束感知轨迹对比与轨迹重定时”
- 当前主要目标：在不引入 MuJoCo、ROS、强化学习、复杂动力学和三维机械臂的前提下，通过一个可运行的小项目理解机械臂运动学、逆运动学、雅可比控制、轨迹跟踪、轨迹规划、速度/加速度约束和轨迹重定时
- 当前使用语言：Python
- 当前主要依赖：`numpy`、`matplotlib`、`pytest`
- 当前运行方式：通过 `scripts/` 下的命令行脚本运行实验，通过 `pytest` 运行测试
- 当前项目面向的任务：学习和展示机器人控制基础算法，形成可解释、可复现实验和文档材料

## 2. 用户背景与使用意图

从项目内容和用户多轮需求看，用户正在通过一个小型 2D 二连杆机械臂项目，逐步学习机器人运动学和控制算法。重点不是搭建大型工程系统，而是理解每个算法模块的输入、输出、公式含义、实验现象和可视化结果。

用户希望获得的能力大致包括：

- 能解释正运动学、解析逆运动学、雅可比矩阵、雅可比伪逆、阻尼最小二乘、resolved-rate 控制、P/PD 控制思想、关节空间轨迹和笛卡尔空间轨迹。
- 能通过图像和 CSV 判断参数变化对控制效果的影响。
- 能把实验现象写进 README、学习笔记、实验报告或简历项目描述。
- 能保持项目“小步迭代、可运行、可验证、可展示”，而不是一次性堆复杂框架。

用户当前可能更关注：

- 算法理解；
- 实验结果解释；
- 文档和报告表达；
- 工程展示；
- 简历可写内容。

项目文件中没有明确体现用户的学历、专业背景或最终用途，需用户进一步确认。

## 3. 当前目录结构概览

当前项目主要目录和文件如下，已忽略 `.git`、`__pycache__`、虚拟环境和缓存类目录。

```text
robot_arm_target_control_study/
├── README.md
├── requirements.txt
├── scripts/
├── src/
│   └── robot_arm_target_control_study/
├── tests/
├── docs/
├── outputs/
└── _project_handoff/
```

核心目录说明：

- `README.md`：项目主说明文档，已经按阶段记录运行命令、输出文件和学习目标。
- `requirements.txt`：当前依赖列表，包含 `numpy`、`matplotlib`、`pytest`。
- `scripts/`：实验入口脚本目录，用户主要通过这里运行不同阶段的实验。
- `src/robot_arm_target_control_study/`：核心算法代码目录，包含运动学、控制器、仿真、轨迹生成、绘图和指标工具。
- `tests/`：pytest 测试目录，覆盖运动学、控制器、轨迹、轨迹指标等功能。
- `docs/`：学习文档、实验模板、阶段说明和交接材料。
- `outputs/`：实验输出目录，保存图片、CSV 和部分历史输出。
- `_project_handoff/`：早期项目交接和状态记录文档，适合作为历史参考。

项目结构整体清晰，适合继续小步扩展。需要注意的是，`docs/` 中阶段文档较多，后续可以整理出一个“文档导航页”，避免学习材料分散。

## 4. 已完成的核心功能

### 已完成

- 2D 平面二连杆机械臂正运动学。
- 二连杆机械臂雅可比矩阵计算。
- 雅可比伪逆迭代目标点控制。
- 解析逆运动学和可达性判断。
- 解析逆运动学 vs 雅可比伪逆控制对比实验。
- 工作空间可视化。
- 参数敏感性实验，包括 `gain`、`max_step`、`damping`。
- 阻尼最小二乘 Damped Least Squares 控制。
- 普通伪逆和阻尼伪逆在接近奇异位形时的对比。
- 多组参数误差曲线和关节角曲线对比。
- resolved-rate 轨迹跟踪。
- `p`、`p_ff`、`pd` 三种轨迹跟踪控制模式。
- 直线和圆形末端轨迹跟踪。
- IK 初始化轨迹起点，避免实际轨迹从远处追赶。
- 关节空间轨迹生成，包括 linear、cubic、quintic 时间缩放。
- 笛卡尔空间直线轨迹跟踪对比。
- 关节速度和关节加速度离散计算。
- 关节空间轨迹 vs 笛卡尔空间轨迹对比。
- 使用真实时间轴比较关节角、速度、加速度。
- `total_time` 轨迹重定时实验。
- 速度和加速度约束检查。
- 路径相对直线的平均偏差和最大偏差指标。
- pytest 测试，最近一次记录为 `29 passed`。

### 部分完成 / 需进一步确认

- 第六阶段相关文件已存在并可运行，但当前 Git 状态显示部分文件尚未提交。
- 输出图片和 CSV 已生成，但没有统一的“实验结果解读报告”汇总所有阶段结论。
- 项目有学习文档和报告模板，但用户是否已经完成正式实验报告，需进一步确认。

### 尚未完成

- 未引入动力学、力矩、电机模型或真实机器人接口。
- 未引入 MuJoCo、ROS、强化学习或三维机械臂。
- 未形成统一的 CLI 总入口，目前仍是多个实验脚本分散运行。
- 未对所有脚本做完整 CLI smoke test。

## 5. 核心代码文件说明

### `src/robot_arm_target_control_study/kinematics.py`

作用：机械臂运动学核心函数。

主要函数：

- `forward_kinematics(theta1, theta2, link1, link2)`：根据两个关节角计算关节位置和末端位置。
- `compute_jacobian(theta, link1, link2)`：计算末端位置相对于关节角的雅可比矩阵。
- `is_target_reachable(target_x, target_y, link1, link2)`：判断目标点是否在二连杆工作空间内。
- `inverse_kinematics_analytic(target_x, target_y, link1, link2, elbow="down")`：用解析几何求目标点对应的关节角。

关系：被控制器、仿真脚本、轨迹对比脚本和测试共同调用。适合继续扩展少量运动学工具，但不建议在此文件加入控制逻辑。

### `src/robot_arm_target_control_study/controller.py`

作用：目标点控制相关的关节角更新函数。

主要函数：

- `limit_joint_step(delta_theta, max_step)`：限制单步关节角变化。
- `compute_control_step(...)`：普通雅可比伪逆目标点控制。
- `compute_damped_jacobian_step(...)`：阻尼最小二乘控制。

关系：用于第二、第三阶段的目标点控制和参数实验。适合继续放“目标点控制”函数，不建议加入轨迹跟踪专用逻辑。

### `src/robot_arm_target_control_study/tracking_controller.py`

作用：轨迹跟踪控制器。

主要函数：

- `compute_task_space_p_control_step(...)`：早期任务空间 P 控制函数。
- `compute_task_space_pd_control_step(...)`：早期任务空间 PD 控制函数。
- `compute_damped_pseudoinverse(...)`：阻尼伪逆工具函数。
- `compute_resolved_rate_p_step(...)`：resolved-rate P / P+前馈 控制。
- `compute_resolved_rate_pd_step(...)`：resolved-rate PD 控制，使用速度误差而不是误差差分。

关系：主要被 `simulate_trajectory_tracking()` 和 `run_trajectory_tracking_demo.py` 使用。当前适合继续做轻量控制器实验。

### `src/robot_arm_target_control_study/trajectory.py`

作用：轨迹生成和离散导数计算。

主要函数：

- `generate_line_trajectory(...)`：生成二维直线末端轨迹。
- `generate_circle_trajectory(...)`：生成二维圆形末端轨迹。
- `compute_trajectory_velocity(...)`：估计末端轨迹速度。
- `cubic_time_scaling(num_points)`：生成三次时间缩放曲线。
- `quintic_time_scaling(num_points)`：生成五次时间缩放曲线。
- `generate_joint_space_trajectory(...)`：生成关节空间轨迹。
- `compute_discrete_velocity(values, dt)`：离散速度。
- `compute_discrete_acceleration(values, dt)`：离散加速度。

关系：被轨迹跟踪、轨迹空间对比和时间缩放扫描使用。适合继续扩展简单轨迹生成函数。

### `src/robot_arm_target_control_study/simulation.py`

作用：仿真流程封装。

主要函数：

- `run_reach_simulation(...)`：目标点迭代控制仿真。
- `simulate_iterative_control(...)`：通用迭代控制仿真，支持普通伪逆和阻尼伪逆。
- `simulate_trajectory_tracking(...)`：逐点跟踪轨迹，支持 `p`、`p_ff`、`pd`，并记录历史数据。

关系：把控制器、运动学和轨迹数据串成完整实验。适合继续放轻量仿真流程，但不建议扩展成大型类框架。

### `src/robot_arm_target_control_study/plotting.py`

作用：Matplotlib 绘图函数集合。

主要功能：

- 机械臂姿态图。
- 误差曲线。
- 关节角曲线。
- 工作空间图。
- 多参数误差和关节角对比。
- 轨迹跟踪路径、误差、关节角图。
- 关节空间 vs 笛卡尔空间路径、关节角、速度、加速度对比。
- 基于真实时间轴的关节角、速度、加速度对比。
- `total_time` 扫描指标图。

关系：被多个脚本调用。适合继续新增小型绘图函数，但后续可考虑按主题拆分。

### `src/robot_arm_target_control_study/utils.py`

作用：第六阶段新增的指标工具。

主要函数：

- `check_joint_limits(...)`：检查关节速度和加速度是否违反给定限制。
- `compute_path_deviation_from_line(...)`：计算实际路径相对起点-终点直线的平均偏差和最大偏差。

关系：被 `run_trajectory_space_compare.py` 和 `run_time_scaling_sweep.py` 使用。适合继续放小型指标计算函数。

## 6. 关键运行流程 / 数据流

### 目标点控制流程

用户输入目标点 `target_x, target_y`  
→ 运行 `scripts/run_reach_demo.py`  
→ `simulation.run_reach_simulation()` 初始化关节角  
→ 每一步调用 `controller.compute_control_step()`  
→ `kinematics.forward_kinematics()` 计算当前末端位置  
→ `kinematics.compute_jacobian()` 计算雅可比矩阵  
→ 雅可比伪逆把末端误差转换为关节角增量  
→ 保存误差历史、关节角历史和末端轨迹  
→ `plotting.py` 输出机械臂图、误差曲线和关节角曲线。

关键参数：

- `target_x, target_y`
- `gain`
- `max_step`
- `max_iterations`
- `tolerance`

### 解析逆运动学 vs 迭代控制流程

用户输入目标点  
→ 运行 `scripts/run_compare_methods.py`  
→ 方法 A 调用 `inverse_kinematics_analytic()` 直接求关节角  
→ 再用 `forward_kinematics()` 验证末端位置  
→ 方法 B 调用雅可比伪逆迭代控制  
→ 对比最终误差、迭代次数和方法特点。

### 参数敏感性和阻尼伪逆流程

用户运行 `scripts/run_parameter_sweep.py`  
→ 多组 `gain` 和 `max_step` 参数被自动测试  
→ 每组调用通用迭代仿真  
→ 输出 CSV：`outputs/logs/parameter_sweep.csv`  
→ 输出多组误差曲线和关节角曲线。

用户运行 `scripts/run_damped_jacobian_demo.py`  
→ 对比普通伪逆和阻尼伪逆  
→ 扫描不同 `damping`  
→ 输出阻尼参数对比图。

### resolved-rate 轨迹跟踪流程

用户运行 `scripts/run_trajectory_tracking_demo.py`  
→ 根据 `--trajectory line/circle` 生成期望轨迹  
→ 根据 `--controller p/p_ff/pd` 选择控制器  
→ 默认用解析 IK 把初始关节角对齐到轨迹起点  
→ `compute_trajectory_velocity()` 计算期望速度  
→ `simulate_trajectory_tracking()` 使用 `inner_steps` 做高频小步控制  
→ resolved-rate 控制器输出关节速度 `q_dot`  
→ 用 `theta = theta + q_dot * dt_inner` 更新关节角  
→ 输出路径图、误差图、关节角图。

关键参数：

- `kp`
- `kd`
- `damping`
- `max_joint_speed`
- `dt`
- `inner_steps`
- `num_points`
- `radius`

### 关节空间轨迹 vs 笛卡尔空间轨迹流程

用户运行 `scripts/run_trajectory_space_compare.py`  
→ 起点和终点用解析 IK 转为关节角  
→ 方法 A：在关节空间用 linear/cubic/quintic 插值生成关节轨迹  
→ 对每个关节角调用 `forward_kinematics()` 得到末端路径  
→ 方法 B：在笛卡尔空间生成直线末端轨迹，再用 p_ff resolved-rate 跟踪  
→ 分别计算关节速度、关节加速度、路径长度、最终误差和路径偏差  
→ 用真实时间轴绘图并保存 CSV。

关键参数：

- `start_x, start_y`
- `goal_x, goal_y`
- `method`
- `num_points`
- `total_time`
- `inner_steps`
- `joint_velocity_limit`
- `joint_acceleration_limit`

### total_time 轨迹重定时流程

用户运行 `scripts/run_time_scaling_sweep.py`  
→ 对多个 `total_time` 重复运行轨迹对比  
→ 记录不同总运动时间下的最大关节速度、最大关节加速度、RMS 指标、约束违反次数、最终误差和路径偏差  
→ 输出 `outputs/logs/time_scaling_sweep.csv`  
→ 输出速度、加速度和指标汇总图。

## 7. 当前运行方式

### 安装依赖

项目存在 `requirements.txt`，可以运行：

```bash
pip install -r requirements.txt
```

当前未发现 `pyproject.toml`、`environment.yml` 或 `Makefile`。如果后续要做更正式的工程展示，可以考虑补充。

### 第一阶段：目标点控制

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
```

输出示例：

- `outputs/arm_pose.png`
- `outputs/error_curve.png`
- `outputs/joint_curve.png`

### 第二阶段：解析逆运动学对比

```bash
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
```

### 第三阶段：参数和阻尼实验

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
python scripts/run_singularity_demo.py
```

输出位置：

- `outputs/logs/parameter_sweep.csv`
- `outputs/figures/gain_error_comparison.png`
- `outputs/figures/gain_theta1_comparison.png`
- `outputs/figures/gain_theta2_comparison.png`
- `outputs/figures/max_step_error_comparison.png`
- `outputs/figures/max_step_theta1_comparison.png`
- `outputs/figures/max_step_theta2_comparison.png`
- `outputs/figures/damping_error_comparison.png`
- `outputs/figures/damping_theta1_comparison.png`
- `outputs/figures/damping_theta2_comparison.png`
- `outputs/figures/singularity_error.png`
- `outputs/figures/singularity_joint_angles.png`

### 第四阶段：轨迹跟踪

```bash
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller p_ff
python scripts/run_trajectory_tracking_demo.py --trajectory circle --controller p_ff
python scripts/run_trajectory_tracking_demo.py --trajectory line --controller pd --kd 0.02
python scripts/run_trajectory_tracking_demo.py --trajectory circle --controller pd
```

输出位置：

- `outputs/figures/trajectory_tracking_path.png`
- `outputs/figures/trajectory_tracking_error.png`
- `outputs/figures/trajectory_tracking_joint_angles.png`

### 第五阶段：轨迹空间对比

```bash
python scripts/run_trajectory_space_compare.py
python scripts/run_trajectory_space_compare.py --method linear
python scripts/run_trajectory_space_compare.py --method cubic
python scripts/run_trajectory_space_compare.py --method quintic
```

### 第六阶段：约束感知和轨迹重定时

```bash
python scripts/run_trajectory_space_compare.py --total_time 5.0
python scripts/run_time_scaling_sweep.py
python scripts/run_time_scaling_sweep.py --total_times 3 5 8 10
```

输出位置：

- `outputs/logs/trajectory_space_compare.csv`
- `outputs/logs/time_scaling_sweep.csv`
- `outputs/figures/trajectory_space_path_compare.png`
- `outputs/figures/trajectory_space_theta_compare.png`
- `outputs/figures/trajectory_space_velocity_compare.png`
- `outputs/figures/trajectory_space_acceleration_compare.png`
- `outputs/figures/time_scaling_velocity_compare.png`
- `outputs/figures/time_scaling_acceleration_compare.png`
- `outputs/figures/time_scaling_metric_summary.png`

### 运行测试

```bash
pytest
```

最近一次记录：`29 passed`。

## 8. 当前测试与验证情况

当前项目存在 `tests/` 目录，并使用 pytest。

主要测试文件：

- `tests/test_kinematics.py`：测试正运动学、雅可比矩阵、可达性判断和解析逆运动学。
- `tests/test_controller.py`：测试普通控制步、阻尼雅可比步、通用迭代仿真历史字段。
- `tests/test_trajectory.py`：测试直线轨迹、圆形轨迹、速度估计、轨迹跟踪历史、IK 起点初始化、resolved-rate 控制、argparse 参数、时间缩放和关节空间轨迹。
- `tests/test_trajectory_metrics.py`：测试路径偏差、关节限制检查和时间历史长度。

已覆盖功能：

- 运动学基础函数。
- 控制器输出形状和基本收敛趋势。
- 轨迹生成形状。
- 轨迹跟踪关键历史字段。
- 第五阶段和第六阶段的部分指标函数。

测试不足：

- 多数脚本没有完整 CLI smoke test。
- 绘图函数只通过脚本间接验证，没有检查图像内容是否符合预期。
- CSV 的字段和数值范围可以增加测试。
- 复杂边界情况不足，例如目标不可达、接近奇异位形、过小/过大 `total_time`、不合理 `num_points`。

根据当前测试和已生成输出，可以判断项目基本可运行，但若要对外展示，建议增加少量脚本级 smoke test。

## 9. 当前输出结果与证据

当前 `outputs/` 中存在较多实验结果文件。

图片输出包括：

- `outputs/arm_pose.png`：机械臂末端到达目标点后的姿态图。
- `outputs/error_curve.png`：目标点控制误差曲线。
- `outputs/joint_curve.png`：目标点控制关节角变化曲线。
- `outputs/figures/workspace.png`：二连杆工作空间图。
- `outputs/figures/gain_*_comparison.png`：不同 `gain` 对误差和关节角的影响。
- `outputs/figures/max_step_*_comparison.png`：不同 `max_step` 对误差和关节角的影响。
- `outputs/figures/damping_*_comparison.png`：不同阻尼系数对阻尼伪逆控制的影响。
- `outputs/figures/pinv_vs_damped_error.png`：普通伪逆和阻尼伪逆误差对比。
- `outputs/figures/pinv_vs_damped_joint_angles.png`：普通伪逆和阻尼伪逆关节角对比。
- `outputs/figures/singularity_error.png`：接近奇异位形时误差变化。
- `outputs/figures/singularity_joint_angles.png`：接近奇异位形时关节角变化。
- `outputs/figures/trajectory_tracking_path.png`：期望轨迹与实际轨迹对比。
- `outputs/figures/trajectory_tracking_error.png`：轨迹跟踪误差曲线。
- `outputs/figures/trajectory_tracking_joint_angles.png`：轨迹跟踪关节角曲线。
- `outputs/figures/trajectory_space_path_compare.png`：期望直线、关节空间路径、笛卡尔跟踪路径对比。
- `outputs/figures/trajectory_space_theta_compare.png`：两种轨迹方式的关节角对比。
- `outputs/figures/trajectory_space_velocity_compare.png`：两种轨迹方式的关节速度对比。
- `outputs/figures/trajectory_space_acceleration_compare.png`：两种轨迹方式的关节加速度对比。
- `outputs/figures/time_scaling_velocity_compare.png`：不同 `total_time` 下速度对比。
- `outputs/figures/time_scaling_acceleration_compare.png`：不同 `total_time` 下加速度对比。
- `outputs/figures/time_scaling_metric_summary.png`：不同 `total_time` 下关键指标汇总。

CSV 输出包括：

- `outputs/logs/parameter_sweep.csv`：参数扫描结果。
- `outputs/logs/trajectory_space_compare.csv`：关节空间轨迹和笛卡尔空间轨迹对比指标。
- `outputs/logs/time_scaling_sweep.csv`：不同总运动时间下的速度、加速度、约束违反和路径偏差指标。

这些输出说明项目已经从“单点控制”发展到“可视化实验对比”。不过，输出文件多为最近一次运行覆盖生成，不一定保留每次实验的参数上下文。后续如果要写报告，建议把关键实验运行命令和对应图片一起记录。

## 10. 当前问题与不足

当前项目主要问题如下：

1. 第六阶段相关文件尚未提交  
   当前 Git 状态显示 `README.md`、`scripts/run_trajectory_space_compare.py`、`src/robot_arm_target_control_study/plotting.py`、`src/robot_arm_target_control_study/simulation.py` 有修改，且 `docs/13_stage6_constraint_aware_trajectory_guide.md`、`docs/14_joint_vs_cartesian_summary.md`、`scripts/run_time_scaling_sweep.py`、`src/robot_arm_target_control_study/utils.py`、`tests/test_trajectory_metrics.py` 为未跟踪文件。建议先审查并提交第六阶段。

2. 运行入口较多  
   项目使用多个 `scripts/run_*.py` 脚本分别运行实验。这对学习清晰，但对外展示时可能显得分散。后续可以保留现有脚本，同时增加一个文档导航或命令索引。

3. 包管理和安装方式较轻量  
   当前有 `requirements.txt`，但没有 `pyproject.toml`。脚本可能通过手动加入 `src` 路径运行。作为学习项目可以接受；若要工程化展示，可考虑标准 Python 包结构。

4. 输出文件会被覆盖  
   多个脚本输出固定文件名，例如 `trajectory_tracking_path.png`。这便于查看最新结果，但不利于保留不同参数实验。后续可增加可选的 `--tag` 或自动带参数的输出文件名。

5. 图像内容缺少自动验证  
   当前测试主要验证函数和数值字段，没有自动检查图像内容。一般学习项目可以接受，但如果后续依赖图像做结论，最好增加 CSV 指标和实验报告来支撑。

6. 文档数量增加，可能需要整理  
   `docs/` 中已有多个阶段学习文档、笔记和模板。后续可以新增 `docs/README.md` 作为文档地图。

7. 当前仍是运动学层面  
   项目没有动力学、力矩、电机、摩擦或真实控制频率建模。因此关于速度和加速度约束的结论属于运动学分析，不应表述成真实机器人动力学验证。

8. 轨迹规划和轨迹跟踪的边界需要持续解释  
   关节空间轨迹是规划好的关节角序列；笛卡尔轨迹跟踪是末端路径跟踪控制。两者容易被初学者混淆，需要在后续文档和实验报告中持续强调。

## 11. 下一阶段建议

### 短期任务

1. 提交第六阶段当前改动  
   为什么做：当前第六阶段文件有未提交状态，交接和回滚都不方便。  
   怎么做：先运行 `pytest`，再查看 `git diff` 和 `git status`，确认无误后提交，例如提交信息可写 `Add stage 6 constraint-aware trajectory analysis`。

2. 整理一份第六阶段实验结果报告  
   为什么做：项目已经能输出图和 CSV，但用户需要把结果转成可解释结论。  
   怎么做：基于 `outputs/logs/trajectory_space_compare.csv` 和 `outputs/logs/time_scaling_sweep.csv`，总结 `total_time` 增大后速度和加速度如何变化、关节空间和笛卡尔空间各自优缺点。

3. 增加 `docs/README.md` 文档导航  
   为什么做：学习文档已经较多，网页端 ChatGPT 或用户接续时容易不知道先看哪个。  
   怎么做：按阶段列出 `05` 到 `14` 的学习文档，每个文件一句话说明用途。

### 中期任务

1. 增加脚本级 smoke test  
   为什么做：当前单元测试较多，但脚本入口是否全部可运行还需要人工验证。  
   怎么做：为关键脚本增加轻量测试，至少检查命令运行成功、输出 CSV 存在、关键列存在。

2. 增加实验输出命名策略  
   为什么做：当前输出图片会覆盖，难以比较多次实验。  
   怎么做：给核心脚本增加可选 `--tag` 参数，把参数名写入输出文件名或单独生成实验文件夹。

3. 写一份“项目简历描述草稿”  
   为什么做：用户明显希望项目可展示，简历表达需要从功能堆叠转成能力证明。  
   怎么做：围绕“实现二连杆机械臂运动学控制与轨迹规划实验平台，比较解析 IK、雅可比控制、阻尼伪逆、resolved-rate 轨迹跟踪、关节空间和笛卡尔空间轨迹约束指标”组织。

### 长期任务

1. 引入更系统的轨迹评价指标  
   为什么做：当前已有速度、加速度、RMS、路径偏差和约束 violation，但还可以增加 jerk、跟踪滞后、最大偏离点等指标。  
   怎么做：在 `utils.py` 中继续新增简单指标，并用 CSV 输出。

2. 做一个轻量交互式展示界面  
   为什么做：当前项目适合学习，但展示时需要反复运行脚本。  
   怎么做：可以先考虑 Jupyter Notebook 或简单 Streamlit，不必上复杂前端。

3. 在完全理解运动学后，再考虑动力学入门  
   为什么做：用户当前项目仍然是运动学控制，贸然上动力学会增加认知负担。  
   怎么做：下一大阶段可只引入非常简单的关节速度限制、加速度限制和 jerk 平滑，不直接上真实力矩控制。

## 12. 建议网页端 ChatGPT 如何继续帮助

下面这段可以直接复制给网页端 ChatGPT：

```text
这是一份由 Codex 扫描当前项目后生成的交接文档。请你先阅读本文档，再继续帮助我维护 robot_arm_target_control_study 项目。

请优先帮助我理解项目逻辑、实验现象和下一步学习路线，而不是直接堆复杂功能。我的目标是通过一个可运行、可解释、可迭代的小项目学习机器人运动学、逆运动学、雅可比控制、轨迹跟踪、轨迹规划、速度/加速度约束和轨迹重定时。

请用适合非纯计算机背景用户理解的方式解释公式、代码和实验图。后续建议请保持“小步迭代、可运行、可验证、可展示”的原则。如果需要让 Codex 改代码，请优先给出清晰、具体、可复制的 Codex 提示词，并说明为什么这样改。
```

