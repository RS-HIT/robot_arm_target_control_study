# 下一步任务

## P0：必须先做

### 1. 确认 GitHub 远端和首次推送状态

- 目标：确认本地 `main` 分支是否已经完整推送到目标 GitHub 仓库。
- 涉及文件：无代码文件；涉及 Git 远端配置。
- 预计验证方式：
  - 运行 `git remote -v` 查看远端地址。
  - 运行 `git status -sb` 查看本地分支和远端分支关系。
  - 在用户明确允许后再运行 `git push -u origin main`。

### 2. 保持当前 demo 和测试可运行

- 目标：确保后续修改不会破坏第一阶段 demo 和第二阶段对比实验。
- 涉及文件：
  - `scripts/run_reach_demo.py`
  - `scripts/run_compare_methods.py`
  - `src/robot_arm_target_control_study/`
  - `tests/`
- 预计验证方式：
  - `python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6`
  - `python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6`
  - `pytest`

## P1：重要但可稍后

### 1. 增加解析逆运动学可视化

- 目标：在对比实验中画出解析逆运动学 elbow up/down 两种姿态。
- 涉及文件：
  - `scripts/run_compare_methods.py`
  - `src/robot_arm_target_control_study/plotting.py`
  - `README.md`
- 预计验证方式：
  - 运行 `python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6`。
  - 人工检查输出图片。

### 2. 增加更多目标点测试

- 目标：验证控制器和解析逆运动学对不同目标点的稳定性。
- 涉及文件：
  - `tests/test_controller.py`
  - `tests/test_kinematics.py`
  - `src/robot_arm_target_control_study/simulation.py`
- 预计验证方式：
  - 新增多个可达目标点、不可达目标点和边界目标点测试。
  - 运行 `pytest`。

### 3. 增加命令行参数

- 目标：允许用户通过命令行配置连杆长度、初始关节角、最大迭代次数和误差阈值。
- 涉及文件：
  - `scripts/run_reach_demo.py`
  - `scripts/run_compare_methods.py`
  - `src/robot_arm_target_control_study/simulation.py`
  - `README.md`
- 预计验证方式：
  - 运行带参数的 demo。
  - 检查输出图和终端结果是否符合预期。

### 3. 增加工作空间可视化

- 目标：让用户直观看到二连杆机械臂的可达范围。
- 涉及文件：
  - `src/robot_arm_target_control_study/plotting.py`
  - `scripts/run_reach_demo.py`
  - `README.md`
- 预计验证方式：
  - 生成新的工作空间图片。
  - 人工检查图片是否能表达最大可达半径。

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
