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
    plot_path_compare,
    plot_time_based_acceleration_compare,
    plot_time_based_joint_compare,
    plot_time_based_velocity_compare,
)
from robot_arm_target_control_study.simulation import simulate_trajectory_tracking
from robot_arm_target_control_study.trajectory import (
    compute_discrete_acceleration,
    compute_discrete_velocity,
    compute_trajectory_velocity,
    generate_joint_space_trajectory,
    generate_line_trajectory,
)
from robot_arm_target_control_study.utils import (
    check_joint_limits,
    compute_path_deviation_from_line,
)


def parse_args():
    """
    作用：读取轨迹空间对比实验的命令行参数。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含起点、终点、点数、总时间和时间缩放方法。
    """
    parser = argparse.ArgumentParser(description="关节空间轨迹 vs 笛卡尔空间轨迹对比")
    parser.add_argument("--start_x", type=float, default=0.8, help="起点 x 坐标")
    parser.add_argument("--start_y", type=float, default=0.4, help="起点 y 坐标")
    parser.add_argument("--goal_x", type=float, default=1.2, help="终点 x 坐标")
    parser.add_argument("--goal_y", type=float, default=0.6, help="终点 y 坐标")
    parser.add_argument("--num_points", type=int, default=100, help="轨迹点数量")
    parser.add_argument("--method", choices=["linear", "cubic", "quintic"], default="quintic", help="关节空间时间缩放方法")
    parser.add_argument("--total_time", type=float, default=5.0, help="整条轨迹希望完成的总时间")
    parser.add_argument("--dt", type=float, default=None, help="兼容旧参数；如果提供，会用 dt 推算 total_time")
    parser.add_argument("--inner_steps", type=int, default=5, help="笛卡尔跟踪每个轨迹点内部的小步数")
    return parser.parse_args()


def resolve_timing(num_points, total_time, dt):
    """
    作用：统一 total_time 和 dt，优先使用 total_time。
    输入：
        num_points: 轨迹点数量。
        total_time: 总运动时间。
        dt: 可选时间步长。
    输出：
        total_time: 最终使用的总时间。
        dt: 相邻轨迹点时间间隔。
    """
    if dt is not None:
        total_time = dt * (num_points - 1)
    dt = total_time / (num_points - 1)
    return total_time, dt


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


