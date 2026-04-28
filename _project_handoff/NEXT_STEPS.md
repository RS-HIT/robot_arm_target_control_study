# 下一步任务

## P0：必须先做

### 1. 确认 GitHub 远端和首次推送状态

- 目标：确认本地 `main` 分支是否已经完整推送到目标 GitHub 仓库。
- 涉及文件：无代码文件；涉及 Git 远端配置。
- 预计验证方式：
  - 运行 `git remote -v` 查看远端地址。
  - 运行 `git status -sb` 查看本地分支和远端分支关系。
  - 在用户明确允许后再运行 `git push -u origin main`。

### 2. 保持当前 demo、实验脚本和测试可运行

- 目标：确保后续修改不会破坏第一阶段 demo、第二阶段对比实验和第三阶段参数实验。
- 涉及文件：
  - `scripts/run_reach_demo.py`
  - `scripts/run_compare_methods.py`
  - `scripts/run_parameter_sweep.py`
  - `scripts/run_damped_jacobian_demo.py`
  - `scripts/run_singularity_demo.py`
  - `src/robot_arm_target_control_study/`
  - `tests/`
- 预计验证方式：
  - `python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6`
  - `python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6`
  - `python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6`
  - `python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05`
  - `python scripts/run_singularity_demo.py`
  - `pytest`

## P1：重要但可稍后

### 1. 整理第三阶段实验报告

- 目标：基于参数扫描 CSV 和曲线图，写出一份正式实验报告。
- 涉及文件：
  - `docs/07_experiment_report_template.md`
  - `outputs/logs/parameter_sweep.csv`
  - `outputs/figures/`
- 预计验证方式：
  - 人工阅读报告，确认结论能对应 CSV 和曲线图。

### 2. 增加更多目标点和初始姿态实验

- 目标：验证参数结论是否只适用于当前目标点和初始姿态。
- 涉及文件：
  - `scripts/run_parameter_sweep.py`
  - `scripts/run_damped_jacobian_demo.py`
  - `tests/test_controller.py`
  - `src/robot_arm_target_control_study/simulation.py`
- 预计验证方式：
  - 新增多个目标点和初始姿态组合。
  - 运行第三阶段实验脚本。
  - 运行 `pytest`。

### 3. 增加命令行参数

- 目标：允许用户通过命令行配置连杆长度、初始关节角、最大迭代次数、误差阈值、参数列表和 damping。
- 涉及文件：
  - `scripts/run_reach_demo.py`
  - `scripts/run_compare_methods.py`
  - `scripts/run_parameter_sweep.py`
  - `scripts/run_damped_jacobian_demo.py`
  - `src/robot_arm_target_control_study/simulation.py`
  - `README.md`
- 预计验证方式：
  - 运行带参数的 demo。
  - 检查输出图和终端结果是否符合预期。

### 4. 增加解析逆运动学可视化

- 目标：在对比实验中画出解析逆运动学 elbow up/down 两种姿态。
- 涉及文件：
  - `scripts/run_compare_methods.py`
  - `src/robot_arm_target_control_study/plotting.py`
  - `README.md`
- 预计验证方式：
  - 运行 `python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6`。
  - 人工检查输出图片。

## P2：优化项

### 1. 增加机械臂运动过程动画

- 目标：展示机械臂从初始姿态逐步靠近目标点的过程。
- 涉及文件：
  - `src/robot_arm_target_control_study/plotting.py`
  - `scripts/run_reach_demo.py`
  - `README.md`
- 预计验证方式：
  - 生成 GIF 或视频文件。
  - 检查 `.gitignore` 是否正确忽略大体积运行输出。

### 2. 精简过长注释

- 目标：让代码更适合 GitHub 阅读，同时保留必要中文解释。
- 涉及文件：
  - `src/robot_arm_target_control_study/plotting.py`
  - `src/robot_arm_target_control_study/kinematics.py`
  - `src/robot_arm_target_control_study/controller.py`
  - `src/robot_arm_target_control_study/simulation.py`
- 预计验证方式：
  - 人工阅读确认注释清晰。
  - 运行 `pytest`。

### 3. 补充配置文件方案

- 目标：决定是否使用 `configs/` 管理默认参数。
- 涉及文件：
  - `configs/`
  - `scripts/run_reach_demo.py`
  - `README.md`
- 预计验证方式：
  - 待确认是否真的需要配置文件。
  - 如果新增配置，运行 demo 和测试确认不破坏现有入口。
