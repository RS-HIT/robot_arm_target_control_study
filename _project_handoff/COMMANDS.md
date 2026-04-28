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
