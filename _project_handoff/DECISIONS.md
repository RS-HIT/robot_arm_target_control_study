# 技术决策记录

## 2026-04-28

### 决策内容

第一阶段只做 2D 平面二连杆机械臂目标点控制 demo，不引入 MuJoCo、ROS、PyBullet 或强化学习框架。

### 为什么这么做

项目目标是面向机器人算法入门，优先保证代码可以运行、可以测试、可以解释。复杂仿真框架会提高学习门槛，也会分散对正运动学、雅可比矩阵和数值控制的理解。

### 影响到哪些文件或功能

- `README.md`
- `scripts/run_reach_demo.py`
- `src/robot_arm_target_control_study/`
- `tests/`

## 2026-04-28

### 决策内容

目标点控制使用雅可比伪逆迭代方法，不写成解析逆运动学。

### 为什么这么做

当前代码实际实现是 `np.linalg.pinv(jacobian) @ error_vector` 的数值迭代控制。保持这个表述能真实反映代码，也方便后续扩展到更多自由度机械臂。

### 影响到哪些文件或功能

- `src/robot_arm_target_control_study/controller.py`
- `src/robot_arm_target_control_study/simulation.py`
- `README.md`
- `docs/02_interview_questions.md`

## 2026-04-28

### 决策内容

运行时输出图片放在 `outputs/`，GitHub README 展示图片放在 `docs/assets/`。

### 为什么这么做

`outputs/` 会被 demo 反复覆盖，更适合作为本地运行输出目录。`docs/assets/` 中的图片更稳定，适合被 README 引用并提交到 GitHub。

### 影响到哪些文件或功能

- `README.md`
- `docs/assets/`
- `outputs/`
- `.gitignore`

## 2026-04-28

### 决策内容

新增 `_project_handoff/` 目录记录项目交接、当前状态、下一步计划、命令、文件地图、问题和进展日志。

### 为什么这么做

该项目会在本地 IDE、网页端 ChatGPT 和 GitHub 之间流转。交接目录可以降低新对话接手成本，也能避免项目状态只存在聊天记录里。

### 影响到哪些文件或功能

- `_project_handoff/`
- 项目协作流程
- 后续任务规划
