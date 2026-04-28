# 第二阶段学习指示：解析逆运动学与雅可比伪逆对比

## 1. 本阶段学习目标

本阶段的目标是看懂两种逆运动学思路：

- 解析逆运动学：用几何公式直接算出关节角。
- 雅可比伪逆迭代控制：用末端误差一步步修正关节角。

学完后，你应该能解释：为什么同一个目标点可能对应两组关节角，以及为什么迭代控制不一定一步到达目标。

## 2. 本阶段新增文件

- `scripts/run_compare_methods.py`：运行解析逆运动学和雅可比伪逆控制的对比实验。
- `docs/05_stage2_learning_guide.md`：本阶段学习指示文档。
- `outputs/figures/workspace.png`：运行对比脚本后生成的工作空间图。

## 3. 本阶段必须看懂的函数

- `is_target_reachable()`
- `inverse_kinematics_analytic()`
- `forward_kinematics()`
- `compute_jacobian()`
- `compute_control_step()`
- `run_reach_simulation()`
- `plot_workspace()`

## 4. 每个函数的输入、输出、作用

### `is_target_reachable(target_x, target_y, link1, link2)`

输入：目标点坐标和两根连杆长度。

输出：`reachable` 和 `reason`。

作用：判断目标点是否在二连杆机械臂可以到达的环形工作空间内。

### `inverse_kinematics_analytic(target_x, target_y, link1, link2, elbow="down")`

输入：目标点坐标、连杆长度和肘部构型。

输出：`theta1`、`theta2`、`reachable`、`message`。

作用：用余弦定理和几何关系直接求关节角。

### `forward_kinematics(theta1, theta2, link1, link2)`

输入：两个关节角和两根连杆长度。

输出：基座、肘关节、末端执行器三个点的坐标。

作用：验证给定关节角时，机械臂末端在哪里。

### `compute_jacobian(theta1, theta2, link1, link2)`

输入：两个关节角和两根连杆长度。

输出：一个 2 行 2 列的雅可比矩阵。

作用：描述关节角小变化会怎样影响末端位置小变化。

### `compute_control_step(theta, target, end_effector, link1, link2, gain, max_step)`

输入：当前关节角、目标点、当前末端位置、连杆长度和控制参数。

输出：关节角增量、误差向量、误差大小。

作用：把末端误差转换成下一步应该调整的关节角。

### `run_reach_simulation(target, link1, link2, initial_theta, max_steps, tolerance)`

输入：目标点、连杆长度、初始关节角、最大迭代次数和停止阈值。

输出：仿真结果字典，包括最终关节角、末端位置、误差和历史记录。

作用：运行完整的雅可比伪逆迭代控制流程。

### `plot_workspace(link1, link2, save_path)`

输入：两根连杆长度和图片保存路径。

输出：工作空间图片路径。

作用：画出最远可达圆和最近不可达内圆，帮助理解目标点是否可达。

## 5. 建议阅读顺序

1. 先读 `README.md` 的第二阶段小节。
2. 再读 `src/robot_arm_target_control_study/kinematics.py` 中的两个新增函数。
3. 运行 `scripts/run_compare_methods.py`，观察两种方法的输出。
4. 读 `src/robot_arm_target_control_study/simulation.py` 和 `controller.py`，理解迭代法。
5. 最后读 `src/robot_arm_target_control_study/plotting.py` 中的 `plot_workspace()`。

## 6. 验收命令

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
pytest
```

## 7. 常见疑问

### 为什么同一个目标点有 elbow up 和 elbow down 两种结果？

因为二连杆机械臂像人的手臂一样，同一个手的位置可以用“肘部朝上”或“肘部朝下”两种姿态达到。

### 为什么解析逆运动学要先判断可达性？

如果目标点太远或太近，几何上就不存在对应的三角形。继续计算会得到没有物理意义的角度。

### 为什么 `cos_theta2` 要 clip 到 `[-1, 1]`？

计算机浮点数有微小误差，理论上等于 1 的值可能算成 1.0000000002。`arccos` 不能处理超过 1 的输入，所以要先裁剪。

### 为什么雅可比伪逆控制要迭代很多步？

雅可比矩阵描述的是“当前姿态附近”的近似关系。每一步只适合小幅调整，所以需要重复多次。

### 为什么雅可比法可能失败或收敛很慢？

它会受初始关节角、单步最大更新量、控制增益和奇异位形影响。奇异位形可以粗略理解为某些姿态下，关节角变化很难让末端朝想要的方向移动。

## 8. 下一阶段可以做什么

- 增加多目标点批量测试。
- 给对比实验加入 elbow up/down 的可视化。
- 增加机械臂运动动画。
- 支持命令行配置连杆长度、初始角度和迭代参数。
- 继续学习奇异位形、阻尼最小二乘和冗余自由度机械臂。
