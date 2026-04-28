"""运行 2D 二连杆机械臂目标点控制 demo。"""

import argparse
import sys
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from robot_arm_target_control_study.plotting import save_all_plots
from robot_arm_target_control_study.simulation import run_reach_simulation


def parse_args():
    """
    作用：读取命令行输入的目标点参数。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含 target_x 和 target_y。
    """
    parser = argparse.ArgumentParser(description="2D 二连杆机械臂目标点控制 demo")
    parser.add_argument("--target_x", type=float, required=True, help="目标点 x 坐标")
    parser.add_argument("--target_y", type=float, required=True, help="目标点 y 坐标")
    return parser.parse_args()


def print_result(result, plot_files):
    """
    作用：在终端打印仿真结果和图片保存路径。
    输入：
        result: run_reach_simulation 返回的结果字典。
        plot_files: save_all_plots 返回的图片路径字典。
    输出：
        无，只负责打印信息。
    """
    target = result["target"]
    end_effector = result["positions"][-1]
    status = "已到达目标附近" if result["reached"] else "未完全到达，已尽量靠近"

    print("=== 2D 二连杆机械臂目标点控制 ===")
    print(f"目标点: ({target[0]:.3f}, {target[1]:.3f})")
    print(f"最终末端位置: ({end_effector[0]:.3f}, {end_effector[1]:.3f})")
    print(f"最终误差: {result['final_error']:.6f}")
    print(f"状态: {status}")
    print("输出图片:")
    for name, path in plot_files.items():
        print(f"  {name}: {path}")


def main():
    """
    作用：程序主入口，完成参数读取、仿真、画图和结果打印。
    输入：
        无，目标点由命令行传入。
    输出：
        无。
    """
    args = parse_args()
    target = np.array([args.target_x, args.target_y], dtype=float)

    result = run_reach_simulation(target)
    plot_files = save_all_plots(result, output_dir=PROJECT_ROOT / "outputs")
    print_result(result, plot_files)


if __name__ == "__main__":
    main()
