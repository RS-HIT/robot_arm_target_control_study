# 第三阶段学习指示：参数敏感性、奇异位形与阻尼雅可比

## 1. 本阶段学习目标

本阶段目标是理解普通雅可比伪逆控制的参数敏感性，以及为什么接近奇异位形时需要阻尼最小二乘方法。

你需要能回答三个问题：

- `gain` 和 `max_step` 改变后，收敛速度和稳定性会怎样变化？
- 机械臂接近伸直边界时，普通雅可比伪逆为什么可能不稳定？
- 阻尼最小二乘为什么能让关节角更新更平滑？

## 2. 本阶段新增文件

- `scripts/run_parameter_sweep.py`：扫描多组 `gain` 和 `max_step`。
- `scripts/run_damped_jacobian_demo.py`：对比普通伪逆和阻尼雅可比。
- `scripts/run_singularity_demo.py`：演示接近伸直边界时的控制表现。
- `docs/06_stage3_experiment_guide.md`：本阶段学习指示。
- `docs/07_experiment_report_template.md`：实验记录模板。

## 3. 必须看懂的函数

- `compute_control_step()`
- `compute_damped_jacobian_step()`
- `simulate_iterative_control()`
- `plot_multiple_error_curves()`
- `plot_multiple_joint_curves()`

其中最重要的是 `compute_damped_jacobian_step()`，它是第三阶段新增算法的核心。

## 4. 推荐阅读顺序

1. 先读 `README.md` 的第三阶段说明。
2. 再读 `src/robot_arm_target_control_study/controller.py`。
3. 对比 `compute_control_step()` 和 `compute_damped_jacobian_step()`。
4. 读 `src/robot_arm_target_control_study/simulation.py` 里的 `simulate_iterative_control()`。
5. 运行三个实验脚本，看终端输出和图像。
6. 用 `docs/07_experiment_report_template.md` 写一份自己的实验记录。

## 5. 参数实验怎么做

运行：

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
```

程序会自动测试多组参数，并保存：

```text
outputs/logs/parameter_sweep.csv
```

读表格时重点看：

- 哪些参数组合 `success=True`。
- 哪些参数组合 `iterations` 更少。
- 哪些参数组合 `final_error` 更小。

## 6. 如何理解 gain、max_step、damping

`gain`：控制增益，表示每次修正误差时有多积极。

- 太小：动作保守，收敛可能慢。
- 太大：动作激进，可能振荡或来回跳。

`max_step`：单个关节每一步最多能变化多少弧度。

- 太小：稳定但慢。
- 太大：更快但可能不平滑。

`damping`：阻尼系数，也常写作 lambda。

- 太小：更接近普通伪逆。
- 适中：接近奇异位形时更稳定。
- 太大：更新过于保守，可能收敛变慢。

## 7. 如何读图

### 7.1 误差曲线怎么看

误差曲线横轴是迭代次数，纵轴是末端距离目标点的距离。

可以重点观察：

- 曲线是否整体下降。
- 是否有明显振荡。
- 是否很快进入平稳但误差较大的状态。
- 普通伪逆和阻尼雅可比谁更平滑。

读图时可以这样判断：

- 下降快：前期响应快。
- 平滑下降：控制稳定，参数比较合适。
- 下降很慢：参数过保守，可能是 `gain` 太小或 `max_step` 太小。
- 上下波动：可能震荡，参数可能过激进。
- 长时间不下降：可能接近奇异位形、目标不可达，或控制参数不合适。
- 最终误差不小：可能未收敛、目标不可达，或当前参数组合不合适。

参数扫描脚本会额外生成固定单参数的对比图：

- `gain_error_comparison.png`：固定 `max_step=0.08`，只比较不同 `gain`。
- `max_step_error_comparison.png`：固定 `gain=0.8`，只比较不同 `max_step`。
- `damping_error_comparison.png`：固定其他参数，只比较不同 `damping`。

这样读图时更容易判断“到底是谁影响了收敛过程”。

### 7.2 关节角曲线怎么看

关节角曲线横轴是迭代次数，纵轴是关节角大小，单位是弧度。

读图时可以这样判断：

- 平滑变化：动作自然。
- 突然尖峰：关节角更新过大。
- 高频锯齿：控制可能震荡。
- 曲线很平但误差下降慢：控制太保守。
- 某个关节变化特别大：该关节承担了主要运动。

第三阶段会分别输出 theta1 和 theta2 的对比图。分开看更清楚，因为两个关节的变化幅度可能差很多。

## 8. 什么是奇异位形

奇异位形可以先粗略理解为：机械臂处在某些特殊姿态时，关节角变化很难让末端朝某些方向移动。

对二连杆平面机械臂来说，机械臂几乎完全伸直或完全折叠时，就容易接近奇异位形。此时雅可比矩阵会变得不稳定，普通伪逆可能给出很大的关节角更新。

## 9. 什么是阻尼最小二乘

阻尼最小二乘是一种更稳的雅可比控制方法。它使用：

```text
delta_theta = J.T @ inv(J @ J.T + damping^2 * I) @ error
```

其中 `damping^2 * I` 像一个缓冲项，可以减少接近奇异位形时过大的关节角更新。

它不是让误差瞬间消失，而是用更稳、更平滑的方式逼近目标。

## 10. 本阶段验收命令

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
python scripts/run_singularity_demo.py
pytest
```

## 11. 下一阶段学习建议

- 尝试不同初始关节角，观察是否影响收敛。
- 给参数扫描增加更多目标点。
- 对比不同 `damping` 的效果。
- 增加机械臂运动动画。
- 学习阻尼最小二乘和奇异值分解之间的关系。
