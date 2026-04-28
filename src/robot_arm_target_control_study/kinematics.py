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
