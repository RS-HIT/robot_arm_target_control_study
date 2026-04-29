"""机械臂目标点控制的仿真循环。"""

import numpy as np

from robot_arm_target_control_study.controller import compute_control_step
from robot_arm_target_control_study.kinematics import forward_kinematics
from robot_arm_target_control_study.tracking_controller import (
    compute_task_space_p_control_step,
    compute_task_space_pd_control_step,
    compute_resolved_rate_p_step,
    compute_resolved_rate_pd_step,
)


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


def simulate_iterative_control(
    control_method,
    initial_theta,
    target,
    link1,
    link2,
    max_iterations,
    tolerance,
    **control_params,
):
    """
    作用：用指定控制方法运行通用迭代仿真，便于比较普通伪逆和阻尼雅可比控制。
    输入：
        control_method: 控制函数，可以是 compute_control_step 或 compute_damped_jacobian_step。
        initial_theta: 长度为 2 的初始关节角。
        target: 形状为 (2,) 的目标点坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        max_iterations: 最大迭代次数。
        tolerance: 判断到达目标附近的误差阈值。
        control_params: 传给控制函数的参数，例如 gain、max_step、damping。
    输出：
        history: 字典，包含关节角历史、末端位置历史、误差历史、是否成功、迭代次数和最终误差。
    """
    theta = np.array(initial_theta, dtype=float)
    target = np.array(target, dtype=float)

    theta_history = []
    end_effector_history = []
    error_history = []
    success = False
    final_error = None

    for iteration in range(max_iterations):
        positions = forward_kinematics(theta[0], theta[1], link1, link2)
        end_effector = positions[-1]
        error_norm = float(np.linalg.norm(target - end_effector))

        theta_history.append(theta.copy())
        end_effector_history.append(end_effector.copy())
        error_history.append(error_norm)
        final_error = error_norm

        if error_norm <= tolerance:
            success = True
            break

        if control_method is compute_control_step:
            # 兼容第一阶段已有的普通雅可比伪逆控制函数：
            # 它返回的是 delta_theta，所以这里需要手动把增量加到当前关节角上。
            delta_theta, _, _ = control_method(
                theta=theta,
                target=target,
                end_effector=end_effector,
                link1=link1,
                link2=link2,
                **control_params,
            )
            theta = theta + delta_theta
        else:
            # 新增的阻尼控制函数直接返回 new_theta，便于实验脚本使用。
            theta, _, _ = control_method(
                theta=theta,
                target=target,
                link1=link1,
                link2=link2,
                **control_params,
            )

    return {
        "theta_history": theta_history,
        "end_effector_history": end_effector_history,
        "error_history": error_history,
        "success": success,
        "iterations": len(error_history),
        "final_error": final_error,
        "target": target,
        "final_theta": theta,
        "link1": link1,
        "link2": link2,
        "tolerance": tolerance,
    }


