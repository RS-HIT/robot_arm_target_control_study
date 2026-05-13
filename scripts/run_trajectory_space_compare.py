"""比较关节空间轨迹和笛卡尔空间轨迹跟踪。"""

import argparse
import csv
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
    plot_joint_acceleration_compare,
    plot_joint_trajectory_compare,
    plot_joint_velocity_compare,
    plot_path_compare,
)
from robot_arm_target_control_study.simulation import simulate_trajectory_tracking
from robot_arm_target_control_study.trajectory import (
    compute_discrete_acceleration,
    compute_discrete_velocity,
    compute_trajectory_velocity,
    generate_joint_space_trajectory,
    generate_line_trajectory,
)


def parse_args():
    """
    作用：读取轨迹空间对比实验的命令行参数。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含起点、终点、点数、时间步长和时间缩放方法。
    """
    parser = argparse.ArgumentParser(description="关节空间轨迹 vs 笛卡尔空间轨迹对比")
    parser.add_argument("--start_x", type=float, default=0.8, help="起点 x 坐标")
    parser.add_argument("--start_y", type=float, default=0.4, help="起点 y 坐标")
    parser.add_argument("--goal_x", type=float, default=1.2, help="终点 x 坐标")
    parser.add_argument("--goal_y", type=float, default=0.6, help="终点 y 坐标")
    parser.add_argument("--num_points", type=int, default=100, help="轨迹点数量")
    parser.add_argument("--method", choices=["linear", "cubic", "quintic"], default="quintic", help="关节空间时间缩放方法")
    parser.add_argument("--dt", type=float, default=0.05, help="轨迹点时间间隔")
    return parser.parse_args()


def compute_path_length(path):
    """
    作用：计算二维路径长度。
    输入：
        path: 形状为 (N, 2) 的路径点数组。
    输出：
        path_length: 路径相邻点距离之和。
    """
    path = np.array(path, dtype=float)
    if len(path) < 2:
        return 0.0
    return float(np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1)))


def compute_metrics(method_name, path, theta_history, velocity, acceleration, goal_xy):
    """
    作用：计算一种轨迹方法的路径长度、速度、加速度和终点误差指标。
    输入：
        method_name: 方法名称。
        path: 末端路径。
        theta_history: 关节角历史。
        velocity: 关节速度数组。
        acceleration: 关节加速度数组。
        goal_xy: 目标末端位置。
    输出：
        metrics: 指标字典，可直接写入 CSV。
    """
    velocity_norm = np.linalg.norm(velocity, axis=1)
    acceleration_norm = np.linalg.norm(acceleration, axis=1)
    final_position_error = float(np.linalg.norm(np.array(goal_xy, dtype=float) - np.array(path[-1], dtype=float)))
    return {
        "method": method_name,
        "path_length": compute_path_length(path),
        "max_joint_velocity": float(np.max(np.abs(velocity))),
        "max_joint_acceleration": float(np.max(np.abs(acceleration))),
        "joint_velocity_rms": float(np.sqrt(np.mean(velocity_norm**2))),
        "joint_acceleration_rms": float(np.sqrt(np.mean(acceleration_norm**2))),
        "final_position_error": final_position_error,
    }


def save_csv(rows, save_path):
    """
    作用：保存轨迹空间对比指标 CSV。
    输入：
        rows: 指标字典列表。
        save_path: CSV 保存路径。
    输出：
        file_path: 保存后的 Path。
    """
    file_path = Path(save_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "method",
        "path_length",
        "max_joint_velocity",
        "max_joint_acceleration",
        "joint_velocity_rms",
        "joint_acceleration_rms",
        "final_position_error",
    ]
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return file_path


