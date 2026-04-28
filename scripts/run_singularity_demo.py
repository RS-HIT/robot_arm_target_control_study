"""演示接近伸直边界时普通伪逆和阻尼雅可比控制的差异。"""

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
    plot_multiple_error_curves,
    plot_multiple_joint_curves,
)
from robot_arm_target_control_study.simulation import simulate_iterative_control


def run_singularity_experiment():
    """
    作用：运行接近最大伸展边界的目标点实验。
    输入：
        无，函数内部使用默认目标点 (1.75, 0.05)。
    输出：
        pinv_history: 普通伪逆控制历史。
        damped_history: 阻尼雅可比控制历史。
        target: 本次实验目标点。
    """
    target = np.array([1.75, 0.05], dtype=float)
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

    return pinv_history, damped_history, target


def save_singularity_plots(pinv_history, damped_history):
    """
    作用：保存奇异位形实验中的误差曲线和关节角曲线。
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
        figure_dir / "singularity_error.png",
        "接近伸直边界时的误差曲线",
    )
    joint_path = plot_multiple_joint_curves(
        [pinv_history["theta_history"], damped_history["theta_history"]],
        ["普通伪逆", "阻尼雅可比"],
        figure_dir / "singularity_joint_angles.png",
        "接近伸直边界时的关节角变化",
    )
    return {"error": error_path, "joint_angles": joint_path}


def print_singularity_result(pinv_history, damped_history, target, plot_files):
    """
    作用：打印奇异位形实验结果和中文解释。
    输入：
        pinv_history: 普通伪逆控制历史。
        damped_history: 阻尼雅可比控制历史。
        target: 本次实验目标点。
        plot_files: 输出图片路径字典。
    输出：
        无，只负责打印信息。
    """
    print("=== 奇异位形实验：接近机械臂最大伸展边界 ===")
    print(f"目标点: ({target[0]:.3f}, {target[1]:.3f})")
    print(f"普通伪逆 final_error: {pinv_history['final_error']:.6f}")
    print(f"普通伪逆 iterations: {pinv_history['iterations']}")
    print(f"阻尼伪逆 final_error: {damped_history['final_error']:.6f}")
    print(f"阻尼伪逆 iterations: {damped_history['iterations']}")
    print()
    print("解释：当机械臂几乎伸直时，雅可比矩阵会变得不稳定。")
    print("普通伪逆可能为了修正很小的末端误差，给出较大的关节角更新。")
    print("阻尼雅可比在矩阵中加入 damping^2 * I，让更新更保守，通常更平滑。")
    print("输出图片:")
    for name, path in plot_files.items():
        print(f"  {name}: {path}")


def main():
    """
    作用：程序主入口，运行奇异位形实验、保存图像并打印解释。
    输入：
        无。
    输出：
        无。
    """
    pinv_history, damped_history, target = run_singularity_experiment()
    plot_files = save_singularity_plots(pinv_history, damped_history)
    print_singularity_result(pinv_history, damped_history, target, plot_files)


if __name__ == "__main__":
    main()
