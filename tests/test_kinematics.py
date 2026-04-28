"""测试二连杆机械臂运动学函数。"""

import numpy as np

from robot_arm_target_control_study.kinematics import (
    compute_jacobian,
    forward_kinematics,
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
