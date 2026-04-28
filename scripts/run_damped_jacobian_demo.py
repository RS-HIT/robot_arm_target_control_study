"""对比普通雅可比伪逆控制和阻尼雅可比控制。"""

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from robot_arm_target_control_study.controller import (
    compute_control_step,
    compute_damped_jacobian_step,
)
from robot_arm_target_control_study.plotting import (
    plot_error_comparison,
    plot_joint_angle_comparison,
    plot_multiple_error_curves,
    plot_multiple_joint_curves,
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
    parser = argparse.ArgumentParser(description="普通伪逆 vs 阻尼雅可比控制")
    parser.add_argument("--target_x", type=float, required=True, help="目标点 x 坐标")
    parser.add_argument("--target_y", type=float, required=True, help="目标点 y 坐标")
    return parser.parse_args()


def run_comparison(target):
    """
    作用：分别运行普通雅可比伪逆控制和阻尼雅可比控制。
    输入：
        target: 形状为 (2,) 的目标点坐标。
    输出：
        pinv_history: 普通伪逆控制历史。
        damped_history: 阻尼雅可比控制历史。
    """
    common_params = {
        "initial_theta": (0.0, 0.0),
        "target": target,
        "link1": 1.0,
        "link2": 0.8,
        "max_iterations": 250,
        "tolerance": 0.01,
    }
    pinv_history = simulate_iterative_control(
        control_method=compute_control_step,
        **common_params,
        gain=0.8,
        max_step=0.08,
    )
    damped_history = simulate_iterative_control(
        control_method=compute_damped_jacobian_step,
        **common_params,
        gain=0.8,
        damping=0.08,
        max_step=0.08,
    )
    return pinv_history, damped_history


def save_plots(pinv_history, damped_history):
    """
    作用：保存两种控制方法的误差曲线和关节角曲线。
    输入：
        pinv_history: 普通伪逆控制历史。
        damped_history: 阻尼雅可比控制历史。
    输出：
        plot_files: 字典，包含两张图片的路径。
    """
    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    error_path = plot_multiple_error_curves(
        [pinv_history["error_history"], damped_history["error_history"]],
        ["普通伪逆", "阻尼雅可比"],
        figure_dir / "pinv_vs_damped_error.png",
        "普通伪逆与阻尼雅可比误差曲线",
    )
    joint_path = plot_multiple_joint_curves(
        [pinv_history["theta_history"], damped_history["theta_history"]],
        ["普通伪逆", "阻尼雅可比"],
        figure_dir / "pinv_vs_damped_joint_angles.png",
        "普通伪逆与阻尼雅可比关节角变化",
    )
    return {"error": error_path, "joint_angles": joint_path}


def run_damping_comparison(target):
    """
    作用：固定目标点和其他控制参数，只改变 damping，观察阻尼大小对控制过程的影响。
    输入：
        target: 形状为 (2,) 的目标点坐标。
    输出：
        histories: 多组阻尼雅可比控制历史。
        labels: 每组历史对应的 damping 标签。
    """
    damping_list = [0.01, 0.05, 0.1, 0.3]
    histories = []

    for damping in damping_list:
        histories.append(
            simulate_iterative_control(
                control_method=compute_damped_jacobian_step,
                initial_theta=(0.0, 0.0),
                target=target,
                link1=1.0,
                link2=0.8,
                max_iterations=250,
                tolerance=0.001,
                gain=0.8,
                damping=damping,
                max_step=0.08,
            )
        )

    labels = [f"damping={damping}" for damping in damping_list]
    return histories, labels


def save_damping_plots(histories, labels):
    """
    作用：保存不同 damping 下的误差曲线、theta1 曲线和 theta2 曲线对比图。
    输入：
        histories: 多组阻尼雅可比控制历史。
        labels: 每组历史对应的 damping 标签。
    输出：
        plot_files: 字典，包含三张图片的路径。
    """
    figure_dir = PROJECT_ROOT / "outputs" / "figures"
    error_path = plot_error_comparison(
        [history["error_history"] for history in histories],
        labels,
        figure_dir / "damping_error_comparison.png",
        "不同 damping 的误差曲线对比",
    )
    theta1_path = plot_joint_angle_comparison(
        [history["theta_history"] for history in histories],
        labels,
        figure_dir / "damping_theta1_comparison.png",
        "不同 damping 的 theta1 变化对比",
    )
    theta2_path = plot_joint_angle_comparison(
        [history["theta_history"] for history in histories],
        labels,
        figure_dir / "damping_theta2_comparison.png",
        "不同 damping 的 theta2 变化对比",
    )
    return {
        "damping_error": error_path,
        "damping_theta1": theta1_path,
        "damping_theta2": theta2_path,
    }


def print_result(pinv_history, damped_history, plot_files, damping_plot_files):
    """
    作用：在终端打印两种控制方法的最终误差、迭代次数和简短结论。
    输入：
        pinv_history: 普通伪逆控制历史。
        damped_history: 阻尼雅可比控制历史。
        plot_files: 输出图片路径字典。
        damping_plot_files: 不同 damping 对比图片路径字典。
    输出：
        无，只负责打印信息。
    """
    print("=== 普通雅可比伪逆 vs 阻尼雅可比控制 ===")
    print(f"普通伪逆 final_error: {pinv_history['final_error']:.6f}")
    print(f"普通伪逆 iterations: {pinv_history['iterations']}")
    print(f"阻尼伪逆 final_error: {damped_history['final_error']:.6f}")
    print(f"阻尼伪逆 iterations: {damped_history['iterations']}")
    print("简短结论：阻尼项会让关节角更新更保守，通常更适合接近奇异位形的目标。")
    print("输出图片:")
    for name, path in plot_files.items():
        print(f"  {name}: {path}")
    print("不同 damping 对比图片:")
    for name, path in damping_plot_files.items():
        print(f"  {name}: {path}")


def main():
    """
    作用：程序主入口，完成参数读取、对比实验、绘图和结果打印。
    输入：
        无，目标点由命令行传入。
    输出：
        无。
    """
    args = parse_args()
    target = np.array([args.target_x, args.target_y], dtype=float)
    pinv_history, damped_history = run_comparison(target)
    plot_files = save_plots(pinv_history, damped_history)
    damping_histories, damping_labels = run_damping_comparison(target)
    damping_plot_files = save_damping_plots(damping_histories, damping_labels)
    print_result(pinv_history, damped_history, plot_files, damping_plot_files)


if __name__ == "__main__":
    main()
