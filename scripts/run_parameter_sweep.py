"""扫描 gain 和 max_step 参数，观察普通雅可比伪逆控制效果。"""

import argparse
import csv
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from robot_arm_target_control_study.controller import compute_control_step
from robot_arm_target_control_study.plotting import (
    plot_error_comparison,
    plot_single_joint_comparison,
)
from robot_arm_target_control_study.simulation import simulate_iterative_control


def parse_args():
    """
    作用：读取命令行输入的目标点坐标。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含 target_x 和 target_y。
    """
    parser = argparse.ArgumentParser(description="扫描普通雅可比伪逆控制参数")
    parser.add_argument("--target_x", type=float, required=True, help="目标点 x 坐标")
    parser.add_argument("--target_y", type=float, required=True, help="目标点 y 坐标")
    return parser.parse_args()


def run_sweep(target):
    """
    作用：自动测试多组 gain 和 max_step 参数。
    输入：
        target: 形状为 (2,) 的目标点坐标。
    输出：
        rows: 列表，每个元素是一组实验结果字典。
    """
    gain_list = [0.2, 0.5, 0.8, 1.0, 1.2]
    max_step_list = [0.03, 0.05, 0.08, 0.12]
    rows = []

    for gain in gain_list:
        for max_step in max_step_list:
            history = simulate_iterative_control(
                control_method=compute_control_step,
                initial_theta=(0.3, 0.3),
                target=target,
                link1=1.0,
                link2=0.8,
                max_iterations=200,
                tolerance=0.01,
                gain=gain,
                max_step=max_step,
            )
            rows.append(
                {
                    "target_x": float(target[0]),
                    "target_y": float(target[1]),
                    "gain": gain,
                    "max_step": max_step,
                    "final_error": history["final_error"],
                    "iterations": history["iterations"],
                    "success": history["success"],
                }
            )

    return rows


