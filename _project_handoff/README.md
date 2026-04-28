# 项目交接总说明

## 项目目标

`robot_arm_target_control_study` 是一个面向机器人算法入门的 2D 平面二连杆机械臂目标点控制 demo。项目目标是用尽量简单、可运行、可测试、可解释的代码，展示机械臂末端如何通过正运动学、雅可比矩阵和雅可比伪逆迭代控制逐步靠近用户输入的目标点。

## 当前阶段

当前处于第三阶段实验版。项目仍不使用 MuJoCo、ROS、PyBullet 或强化学习框架，重点从“能跑通目标点控制”扩展到“能比较解析逆运动学、普通雅可比伪逆、阻尼雅可比以及参数敏感性”。

## 已经完成的内容

- 实现二连杆机械臂正运动学。
- 实现 2D 二连杆机械臂雅可比矩阵。
- 实现基于雅可比伪逆的目标点迭代控制。
- 实现解析逆运动学，用于和雅可比伪逆迭代控制做对比。
- 实现阻尼雅可比控制，用于观察接近奇异位形时的稳定性。
- 实现参数扫描实验，比较不同 `gain`、`max_step` 和 `damping` 的影响。
- 实现仿真循环，记录关节角、末端位置和误差。
- 实现三张结果图输出：最终姿态图、误差曲线、关节角变化曲线。
- 实现工作空间图输出，展示最远可达圆和最近不可达内圆。
- 实现多组误差曲线和关节角曲线对比输出。
- 实现命令行 demo 入口。
- 实现解析逆运动学与雅可比伪逆对比入口。
- 实现参数扫描、阻尼雅可比对比和奇异位形实验入口。
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

运行第二阶段对比实验：

```bash
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
```

运行第三阶段实验：

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
python scripts/run_singularity_demo.py
```

## 当前验证结果

在 2026-04-28 验证：

- demo 可以运行并生成 `outputs/arm_pose.png`、`outputs/error_curve.png`、`outputs/joint_curve.png`。
- 目标点 `(1.2, 0.6)` 的最终误差为 `0.002829`，状态为“已到达目标附近”。
- 对比脚本可以运行并生成 `outputs/figures/workspace.png`。
- 第三阶段脚本可以生成参数扫描 CSV 和多张对比曲线图。
- `pytest` 通过，测试数量以当前测试输出为准。

## 下一步建议

建议下一轮优先做两件事：

1. 把 `outputs/logs/parameter_sweep.csv` 中的结果整理成一份正式实验报告。
2. 给参数扫描增加更多目标点和初始姿态组合，观察参数结论是否稳定。

如果把这个项目发给新的 ChatGPT 对话，可以先让它阅读本目录下的 `CURRENT_STATUS.md`、`NEXT_STEPS.md` 和 `FILE_MAP.md`。
