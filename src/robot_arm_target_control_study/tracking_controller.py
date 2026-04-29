"""轨迹跟踪用的简化任务空间控制器。"""

import numpy as np

from robot_arm_target_control_study.controller import limit_joint_step
from robot_arm_target_control_study.kinematics import compute_jacobian, forward_kinematics


def compute_damped_pseudoinverse(jacobian, damping):
    """
    作用：计算雅可比矩阵的阻尼伪逆，用于把末端速度命令转换成关节速度。
    输入：
        jacobian: 形状为 (2, 2) 的雅可比矩阵。
        damping: 阻尼系数，用来减小奇异位形附近的速度放大。
    输出：
        damped_pinv: 形状为 (2, 2) 的阻尼伪逆矩阵。
    """
    identity = np.eye(jacobian.shape[0])
    # J_damped_pinv = J.T @ inv(J @ J.T + lambda^2 I)
    # lambda^2 I 是数值“刹车”，避免接近奇异位形时关节速度被放得过大。
    return jacobian.T @ np.linalg.solve(
        jacobian @ jacobian.T + (damping**2) * identity,
        identity,
    )


def compute_task_space_p_control_step(
    theta,
    desired_xy,
    link1,
    link2,
    gain=0.8,
    max_step=0.08,
):
    """
    作用：使用任务空间 P 控制思想，让末端从当前位置向期望位置移动一步。
    输入：
        theta: 形状为 (2,) 的当前关节角。
        desired_xy: 形状为 (2,) 的期望末端位置。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        gain: P 控制增益，误差越大时修正越积极。
        max_step: 单个关节每一步允许变化的最大弧度。
    输出：
        new_theta: 更新后的关节角。
        current_xy: 当前末端位置。
        error_norm: 当前末端到期望点的距离。
        delta_theta: 本轮关节角更新量。
    """
    theta = np.array(theta, dtype=float)
    desired_xy = np.array(desired_xy, dtype=float)

    positions = forward_kinematics(theta[0], theta[1], link1, link2)
    current_xy = positions[-1]
    error = desired_xy - current_xy
    error_norm = float(np.linalg.norm(error))

    jacobian = compute_jacobian(theta[0], theta[1], link1, link2)
    # P 控制：只根据“当前位置误差”生成末端修正量，再用雅可比伪逆换算成关节角更新。
    delta_theta = gain * np.linalg.pinv(jacobian) @ error
    delta_theta = limit_joint_step(delta_theta, max_step)
    new_theta = theta + delta_theta

    return new_theta, current_xy, error_norm, delta_theta


def compute_task_space_pd_control_step(
    theta,
    prev_error,
    desired_xy,
    desired_velocity,
    link1,
    link2,
    dt,
    kp=0.8,
    kd=0.1,
    max_step=0.08,
):
    """
    作用：使用简化任务空间 PD 控制思想，让机械臂末端跟踪轨迹上的一个期望点。
    输入：
        theta: 形状为 (2,) 的当前关节角。
        prev_error: 上一时刻的末端位置误差。
        desired_xy: 当前期望末端位置。
        desired_velocity: 当前期望末端速度，用作简单前馈项。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        dt: 时间步长。
        kp: P 项增益，根据位置误差进行修正。
        kd: D 项增益，根据误差变化速度抑制过快变化。
        max_step: 单个关节每一步允许变化的最大弧度。
    输出：
        new_theta: 更新后的关节角。
        current_xy: 当前末端位置。
        error_norm: 当前末端到期望点的距离。
        delta_theta: 本轮关节角更新量。
        error: 当前末端位置误差，供下一步计算 D 项使用。

    说明：
        这是用于理解 PD 思想的简化任务空间控制，不包含质量、惯量、力矩等完整动力学。
    """
    theta = np.array(theta, dtype=float)
    prev_error = np.array(prev_error, dtype=float)
    desired_xy = np.array(desired_xy, dtype=float)
    desired_velocity = np.array(desired_velocity, dtype=float)

    positions = forward_kinematics(theta[0], theta[1], link1, link2)
    current_xy = positions[-1]
    error = desired_xy - current_xy
    error_norm = float(np.linalg.norm(error))

    # P 项：根据当前位置误差把末端拉向期望轨迹点。
    p_term = kp * error
    # D 项：根据误差变化速度修正控制量，帮助抑制快速来回摆动。
    error_derivative = (error - prev_error) / dt
    d_term = kd * error_derivative
    # 前馈项：期望轨迹本身有速度时，给控制器一个沿轨迹前进的提示。
    feedforward_term = desired_velocity * dt
    task_space_command = p_term + d_term + feedforward_term

    jacobian = compute_jacobian(theta[0], theta[1], link1, link2)
    delta_theta = np.linalg.pinv(jacobian) @ task_space_command
    delta_theta = limit_joint_step(delta_theta, max_step)
    new_theta = theta + delta_theta

    return new_theta, current_xy, error_norm, delta_theta, error


