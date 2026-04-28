"""对比解析逆运动学和雅可比伪逆迭代控制。"""

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
    is_target_reachable,
)
from robot_arm_target_control_study.plotting import plot_workspace
from robot_arm_target_control_study.simulation import run_reach_simulation


def parse_args():
    """
    作用：读取命令行输入的目标点参数。
    输入：
        无，参数来自命令行。
    输出：
        args: argparse.Namespace，包含 target_x 和 target_y。
    """
    parser = argparse.ArgumentParser(description="解析逆运动学 vs 雅可比伪逆控制对比")
    parser.add_argument("--target_x", type=float, required=True, help="目标点 x 坐标")
    parser.add_argument("--target_y", type=float, required=True, help="目标点 y 坐标")
    return parser.parse_args()


def run_analytic_method(target_x, target_y, link1, link2):
    """
    作用：运行解析逆运动学，并用正运动学验证末端位置。
    输入：
        target_x: 目标点 x 坐标。
        target_y: 目标点 y 坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
    输出：
        result: 字典，包含关节角、末端位置、误差和说明信息。
    """
    theta1, theta2, reachable, message = inverse_kinematics_analytic(
        target_x,
        target_y,
        link1,
        link2,
        elbow="down",
    )

    if not reachable:
        return {
            "theta1": theta1,
            "theta2": theta2,
            "reachable": reachable,
            "message": message,
            "positions": None,
            "end_effector": None,
            "final_error": None,
        }

    positions = forward_kinematics(theta1, theta2, link1, link2)
    end_effector = positions[-1]
    target = np.array([target_x, target_y], dtype=float)
    final_error = float(np.linalg.norm(target - end_effector))

    return {
        "theta1": theta1,
        "theta2": theta2,
        "reachable": reachable,
        "message": message,
        "positions": positions,
        "end_effector": end_effector,
        "final_error": final_error,
    }


def print_compare_result(target, reachable_info, analytic_result, iterative_result, workspace_path):
    """
    作用：在终端打印两种方法的对比结果。
    输入：
        target: 形状为 (2,) 的数组，目标点坐标。
        reachable_info: 二元组，包含是否可达和中文原因。
        analytic_result: 解析逆运动学结果字典。
        iterative_result: 雅可比伪逆控制结果字典。
        workspace_path: 工作空间图片路径。
    输出：
        无，只负责打印信息。
    """
    reachable, reason = reachable_info
    iterative_end = iterative_result["positions"][-1]
    iterative_steps = len(iterative_result["history"]["error"])

    print("=== 解析逆运动学 vs 雅可比伪逆迭代控制 ===")
    print(f"目标点: ({target[0]:.3f}, {target[1]:.3f})")
    print(f"是否可达: {reachable}")
    print(f"可达性说明: {reason}")
    print()

    print("方法 A：解析逆运动学")
    if analytic_result["reachable"]:
        print(f"theta1: {analytic_result['theta1']:.6f} rad")
        print(f"theta2: {analytic_result['theta2']:.6f} rad")
        analytic_end = analytic_result["end_effector"]
        print(f"最终末端位置: ({analytic_end[0]:.6f}, {analytic_end[1]:.6f})")
        print(f"最终误差: {analytic_result['final_error']:.9f}")
    else:
        print("theta1: None")
        print("theta2: None")
        print(f"说明: {analytic_result['message']}")
    print()

    print("方法 B：雅可比伪逆迭代控制")
    print(f"最终末端位置: ({iterative_end[0]:.6f}, {iterative_end[1]:.6f})")
    print(f"最终误差: {iterative_result['final_error']:.9f}")
    print(f"迭代步数: {iterative_steps}")
    print()

    print("简短对比说明:")
    print("- 解析逆运动学是直接求解，目标可达且结构简单时通常一步得到答案。")
    print("- 雅可比伪逆控制是迭代逼近，更容易推广到复杂机械臂，但会受初始角度、步长和奇异位形影响。")
    print(f"工作空间图片: {workspace_path}")


def main():
    """
    作用：程序主入口，完成参数读取、两种方法运行、工作空间画图和结果打印。
    输入：
        无，目标点由命令行传入。
    输出：
        无。
    """
    args = parse_args()
    link1 = 1.0
    link2 = 0.8
    target = np.array([args.target_x, args.target_y], dtype=float)

    reachable_info = is_target_reachable(args.target_x, args.target_y, link1, link2)
    analytic_result = run_analytic_method(args.target_x, args.target_y, link1, link2)
    iterative_result = run_reach_simulation(target, link1=link1, link2=link2)
    workspace_path = plot_workspace(link1, link2, PROJECT_ROOT / "outputs" / "figures" / "workspace.png")

    print_compare_result(target, reachable_info, analytic_result, iterative_result, workspace_path)


if __name__ == "__main__":
    main()
