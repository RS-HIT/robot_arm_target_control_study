"""机械臂目标点控制的仿真循环。"""

import numpy as np

from robot_arm_target_control_study.controller import compute_control_step
from robot_arm_target_control_study.kinematics import forward_kinematics


def create_empty_history():
    """
    作用：创建用于记录仿真过程的字典。
    输入：
        无。
    输出：
        history: 字典，保存关节角、末端位置和误差曲线。
    """
    return {
        "theta1": [],
        "theta2": [],
        "end_x": [],
        "end_y": [],
        "error": [],
    }


def record_history(history, theta, end_effector, error_norm):
    """
    作用：把当前一步的关节角、末端位置和误差保存下来。
    输入：
        history: 记录仿真过程的字典。
        theta: 形状为 (2,) 的数组，当前关节角。
        end_effector: 形状为 (2,) 的数组，当前末端坐标。
        error_norm: 浮点数，当前末端误差。
    输出：
        无。函数会直接更新 history。
    """
    # 实例化字典的列表，保存当前的关节角、末端位置和误差值
    history["theta1"].append(float(theta[0]))
    history["theta2"].append(float(theta[1]))
    history["end_x"].append(float(end_effector[0]))
    history["end_y"].append(float(end_effector[1]))
    history["error"].append(float(error_norm))


def run_reach_simulation(
    target,
    link1=1.0,
    link2=0.8,
    initial_theta=(0.3, 0.3),
    max_steps=200,
    tolerance=0.01,
):
    """
    作用：运行二连杆机械臂追踪目标点的完整迭代仿真。
    输入：
        target: 形状为 (2,) 的数组，目标点坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        initial_theta: 长度为 2 的元组，初始关节角。
        max_steps: 最大迭代次数。
        tolerance: 判断“到达目标附近”的误差阈值。
    输出：
        result: 字典，包含最终姿态、误差、是否到达和历史记录。
    """
    theta = np.array(initial_theta, dtype=float)
    target = np.array(target, dtype=float)
    history = create_empty_history()

    reached = False
    final_positions = None
    final_error = None

    for _ in range(max_steps):
        positions = forward_kinematics(theta[0], theta[1], link1, link2)
        # 最后一个参数，末端坐标
        end_effector = positions[-1]
        # 平方和开方，求位置欧氏距离
        error_norm = float(np.linalg.norm(target - end_effector))
        # 记录数据到 history 中，方便后续分析和绘图
        record_history(history, theta, end_effector, error_norm)
        # 每次迭代都更新 final_positions 和 final_error，这样即使没有完全达到目标，我们也能知道最后的状态和误差。
        final_positions = positions
        final_error = error_norm

        if error_norm <= tolerance:
            reached = True
            break
        # 获得变化角度，暂未传递矢量和距离
        delta_theta, _, _ = compute_control_step(
            theta=theta,
            target=target,
            end_effector=end_effector,
            link1=link1,
            link2=link2,
        )
        theta = theta + delta_theta

    return {
        "target": target,
        "theta": theta,
        "positions": final_positions,
        "final_error": final_error,
        "reached": reached,
        "history": history,
        "link1": link1,
        "link2": link2,
        "tolerance": tolerance,
    }
