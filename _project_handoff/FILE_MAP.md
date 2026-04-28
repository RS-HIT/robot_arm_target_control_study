# 项目文件地图

## 根目录文件

- `README.md`：GitHub 首页说明，介绍项目目标、运行方式、测试方式、算法解释和后续计划。
- `requirements.txt`：Python 依赖列表，目前包含 `numpy`、`matplotlib`、`pytest`。
- `.gitignore`：Git 忽略规则，忽略缓存、虚拟环境、运行输出、日志、视频和临时文件。

## 源代码目录

- `src/robot_arm_target_control_study/__init__.py`：Python 包初始化文件。
- `src/robot_arm_target_control_study/kinematics.py`：正运动学、雅可比矩阵、目标点可达性判断和二连杆解析逆运动学。
- `src/robot_arm_target_control_study/controller.py`：普通雅可比伪逆控制、阻尼雅可比控制，以及单步关节角限幅。
- `src/robot_arm_target_control_study/simulation.py`：目标点控制仿真循环和通用迭代仿真函数，负责迭代、记录历史和返回结果。
- `src/robot_arm_target_control_study/plotting.py`：绘图和保存图片，包括最终姿态图、误差曲线、关节角变化曲线、工作空间图和多组对比曲线。

## 脚本目录

- `scripts/run_reach_demo.py`：命令行 demo 入口，读取目标点参数，运行仿真，保存图片，打印结果。
- `scripts/run_compare_methods.py`：第二阶段对比入口，比较解析逆运动学和雅可比伪逆迭代控制。
- `scripts/run_parameter_sweep.py`：第三阶段参数扫描入口，比较不同 `gain` 和 `max_step`。
- `scripts/run_damped_jacobian_demo.py`：第三阶段阻尼雅可比对比入口，比较普通伪逆和阻尼雅可比。
- `scripts/run_singularity_demo.py`：第三阶段奇异位形实验入口，观察接近伸直边界时的控制表现。

## 测试目录

- `tests/conftest.py`：pytest 配置，让测试可以导入 `src/` 下的项目代码。
- `tests/test_kinematics.py`：测试正运动学结果、雅可比矩阵形状、目标点可达性和解析逆运动学。
- `tests/test_controller.py`：测试可达目标是否收敛、不可达目标是否不会崩溃、阻尼雅可比控制和通用仿真历史。

## 文档目录

- `docs/01_code_reading_notes.md`：代码阅读顺序和模块解释。
- `docs/02_code_reading_notes.md`：项目数据流说明。
- `docs/02_interview_questions.md`：面试问题和回答参考。
- `docs/05_stage2_learning_guide.md`：第二阶段学习指示，解释解析逆运动学与雅可比伪逆对比。
- `docs/06_stage3_experiment_guide.md`：第三阶段学习指示，解释参数敏感性、奇异位形和阻尼雅可比。
- `docs/07_experiment_report_template.md`：参数实验报告模板。
- `docs/progress_report_for_chatgpt.md`：已有进度说明，内容是否继续维护待确认。
- `docs/assets/`：README 展示用图片。

## 输出目录

- `outputs/.gitkeep`：保留空输出目录。
- `outputs/`：demo 运行时输出目录，会生成姿态图和曲线图。图片默认不提交到 Git。
- `outputs/figures/`：工作空间图和第三阶段对比曲线输出目录，保留 `.gitkeep`，生成图片不提交。
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
