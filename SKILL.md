---
name: course-knowledge-reconstruction
description: Rebuild the knowledge-note stage of a sustained course project through source-use agreement, module architecture, first-module writing calibration, and chapter-by-chapter QA. Use only when explicitly invoked; preserve existing learning plans and outputs outside the authorized note scope.
metadata:
  revision: "2026-11-13.4"
---

# Course Knowledge Reconstruction

将课程材料重构为可独立理解、快速定位和实际使用的知识体系。只负责知识点梳理，不接管整门课程的学习规划。

## 范围与启动

- 仅处理用户指定课程及允许来源；排除或废弃稿不得读取、引用或进入基准。既有规划、学习进度、作业、术语表、错题、复习提纲和题型材料均属外部阶段，未经另行授权不创建、重排或修改。
- 本 Skill 用于持续课程项目，不用于孤立问答、临时翻译或一次性短摘要。保持显式调用策略。
- 确定课程根目录、允许/排除来源、正式目录 `obsidian_output_root` 和代理目录 `agent_workspace_root`；可可靠取得的信息不重复询问。登记 Vault 根，工作区位于库外，正式展示目录位于库内，按 [存放规则](references/shared/storage-policy.md) 执行。
- 从登记的工作区固定路径读取三个课程状态文件；已有课程先读 [嵌入规则](references/shared/existing-course-integration.md)。旧状态兼容读取，升级不自动迁移文件或重开确认点。
- 将请求路由为一个或多个阶段，连续执行到最近的必要确认点；只加载当前阶段及所需共享规则、一个主导适配器。

## O、A、B 的职责与确认

| 阶段 | 决定什么 | 主要记录 |
|---|---|---|
| O | 来源参与方式、用途、使用范围与程度、用途内优先级；学习目的与明确课程情境 | `course-capability.md` |
| A | 材料怎样对应模块、如何划分排序及衔接、正式文件分工；首次 B 使用第一模块 | `course-context.md` |
| B | 继承基础共识为课程 B-v0，以首模块样稿校准；后续结合章节阅读解释并迭代方法 | `execution-baseline.md`，引用内部审阅材料 |

初次建立按 `O → A → B → 逐模块生成` 执行，O/A/B 均须用户明确确认，不能合并或用代理自检代替。O/A 不预先编制全课逐知识点纳入、详略、推导或配图清单；本章学习要求和具体取舍在深入读取本章材料后决定。

O、A、B 均采用“阶段文件另存＋聊天简报”的双路交付。进入这些阶段时读取 [双路交互规则](references/shared/checkpoint-interaction.md)，按讨论中、等待确认、已确认组织本轮交互；文件内容与聊天框架分别由对应阶段定义，同一方案只确认一次。

用户可随时主动更新 O、A 或 B。新材料、单条反馈、代理新写法不自动改写活动共识。更新讨论确认后记录版本、适用范围与生效起点，默认向前生效；不自动审查旧章、修改代表文件或重启其他确认点。明确的后续执行指令可构成相应条目的确认，不重复索要同一批准。重启阶段默认独立结束，不自动衔接下一阶段；明确授权联动时按依赖顺序继续。具体流程由各阶段定义。

## 路由与规则归属

- 新课程初始化、O 后的 A 设计及用户主动重启 A：[01-setup-course.md](references/stages/01-setup-course.md)。初始/增量 O 的确认与兼容逻辑只在 [capability-confirmation.md](references/shared/capability-confirmation.md) 定义。
- 首次 B、用户主动更新编写方法：[02-calibrate-course.md](references/stages/02-calibrate-course.md)。后续 B 不默认重做完整样稿。
- 已通过 O/A/B 的生成：[03-produce-modules.md](references/stages/03-produce-modules.md)。
- 既有笔记审查、授权修订、材料登记及反馈分流：[04-audit-and-update.md](references/stages/04-audit-and-update.md)。旧章修订与 O/A/B 更新是不同授权。
- 来源用途、证据与冲突：[evidence-policy.md](references/shared/evidence-policy.md)。
- 基础内容组织共识、逐章取舍、同类框架、图形角色与内容回归：[content-decision-rules.md](references/shared/content-decision-rules.md)。
- 基础表达呈现共识、标题/短标签、正文语言、图文布局及验收：[presentation-rules.md](references/shared/presentation-rules.md)。
- 按模块主体选 [定量与模型](references/adapters/quantitative-model.md)、[历史与思想理论](references/adapters/historical-theory.md)、[编程与算法](references/adapters/programming-algorithm.md)，或 general（不加载适配器）。交叉内容仅补对象级规则，不并行套用宏观模板。

首次 B 实际读取两份基础规则，将完整编写共识保存为课程 B-v0，再依有效 O、A、课程 B 及本章材料编写。课程基准维护完整有效共识，通用 Skill 升级不静默覆盖它；工具和检查流程仍由 Skill 负责。课程方法分内容组织、表达呈现，按整课/知识类型/单章限制范围；具体课程案例不硬编码进通用 Skill。

## 逐模块执行不变量

1. 开始本单元时读取最新已确认且已生效的 O → A → B，再深读本章材料；B 阅读包含其实际参考样稿。实际读取课程完整共识，不能只读版本或指针；当前明确指令和有效课程方法优先于样稿的历史写法；不复制样稿目录、详略或图数。新要求不追溯伪造旧样稿已验证内容。
2. 本章真实课件与训练决定学习任务；区分材料事实、用户课程情境与推断。执行轻量覆盖核对、逻辑归属及理解/调用回归，不能以字数或压缩比判断质量。
3. 同类知识可用稳定框架，但没有学习需要的栏目不补齐。图形是否主导按知识单元的实际调用与理解需要判断，不以“文字不足”作为唯一门槛。
4. 每章候选稿保存后实际读取[单模块审阅提示](references/shared/module-review.md)，重新读取本章适用 O/A/B、校准样稿和映射材料，再审阅实际稿件。修正、复核并发布后继续下一章。
5. 记录每个模块使用的 O/A/B 版本与实际检验结果；活动单元不混用待确认草案。中途更新从明确生效任务应用，恢复时核对已有版本与未完成步骤。
6. 保留用户当前修改，按授权和备份规则发布。遇影响范围、架构、正确性的实质冲突或关键证据缺失，暂停受影响部分并说明。

## 文件与交付

- 正式知识点及必要附件进入 `obsidian_output_root`；状态、样稿、说明、审查与备份进入 `agent_workspace_root`，库外课程根可采用 `<课程根>/角色/course-knowledge-reconstruction/`，内部定版与 B 校准样稿按存放规则维护。
- 三份状态各有唯一职责，使用 [O 模板](assets/course-capability.template.md)、[A 模板](assets/course-context.template.md)、[B 模板](assets/execution-baseline.template.md)。保留一个活动版本、候选差异和简要历史，不维护重复能力模型、风格锚点或例外表。
- [覆盖核对表](assets/coverage-checklist.template.md) 默认临时使用；仅需审计轨迹时保存，不进入学习正文。
- 交付前运行 `python scripts/markdown_qa.py <文件或目录>`，只检查格式及常见本地图片引用；不能证明内容、图文语义或学习效果。脚本回归为 `python scripts/test_markdown_qa.py`。
- O/A/B 按双路交互规则汇报方案、依据与待决事项，常规检查留在内部记录。生成/审修交付简报文件路径、完成范围、关键缺口及实际验证结果和未验证项。影响判断的异常始终告知；不把内部检查写成用户已确认或真实学生已学会。
