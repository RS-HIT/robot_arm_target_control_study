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