def main():
    """
    作用：程序主入口，运行关节空间轨迹和笛卡尔空间轨迹跟踪对比实验。
    输入：
        无，实验参数来自命令行。
    输出：
        无，结果打印到终端并保存图片和 CSV。
    """
    args = parse_args()
    link1 = 1.0
    link2 = 0.8
    start_xy = np.array([args.start_x, args.start_y], dtype=float)
    goal_xy = np.array([args.goal_x, args.goal_y], dtype=float)

    start_theta1, start_theta2, start_reachable, start_message = inverse_kinematics_analytic(
        start_xy[0], start_xy[1], link1, link2
    )
    goal_theta1, goal_theta2, goal_reachable, goal_message = inverse_kinematics_analytic(
        goal_xy[0], goal_xy[1], link1, link2
    )
    print("=== 关节空间轨迹 vs 笛卡尔空间轨迹 ===")
    print(f"起点可达: {start_reachable}，说明: {start_message}")
    print(f"终点可达: {goal_reachable}，说明: {goal_message}")
    if not (start_reachable and goal_reachable):
        print("起点或终点不可达，实验终止。")
        return

    start_theta = np.array([start_theta1, start_theta2], dtype=float)
    goal_theta = np.array([goal_theta1, goal_theta2], dtype=float)

    joint_theta = generate_joint_space_trajectory(start_theta, goal_theta, args.num_points, method=args.method)
    joint_path = np.array([forward_kinematics(theta[0], theta[1], link1, link2)[-1] for theta in joint_theta])
    joint_velocity = compute_discrete_velocity(joint_theta, args.dt)
    joint_acceleration = compute_discrete_acceleration(joint_theta, args.dt)

    desired_line = generate_line_trajectory(start_xy, goal_xy, args.num_points)
    desired_velocity = compute_trajectory_velocity(desired_line, args.dt)
    cartesian_history = simulate_trajectory_tracking(
        controller_type="p_ff",
        initial_theta=start_theta,
        desired_trajectory=desired_line,
        desired_velocity=desired_velocity,
        link1=link1,
        link2=link2,
        dt=args.dt,
        control_params={"kp": 3.0, "max_joint_speed": 1.5, "damping": 0.05},
        inner_steps=5,
    )
    cartesian_path = cartesian_history["actual_trajectory"]
    cartesian_theta = np.array(cartesian_history["theta_history"], dtype=float)
    dt_inner = args.dt / cartesian_history["inner_steps"]
    cartesian_velocity = compute_discrete_velocity(cartesian_theta, dt_inner)
    cartesian_acceleration = compute_discrete_acceleration(cartesian_theta, dt_inner)

    joint_metrics = compute_metrics("joint_space", joint_path, joint_theta, joint_velocity, joint_acceleration, goal_xy)
    cartesian_metrics = compute_metrics(
        "cartesian_tracking",
        cartesian_path,
        cartesian_theta,
        cartesian_velocity,
        cartesian_acceleration,
        goal_xy,
    )

    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    plot_files = {
        "path": plot_path_compare(
            desired_line,
            joint_path,
            cartesian_path,
            figure_dir / "trajectory_space_path_compare.png",
        ),
        "theta": plot_joint_trajectory_compare(
            joint_theta,
            cartesian_theta,
            figure_dir / "trajectory_space_theta_compare.png",
        ),
        "velocity": plot_joint_velocity_compare(
            joint_velocity,
            cartesian_velocity,
            figure_dir / "trajectory_space_velocity_compare.png",
        ),
        "acceleration": plot_joint_acceleration_compare(
            joint_acceleration,
            cartesian_acceleration,
            figure_dir / "trajectory_space_acceleration_compare.png",
        ),
    }
    csv_path = save_csv(
        [joint_metrics, cartesian_metrics],
        PROJECT_ROOT / "outputs" / "logs" / "trajectory_space_compare.csv",
    )

    print(f"关节空间轨迹的末端路径长度: {joint_metrics['path_length']:.6f}")
    print(f"笛卡尔空间轨迹的末端路径长度: {cartesian_metrics['path_length']:.6f}")
    print(f"关节空间最大关节速度: {joint_metrics['max_joint_velocity']:.6f}")
    print(f"笛卡尔空间最大关节速度: {cartesian_metrics['max_joint_velocity']:.6f}")
    print(f"关节空间最大关节加速度: {joint_metrics['max_joint_acceleration']:.6f}")
    print(f"笛卡尔空间最大关节加速度: {cartesian_metrics['max_joint_acceleration']:.6f}")
    print(f"关节空间关节加速度 RMS: {joint_metrics['joint_acceleration_rms']:.6f}")
    print(f"笛卡尔空间关节加速度 RMS: {cartesian_metrics['joint_acceleration_rms']:.6f}")
    print("简短结论：关节空间轨迹通常让关节运动更直接平滑，但末端路径不一定是直线；笛卡尔轨迹更关注末端路径形状，但可能带来更复杂的关节速度和加速度变化。")
    print(f"CSV 已保存: {csv_path}")
    print("输出图片:")
    for name, path in plot_files.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
