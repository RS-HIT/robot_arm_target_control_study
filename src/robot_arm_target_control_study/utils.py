"""轨迹评估和约束检查工具函数。"""

import numpy as np


def check_joint_limits(
    theta_history,
    velocity_history,
    acceleration_history,
    joint_velocity_limit=1.5,
    joint_acceleration_limit=5.0,
):
    """
    作用：检查关节速度和关节加速度是否超过给定限制。
    输入：
        theta_history: 关节角历史，当前函数保留该输入，便于以后扩展关节角范围检查。
        velocity_history: 关节速度历史，形状通常为 (N, 2)。
        acceleration_history: 关节加速度历史，形状通常为 (N, 2)。
        joint_velocity_limit: 允许的最大关节速度绝对值，单位 rad/s。
        joint_acceleration_limit: 允许的最大关节加速度绝对值，单位 rad/s^2。
    输出：
        result: 字典，包含最大速度、最大加速度、违规次数和违规比例。
    """
    _ = np.array(theta_history, dtype=float)
    velocity = np.array(velocity_history, dtype=float)
    acceleration = np.array(acceleration_history, dtype=float)

    velocity_violation_mask = np.abs(velocity) > joint_velocity_limit
    acceleration_violation_mask = np.abs(acceleration) > joint_acceleration_limit
    velocity_count = int(np.count_nonzero(velocity_violation_mask))
    acceleration_count = int(np.count_nonzero(acceleration_violation_mask))
    velocity_total = int(velocity.size) if velocity.size else 1
    acceleration_total = int(acceleration.size) if acceleration.size else 1

    return {
        "max_joint_velocity": float(np.max(np.abs(velocity))) if velocity.size else 0.0,
        "max_joint_acceleration": float(np.max(np.abs(acceleration))) if acceleration.size else 0.0,
        "velocity_violation_count": velocity_count,
        "acceleration_violation_count": acceleration_count,
        "velocity_violation_ratio": float(velocity_count / velocity_total),
        "acceleration_violation_ratio": float(acceleration_count / acceleration_total),
    }


def compute_path_deviation_from_line(path, start_xy, goal_xy):
    """
    作用：计算一条末端路径相对起点-终点直线的平均偏差和最大偏差。
    输入：
        path: 形状为 (N, 2) 的末端路径。
        start_xy: 直线起点坐标。
        goal_xy: 直线终点坐标。
    输出：
        result: 字典，包含 mean_deviation 和 max_deviation。
    """
    path = np.array(path, dtype=float)
    start_xy = np.array(start_xy, dtype=float)
    goal_xy = np.array(goal_xy, dtype=float)
    line_vector = goal_xy - start_xy
    line_length = float(np.linalg.norm(line_vector))

    if len(path) == 0 or line_length == 0.0:
        return {"mean_deviation": 0.0, "max_deviation": 0.0}

    # 二维点到直线距离：|cross(line_vector, point-start)| / |line_vector|。
    offsets = path - start_xy
    cross_values = line_vector[0] * offsets[:, 1] - line_vector[1] * offsets[:, 0]
    distances = np.abs(cross_values) / line_length

    return {
        "mean_deviation": float(np.mean(distances)),
        "max_deviation": float(np.max(distances)),
    }
