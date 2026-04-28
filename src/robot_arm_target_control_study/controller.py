"""基于雅可比伪逆的简单目标点控制器。"""

import numpy as np

from robot_arm_target_control_study.kinematics import compute_jacobian, forward_kinematics


def limit_joint_step(delta_theta, max_step):
    """
    作用：限制单次关节角更新量，避免机械臂数值上突然大幅跳动。
    输入：
        delta_theta: 形状为 (2,) 的数组，表示本次希望更新的两个关节角。
        max_step: 单个关节每次允许变化的最大弧度。
    输出：
        limited_delta: 限幅后的关节角更新量。
    """
    return np.clip(delta_theta, -max_step, max_step)


def compute_control_step(
    theta,
    target,
    end_effector,
    link1,
    link2,
    gain=0.8,
    max_step=0.08,
):
    """
    作用：根据当前末端误差，计算下一步应该调整多少关节角。
    输入：
        theta: 形状为 (2,) 的数组，当前两个关节角。
        target: 形状为 (2,) 的数组，目标点坐标。
        end_effector: 形状为 (2,) 的数组，当前末端坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        gain: 控制增益，越大表示越积极地朝目标移动。
        max_step: 单步关节角更新限幅。
    输出：
        delta_theta: 形状为 (2,) 的数组，下一步关节角更新量。
        error_vector: 形状为 (2,) 的数组，目标点减去当前末端点。
        error_norm: 浮点数，当前末端距离目标点的欧氏距离。
    """
    error_vector = target - end_effector
    # 平方之和开平方，计算距离
    error_norm = float(np.linalg.norm(error_vector))
    # 实例化计算雅可比矩阵
    jacobian = compute_jacobian(theta[0], theta[1], link1, link2)
    # Δx ≈ J Δθ => Δθ ≈ J^+ Δx，其中 J^+ 是雅可比矩阵的伪逆，np.linalg.pinv 会自动处理奇异情况
    # 根据当前机械臂姿态，用雅可比矩阵的伪逆，把末端到目标点的误差转换成两个关节应该调整的角度，并乘上一个控制增益，让机械臂逐步向目标靠近。
    delta_theta = gain * np.linalg.pinv(jacobian) @ error_vector
    # 限制单步更新量，避免数值不稳定
    delta_theta = limit_joint_step(delta_theta, max_step)
    # 最后返回计算好的关节角更新量、误差向量和误差大小
    return delta_theta, error_vector, error_norm


def compute_damped_jacobian_step(
    theta,
    target,
    link1,
    link2,
    gain=0.8,
    damping=0.05,
    max_step=0.08,
):
    """
    作用：使用阻尼最小二乘方法计算本轮关节角更新量，并返回更新后的关节角。
    输入：
        theta: 形状为 (2,) 的数组，当前两个关节角。
        target: 形状为 (2,) 的数组，目标点坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        gain: 控制增益，越大表示越积极地朝目标移动。
        damping: 阻尼系数 lambda，用来减小接近奇异位形时的剧烈更新。
        max_step: 单个关节每次允许变化的最大弧度。
    输出：
        new_theta: 形状为 (2,) 的数组，更新后的关节角。
        error_norm: 浮点数，当前末端距离目标点的欧氏距离。
        delta_theta: 形状为 (2,) 的数组，本轮关节角更新量。
    """
    theta = np.array(theta, dtype=float)
    target = np.array(target, dtype=float)

    positions = forward_kinematics(theta[0], theta[1], link1, link2)
    end_effector = positions[-1]
    error_vector = target - end_effector
    error_norm = float(np.linalg.norm(error_vector))

    jacobian = compute_jacobian(theta[0], theta[1], link1, link2)
    identity = np.eye(2)
    # 阻尼最小二乘公式：
    # Δθ = J.T @ inv(J @ J.T + λ^2 I) @ error
    # 其中 λ^2 I 会让矩阵更容易求解，也会压住接近奇异位形时过大的关节角更新。
    damping_matrix = jacobian @ jacobian.T + (damping**2) * identity
    delta_theta = gain * jacobian.T @ np.linalg.solve(damping_matrix, error_vector)

    # 和普通伪逆控制一样，限制单步关节角变化，避免一次跳得太大。
    delta_theta = limit_joint_step(delta_theta, max_step)
    new_theta = theta + delta_theta

    return new_theta, error_norm, delta_theta