def compute_metrics(method_name, path, theta_history, velocity, acceleration, goal_xy, start_xy, limit_result):
    """
    作用：计算一种轨迹方法的路径、速度、加速度、约束和偏离直线指标。
    输入：
        method_name: 方法名称。
        path: 末端路径。
        theta_history: 关节角历史。
        velocity: 关节速度数组。
        acceleration: 关节加速度数组。
        goal_xy: 目标末端位置。
        start_xy: 起点末端位置。
        limit_result: check_joint_limits 返回的约束检查结果。
    输出：
        metrics: 指标字典，可直接写入 CSV。
    """
    velocity_norm = np.linalg.norm(velocity, axis=1)
    acceleration_norm = np.linalg.norm(acceleration, axis=1)
    deviation = compute_path_deviation_from_line(path, start_xy, goal_xy)
    final_position_error = float(np.linalg.norm(np.array(goal_xy, dtype=float) - np.array(path[-1], dtype=float)))
    return {
        "method": method_name,
        "path_length": compute_path_length(path),
        "max_joint_velocity": limit_result["max_joint_velocity"],
        "max_joint_acceleration": limit_result["max_joint_acceleration"],
        "joint_velocity_rms": float(np.sqrt(np.mean(velocity_norm**2))),
        "joint_acceleration_rms": float(np.sqrt(np.mean(acceleration_norm**2))),
        "velocity_violation_count": limit_result["velocity_violation_count"],
        "acceleration_violation_count": limit_result["acceleration_violation_count"],
        "velocity_violation_ratio": limit_result["velocity_violation_ratio"],
        "acceleration_violation_ratio": limit_result["acceleration_violation_ratio"],
        "final_position_error": final_position_error,
        "path_deviation_from_line": deviation["mean_deviation"],
        "mean_path_deviation": deviation["mean_deviation"],
        "max_path_deviation": deviation["max_deviation"],
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
    fieldnames = list(rows[0].keys())
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return file_path


def run_compare_experiment(
    start_xy,
    goal_xy,
    num_points=100,
    method="quintic",
    total_time=5.0,
    inner_steps=5,
    joint_velocity_limit=1.5,
    joint_acceleration_limit=5.0,
):
    """
    作用：运行一次关节空间轨迹和笛卡尔空间轨迹对比实验。
    输入：
        start_xy: 末端起点。
        goal_xy: 末端终点。
        num_points: 轨迹点数量。
        method: 关节空间时间缩放方法。
        total_time: 总运动时间。
        inner_steps: 笛卡尔跟踪内部小步数。
        joint_velocity_limit: 关节速度限制。
        joint_acceleration_limit: 关节加速度限制。
    输出：
        result: 字典，包含两类轨迹、时间轴、速度加速度和指标。
    """
    link1 = 1.0
    link2 = 0.8
    dt = total_time / (num_points - 1)
    dt_inner = dt / inner_steps

    start_theta1, start_theta2, start_reachable, start_message = inverse_kinematics_analytic(
        start_xy[0], start_xy[1], link1, link2
    )
    goal_theta1, goal_theta2, goal_reachable, goal_message = inverse_kinematics_analytic(
        goal_xy[0], goal_xy[1], link1, link2
    )
    if not (start_reachable and goal_reachable):
        return {
            "start_reachable": start_reachable,
            "goal_reachable": goal_reachable,
            "start_message": start_message,
            "goal_message": goal_message,
            "rows": [],
        }

    start_theta = np.array([start_theta1, start_theta2], dtype=float)
    goal_theta = np.array([goal_theta1, goal_theta2], dtype=float)
    joint_time = np.linspace(0.0, total_time, num_points)

    joint_theta = generate_joint_space_trajectory(start_theta, goal_theta, num_points, method=method)
    joint_path = np.array([forward_kinematics(theta[0], theta[1], link1, link2)[-1] for theta in joint_theta])
    joint_velocity = compute_discrete_velocity(joint_theta, dt)
    joint_acceleration = compute_discrete_acceleration(joint_theta, dt)
    joint_limits = check_joint_limits(
        joint_theta,
        joint_velocity,
        joint_acceleration,
        joint_velocity_limit,
        joint_acceleration_limit,
    )

    desired_line = generate_line_trajectory(start_xy, goal_xy, num_points)
    desired_velocity = compute_trajectory_velocity(desired_line, dt)
    cartesian_history = simulate_trajectory_tracking(
        controller_type="p_ff",
        initial_theta=start_theta,
        desired_trajectory=desired_line,
        desired_velocity=desired_velocity,
        link1=link1,
        link2=link2,
        dt=dt,
        control_params={"kp": 3.0, "max_joint_speed": joint_velocity_limit, "damping": 0.05},
        inner_steps=inner_steps,
    )
    cartesian_path = cartesian_history["actual_trajectory"]
    cartesian_theta = np.array(cartesian_history["theta_history"], dtype=float)
    cartesian_time = np.array(cartesian_history["time_history"], dtype=float)
    cartesian_velocity = compute_discrete_velocity(cartesian_theta, dt_inner)
    cartesian_acceleration = compute_discrete_acceleration(cartesian_theta, dt_inner)
    cartesian_limits = check_joint_limits(
        cartesian_theta,
        cartesian_velocity,
        cartesian_acceleration,
        joint_velocity_limit,
        joint_acceleration_limit,
    )

    joint_metrics = compute_metrics(
        "joint_space",
        joint_path,
        joint_theta,
        joint_velocity,
        joint_acceleration,
        goal_xy,
        start_xy,
        joint_limits,
    )
    cartesian_metrics = compute_metrics(
        "cartesian_tracking",
        cartesian_path,
        cartesian_theta,
        cartesian_velocity,
        cartesian_acceleration,
        goal_xy,
        start_xy,
        cartesian_limits,
    )
    for row in (joint_metrics, cartesian_metrics):
        row["total_time"] = float(total_time)
        row["dt"] = float(dt)
        row["inner_steps"] = int(inner_steps)

    return {
        "start_reachable": start_reachable,
        "goal_reachable": goal_reachable,
        "start_message": start_message,
        "goal_message": goal_message,
        "total_time": total_time,
        "num_points": num_points,
        "dt": dt,
        "inner_steps": inner_steps,
        "dt_inner": dt_inner,
        "desired_line": desired_line,
        "joint_time": joint_time,
        "joint_theta": joint_theta,
        "joint_path": joint_path,
        "joint_velocity": joint_velocity,
        "joint_acceleration": joint_acceleration,
        "cartesian_time": cartesian_time,
        "cartesian_theta": cartesian_theta,
        "cartesian_path": cartesian_path,
        "cartesian_velocity": cartesian_velocity,
        "cartesian_acceleration": cartesian_acceleration,
        "rows": [joint_metrics, cartesian_metrics],
    }


def save_compare_plots(result, figure_dir):
    """
    作用：保存一次轨迹空间对比实验的四张图片。
    输入：
        result: run_compare_experiment 返回的结果字典。
        figure_dir: 图片输出目录。
    输出：
        plot_files: 图片路径字典。
    """
    figure_dir = Path(figure_dir)
    return {
        "path": plot_path_compare(
            result["desired_line"],
            result["joint_path"],
            result["cartesian_path"],
            figure_dir / "trajectory_space_path_compare.png",
        ),
        "theta": plot_time_based_joint_compare(
            result["joint_time"],
            result["joint_theta"],
            result["cartesian_time"],
            result["cartesian_theta"],
            figure_dir / "trajectory_space_theta_compare.png",
        ),
        "velocity": plot_time_based_velocity_compare(
            result["joint_time"],
            result["joint_velocity"],
            result["cartesian_time"],
            result["cartesian_velocity"],
            figure_dir / "trajectory_space_velocity_compare.png",
        ),
        "acceleration": plot_time_based_acceleration_compare(
            result["joint_time"],
            result["joint_acceleration"],
            result["cartesian_time"],
            result["cartesian_acceleration"],
            figure_dir / "trajectory_space_acceleration_compare.png",
        ),
    }


def main():
    """
    作用：程序主入口，运行关节空间轨迹和笛卡尔空间轨迹跟踪对比实验。
    输入：
        无，实验参数来自命令行。
    输出：
        无，结果打印到终端并保存图片和 CSV。
    """
    args = parse_args()
    total_time, dt = resolve_timing(args.num_points, args.total_time, args.dt)
    start_xy = np.array([args.start_x, args.start_y], dtype=float)
    goal_xy = np.array([args.goal_x, args.goal_y], dtype=float)
    result = run_compare_experiment(
        start_xy=start_xy,
        goal_xy=goal_xy,
        num_points=args.num_points,
        method=args.method,
        total_time=total_time,
        inner_steps=args.inner_steps,
    )

    print("=== 关节空间轨迹 vs 笛卡尔空间轨迹 ===")
    print(f"起点可达: {result['start_reachable']}，说明: {result['start_message']}")
    print(f"终点可达: {result['goal_reachable']}，说明: {result['goal_message']}")
    if not result["rows"]:
        print("起点或终点不可达，实验终止。")
        return

    print(f"total_time: {result['total_time']:.6f} s")
    print(f"num_points: {result['num_points']}")
    print(f"dt: {result['dt']:.6f} s")
    print(f"inner_steps: {result['inner_steps']}")
    print(f"dt_inner: {result['dt_inner']:.6f} s")

    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    plot_files = save_compare_plots(result, figure_dir)
    csv_path = save_csv(result["rows"], PROJECT_ROOT / "outputs" / "logs" / "trajectory_space_compare.csv")

    joint_metrics, cartesian_metrics = result["rows"]
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
