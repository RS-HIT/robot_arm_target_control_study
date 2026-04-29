"""测试轨迹生成和轨迹跟踪仿真。"""

import importlib.util
from pathlib import Path

import numpy as np

from robot_arm_target_control_study.kinematics import (
    forward_kinematics,
    inverse_kinematics_analytic,
)
from robot_arm_target_control_study.simulation import simulate_trajectory_tracking
from robot_arm_target_control_study.tracking_controller import compute_resolved_rate_p_step
from robot_arm_target_control_study.trajectory import (
    compute_trajectory_velocity,
    generate_circle_trajectory,
    generate_line_trajectory,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "run_trajectory_tracking_demo.py"
SPEC = importlib.util.spec_from_file_location("run_trajectory_tracking_demo", SCRIPT_PATH)
run_trajectory_tracking_demo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_trajectory_tracking_demo)


def test_generate_line_trajectory_shape():
    """
    作用：检查直线轨迹输出形状是否正确。
    输入：
        无，测试内部给定起点、终点和轨迹点数量。
    输出：
        无，通过断言判断结果。
    """
    trajectory = generate_line_trajectory([0.8, 0.4], [1.2, 0.6], 20)

    assert trajectory.shape == (20, 2)


def test_generate_circle_trajectory_shape():
    """
    作用：检查圆形轨迹输出形状是否正确。
    输入：
        无，测试内部给定圆心、半径和轨迹点数量。
    输出：
        无，通过断言判断结果。
    """
    trajectory = generate_circle_trajectory([0.9, 0.4], 0.2, 30)

    assert trajectory.shape == (30, 2)


def test_compute_trajectory_velocity_shape():
    """
    作用：检查轨迹速度数组形状是否和轨迹点数组一致。
    输入：
        无，测试内部生成一条直线轨迹。
    输出：
        无，通过断言判断结果。
    """
    trajectory = generate_line_trajectory([0.8, 0.4], [1.2, 0.6], 20)
    velocity = compute_trajectory_velocity(trajectory, dt=0.05)

    assert velocity.shape == trajectory.shape


def test_trajectory_tracking_history_keys():
    """
    作用：检查轨迹跟踪仿真返回的 history 是否包含关键字段。
    输入：
        无，测试内部使用一条短直线轨迹和 P 控制器。
    输出：
        无，通过断言判断字段是否完整。
    """
    trajectory = generate_line_trajectory([0.8, 0.4], [1.0, 0.5], 10)
    velocity = compute_trajectory_velocity(trajectory, dt=0.05)
    history = simulate_trajectory_tracking(
        controller_type="p",
        initial_theta=(0.3, 0.3),
        desired_trajectory=trajectory,
        desired_velocity=velocity,
        link1=1.0,
        link2=0.8,
        dt=0.05,
        control_params={"gain": 0.8, "max_step": 0.08},
    )

    assert "desired_trajectory" in history
    assert "actual_trajectory" in history
    assert "theta_history" in history
    assert "error_history" in history
    assert "q_dot" in history
    assert "q_dot_clipped" in history
    assert "average_error" in history
    assert "max_error" in history
    assert history["actual_trajectory"].shape == history["desired_trajectory"].shape
    assert len(history["theta_history"]) == len(history["desired_trajectory"])
    assert len(history["error_history"]) == len(history["desired_trajectory"])


def test_ik_start_initialization_close_to_trajectory_start():
    """
    作用：验证用解析逆运动学初始化后，初始末端位置接近期望轨迹起点。
    输入：
        无，测试内部生成一条直线轨迹。
    输出：
        无，通过断言判断初始误差。
    """
    trajectory = generate_line_trajectory([0.8, 0.4], [1.2, 0.6], 10)
    start_xy = trajectory[0]
    theta1, theta2, reachable, _ = inverse_kinematics_analytic(
        start_xy[0],
        start_xy[1],
        1.0,
        0.8,
    )
    initial_end = forward_kinematics(theta1, theta2, 1.0, 0.8)[-1]

    assert reachable is True
    assert np.linalg.norm(start_xy - initial_end) < 1e-8


def test_resolved_rate_p_step_output_shape():
    """
    作用：验证 resolved-rate P 控制单步输出维度正确。
    输入：
        无，测试内部给定关节角和期望末端点。
    输出：
        无，通过断言判断输出格式。
    """
    new_theta, current_xy, error_norm, q_dot, error = compute_resolved_rate_p_step(
        theta=np.array([0.3, 0.3]),
        desired_xy=np.array([1.0, 0.5]),
        desired_velocity=np.array([0.0, 0.0]),
        link1=1.0,
        link2=0.8,
        dt=0.01,
    )

    assert new_theta.shape == (2,)
    assert current_xy.shape == (2,)
    assert q_dot.shape == (2,)
    assert error.shape == (2,)
    assert isinstance(error_norm, float)


def test_resolved_rate_tracking_reduces_error():
    """
    作用：验证短直线轨迹使用 resolved-rate p_ff 控制后，平均误差小于初始误差。
    输入：
        无，测试内部生成短直线轨迹。
    输出：
        无，通过断言判断跟踪误差是否下降。
    """
    trajectory = generate_line_trajectory([0.8, 0.4], [1.0, 0.5], 20)
    velocity = compute_trajectory_velocity(trajectory, dt=0.05)
    initial_theta = np.array([0.3, 0.3])
    initial_end = forward_kinematics(initial_theta[0], initial_theta[1], 1.0, 0.8)[-1]
    initial_error = float(np.linalg.norm(trajectory[0] - initial_end))

    history = simulate_trajectory_tracking(
        controller_type="p_ff",
        initial_theta=initial_theta,
        desired_trajectory=trajectory,
        desired_velocity=velocity,
        link1=1.0,
        link2=0.8,
        dt=0.05,
        control_params={"kp": 3.0, "max_joint_speed": 1.5, "damping": 0.05},
        inner_steps=5,
    )

    assert history["average_error"] < initial_error


def test_run_trajectory_args_accept_pd_tuning_params():
    """
    作用：检查轨迹跟踪脚本的命令行参数是否支持 PD 调参所需字段。
    输入：
        无，测试内部构造命令行参数列表。
    输出：
        无，通过断言判断 argparse 解析结果。
    """
    args = run_trajectory_tracking_demo.parse_args(
        [
            "--trajectory",
            "line",
            "--controller",
            "pd",
            "--kp",
            "3.0",
            "--kd",
            "0.05",
            "--damping",
            "0.05",
            "--max_joint_speed",
            "1.5",
            "--inner_steps",
            "5",
        ]
    )

    assert args.controller == "pd"
    assert args.kp == 3.0
    assert args.kd == 0.05
    assert args.damping == 0.05
    assert args.max_joint_speed == 1.5
    assert args.inner_steps == 5
