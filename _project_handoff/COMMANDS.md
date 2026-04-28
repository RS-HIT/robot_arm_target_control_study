# 已验证命令记录

## 环境准备

```bash
pip install -r requirements.txt
```

作用：安装项目依赖，包括 `numpy`、`matplotlib` 和 `pytest`。

## 运行 demo

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
```

作用：运行 2D 二连杆机械臂目标点控制 demo，目标点为 `(1.2, 0.6)`。程序会执行仿真、保存图片并在终端打印最终结果。

## 运行第二阶段对比实验

```bash
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
```

作用：对比解析逆运动学和雅可比伪逆迭代控制，输出两种方法的最终误差和工作空间图片。

## 运行第三阶段参数实验

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
```

作用：扫描多组 `gain` 和 `max_step`，保存 `outputs/logs/parameter_sweep.csv`，并生成参数对比曲线。

```bash
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
```

作用：对比普通雅可比伪逆和阻尼雅可比控制，观察接近边界目标时的误差和关节角变化。

```bash
python scripts/run_singularity_demo.py
```

作用：运行接近伸直边界的奇异位形实验，生成普通伪逆和阻尼雅可比的对比曲线。

## 运行测试

```bash
pytest
```

作用：运行当前项目测试集，验证正运动学、可达目标收敛和不可达目标不会崩溃。

## 画图输出

当前没有单独的画图脚本。画图由 demo 自动触发：

```bash
python scripts/run_reach_demo.py --target_x 1.2 --target_y 0.6
```

作用：运行后会自动生成：

- `outputs/arm_pose.png`
- `outputs/error_curve.png`
- `outputs/joint_curve.png`

第二阶段工作空间图由对比脚本自动触发：

```bash
python scripts/run_compare_methods.py --target_x 1.2 --target_y 0.6
```

作用：生成 `outputs/figures/workspace.png`。

第三阶段图表由参数实验和阻尼实验自动触发：

```bash
python scripts/run_parameter_sweep.py --target_x 1.2 --target_y 0.6
python scripts/run_damped_jacobian_demo.py --target_x 1.75 --target_y 0.05
python scripts/run_singularity_demo.py
```

作用：生成 `outputs/logs/parameter_sweep.csv` 和 `outputs/figures/` 下的多组对比曲线。

## Git 状态检查

```bash
git status -sb
```

作用：查看当前分支、远端跟踪关系，以及是否有未提交文件。

```bash
git remote -v
```

作用：查看当前本地仓库连接的远端 GitHub 地址。

## 首次推送相关命令

```bash
git init
```

作用：把当前文件夹初始化为 Git 仓库。当前项目已经是 Git 仓库，通常不需要再次执行。

```bash
git add .
```

作用：把当前目录下准备提交的新文件和修改加入暂存区。

```bash
git commit -m "Initial robot arm target control demo"
```

作用：把暂存区内容保存成一次 Git 提交记录。

```bash
git remote add origin <你的 GitHub 仓库地址>
```

作用：把本地仓库和 GitHub 远端仓库建立连接。当前项目已经配置了 `origin`，如需更换远端地址，应先确认再修改。

```bash
git push -u origin main
```

作用：把本地 `main` 分支推送到远端 `origin`，并建立本地 `main` 和远端 `origin/main` 的跟踪关系。只有在用户明确允许后才执行。
