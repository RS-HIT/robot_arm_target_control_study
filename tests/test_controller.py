"""测试目标点控制仿真是否能够收敛。"""

from robot_arm_target_control_study.simulation import run_reach_simulation


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
