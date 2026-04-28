# 项目进展日志

## 2026-04-28

- 整理 GitHub 首页 README，补充项目简介、功能特点、项目结构、安装、运行、测试、输出说明、核心算法、当前阶段边界和后续计划。
- 将 README 展示图片复制到 `docs/assets/`，保留 `outputs/` 作为本地运行输出目录。
- 完善 `.gitignore`，忽略 Python 缓存、pytest 缓存、虚拟环境、IDE 个人配置、日志、视频和临时文件。
- 新增 `docs/02_code_reading_notes.md`，记录项目数据流。
- 验证 demo 命令可运行，目标点 `(1.2, 0.6)` 最终误差为 `0.002829`。
- 验证测试通过，`pytest` 结果为 `5 passed`。
- 新增 `_project_handoff/` 交接目录，用于后续网页端 ChatGPT 或人类读者快速接手项目。
