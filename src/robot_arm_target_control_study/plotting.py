"""仿真结果画图函数。"""

from pathlib import Path
# 导入 Path，用来处理文件路径。
# 比如 "outputs/arm_pose.png" 可以被 Path 更稳妥地处理。
# 好处是 Windows、Linux、WSL 下路径处理更统一。

import matplotlib as mpl
# 导入 matplotlib 的主配置模块。
# 这里主要是为了修改全局配置，比如中文字体、负号显示等。
import matplotlib.pyplot as plt
# 导入 matplotlib 的 pyplot 模块，并简写成 plt。
# 以后画图基本都靠 plt.figure(), plt.plot(), plt.savefig() 这些函数。
from matplotlib import font_manager
# 导入字体管理器。
# 这个模块可以查找系统字体、手动添加字体，用于解决中文乱码问题。
import numpy as np


def configure_chinese_font():
    """
    作用：为 Matplotlib 配置常见中文字体，减少中文标题无法显示的问题。
    输入：
        无，函数会自动检查当前系统可用字体。
    输出：
        font_name: 字符串或 None，表示实际使用的中文字体名称。
    """
    # 定义一个函数，用来配置中文字体。
    # 因为 Matplotlib 默认字体经常不支持中文，所以标题、坐标轴可能显示成方块。
    font_files = [
        "/usr/share/fonts/truetype/arphic/uming.ttc",
        "/usr/share/fonts/truetype/arphic-gkai00mp/gkai00mp.ttf",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    # 这里列出几个 Linux/WSL 系统中可能存在的中文字体文件路径。
    # 注意：这是“字体文件的绝对路径”，不是字体名字。
    # 程序会逐个检查这些文件是否存在。
    for font_file in font_files:
        # 遍历上面列出的每一个字体文件路径。
        font_path = Path(font_file)
        # 把字符串路径转换成 Path 对象。
        # 这样可以使用 font_path.exists() 判断文件是否存在。
        # 如果这个字体文件不存在，就跳过它。
        if not font_path.exists():
            # continue 表示进入下一轮循环，检查下一个字体文件。
            continue
        # 如果字体文件存在，就把这个字体添加到 Matplotlib 的字体管理器中。
        # 否则 Matplotlib 不一定知道这个字体可用。
        font_manager.fontManager.addfont(font_path)
        font_name = font_manager.FontProperties(fname=font_path).get_name()
        # 根据字体文件读取它真正的字体名称。
        # 例如某个 .ttf 文件对应的字体名可能叫 "AR PL UMing CN"。
        mpl.rcParams["font.sans-serif"] = [font_name, "DejaVu Sans"]
        # 修改 Matplotlib 的全局字体配置。
        # 意思是：优先用 font_name 这个中文字体；
        # 如果某些字符它没有，就退回用 DejaVu Sans。
        mpl.rcParams["axes.unicode_minus"] = False
        # 解决坐标轴负号显示为方块的问题。
        # 很多中文字体不支持默认的 Unicode 负号，所以这里改成普通负号显示。
        return font_name
        # 找到可用字体后，就返回字体名称，并结束函数。

    candidates = [
        "AR PL UMing CN",
        "AR PL KaitiM GB",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Microsoft YaHei",
        "SimHei",
        "WenQuanYi Micro Hei",
        "Droid Sans Fallback",
    ]
    # 如果上面的字体文件路径都没找到，就尝试按“字体名称”查找。
    # 这些是常见中文字体名：
    # Microsoft YaHei 是微软雅黑；
    # SimHei 是黑体；
    # Noto Sans CJK SC 是思源/Noto 中文字体。
    for font_name in candidates:
        # 遍历候选字体名称。
        try:
             # try 表示尝试执行下面的代码。
            # 因为查找字体可能失败，所以要用 try-except 防止程序崩溃。

            font_manager.findfont(font_name, fallback_to_default=False)
            # 尝试查找这个字体。
            # fallback_to_default=False 表示：
            # 如果找不到这个字体，不要偷偷换成默认字体，而是直接报错。
        except ValueError:
            # 如果找不到字体，Matplotlib 会抛出 ValueError 错误。
            continue

        mpl.rcParams["font.sans-serif"] = [font_name]
        # 找到了这个字体，就设置为默认无衬线字体。
        # 后面画中文标题、中文图例时就会用这个字体。
        mpl.rcParams["axes.unicode_minus"] = False
        # 同样解决负号显示问题。
        return font_name
    # 返回找到的字体名称，并结束函数。

    # 如果所有字体文件和字体名称都找不到，就返回 None。
    # 这表示没有成功配置中文字体。
    # 这时图仍然能画，但中文可能显示成乱码或方块。
    return None


def ensure_output_dir(output_dir):
    """
    作用：确保输出图片目录存在。
    输入：
        output_dir: 字符串或 Path，表示输出目录。
    输出：
        output_path: Path 对象，表示已经创建好的输出目录。
    """
    # 定义一个函数，用来确保输出文件夹存在。
    # 例如 outputs 文件夹不存在时，自动创建它。
    output_path = Path(output_dir)
    # 把传入的 output_dir 转换为 Path 对象。
    # 例如 "outputs" 会变成 Path("outputs")。
    output_path.mkdir(parents=True, exist_ok=True)
    # 创建这个文件夹。
    # parents=True 表示如果上级目录也不存在，就一起创建。
    # exist_ok=True 表示如果文件夹已经存在，不要报错。
    return output_path
    # 返回创建好的 Path 对象，后面可以用它拼接图片文件名。



def plot_arm_pose(positions, target, output_dir):
    """
    作用：绘制机械臂最终姿态图，包括目标点和末端点。
    输入：
        positions: 形状为 (3, 2) 的数组，基座、肘关节、末端坐标。
        target: 形状为 (2,) 的数组，目标点坐标。
        output_dir: 输出目录。
    输出：
        file_path: 保存图片的 Path。
    """
    # 定义一个函数，用来画机械臂最终姿态图。
    # 这个图的作用是直观看机械臂最后有没有够到目标点。
    output_path = ensure_output_dir(output_dir)
    # 确保输出目录存在。
    # 比如 output_dir="outputs"，如果 outputs 不存在，就自动创建。
    file_path = output_path / "arm_pose.png"
    # 拼接最终图片路径。
    # 比如 output_path 是 Path("outputs")，
    # 那么 file_path 就是 Path("outputs/arm_pose.png")。


    plt.figure(figsize=(6, 6))
    # 创建一张新图。
    # figsize=(6, 6) 表示图的宽和高都是 6 英寸。
    # 因为机械臂姿态图需要 x/y 比例一致，所以这里设置成正方形比较合适。
    plt.plot(positions[:, 0], positions[:, 1], "-o", linewidth=3, label="机械臂")
    # 画机械臂连杆。
    # positions[:, 0] 表示取所有点的 x 坐标。
    # positions[:, 1] 表示取所有点的 y 坐标。
    # "-o" 表示用线连接，并且每个关节点画一个圆点。
    # linewidth=3 表示线宽为 3，线会比较粗。
    # label="机械臂" 表示这条线在图例中叫“机械臂”。

    plt.scatter(target[0], target[1], c="red", marker="x", s=100, label="目标点")
    # 画目标点。
    # target[0] 是目标点 x 坐标。
    # target[1] 是目标点 y 坐标。
    # c="red" 表示颜色为红色。
    # marker="x" 表示用叉号标记。
    # s=100 表示点的大小。
    # label="目标点" 表示图例名称。

    plt.scatter(
        positions[-1, 0],
        positions[-1, 1],
        c="green",
        marker="o",
        s=70,
        label="末端点",
    )
    # 画机械臂末端点。
    # positions[-1, 0] 表示最后一个点的 x 坐标，也就是末端 x。
    # positions[-1, 1] 表示最后一个点的 y 坐标，也就是末端 y。
    # c="green" 表示绿色。
    # marker="o" 表示圆点。
    # s=70 表示点大小。
    # label="末端点" 表示图例名称。
    plt.title("二连杆机械臂最终姿态")
    # 设置图标题。
    plt.xlabel("x 位置")
    # 设置 x 轴名称。
    plt.ylabel("y 位置")
    # 设置 y 轴名称。
    plt.axis("equal")
    # 设置 x 轴和 y 轴等比例显示。
    # 这一句对机械臂图很重要。
    # 否则图像可能被拉伸，看起来连杆角度和实际不一致。
    plt.grid(True)
    # 显示网格，方便观察坐标位置。
    plt.legend()
    # 显示图例。
    # 图例内容来自前面 plot/scatter 里面的 label。
    plt.tight_layout()
    # 自动调整图像布局。
    # 可以防止标题、坐标轴标签、图例被挤出画布。
    plt.savefig(file_path, dpi=150)
    # 保存图片到 file_path。
    # dpi=150 表示图片分辨率。
    # dpi 越高图片越清晰，但文件也更大。
    plt.close()
    # 关闭当前图。
    # 这是一个好习惯。
    # 如果循环中画很多图，不 close 会占用内存，甚至导致图像混乱。
    return file_path
    # 返回保存好的图片路径。
    # 主程序可以打印这个路径，告诉用户图片保存在哪里。


def plot_error_curve(history, output_dir):
    """
    作用：绘制末端误差随迭代次数变化的曲线。
    输入：
        history: 仿真历史字典，至少包含 error。
        output_dir: 输出目录。
    输出：
        file_path: 保存图片的 Path。
    """
    # 定义一个函数，用来画误差曲线。
    # 这个图很重要，因为它能告诉你控制器是否让机械臂逐渐接近目标点。
    output_path = ensure_output_dir(output_dir)
    # 确保输出目录存在。
    file_path = output_path / "error_curve.png"
    # 设置误差曲线图片的保存路径。

    plt.figure(figsize=(7, 4))
    # 创建一张新图。
    # figsize=(7, 4) 表示图比较宽，适合显示曲线。
    plt.plot(history["error"], label="末端误差")
    # 绘制误差曲线。
    # history["error"] 是一个列表，里面记录了每次迭代后的末端误差。
    # x 轴默认就是列表下标：0, 1, 2, 3...
    # 所以这里不需要手动传入迭代次数。
    # label="末端误差" 是图例名称。
    plt.title("末端误差曲线")
    plt.xlabel("迭代次数")
    plt.ylabel("误差距离")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path


def plot_joint_curve(history, output_dir):
    """
    作用：绘制两个关节角随迭代次数变化的曲线。
    输入：
        history: 仿真历史字典，至少包含 theta1 和 theta2。
        output_dir: 输出目录。
    输出：
        file_path: 保存图片的 Path。
    """
    # 定义一个函数，用来画两个关节角的变化曲线。
    # 这个图能帮助你观察控制过程中关节角是否平稳变化。
    output_path = ensure_output_dir(output_dir)
    file_path = output_path / "joint_curve.png"

    plt.figure(figsize=(7, 4))
    # 创建一张新图。
    # 关节角曲线通常是随时间/迭代变化的折线图，所以用宽一点的图。
    plt.plot(history["theta1"], label="关节角 theta1")
    # 绘制第一个关节角 theta1 的变化曲线。
    # history["theta1"] 是一个列表，记录每次迭代后的 theta1。
    # x 轴默认是迭代次数。
    plt.plot(history["theta2"], label="关节角 theta2")
    # 绘制第二个关节角 theta2 的变化曲线。
    # 因为它和 theta1 画在同一张图上，所以可以比较两个关节的变化趋势。
    plt.title("关节角变化曲线")
    plt.xlabel("迭代次数")
    plt.ylabel("关节角 / 弧度")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path


def plot_workspace(link1, link2, save_path):
    """
    作用：绘制二连杆机械臂的可达工作空间。
    输入：
        link1: 第一根连杆长度。
        link2: 第二根连杆长度。
        save_path: 图片保存路径，例如 outputs/figures/workspace.png。
    输出：
        file_path: 保存图片的 Path。
    """
    configure_chinese_font()

    file_path = Path(save_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    max_reach = link1 + link2
    min_reach = abs(link1 - link2)
    margin = 0.2
    axis_limit = max_reach + margin

    fig, ax = plt.subplots(figsize=(6, 6))

    # 最远可达圆：两根连杆完全伸直时，末端能到达的最大半径。
    outer_circle = plt.Circle(
        (0.0, 0.0),
        max_reach,
        fill=False,
        color="tab:blue",
        linewidth=2,
        label=f"最远可达圆 r={max_reach:.2f}",
    )
    ax.add_patch(outer_circle)

    # 最近不可达内圆：当两根连杆长度不同，离基座太近的区域无法到达。
    if min_reach > 0:
        inner_circle = plt.Circle(
            (0.0, 0.0),
            min_reach,
            fill=False,
            color="tab:red",
            linestyle="--",
            linewidth=2,
            label=f"最近不可达内圆 r={min_reach:.2f}",
        )
        ax.add_patch(inner_circle)

    ax.scatter(0.0, 0.0, color="black", s=40, label="基座")
    ax.axhline(0.0, color="gray", linewidth=1)
    ax.axvline(0.0, color="gray", linewidth=1)
    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("二连杆机械臂可达工作空间")
    ax.set_xlabel("x 位置")
    ax.set_ylabel("y 位置")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()
    fig.savefig(file_path, dpi=150)
    plt.close(fig)

    return file_path


def plot_multiple_error_curves(error_histories, labels, save_path, title):
    """
    作用：在同一张图中绘制多条误差曲线，用来比较不同参数或不同控制方法。
    输入：
        error_histories: 列表，每个元素是一组误差历史数据。
        labels: 列表，每条曲线对应的图例名称。
        save_path: 图片保存路径。
        title: 图片标题。
    输出：
        file_path: 保存图片的 Path。
    """
    configure_chinese_font()

    file_path = Path(save_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(7, 4))
    for error_history, label in zip(error_histories, labels):
        plt.plot(error_history, label=label)

    plt.title(title)
    plt.xlabel("迭代次数")
    plt.ylabel("末端误差距离")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path


def plot_multiple_joint_curves(theta_histories, labels, save_path, title):
    """
    作用：在同一张图中比较不同控制方法下 theta1、theta2 的变化趋势。
    输入：
        theta_histories: 列表，每个元素是一组关节角历史；每一步包含 theta1 和 theta2。
        labels: 列表，每组关节角历史对应的图例名称。
        save_path: 图片保存路径。
        title: 图片标题。
    输出：
        file_path: 保存图片的 Path。
    """
    configure_chinese_font()

    file_path = Path(save_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    for theta_history, label in zip(theta_histories, labels):
        theta_array = list(theta_history)
        if len(theta_array) == 0:
            continue
        theta_array = np.array(theta_array, dtype=float)
        plt.plot(theta_array[:, 0], label=f"{label} theta1")
        plt.plot(theta_array[:, 1], linestyle="--", label=f"{label} theta2")

    plt.title(title)
    plt.xlabel("迭代次数")
    plt.ylabel("关节角 / 弧度")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path


def plot_error_comparison(error_histories, labels, save_path, title):
    """
    作用：绘制多组参数或多种控制方法的误差曲线对比图。
    输入：
        error_histories: 多组误差历史数据列表；每一组是一条误差曲线。
        labels: 每条曲线的标签，例如 "gain=0.2"。
        save_path: 图片保存路径。
        title: 图片标题。
    输出：
        file_path: 保存图片的 Path。
    """
    return plot_multiple_error_curves(error_histories, labels, save_path, title)


def plot_joint_angle_comparison(theta_histories, labels, save_path, title):
    """
    作用：绘制多组参数或多种控制方法的关节角曲线对比图。
    输入：
        theta_histories: 多组关节角历史数据列表；每一步包含 theta1 和 theta2。
        labels: 每组参数或控制方法的标签，例如 "max_step=0.08"。
        save_path: 图片保存路径。如果文件名包含 theta1，则只画 theta1；包含 theta2，则只画 theta2；否则同时画两个关节角。
        title: 图片标题。
    输出：
        file_path: 保存图片的 Path。
    """
    configure_chinese_font()

    file_path = Path(save_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    name = file_path.stem.lower()

    if "theta1" in name:
        joint_indices = [0]
        joint_names = ["theta1"]
    elif "theta2" in name:
        joint_indices = [1]
        joint_names = ["theta2"]
    else:
        joint_indices = [0, 1]
        joint_names = ["theta1", "theta2"]

    plt.figure(figsize=(8, 5))
    for theta_history, label in zip(theta_histories, labels):
        if len(theta_history) == 0:
            continue
        theta_array = np.array(theta_history, dtype=float)
        for joint_index, joint_name in zip(joint_indices, joint_names):
            curve_label = label if len(joint_indices) == 1 else f"{label} {joint_name}"
            linestyle = "-" if joint_index == 0 else "--"
            plt.plot(theta_array[:, joint_index], linestyle=linestyle, label=curve_label)

    plt.title(title)
    plt.xlabel("迭代次数")
    plt.ylabel("关节角 / 弧度")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(file_path, dpi=150)
    plt.close()

    return file_path


def save_all_plots(result, output_dir="outputs"):
    """
    作用：统一保存姿态图、误差曲线和关节角曲线。
    输入：
        result: run_reach_simulation 返回的结果字典。
        output_dir: 输出目录，默认为 outputs。
    输出：
        files: 字典，包含三张图片的保存路径。
    """
    # 定义一个总函数。
    # 它负责一次性生成所有需要的仿真结果图。
    configure_chinese_font()
    # 先配置中文字体。 
    # 这样后面所有图的中文标题、图例、坐标轴都尽量能正常显示。

    return {
        "arm_pose": plot_arm_pose(result["positions"], result["target"], output_dir),
        "error_curve": plot_error_curve(result["history"], output_dir),
        "joint_curve": plot_joint_curve(result["history"], output_dir),
    }
    # 返回一个字典，里面存放三张图的路径。
    #
    # "arm_pose":
    #   调用 plot_arm_pose()，画机械臂最终姿态图。
    #   需要 result["positions"] 和 result["target"]。
    #
    # "error_curve":
    #   调用 plot_error_curve()，画误差曲线。
    #   需要 result["history"]。
    #
    # "joint_curve":
    #   调用 plot_joint_curve()，画关节角变化曲线。
    #   也需要 result["history"]。