def save_csv(rows, save_path):
    """
    作用：把参数扫描结果保存成 CSV 文件，方便后续整理实验记录。
    输入：
        rows: 实验结果字典列表。
        save_path: CSV 保存路径。
    输出：
        file_path: 保存后的 Path。
    """
    file_path = Path(save_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["target_x", "target_y", "gain", "max_step", "final_error", "iterations", "success"]

    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return file_path


def run_single_parameter_comparisons(target):
    """
    作用：分别固定一个参数、改变另一个参数，生成用于画曲线的实验历史。
    输入：
        target: 形状为 (2,) 的目标点坐标。
    输出：
        comparisons: 字典，包含 gain 对比和 max_step 对比的误差与关节角历史。
    """
    gain_list = [0.2, 0.5, 0.8, 1.0, 1.2]
    max_step_list = [0.03, 0.05, 0.08, 0.12]
    fixed_gain = 0.8
    fixed_max_step = 0.08

    gain_histories = []
    for gain in gain_list:
        # 比较 gain 时固定 max_step，避免两个参数同时变化导致原因不清楚。
        gain_histories.append(
            simulate_iterative_control(
                control_method=compute_control_step,
                initial_theta=(0.3, 0.3),
                target=target,
                link1=1.0,
                link2=0.8,
                max_iterations=200,
                tolerance=0.001,
                gain=gain,
                max_step=fixed_max_step,
            )
        )

    max_step_histories = []
    for max_step in max_step_list:
        # 比较 max_step 时固定 gain，让曲线主要反映单步限幅的影响。
        max_step_histories.append(
            simulate_iterative_control(
                control_method=compute_control_step,
                initial_theta=(0.3, 0.3),
                target=target,
                link1=1.0,
                link2=0.8,
                max_iterations=200,
                tolerance=0.001,
                gain=fixed_gain,
                max_step=max_step,
            )
        )

    return {
        "gain": {
            "histories": gain_histories,
            "labels": [f"gain={gain}" for gain in gain_list],
            "fixed": f"固定 max_step={fixed_max_step}",
        },
        "max_step": {
            "histories": max_step_histories,
            "labels": [f"max_step={max_step}" for max_step in max_step_list],
            "fixed": f"固定 gain={fixed_gain}",
        },
    }


def save_comparison_plots(comparisons):
    """
    作用：保存 gain 和 max_step 的误差曲线、theta1 曲线、theta2 曲线对比图。
    输入：
        comparisons: run_single_parameter_comparisons 返回的实验历史字典。
    输出：
        plot_files: 字典，记录所有输出图片路径。
    """
    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    plot_files = {}

    gain_histories = comparisons["gain"]["histories"]
    gain_labels = comparisons["gain"]["labels"]
    gain_fixed = comparisons["gain"]["fixed"]
    plot_files["gain_error"] = plot_error_comparison(
        [history["error_history"] for history in gain_histories],
        gain_labels,
        figure_dir / "gain_error_comparison.png",
        f"不同 gain 的误差曲线对比（{gain_fixed}）",
    )
    plot_files["gain_theta1"] = plot_single_joint_comparison(
        [history["theta_history"] for history in gain_histories],
        gain_labels,
        0,
        figure_dir / "gain_theta1_comparison.png",
        f"不同 gain 的 theta1 变化对比（{gain_fixed}）",
    )
    plot_files["gain_theta2"] = plot_single_joint_comparison(
        [history["theta_history"] for history in gain_histories],
        gain_labels,
        1,
        figure_dir / "gain_theta2_comparison.png",
        f"不同 gain 的 theta2 变化对比（{gain_fixed}）",
    )

    max_step_histories = comparisons["max_step"]["histories"]
    max_step_labels = comparisons["max_step"]["labels"]
    max_step_fixed = comparisons["max_step"]["fixed"]
    plot_files["max_step_error"] = plot_error_comparison(
        [history["error_history"] for history in max_step_histories],
        max_step_labels,
        figure_dir / "max_step_error_comparison.png",
        f"不同 max_step 的误差曲线对比（{max_step_fixed}）",
    )
    plot_files["max_step_theta1"] = plot_single_joint_comparison(
        [history["theta_history"] for history in max_step_histories],
        max_step_labels,
        0,
        figure_dir / "max_step_theta1_comparison.png",
        f"不同 max_step 的 theta1 变化对比（{max_step_fixed}）",
    )
    plot_files["max_step_theta2"] = plot_single_joint_comparison(
        [history["theta_history"] for history in max_step_histories],
        max_step_labels,
        1,
        figure_dir / "max_step_theta2_comparison.png",
        f"不同 max_step 的 theta2 变化对比（{max_step_fixed}）",
    )

    return plot_files


def print_table(rows):
    """
    作用：在终端打印简洁表格，快速比较不同参数组合的效果。
    输入：
        rows: 实验结果字典列表。
    输出：
        无，只负责打印信息。
    """
    print("=== 参数扫描：普通雅可比伪逆控制 ===")
    print(f"{'gain':>6} {'max_step':>9} {'final_error':>13} {'iterations':>10} {'success':>8}")
    print("-" * 52)
    for row in rows:
        print(
            f"{row['gain']:>6.2f} "
            f"{row['max_step']:>9.2f} "
            f"{row['final_error']:>13.6f} "
            f"{row['iterations']:>10d} "
            f"{str(row['success']):>8}"
        )


def main():
    """
    作用：程序主入口，完成参数读取、扫描、CSV 保存和结果打印。
    输入：
        无，目标点由命令行传入。
    输出：
        无。
    """
    args = parse_args()
    target = np.array([args.target_x, args.target_y], dtype=float)
    rows = run_sweep(target)
    csv_path = save_csv(rows, PROJECT_ROOT / "outputs" / "logs" / "parameter_sweep.csv")
    comparisons = run_single_parameter_comparisons(target)
    plot_files = save_comparison_plots(comparisons)
    print_table(rows)
    print(f"CSV 已保存: {csv_path}")
    print("对比曲线已保存:")
    for name, path in plot_files.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
