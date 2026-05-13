"""二维末端轨迹生成工具。"""

import numpy as np


def generate_line_trajectory(start_xy, end_xy, num_points):
    """
    作用：生成从起点到终点的二维直线轨迹。
    输入：
        start_xy: 起点坐标，例如 [0.8, 0.4]。
        end_xy: 终点坐标，例如 [1.2, 0.6]。
        num_points: 轨迹点数量。
    输出：
        trajectory: 形状为 (num_points, 2) 的 numpy 数组，每一行是一个期望末端位置。
    """
    start_xy = np.array(start_xy, dtype=float)
    end_xy = np.array(end_xy, dtype=float)
    return np.linspace(start_xy, end_xy, num_points)


def generate_circle_trajectory(center_xy, radius, num_points):
    """
    作用：生成二维圆形轨迹。
    输入：
        center_xy: 圆心坐标，例如 [0.9, 0.4]。
        radius: 圆半径。
        num_points: 轨迹点数量。
    输出：
        trajectory: 形状为 (num_points, 2) 的 numpy 数组，每一行是圆上的一个期望末端位置。
    """
    center_xy = np.array(center_xy, dtype=float)
    angles = np.linspace(0.0, 2.0 * np.pi, num_points, endpoint=False)
    x = center_xy[0] + radius * np.cos(angles)
    y = center_xy[1] + radius * np.sin(angles)
    return np.column_stack([x, y])


def compute_trajectory_velocity(trajectory, dt):
    """
    作用：根据相邻轨迹点的差分，估计每个轨迹点的期望速度。
    输入：
        trajectory: 形状为 (N, 2) 的轨迹点数组。
        dt: 时间步长，表示相邻两个轨迹点之间的时间间隔。
    输出：
        velocity: 形状为 (N, 2) 的速度数组，每一行是对应轨迹点的速度估计。
    """
    trajectory = np.array(trajectory, dtype=float)
    velocity = np.zeros_like(trajectory)

    if len(trajectory) == 0:
        return velocity
    if len(trajectory) == 1:
        return velocity

    # 第一个点没有前一个点，所以用 forward difference：下一点减当前点。
    velocity[0] = (trajectory[1] - trajectory[0]) / dt
    # 中间点用中心差分：后一点减前一点，再除以 2dt，速度估计更平滑。
    if len(trajectory) > 2:
        velocity[1:-1] = (trajectory[2:] - trajectory[:-2]) / (2.0 * dt)
    # 最后一个点没有后一个点，所以用 backward difference：当前点减前一点。
    velocity[-1] = (trajectory[-1] - trajectory[-2]) / dt

    return velocity


def cubic_time_scaling(num_points):
    """
    作用：生成三次时间缩放曲线 s(t)，让参数从 0 平滑变化到 1。
    输入：
        num_points: 时间缩放曲线的采样点数量。
    输出：
        s: 形状为 (num_points,) 的数组，满足起点为 0、终点为 1，且起点和终点速度为 0。
    """
    tau = np.linspace(0.0, 1.0, num_points)
    return 3.0 * tau**2 - 2.0 * tau**3


def quintic_time_scaling(num_points):
    """
    作用：生成五次时间缩放曲线 s(t)，让参数从 0 更平滑地变化到 1。
    输入：
        num_points: 时间缩放曲线的采样点数量。
    输出：
        s: 形状为 (num_points,) 的数组，满足起点为 0、终点为 1，起终点速度和加速度都尽量为 0。

    说明：
        三次时间缩放能让起点和终点速度为 0；五次时间缩放进一步让起点和终点加速度也更平滑。
    """
    tau = np.linspace(0.0, 1.0, num_points)
    return 10.0 * tau**3 - 15.0 * tau**4 + 6.0 * tau**5


def generate_joint_space_trajectory(start_theta, goal_theta, num_points, method="quintic"):
    """
    作用：在关节空间中生成从 start_theta 到 goal_theta 的平滑关节角轨迹。
    输入：
        start_theta: 起始关节角，形状为 (2,)。
        goal_theta: 目标关节角，形状为 (2,)。
        num_points: 轨迹点数量。
        method: 时间缩放方法，可选 "linear"、"cubic"、"quintic"。
    输出：
        theta_trajectory: 形状为 (num_points, 2) 的关节角轨迹。
    """
    start_theta = np.array(start_theta, dtype=float)
    goal_theta = np.array(goal_theta, dtype=float)

    if method == "linear":
        s = np.linspace(0.0, 1.0, num_points)
    elif method == "cubic":
        s = cubic_time_scaling(num_points)
    elif method == "quintic":
        s = quintic_time_scaling(num_points)
    else:
        raise ValueError('method 只能是 "linear"、"cubic" 或 "quintic"。')

    # s(t) 是从 0 到 1 的进度条：0 表示起点，1 表示终点。
    # 用同一个 s(t) 同时插值两个关节角，就得到关节空间轨迹。
    return start_theta + s[:, None] * (goal_theta - start_theta)


def compute_discrete_velocity(values, dt):
    """
    作用：对一串位置或角度序列做差分，计算离散速度。
    输入：
        values: 形状可以是 (N,) 或 (N, 2) 的位置/角度序列。
        dt: 时间步长。
    输出：
        velocity: 与 values 形状相同的速度估计数组。
    """
    values = np.array(values, dtype=float)
    velocity = np.zeros_like(values)

    if len(values) == 0:
        return velocity
    if len(values) == 1:
        return velocity

    velocity[0] = (values[1] - values[0]) / dt
    if len(values) > 2:
        velocity[1:-1] = (values[2:] - values[:-2]) / (2.0 * dt)
    velocity[-1] = (values[-1] - values[-2]) / dt
    return velocity


def compute_discrete_acceleration(values, dt):
    """
    作用：对位置、速度或角度序列做二次差分，计算离散加速度。
    输入：
        values: 形状可以是 (N,) 或 (N, 2) 的序列。
        dt: 时间步长。
    输出：
        acceleration: 与 values 形状相同的加速度估计数组。
    """
    velocity = compute_discrete_velocity(values, dt)
    return compute_discrete_velocity(velocity, dt)