def simulate_trajectory_tracking(
    controller_type,
    initial_theta,
    desired_trajectory,
    desired_velocity,
    link1,
    link2,
    dt,
    control_params,
    inner_steps=5,
):
    """
    作用：让机械臂末端逐点跟踪一条期望轨迹。
    输入：
        controller_type: 字符串，"p" 表示纯 P，"p_ff" 表示 P 加速度前馈，"pd" 表示简化 resolved-rate PD。
        initial_theta: 长度为 2 的初始关节角。
        desired_trajectory: 形状为 (N, 2) 的期望末端轨迹。
        desired_velocity: 形状为 (N, 2) 的期望末端速度。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        dt: 时间步长。
        control_params: 控制参数字典，例如 gain、kp、kd、max_step。
        inner_steps: 每个轨迹点内部执行的小步控制次数。
    输出：
        history: 字典，包含期望轨迹、实际轨迹、关节角历史、误差历史、平均误差和最大误差。
    """
    theta = np.array(initial_theta, dtype=float)
    desired_trajectory = np.array(desired_trajectory, dtype=float)
    desired_velocity = np.array(desired_velocity, dtype=float)

    actual_trajectory = []
    expanded_desired_trajectory = []
    theta_history = []
    error_history = []
    desired_xy_history = []
    current_xy_history = []
    q_dot_history = []
    q_dot_clipped_history = []
    position_error_history = []
    velocity_error_history = []
    prev_current_xy = None
    max_joint_speed = control_params.get("max_joint_speed", 1.5)
    dt_inner = dt / inner_steps

    for desired_xy, velocity_xy in zip(desired_trajectory, desired_velocity):
        for _ in range(inner_steps):
            if controller_type == "p":
                step_velocity = np.zeros(2, dtype=float)
                theta, _, _, q_dot, position_error = compute_resolved_rate_p_step(
                    theta=theta,
                    desired_xy=desired_xy,
                    desired_velocity=step_velocity,
                    link1=link1,
                    link2=link2,
                    dt=dt_inner,
                    kp=control_params.get("kp", control_params.get("gain", 3.0)),
                    max_joint_speed=max_joint_speed,
                    damping=control_params.get("damping", 0.05),
                )
                velocity_error = step_velocity
            elif controller_type == "p_ff":
                theta, _, _, q_dot, position_error = compute_resolved_rate_p_step(
                    theta=theta,
                    desired_xy=desired_xy,
                    desired_velocity=velocity_xy,
                    link1=link1,
                    link2=link2,
                    dt=dt_inner,
                    kp=control_params.get("kp", control_params.get("gain", 3.0)),
                    max_joint_speed=max_joint_speed,
                    damping=control_params.get("damping", 0.05),
                )
                velocity_error = velocity_xy
            elif controller_type == "pd":
                (
                    theta,
                    _,
                    _,
                    q_dot,
                    position_error,
                    velocity_error,
                ) = compute_resolved_rate_pd_step(
                    theta=theta,
                    prev_current_xy=prev_current_xy,
                    desired_xy=desired_xy,
                    desired_velocity=velocity_xy,
                    link1=link1,
                    link2=link2,
                    dt=dt_inner,
                    kp=control_params.get("kp", 3.0),
                    kd=control_params.get("kd", 0.05),
                    max_joint_speed=max_joint_speed,
                    damping=control_params.get("damping", 0.05),
                )
            else:
                raise ValueError('controller_type 只能是 "p"、"p_ff" 或 "pd"。')

            updated_xy = forward_kinematics(theta[0], theta[1], link1, link2)[-1]
            updated_error_vector = desired_xy - updated_xy
            updated_error = float(np.linalg.norm(updated_error_vector))
            q_dot_clipped = bool(np.any(np.isclose(np.abs(q_dot), max_joint_speed)))

            expanded_desired_trajectory.append(desired_xy.copy())
            actual_trajectory.append(updated_xy.copy())
            desired_xy_history.append(desired_xy.copy())
            current_xy_history.append(updated_xy.copy())
            theta_history.append(theta.copy())
            error_history.append(updated_error)
            q_dot_history.append(q_dot.copy())
            q_dot_clipped_history.append(q_dot_clipped)
            position_error_history.append(updated_error_vector.copy())
            velocity_error_history.append(np.array(velocity_error, dtype=float).copy())
            prev_current_xy = updated_xy.copy()

    error_array = np.array(error_history, dtype=float)
    average_error = float(np.mean(error_array)) if len(error_array) > 0 else 0.0
    max_error = float(np.max(error_array)) if len(error_array) > 0 else 0.0

    return {
        "desired_trajectory": np.array(expanded_desired_trajectory, dtype=float),
        "original_desired_trajectory": desired_trajectory,
        "actual_trajectory": np.array(actual_trajectory, dtype=float),
        "theta_history": theta_history,
        "error_history": error_history,
        "desired_xy": desired_xy_history,
        "current_xy": current_xy_history,
        "error_norm": error_history,
        "theta": theta_history,
        "q_dot": q_dot_history,
        "q_dot_clipped": q_dot_clipped_history,
        "q_dot_clipped_count": int(sum(q_dot_clipped_history)),
        "position_error": position_error_history,
        "velocity_error": velocity_error_history,
        "success": average_error < 0.05,
        "average_error": average_error,
        "max_error": max_error,
        "final_error": float(error_history[-1]) if error_history else 0.0,
        "controller_type": controller_type,
        "dt": dt,
        "inner_steps": inner_steps,
    }
