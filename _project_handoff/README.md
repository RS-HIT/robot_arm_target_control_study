# 项目交接总说明

## 项目目标

`robot_arm_target_control_study` 是一个面向机器人算法入门的 2D 平面二连杆机械臂目标点控制 demo。项目目标是用尽量简单、可运行、可测试、可解释的代码，展示机械臂末端如何通过正运动学、雅可比矩阵和雅可比伪逆迭代控制逐步靠近用户输入的目标点。

## 当前阶段

当前处于第一版 GitHub 展示阶段。项目不使用 MuJoCo、ROS、PyBullet 或强化学习框架，只保留一个清晰的小型运动学控制 demo。

## 已经完成的内容

- 实现二连杆机械臂正运动学。
- 实现 2D 二连杆机械臂雅可比矩阵。
- 实现基于雅可比伪逆的目标点迭代控制。
- 实现仿真循环，记录关节角、末端位置和误差。
- 实现三张结果图输出：最终姿态图、误差曲线、关节角变化曲线。
- 实现命令行 demo 入口。
- 实现基础 pytest 测试。
- 整理 GitHub README、代码阅读文档和展示图片。

## 当前可运行入口

运行 demo：

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
```

运行测试：

```bash
pytest
```

## 当前验证结果

在 2026-04-28 验证：

- demo 可以运行并生成 `outputs/arm_pose.png`、`outputs/error_curve.png`、`outputs/joint_curve.png`。
- 目标点 `(1.2, 0.6)` 的最终误差为 `0.002829`，状态为“已到达目标附近”。
- `pytest` 通过，结果为 `5 passed`。

## 下一步建议

建议下一轮优先做两件事：

1. 增加更多目标点和初始姿态测试，确认控制器在不同场景下的稳定性。
2. 支持通过命令行配置连杆长度、初始关节角、最大迭代次数和误差阈值，让 demo 更适合实验展示。

如果把这个项目发给新的 ChatGPT 对话，可以先让它阅读本目录下的 `CURRENT_STATUS.md`、`NEXT_STEPS.md` 和 `FILE_MAP.md`。
