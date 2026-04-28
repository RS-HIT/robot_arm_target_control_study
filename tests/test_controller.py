"""测试目标点控制仿真是否能够收敛。"""

import numpy as np

from robot_arm_target_control_study.controller import compute_damped_jacobian_step
from robot_arm_target_control_study.kinematics import forward_kinematics
from robot_arm_target_control_study.simulation import run_reach_simulation
from robot_arm_target_control_study.simulation import simulate_iterative_control


def test_reachable_target_converges():
    """
    作用：测试目标点在工作空间内时，机械臂末端误差能够收敛到较小值。
    输入：
        无，测试内部使用目标点 (1.2, 0.6)。
    输出：
        无，通过断言判断是否收敛。
    """
    result = run_reach_simulation(target=(1.2, 0.6))

    assert result["final_error"] < 0.02
    assert result["reached"] is True


def test_unreachable_target_does_not_crash():
    """
    作用：测试目标点不可达时，程序不会崩溃，并且会返回有限误差。
    输入：
        无，测试内部使用超出工作空间的目标点。
    输出：
        无，通过断言判断结果是否有效。
    """
    result = run_reach_simulation(target=(3.0, 0.0))

    assert result["final_error"] >= 0.0
    assert result["reached"] is False


def test_damped_jacobian_step_shape():
    """
    作用：检查阻尼雅可比控制单步输出的维度是否正确。
    输入：
        无，测试内部给定初始关节角和目标点。
    输出：
        无，通过断言判断输出格式。
    """
    new_theta, error_norm, delta_theta = compute_damped_jacobian_step(
        theta=np.array([0.3, 0.3]),
        target=np.array([1.2, 0.6]),
        link1=1.0,
        link2=0.8,
    )

    assert new_theta.shape == (2,)
    assert delta_theta.shape == (2,)
    assert isinstance(error_norm, float)


def test_damped_jacobian_reduces_error():
    """
    作用：运行若干步阻尼雅可比控制，验证最终误差小于初始误差。
    输入：
        无，测试内部给定目标点和初始关节角。
    输出：
        无，通过断言判断误差是否下降。
    """
    theta = np.array([0.3, 0.3])
    target = np.array([1.2, 0.6])
    initial_end = forward_kinematics(theta[0], theta[1], 1.0, 0.8)[-1]
    initial_error = float(np.linalg.norm(target - initial_end))

    for _ in range(30):
        theta, _, _ = compute_damped_jacobian_step(
            theta=theta,
            target=target,
            link1=1.0,
            link2=0.8,
            gain=0.8,
            damping=0.05,
            max_step=0.08,
        )

    final_end = forward_kinematics(theta[0], theta[1], 1.0, 0.8)[-1]
    final_error = float(np.linalg.norm(target - final_end))

    assert final_error < initial_error


def test_simulate_iterative_control_returns_history():
    """
    作用：检查通用迭代仿真函数是否返回完整 history 字典。
    输入：
        无，测试内部使用阻尼雅可比控制。
    输出：
        无，通过断言判断关键字段是否存在且有效。
    """
    history = simulate_iterative_control(
        control_method=compute_damped_jacobian_step,
        initial_theta=(0.3, 0.3),
        target=(1.2, 0.6),
        link1=1.0,
        link2=0.8,
        max_iterations=50,
        tolerance=0.01,
        gain=0.8,
        damping=0.05,
        max_step=0.08,
    )

    assert "error_history" in history
    assert "theta_history" in history
    assert "end_effector_history" in history
    assert "success" in history
    assert "final_error" in history
    assert history["iterations"] == len(history["error_history"])
    assert history["final_error"] >= 0.0
