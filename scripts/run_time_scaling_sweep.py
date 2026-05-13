"""扫描 total_time，观察轨迹重定时对速度和加速度的影响。"""

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
SCRIPT_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from robot_arm_target_control_study.plotting import (
    plot_time_scaling_metric,
    plot_time_scaling_metrics,
)
from run_trajectory_space_compare import run_compare_experiment


def parse_args():
    """
    作用：读取 total_time 扫描实验的命令行参数。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含方法、总时间列表、起终点和采样参数。
    """
    parser = argparse.ArgumentParser(description="扫描 total_time 对轨迹速度和加速度的影响")
    parser.add_argument("--method", choices=["joint", "cartesian", "both"], default="both", help="记录哪类轨迹方法")
    parser.add_argument("--total_times", type=float, nargs="+", default=[3.0, 5.0, 8.0, 10.0], help="要扫描的总运动时间列表")
    parser.add_argument("--start_x", type=float, default=0.8, help="起点 x 坐标")
    parser.add_argument("--start_y", type=float, default=0.4, help="起点 y 坐标")
    parser.add_argument("--goal_x", type=float, default=1.2, help="终点 x 坐标")
    parser.add_argument("--goal_y", type=float, default=0.6, help="终点 y 坐标")
    parser.add_argument("--num_points", type=int, default=100, help="轨迹点数量")
    parser.add_argument("--inner_steps", type=int, default=5, help="笛卡尔跟踪每个轨迹点内部的小步数")
    return parser.parse_args()


def save_csv(rows, save_path):
    """
    作用：保存 total_time 扫描结果 CSV。
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


def select_rows(rows, method):
    """
    作用：根据命令行 method 参数筛选 joint/cartesian/both。
    输入：
        rows: 单次实验的两行指标。
        method: "joint"、"cartesian" 或 "both"。
    输出：
        selected_rows: 筛选后的指标列表。
    """
    if method == "both":
        return rows
    if method == "joint":
        return [row for row in rows if row["method"] == "joint_space"]
    return [row for row in rows if row["method"] == "cartesian_tracking"]


def main():
    """
    作用：程序主入口，扫描不同 total_time 并保存 CSV 和趋势图。
    输入：
        无，实验参数来自命令行。
    输出：
        无，结果保存到 outputs。
    """
    args = parse_args()
    start_xy = np.array([args.start_x, args.start_y], dtype=float)
    goal_xy = np.array([args.goal_x, args.goal_y], dtype=float)
    all_rows = []

    for total_time in args.total_times:
        result = run_compare_experiment(
            start_xy=start_xy,
            goal_xy=goal_xy,
            num_points=args.num_points,
            method="quintic",
            total_time=total_time,
            inner_steps=args.inner_steps,
        )
        if not result["rows"]:
            print(f"total_time={total_time}: 起点或终点不可达，跳过。")
            continue
        for row in select_rows(result["rows"], args.method):
            row = dict(row)
            row["total_time"] = float(total_time)
            all_rows.append(row)

    if not all_rows:
        print("没有可保存的实验结果。")
        return

    csv_path = save_csv(all_rows, PROJECT_ROOT / "outputs" / "logs" / "time_scaling_sweep.csv")
    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    velocity_path = plot_time_scaling_metric(
        all_rows,
        "max_joint_velocity",
        figure_dir / "time_scaling_velocity_compare.png",
        "不同 total_time 下的最大关节速度",
        "最大关节速度 / rad/s",
    )
    acceleration_path = plot_time_scaling_metric(
        all_rows,
        "max_joint_acceleration",
        figure_dir / "time_scaling_acceleration_compare.png",
        "不同 total_time 下的最大关节加速度",
        "最大关节加速度 / rad/s^2",
    )
    summary_path = plot_time_scaling_metrics(
        all_rows,
        figure_dir / "time_scaling_metric_summary.png",
    )

    print("=== total_time 扫描完成 ===")
    print(f"CSV 已保存: {csv_path}")
    print(f"速度对比图: {velocity_path}")
    print(f"加速度对比图: {acceleration_path}")
    print(f"指标汇总图: {summary_path}")
    print("观察建议：total_time 变大时，速度和加速度通常会降低；如果仍然违规，说明轨迹或控制参数需要继续调整。")


if __name__ == "__main__":
    main()
