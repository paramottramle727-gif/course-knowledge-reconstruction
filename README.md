# Course Knowledge Reconstruction

面向长期课程学习的 Codex Skill。它根据课件、教材与练习重建逐章知识点笔记，用于首次学习、复习和实际解题。

## 使用

将本仓库下载到本机，把含有 `SKILL.md`、`references/`、`assets/`、`agents/` 和 `scripts/` 的完整目录安装为 Codex 的个人 Skill。在课程聊天中显式调用 `$course-knowledge-reconstruction`，填写仓库中的启动提示词，指定课程材料、Vault 内的知识点目录和 Vault 外的课程工作目录。

1. **O** 确认来源怎样使用。
2. **A** 确认模块划分、材料映射和顺序。
3. **B** 阅读首模块样稿，确认内容组织与表达方法。
4. **逐章生成** 每章保存候选稿，重新读取材料与共识，审阅后发布到 Obsidian。

O、A、B 可独立重启。已确认的更新按生效范围用于后续任务。状态、样稿和审阅记录保存在课程工作目录。

核心说明见 [SKILL.md](SKILL.md)，审阅方法见 [单模块审阅](references/shared/module-review.md)。
