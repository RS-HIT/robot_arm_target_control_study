# 参数实验报告：gain、max_step 与 damping 对控制效果的影响

## 1. 实验目的

本实验用于观察 `gain`、`max_step` 和 `damping` 对二连杆机械臂雅可比控制过程的影响。

重点不是只看最终误差，而是结合误差曲线和关节角曲线判断控制过程是否稳定、是否收敛慢、是否震荡、是否出现关节角突变。

## 2. 实验设置

- 机械臂类型：2D 平面二连杆机械臂
- 连杆长度：`link1=1.0`，`link2=0.8`
- 初始关节角：
- 目标点：
- 最大迭代次数：
- 收敛阈值：
- 控制方法：

## 3. gain 对比实验

### 3.1 固定参数

- 固定 `max_step=0.08`
- 改变 `gain=[0.2, 0.5, 0.8, 1.0, 1.2]`
- 输出图像：
  - `outputs/figures/gain_error_comparison.png`
  - `outputs/figures/gain_theta1_comparison.png`
  - `outputs/figures/gain_theta2_comparison.png`

### 3.2 观察误差曲线

记录不同 `gain` 下误差下降速度、是否震荡、最终是否收敛。

| gain | 下降速度 | 是否震荡 | 最终误差 | 备注 |
| --- | --- | --- | --- | --- |
| 0.2 | 慢 | 小 | 小 |  |
| 0.5 | 快 | 大 | 小 |  |
| 0.8 | 快 | 大 | 小 |  |
| 1.0 | 快 | 大 | 小 |  |
| 1.2 | 快 | 大 | 小 |  |

### 3.3 观察关节角曲线

记录 theta1 和 theta2 是否平滑，是否出现尖峰或锯齿。
theta2均平滑，而theta1中，gain=0.2时较为平滑，而其他数据存在尖峰

### 3.4 结论

gain 太小：末端慢慢爬向目标点
gain 太大：末端可能冲过目标点，来回修正

## 4. max_step 对比实验

### 4.1 固定参数

- 固定 `gain=0.8`
- 改变 `max_step=[0.03, 0.05, 0.08, 0.12]`
- 输出图像：
  - `outputs/figures/max_step_error_comparison.png`
  - `outputs/figures/max_step_theta1_comparison.png`
  - `outputs/figures/max_step_theta2_comparison.png`

### 4.2 观察误差曲线

记录不同 `max_step` 下收敛速度和稳定性。

| max_step | 下降速度 | 是否跳动 | 最终误差 | 备注 |
| --- | --- | --- | --- | --- |
| 0.03 | 最慢 | 有 | 0 |  |
| 0.05 | 慢 | 有 | 0 |  |
| 0.08 | 快 | 有 | 0 |  |
| 0.12 | 最快 | 有 | 0 |  |

### 4.3 观察关节角曲线

不同关节角度变化曲线形状基本相同，变化速度不同。

### 4.4 结论

控制输出限幅
关节速度限制
单步运动安全限制

## 5. damping 对比实验

### 5.1 固定参数

- 固定 `gain=0.8`
- 固定 `max_step=0.08`
- 改变 `damping=[0.01, 0.05, 0.1, 0.3]`
- 输出图像：
  - `outputs/figures/damping_error_comparison.png`
  - `outputs/figures/damping_theta1_comparison.png`
  - `outputs/figures/damping_theta2_comparison.png`

### 5.2 观察误差曲线

记录不同 `damping` 下误差下降速度和接近目标时的稳定性。

| damping | 下降速度 | 是否平滑 | 最终误差 | 备注 |
| --- | --- | --- | --- | --- |
| 0.01 | 快 | 否 | 0 |  |
| 0.05 | 快 | 否 | 0 |  |
| 0.1 | 快 | 否 | 0 |  |
| 0.3 | 慢 | 是 | 0 |  |

### 5.3 观察关节角曲线

重点看阻尼变大后，theta1 和 theta2 更平滑，也因此收敛变慢。

### 5.4 结论

damping 小：接近普通伪逆，快但可能不稳
damping 大：动作更保守，更稳，但可能慢，甚至精度下降

## 6. 和 PID 调参的类比

- `gain` 类似 P 控制中的 `Kp`：误差越大，修正越积极。
- `max_step` 更像输出限幅或速度限制，不是 `Kp`：它限制每一步最多能动多少。
- `damping` 更像数值阻尼、正则化或刹车，用来抑制奇异附近的过大更新，不等同于 PID 的 D 项。

这个类比只能帮助建立直觉，不能把三者完全等同。

## 7. 我目前还不理解的问题

记录你看图后还不清楚的问题：

- 
