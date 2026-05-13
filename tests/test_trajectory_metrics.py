"""测试轨迹指标和约束检查工具。"""

import numpy as np

from robot_arm_target_control_study.simulation import simulate_trajectory_tracking
from robot_arm_target_control_study.trajectory import (
    compute_trajectory_velocity,
    generate_line_trajectory,
)
from robot_arm_target_control_study.utils import (
    check_joint_limits,
    compute_path_deviation_from_line,
)


def test_compute_path_deviation_from_line_zero():
    """
    作用：完全落在直线上的路径，平均偏差和最大偏差应接近 0。
    输入：
        无，测试内部生成一条直线路径。
    输出：
        无，通过断言判断偏差。
    """
    path = generate_line_trajectory([0.0, 0.0], [1.0, 1.0], 10)
    result = compute_path_deviation_from_line(path, [0.0, 0.0], [1.0, 1.0])

    assert np.isclose(result["mean_deviation"], 0.0)
    assert np.isclose(result["max_deviation"], 0.0)


def test_compute_path_deviation_from_line_nonzero():
    """
    作用：偏离直线的点，路径偏差应大于 0。
    输入：
        无，测试内部给定一个偏离直线的路径。
    输出：
        无，通过断言判断偏差。
    """
    path = np.array([[0.0, 0.0], [0.5, 0.2], [1.0, 0.0]])
    result = compute_path_deviation_from_line(path, [0.0, 0.0], [1.0, 0.0])

    assert result["mean_deviation"] > 0.0
    assert result["max_deviation"] > 0.0


def test_check_joint_limits_fields():
    """
    作用：检查关节速度和加速度约束检查结果是否包含关键字段。
    输入：
        无，测试内部给定简单关节历史、速度和加速度。
    输出：
        无，通过断言判断字段完整性。
    """
    theta = np.zeros((5, 2))
    velocity = np.array([[0.0, 0.0], [2.0, 0.1], [0.2, 0.3], [0.1, 0.2], [0.0, 0.0]])
    acceleration = np.array([[0.0, 0.0], [6.0, 0.1], [0.2, 0.3], [0.1, 0.2], [0.0, 0.0]])
    result = check_joint_limits(theta, velocity, acceleration, 1.5, 5.0)

    assert "max_joint_velocity" in result
    assert "max_joint_acceleration" in result
    assert "velocity_violation_count" in result
    assert "acceleration_violation_count" in result
    assert "velocity_violation_ratio" in result
    assert "acceleration_violation_ratio" in result
    assert result["velocity_violation_count"] > 0
    assert result["acceleration_violation_count"] > 0


def test_time_history_length():
    """
    作用：检查轨迹跟踪 time_history 长度与实际轨迹长度一致。
    输入：
        无，测试内部运行一条短直线轨迹。
    输出：
        无，通过断言判断长度。
    """
    trajectory = generate_line_trajectory([0.8, 0.4], [1.0, 0.5], 10)
    velocity = compute_trajectory_velocity(trajectory, dt=0.05)
    history = simulate_trajectory_tracking(
        controller_type="p_ff",
        initial_theta=(-0.4, 2.1),
        desired_trajectory=trajectory,
        desired_velocity=velocity,
        link1=1.0,
        link2=0.8,
        dt=0.05,
        control_params={"kp": 3.0, "max_joint_speed": 1.5, "damping": 0.05},
        inner_steps=5,
    )

    assert len(history["time_history"]) == len(history["actual_trajectory"])
