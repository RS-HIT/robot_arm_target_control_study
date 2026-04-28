# 项目进展日志

## 2026-04-28

- 整理 GitHub 首页 README，补充项目简介、功能特点、项目结构、安装、运行、测试、输出说明、核心算法、当前阶段边界和后续计划。
- 将 README 展示图片复制到 `docs/assets/`，保留 `outputs/` 作为本地运行输出目录。
- 完善 `.gitignore`，忽略 Python 缓存、pytest 缓存、虚拟环境、IDE 个人配置、日志、视频和临时文件。
- 新增 `docs/02_code_reading_notes.md`，记录项目数据流。
- 验证 demo 命令可运行，目标点 `(1.2, 0.6)` 最终误差为 `0.002829`。
- 验证测试通过，`pytest` 结果为 `5 passed`。
- 新增 `_project_handoff/` 交接目录，用于后续网页端 ChatGPT 或人类读者快速接手项目。

## 2026-04-28

- 第二阶段新增解析逆运动学与雅可比伪逆迭代控制对比实验。
- 新增 `scripts/run_compare_methods.py`，用于打印两种方法的结果差异。
- 在 `kinematics.py` 中新增目标点可达性判断和二连杆解析逆运动学函数。
- 在 `plotting.py` 中新增工作空间图绘制函数。
- 新增 `docs/05_stage2_learning_guide.md`，解释第二阶段学习目标和阅读顺序。
- 扩展 `tests/test_kinematics.py`，覆盖可达性判断、解析逆运动学和 elbow up/down 两种构型。

## 2026-04-28

- 第三阶段新增参数敏感性、奇异位形和阻尼雅可比实验工作流。
- 新增 `scripts/run_parameter_sweep.py`，扫描 `gain` 和 `max_step` 并输出 CSV 与对比曲线。
- 新增 `scripts/run_damped_jacobian_demo.py`，对比普通伪逆和阻尼雅可比控制。
- 新增 `scripts/run_singularity_demo.py`，观察接近伸直边界时的控制表现。
- 在 `controller.py` 中新增阻尼雅可比控制步骤。
- 在 `simulation.py` 中新增通用迭代仿真函数。
- 在 `plotting.py` 中新增多组误差曲线和关节角曲线对比函数。
- 新增 `docs/06_stage3_experiment_guide.md` 和 `docs/07_experiment_report_template.md`。
