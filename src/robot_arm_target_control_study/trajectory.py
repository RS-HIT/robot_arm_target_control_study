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
