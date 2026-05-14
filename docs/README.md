# 文档导航

这个页面用于快速了解 `docs/` 目录应该按什么顺序阅读。建议先看项目目标和代码数据流，再看各阶段学习文档，最后看实验报告、总结和交接材料。

## 推荐阅读顺序

1. 项目目标与总体说明：先看根目录 `README.md`，了解项目能运行什么、输出什么。
2. 代码阅读笔记：理解命令行输入、控制器、运动学、绘图和输出文件之间的数据流。
3. 阶段学习文档：按阶段理解解析逆运动学、参数实验、轨迹跟踪和轨迹规划。
4. 参数实验报告：学习如何从误差曲线和关节角曲线解释实验现象。
5. 轨迹规划与轨迹跟踪文档：理解 resolved-rate 控制、关节空间轨迹、笛卡尔空间轨迹和约束检查。
6. 实验结论与展示材料：把项目整理成 README、GitHub 和简历可以使用的表达。
7. 交接文档：需要让新的 Codex/ChatGPT 接手时再看。

## 核心文档说明

| 文档路径 | 内容主题 | 适合什么时候看 |
| --- | --- | --- |
| `../README.md` | 项目总览、运行命令、输出结果和项目边界 | 第一次打开仓库时 |
| `docs/01_code_reading_notes.md` | 代码阅读笔记 | 想理解项目文件分工时 |
| `docs/02_code_reading_notes.md` | 项目数据流 | 想理解脚本如何调用核心模块时 |
| `docs/02_interview_questions.md` | 面试问题整理 | 准备用口头方式解释项目时 |
| `docs/05_stage2_learning_guide.md` | 解析逆运动学与雅可比伪逆对比 | 学完正运动学后 |
| `docs/06_stage3_experiment_guide.md` | 参数敏感性、奇异位形与阻尼雅可比 | 开始做参数实验时 |
| `docs/07_experiment_report_template.md` | 参数实验记录模板 | 写实验报告前 |
| `docs/08_parameter_experiment_report.md` | gain、max_step、damping 实验报告 | 想看完整参数实验结论时 |
| `docs/09_stage4_trajectory_tracking_guide.md` | 轨迹跟踪与 PD 控制思想 | 从目标点控制过渡到轨迹跟踪时 |
| `docs/10_pd_control_notes.md` | PD 控制学习笔记 | 想单独理解 P、P+前馈、PD 差异时 |
| `docs/11_stage5_trajectory_planning_guide.md` | 轨迹规划、时间缩放与轨迹空间对比 | 学习关节空间和笛卡尔空间轨迹时 |
| `docs/12_trajectory_planning_notes.md` | 轨迹规划学习笔记 | 复习轨迹生成概念时 |
| `docs/13_stage6_constraint_aware_trajectory_guide.md` | 约束感知轨迹与轨迹重定时 | 分析速度、加速度和 total_time 时 |
| `docs/14_joint_vs_cartesian_summary.md` | 关节空间轨迹与笛卡尔空间轨迹总结 | 对比两种轨迹方式时 |
| `docs/15_experiment_summary.md` | 实验结论汇总 | 写 README、报告或复盘项目时 |
| `docs/16_resume_description.md` | 简历项目描述 | 准备简历和面试自述时 |
| `docs/progress_report_for_chatgpt.md` | 阶段性进展汇报 | 需要回顾历史阶段时 |
| `docs/chatgpt_web_handoff.md` | 网页端 ChatGPT 交接文档 | 需要换工具或新会话接手时 |
