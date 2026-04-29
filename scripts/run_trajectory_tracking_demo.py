"""运行 2D 二连杆机械臂轨迹跟踪 demo。"""

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from robot_arm_target_control_study.kinematics import (
    forward_kinematics,
    inverse_kinematics_analytic,
)
from robot_arm_target_control_study.plotting import (
    plot_tracking_error,
    plot_tracking_joint_angles,
    plot_trajectory_tracking,
)
from robot_arm_target_control_study.simulation import simulate_trajectory_tracking
from robot_arm_target_control_study.trajectory import (
    compute_trajectory_velocity,
    generate_circle_trajectory,
    generate_line_trajectory,
)


def parse_args(argv=None):
    """
    作用：读取命令行中的轨迹类型和控制器类型。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含 trajectory 和 controller。
    """
    parser = argparse.ArgumentParser(description="轨迹跟踪与 resolved-rate 控制 demo")
    parser.add_argument("--trajectory", choices=["line", "circle"], required=True, help="轨迹类型")
    parser.add_argument("--controller", choices=["p", "p_ff", "pd"], default="p_ff", help="控制器类型")
    parser.add_argument("--init_mode", choices=["ik_start", "default"], default="ik_start", help="初始关节角模式")
    parser.add_argument("--kp", type=float, default=3.0, help="位置误差比例增益")
    parser.add_argument("--kd", type=float, default=0.02, help="速度误差增益，主要用于 controller=pd")
    parser.add_argument("--damping", type=float, default=0.05, help="阻尼伪逆中的阻尼系数")
    parser.add_argument("--max_joint_speed", type=float, default=1.5, help="最大关节速度限制，单位 rad/s")
    parser.add_argument("--dt", type=float, default=0.05, help="轨迹点之间的时间间隔")
    parser.add_argument("--inner_steps", type=int, default=5, help="每个轨迹点内部的控制小步数")
    parser.add_argument("--num_points", type=int, default=100, help="轨迹点数量")
    parser.add_argument("--radius", type=float, default=0.2, help="圆形轨迹半径，仅 trajectory=circle 时使用")
    return parser.parse_args(argv)


def build_trajectory(trajectory_type, num_points, radius):
    """
    作用：根据轨迹类型生成期望末端轨迹。
    输入：
        trajectory_type: "line" 或 "circle"。
        num_points: 轨迹点数量。
    输出：
        trajectory: 形状为 (num_points, 2) 的期望轨迹数组。
    """
    if trajectory_type == "line":
        return generate_line_trajectory([0.8, 0.4], [1.2, 0.6], num_points)

    return generate_circle_trajectory([0.9, 0.4], radius, num_points)


def save_tracking_plots(history):
    """
    作用：保存轨迹跟踪路径图、误差曲线和关节角曲线。
    输入：
        history: simulate_trajectory_tracking 返回的历史记录字典。
    输出：
        plot_files: 字典，包含三张图片的保存路径。
    """
    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    return {
        "path": plot_trajectory_tracking(
            history["desired_trajectory"],
            history["actual_trajectory"],
            figure_dir / "trajectory_tracking_path.png",
        ),
        "error": plot_tracking_error(
            history["error_history"],
            figure_dir / "trajectory_tracking_error.png",
        ),
        "joint_angles": plot_tracking_joint_angles(
            history["theta_history"],
            figure_dir / "trajectory_tracking_joint_angles.png",
        ),
    }


def choose_initial_theta(init_mode, trajectory, link1, link2):
    """
    作用：根据 init_mode 选择轨迹跟踪初始关节角。
    输入：
        init_mode: "ik_start" 表示用解析逆运动学对齐轨迹起点，"default" 表示使用默认角度。
        trajectory: 期望轨迹数组。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
    输出：
        initial_theta: 长度为 2 的初始关节角数组。
        diagnostics: 字典，包含初始末端位置、轨迹起点和初始误差。
    """
    default_theta = np.array([0.3, 0.3], dtype=float)
    start_xy = trajectory[0]

    if init_mode == "ik_start":
        theta1, theta2, reachable, message = inverse_kinematics_analytic(
            start_xy[0],
            start_xy[1],
            link1,
            link2,
            elbow="down",
        )
        if reachable:
            initial_theta = np.array([theta1, theta2], dtype=float)
        else:
            print(f"警告：轨迹起点 IK 初始化失败，退回默认 initial_theta。原因：{message}")
            initial_theta = default_theta
    else:
        initial_theta = default_theta

    initial_end = forward_kinematics(initial_theta[0], initial_theta[1], link1, link2)[-1]
    initial_error = float(np.linalg.norm(start_xy - initial_end))
    diagnostics = {
        "initial_theta": initial_theta,
        "initial_end": initial_end,
        "trajectory_start": start_xy,
        "initial_error": initial_error,
    }
    return initial_theta, diagnostics