def compute_resolved_rate_p_step(
    theta,
    desired_xy,
    desired_velocity,
    link1,
    link2,
    dt,
    kp=3.0,
    max_joint_speed=1.5,
    damping=0.05,
):
    """
    作用：使用 resolved-rate P 控制进行一步轨迹跟踪。
    输入：
        theta: 形状为 (2,) 的当前关节角。
        desired_xy: 当前期望末端位置。
        desired_velocity: 当前期望末端速度；纯 P 控制时可传入 [0, 0]。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        dt: 本次控制步长。
        kp: 位置误差增益。
        max_joint_speed: 单个关节允许的最大速度，单位是弧度/秒。
        damping: 阻尼伪逆中的阻尼系数。
    输出：
        new_theta: 更新后的关节角。
        current_xy: 当前末端位置。
        error_norm: 当前末端到期望点的距离。
        q_dot: 本轮关节速度。
        error: 当前末端位置误差。
    """
    theta = np.array(theta, dtype=float)
    desired_xy = np.array(desired_xy, dtype=float)
    desired_velocity = np.array(desired_velocity, dtype=float)

    current_xy = forward_kinematics(theta[0], theta[1], link1, link2)[-1]
    error = desired_xy - current_xy
    error_norm = float(np.linalg.norm(error))
    # resolved-rate 控制先生成末端速度命令，而不是直接生成关节角增量。
    x_dot_cmd = desired_velocity + kp * error

    jacobian = compute_jacobian(theta[0], theta[1], link1, link2)
    q_dot = compute_damped_pseudoinverse(jacobian, damping) @ x_dot_cmd
    q_dot = np.clip(q_dot, -max_joint_speed, max_joint_speed)
    # q_dot 是关节速度，更新角度时必须乘以 dt。
    new_theta = theta + q_dot * dt

    return new_theta, current_xy, error_norm, q_dot, error


def compute_resolved_rate_pd_step(
    theta,
    prev_current_xy,
    desired_xy,
    desired_velocity,
    link1,
    link2,
    dt,
    kp=3.0,
    kd=0.1,
    max_joint_speed=1.5,
    damping=0.05,
):
    """
    作用：使用简化 resolved-rate PD 控制进行一步轨迹跟踪。
    输入：
        theta: 形状为 (2,) 的当前关节角。
        prev_current_xy: 上一步实际末端位置；第一步可为 None。
        desired_xy: 当前期望末端位置。
        desired_velocity: 当前期望末端速度。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        dt: 本次控制步长。
        kp: 位置误差增益。
        kd: 速度误差增益。
        max_joint_speed: 单个关节允许的最大速度，单位是弧度/秒。
        damping: 阻尼伪逆中的阻尼系数。
    输出：
        new_theta: 更新后的关节角。
        current_xy: 当前末端位置。
        error_norm: 当前末端到期望点的距离。
        q_dot: 本轮关节速度。
        position_error: 当前末端位置误差。
        velocity_error: 期望末端速度减去实际末端速度。
    """
    theta = np.array(theta, dtype=float)
    desired_xy = np.array(desired_xy, dtype=float)
    desired_velocity = np.array(desired_velocity, dtype=float)

    current_xy = forward_kinematics(theta[0], theta[1], link1, link2)[-1]
    if prev_current_xy is None:
        actual_velocity = np.zeros(2, dtype=float)
    else:
        actual_velocity = (current_xy - np.array(prev_current_xy, dtype=float)) / dt

    position_error = desired_xy - current_xy
    velocity_error = desired_velocity - actual_velocity
    error_norm = float(np.linalg.norm(position_error))
    # D 项用速度误差，而不是 error_derivative，减少离散轨迹点上的 derivative kick。
    x_dot_cmd = desired_velocity + kp * position_error + kd * velocity_error

    jacobian = compute_jacobian(theta[0], theta[1], link1, link2)
    q_dot = compute_damped_pseudoinverse(jacobian, damping) @ x_dot_cmd
    q_dot = np.clip(q_dot, -max_joint_speed, max_joint_speed)
    new_theta = theta + q_dot * dt

    return new_theta, current_xy, error_norm, q_dot, position_error, velocity_error
