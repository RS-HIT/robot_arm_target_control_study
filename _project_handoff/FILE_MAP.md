# 项目文件地图

## 根目录文件

- `README.md`：GitHub 首页说明，介绍项目目标、运行方式、测试方式、算法解释和后续计划。
- `requirements.txt`：Python 依赖列表，目前包含 `numpy`、`matplotlib`、`pytest`。
- `.gitignore`：Git 忽略规则，忽略缓存、虚拟环境、运行输出、日志、视频和临时文件。

## 源代码目录

- `src/robot_arm_target_control_study/__init__.py`：Python 包初始化文件。
- `src/robot_arm_target_control_study/kinematics.py`：正运动学和雅可比矩阵计算。
- `src/robot_arm_target_control_study/controller.py`：基于雅可比伪逆的控制步计算，以及单步关节角限幅。
- `src/robot_arm_target_control_study/simulation.py`：目标点控制仿真循环，负责迭代、记录历史和返回结果。
- `src/robot_arm_target_control_study/plotting.py`：绘图和保存图片，包括最终姿态图、误差曲线和关节角变化曲线。

## 脚本目录

- `scripts/run_reach_demo.py`：命令行 demo 入口，读取目标点参数，运行仿真，保存图片，打印结果。

## 测试目录

- `tests/conftest.py`：pytest 配置，让测试可以导入 `src/` 下的项目代码。
- `tests/test_kinematics.py`：测试正运动学结果和雅可比矩阵形状。
- `tests/test_controller.py`：测试可达目标是否收敛，以及不可达目标是否不会崩溃。

## 文档目录

- `docs/01_code_reading_notes.md`：代码阅读顺序和模块解释。
- `docs/02_code_reading_notes.md`：项目数据流说明。
- `docs/02_interview_questions.md`：面试问题和回答参考。
- `docs/progress_report_for_chatgpt.md`：已有进度说明，内容是否继续维护待确认。
- `docs/assets/`：README 展示用图片。

## 输出目录

- `outputs/.gitkeep`：保留空输出目录。
- `outputs/`：demo 运行时输出目录，会生成姿态图和曲线图。图片默认不提交到 Git。
- `outputs/figures/`：当前为空，后续是否使用待确认。
- `outputs/logs/`：日志输出预留目录，已被 `.gitignore` 忽略。
- `outputs/videos/`：视频或动画输出预留目录，已被 `.gitignore` 忽略。

## 配置目录

- `configs/`：当前为空。是否引入配置文件管理默认参数待确认。

## 交接目录

- `_project_handoff/README.md`：交接总说明。
- `_project_handoff/CURRENT_STATUS.md`：当前状态。
- `_project_handoff/NEXT_STEPS.md`：下一步任务。
- `_project_handoff/DECISIONS.md`：技术决策记录。
- `_project_handoff/COMMANDS.md`：已验证命令记录。
- `_project_handoff/FILE_MAP.md`：关键文件结构说明。
- `_project_handoff/ISSUES.md`：未解决问题记录。
- `_project_handoff/LOG.md`：追加式进展日志。
