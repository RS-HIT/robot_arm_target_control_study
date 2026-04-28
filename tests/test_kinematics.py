"""测试二连杆机械臂运动学函数。"""

import numpy as np

from robot_arm_target_control_study.kinematics import (
    compute_jacobian,
    forward_kinematics,
    inverse_kinematics_analytic,
    is_target_reachable,
)


def test_forward_kinematics_straight_pose():
    """
    作用：测试两个关节角为 0 时，机械臂应沿 x 轴完全伸直。
    输入：
        无，测试内部给定参数。
    输出：
        无，通过断言判断结果是否正确。
    """
    positions = forward_kinematics(0.0, 0.0, 1.0, 0.8)

    assert np.allclose(positions[-1], np.array([1.8, 0.0]))


def test_forward_kinematics_vertical_pose():
    """
    作用：测试第一关节为 pi/2、第二关节为 0 时，机械臂应沿 y 轴伸直。
    输入：
        无，测试内部给定参数。
    输出：
        无，通过断言判断结果是否正确。
    """
    positions = forward_kinematics(np.pi / 2.0, 0.0, 1.0, 0.8)

    assert np.allclose(positions[-1], np.array([0.0, 1.8]), atol=1e-8)


def test_jacobian_shape():
    """
    作用：测试雅可比矩阵的形状是否为 2 行 2 列。
    输入：
        无，测试内部给定参数。
    输出：
        无，通过断言判断结果是否正确。
    """
    jacobian = compute_jacobian(0.3, 0.3, 1.0, 0.8)

    assert jacobian.shape == (2, 2)


def test_target_reachable():
    """
    作用：测试目标点 (1.2, 0.6) 在 link1=1.0、link2=0.8 时可达。
    输入：
        无，测试内部给定目标点和连杆长度。
    输出：
        无，通过断言判断可达性是否正确。
    """
    reachable, reason = is_target_reachable(1.2, 0.6, 1.0, 0.8)

    assert reachable is True
    assert "可达" in reason


def test_target_too_far():
    """
    作用：测试目标点 (3.0, 0.0) 超出最远工作空间时不可达。
    输入：
        无，测试内部给定目标点和连杆长度。
    输出：
        无，通过断言判断不可达原因是否正确。
    """
    reachable, reason = is_target_reachable(3.0, 0.0, 1.0, 0.8)

    assert reachable is False
    assert "太远" in reason


def test_inverse_kinematics_analytic_reaches_target():
    """
    作用：测试解析逆运动学算出的关节角，代入正运动学后能接近目标点。
    输入：
        无，测试内部给定目标点和连杆长度。
    输出：
        无，通过断言判断末端位置是否接近目标点。
    """
    target = np.array([1.2, 0.6])
    theta1, theta2, reachable, _ = inverse_kinematics_analytic(
        target[0],
        target[1],
        1.0,
        0.8,
    )
    positions = forward_kinematics(theta1, theta2, 1.0, 0.8)

    assert reachable is True
    assert np.allclose(positions[-1], target, atol=1e-8)


def test_inverse_kinematics_analytic_elbow_up_down():
    """
    作用：测试 elbow='up' 和 elbow='down' 都能到达同一目标点，但关节角不同。
    输入：
        无，测试内部给定目标点和连杆长度。
    输出：
        无，通过断言判断两种构型的结果。
    """
    target = np.array([1.2, 0.6])
    down_theta1, down_theta2, down_reachable, _ = inverse_kinematics_analytic(
        target[0],
        target[1],
        1.0,
        0.8,
        elbow="down",
    )
    up_theta1, up_theta2, up_reachable, _ = inverse_kinematics_analytic(
        target[0],
        target[1],
        1.0,
        0.8,
        elbow="up",
    )

    down_positions = forward_kinematics(down_theta1, down_theta2, 1.0, 0.8)
    up_positions = forward_kinematics(up_theta1, up_theta2, 1.0, 0.8)

    assert down_reachable is True
    assert up_reachable is True
    assert np.allclose(down_positions[-1], target, atol=1e-8)
    assert np.allclose(up_positions[-1], target, atol=1e-8)
    assert not np.allclose(
        np.array([down_theta1, down_theta2]),
        np.array([up_theta1, up_theta2]),
    )
