"""二连杆机械臂的基础运动学函数。"""

import numpy as np


def forward_kinematics(theta1, theta2, link1, link2):
    """
    作用：根据两个关节角，计算机械臂基座、肘关节和末端的位置。
    输入：
        theta1: 第一个关节角，单位为弧度。
        theta2: 第二个关节角，单位为弧度，是相对第一根连杆的角度。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
    输出：
        positions: 形状为 (3, 2) 的数组，依次是基座、肘关节、末端坐标。
    """
    base = np.array([0.0, 0.0]) # 基座固定点，规格为 (2,)
    # 肘关节坐标计算：第一根连杆的末端位置就是肘关节的位置
    elbow_x = link1 * np.cos(theta1) 
    elbow_y = link1 * np.sin(theta1) 
    elbow = np.array([elbow_x, elbow_y]) # 肘关节坐标，规格为 (2,)
    # 末端坐标计算：从肘关节出发，第二根连杆的末端位置就是末端执行器的位置
    end_x = elbow_x + link2 * np.cos(theta1 + theta2) 
    end_y = elbow_y + link2 * np.sin(theta1 + theta2) 
    end_effector = np.array([end_x, end_y]) # 末端执行器坐标，规格为 (2,)
    # 最后把三个点的坐标堆叠成一个 (3, 2) 的数组返回
    return np.vstack([base, elbow, end_effector])


def compute_jacobian(theta1, theta2, link1, link2):
    """
    作用：计算 2D 二连杆机械臂末端位置对关节角的雅可比矩阵。
    输入：
        theta1: 第一个关节角，单位为弧度。
        theta2: 第二个关节角，单位为弧度。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
    输出：
        jacobian: 形状为 (2, 2) 的数组，把关节角速度映射到末端速度。
    """
    total_angle = theta1 + theta2
    # 雅可比矩阵的元素计算：根据末端位置对每个关节角的偏导数来填充矩阵
    dx_dtheta1 = -link1 * np.sin(theta1) - link2 * np.sin(total_angle)
    dx_dtheta2 = -link2 * np.sin(total_angle)
    dy_dtheta1 = link1 * np.cos(theta1) + link2 * np.cos(total_angle)
    dy_dtheta2 = link2 * np.cos(total_angle)
    # 最后把计算好的元素组成一个 (2, 2) 的雅可比矩阵返回
    return np.array(
        [
            [dx_dtheta1, dx_dtheta2],
            [dy_dtheta1, dy_dtheta2],
        ]
    )


def is_target_reachable(target_x, target_y, link1, link2):
    """
    作用：判断目标点是否在二连杆机械臂的可达工作空间内。
    输入：
        target_x: 目标点的 x 坐标。
        target_y: 目标点的 y 坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
    输出：
        reachable: 布尔值，True 表示可达，False 表示不可达。
        reason: 中文说明，解释为什么可达或不可达。
    """
    # 目标点到基座的直线距离。这里把基座看作原点 (0, 0)。
    radius = float(np.sqrt(target_x**2 + target_y**2))
    # 两根连杆完全伸直时，末端离基座最远。
    max_reach = link1 + link2
    # 如果两根连杆长度不同，较长的那根无法完全“缩进”较短的那根里面。
    # 因此离基座太近的点也可能不可达。
    min_reach = abs(link1 - link2)

    if radius > max_reach:
        return False, f"目标点太远：距离基座 {radius:.3f}，最远只能到 {max_reach:.3f}。"

    if radius < min_reach:
        return False, f"目标点太近：距离基座 {radius:.3f}，最近只能到 {min_reach:.3f}。"

    return True, f"目标点可达：距离基座 {radius:.3f}，位于工作空间范围内。"


def inverse_kinematics_analytic(target_x, target_y, link1, link2, elbow="down"):
    """
    作用：用解析几何方法直接计算二连杆机械臂到达目标点所需的两个关节角。
    输入：
        target_x: 目标点的 x 坐标。
        target_y: 目标点的 y 坐标。
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        elbow: 肘部构型，可选 "down" 或 "up"。
    输出：
        theta1: 第一个关节角，单位为弧度；不可达时为 None。
        theta2: 第二个关节角，单位为弧度；不可达时为 None。
        reachable: 布尔值，表示目标点是否可达。
        message: 中文说明，解释计算结果或失败原因。
    """
    reachable, reason = is_target_reachable(target_x, target_y, link1, link2)
    if not reachable:
        return None, None, False, reason

    if elbow not in ("down", "up"):
        return None, None, False, 'elbow 参数只能是 "down" 或 "up"。'

    # r^2 是目标点到基座距离的平方。用平方可以少做一次开方，公式也更简洁。
    radius_squared = target_x**2 + target_y**2

    # 余弦定理：
    # r^2 = link1^2 + link2^2 + 2 * link1 * link2 * cos(theta2)
    # 变形后得到 cos(theta2)，也就是第二个关节角的余弦值。
    cos_theta2 = (radius_squared - link1**2 - link2**2) / (2.0 * link1 * link2)
    # 浮点计算可能得到 1.0000000002 这类很接近但略微越界的数。
    # arccos 只接受 [-1, 1]，所以这里先裁剪，避免数值误差让程序报错。
    cos_theta2 = float(np.clip(cos_theta2, -1.0, 1.0))

    # arccos 会给出一个非负角度。二连杆到同一个点通常有两种构型：
    # elbow="down" 使用正的 theta2，elbow="up" 使用负的 theta2。
    theta2_abs = float(np.arccos(cos_theta2))
    theta2 = theta2_abs if elbow == "down" else -theta2_abs

    # phi 是目标点相对基座的方向角，可以理解为“从原点看向目标点”的角度。
    phi = float(np.arctan2(target_y, target_x))
    # beta 是第一根连杆和“基座到目标点连线”之间的夹角。
    # atan2(对边, 邻边) 比直接 atan 更稳定，也能自动处理象限问题。
    beta = float(np.arctan2(link2 * np.sin(theta2), link1 + link2 * np.cos(theta2)))
    # 第一关节角 = 目标方向角 - 这段三角形内部偏转角。
    theta1 = phi - beta

    message = f"解析逆运动学计算成功，使用 elbow={elbow} 构型。"
    return float(theta1), float(theta2), True, message