def print_result(history, plot_files, init_diagnostics):
    """
    作用：在终端打印轨迹跟踪误差指标和图片保存路径。
    输入：
        history: simulate_trajectory_tracking 返回的历史记录字典。
        plot_files: 输出图片路径字典。
        init_diagnostics: 初始姿态诊断信息。
    输出：
        无，只负责打印信息。
    """
    print("=== 轨迹跟踪 demo ===")
    print(f"轨迹类型: {history['trajectory_type']}")
    print(f"控制器: {history['controller_type']}")
    print(f"kp: {history['control_params']['kp']}")
    print(f"kd: {history['control_params']['kd']}")
    print(f"damping: {history['control_params']['damping']}")
    print(f"max_joint_speed: {history['control_params']['max_joint_speed']} rad/s")
    print(f"dt: {history['dt']}")
    print(f"inner_steps: {history['inner_steps']}")
    print(f"num_points: {history['num_points']}")
    print(
        "初始关节角: "
        f"({init_diagnostics['initial_theta'][0]:.6f}, {init_diagnostics['initial_theta'][1]:.6f})"
    )
    print(
        "初始末端位置: "
        f"({init_diagnostics['initial_end'][0]:.6f}, {init_diagnostics['initial_end'][1]:.6f})"
    )
    print(
        "轨迹起点: "
        f"({init_diagnostics['trajectory_start'][0]:.6f}, {init_diagnostics['trajectory_start'][1]:.6f})"
    )
    print(f"初始误差: {init_diagnostics['initial_error']:.6f}")
    print(f"平均误差: {history['average_error']:.6f}")
    print(f"最大误差: {history['max_error']:.6f}")
    print(f"最终误差: {history['final_error']:.6f}")
    print(f"q_dot 被限幅次数: {history['q_dot_clipped_count']}")
    if history["q_dot_clipped_count"] > 0.5 * len(history["q_dot_clipped"]):
        print("提示：关节速度长期触发限幅，说明 kp/kd 可能过大，或轨迹速度过快。")
    if history["controller_type"] == "pd" and history["max_error"] > 0.05:
        print("提示：如果 PD 仍然震荡，可尝试 kd=0.0、0.02、0.05。")
    print("输出图片:")
    for name, path in plot_files.items():
        print(f"  {name}: {path}")


def main():
    """
    作用：程序主入口，完成轨迹生成、速度估计、跟踪仿真、绘图和结果打印。
    输入：
        无，轨迹和控制器由命令行传入。
    输出：
        无。
    """
    args = parse_args()

    link1 = 1.0
    link2 = 0.8
    trajectory = build_trajectory(args.trajectory, args.num_points, args.radius)
    velocity = compute_trajectory_velocity(trajectory, args.dt)
    initial_theta, init_diagnostics = choose_initial_theta(args.init_mode, trajectory, link1, link2)

    control_params = {
        "kp": args.kp,
        "kd": args.kd,
        "max_joint_speed": args.max_joint_speed,
        "damping": args.damping,
    }
    history = simulate_trajectory_tracking(
        controller_type=args.controller,
        initial_theta=initial_theta,
        desired_trajectory=trajectory,
        desired_velocity=velocity,
        link1=link1,
        link2=link2,
        dt=args.dt,
        control_params=control_params,
        inner_steps=args.inner_steps,
    )
    history["trajectory_type"] = args.trajectory
    history["num_points"] = args.num_points
    history["control_params"] = control_params
    plot_files = save_tracking_plots(history)
    print_result(history, plot_files, init_diagnostics)


if __name__ == "__main__":
    main()
