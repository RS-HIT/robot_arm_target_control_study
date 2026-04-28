# 当前项目状态

## 已经完成的功能

- 2D 平面二连杆机械臂建模。
- 正运动学计算：
  - 基座位置。
  - 肘关节位置。
  - 末端执行器位置。
- 雅可比矩阵计算。
- 雅可比伪逆目标点控制。
- 阻尼雅可比目标点控制。
- 解析逆运动学计算，支持 `elbow="down"` 和 `elbow="up"` 两种构型。
- 目标点可达性判断。
- 单步关节角更新限幅，降低数值跳变风险。
- 仿真循环和历史记录。
- 最终姿态图、误差曲线、关节角变化曲线输出。
- 工作空间图输出。
- 多组参数和多种控制方法的误差曲线、关节角曲线对比输出。
- 参数扫描 CSV 输出。
- 命令行输入目标点。
- 解析逆运动学与雅可比伪逆迭代控制对比脚本。
- 参数扫描脚本。
- 普通伪逆与阻尼雅可比对比脚本。
- 接近奇异位形实验脚本。
- 基础自动化测试。
- GitHub 首页 README 和展示图片整理。

## 目前能跑通的脚本

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
```

作用：运行默认二连杆机械臂目标点控制 demo，并输出三张结果图。

```bash
pytest
```

作用：运行当前测试集，验证正运动学和控制仿真基础行为。

```bash
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
```

作用：对比解析逆运动学和雅可比伪逆迭代控制，并输出工作空间图。

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
```

作用：扫描多组 `gain` 和 `max_step`，输出 CSV 和参数对比曲线。

```bash
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
```

作用：对比普通雅可比伪逆和阻尼雅可比控制。

```bash
python scripts/run_singularity_demo.py
```

作用：演示接近机械臂最大伸展边界时的普通伪逆和阻尼雅可比差异。

## 当前结果

2026-04-28 本地验证结果：

- demo 运行成功。
- 目标点：`(1.2, 0.6)`。
- 最终末端位置：`(1.202, 0.598)`。
- 最终误差：`0.002829`。
- 状态：已到达目标附近。
- 输出图片：
  - `outputs/arm_pose.png`
  - `outputs/error_curve.png`
  - `outputs/joint_curve.png`
- 对比脚本输出工作空间图片：
  - `outputs/figures/workspace.png`
- 第三阶段实验输出：
  - `outputs/logs/parameter_sweep.csv`
  - `outputs/figures/gain_*_comparison.png`
  - `outputs/figures/max_step_*_comparison.png`
  - `outputs/figures/damping_*_comparison.png`
  - `outputs/figures/pinv_vs_damped_*.png`
  - `outputs/figures/singularity_*.png`
- 阻尼对比实验目标点：`(1.75, 0.05)`。
- 普通伪逆最终误差：`0.002706`，迭代步数：`10`。
- 阻尼伪逆最终误差：`0.002163`，迭代步数：`10`。
- 测试结果：`12 passed`。

## 已知限制

- 只支持 2D 平面二连杆机械臂。
- 第一阶段主 demo 仍是雅可比伪逆迭代控制；第二阶段新增解析逆运动学只用于对比实验；第三阶段新增阻尼雅可比和参数实验。
- 未实现 3D 机械臂。
- 未实现动力学控制。
- 未接入 MuJoCo、ROS、PyBullet 或强化学习框架。
- 未实现障碍物避障。
- 当前命令行仍主要只能输入目标点，连杆长度、初始关节角、迭代步数、误差阈值和参数列表还不能直接通过命令行配置。
- `configs/` 目录当前为空，后续是否使用配置文件待确认。
- 仓库已连接远端 `origin`，但最终推送状态和远端权限待确认。
