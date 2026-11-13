# A：课程材料与模块方案

> 唯一材料清单与架构记录。O 前可只填写清单，未通过 O 不提交最终 A。来源策略只引用 O，具体知识点取舍留到逐章分析。

## 状态与路径

- course_name:
- course_root:
- source_roots:
- excluded_paths:
- obsidian_vault_root:
- obsidian_output_root:
- agent_workspace_root:
- storage_boundary_confirmed: false
- workflow_status: inventory-only
- integration_mode: new-course | existing-course-stage
- a_schema: architecture-v2
- active_a_version: none
- active_a_status: none
- active_a_effective_from:
- pending_a_version:
- pending_a_status:
- forward_only: true
- architecture_based_on_o_version:
- architecture_approved_at:
- architecture_confirmation_basis:
- capability_record: <agent_workspace_root>/course-capability.md
- updated_at:

## 已有课程流程与保护边界

- existing_learning_stage:
- protected_course_plan_paths:
- protected_existing_outputs:
- inherited_constraints:
- authorized_write_scope:

## 材料清单与读取边界

| 来源ID | 路径与版本 | 可读状态 | 允许/排除范围 | 备注 |
|---|---|---|---|---|

> 使用方向和用途内重要程度读取 capability_record，不在此另记活动 O。architecture_based_on_o_version 是架构批准时的历史基础。

## 架构依据

- 全课核心问题与主要知识类型：
- 划分及学习顺序依据：
- 相对教师/教材结构的保留与调整理由：

## 模块地图

| ID | 模块/核心问题 | 对应材料范围 | 前置与接口 | 划分与排序依据 | 主导适配器 | 状态 |
|---|---|---|---|---|---|---|

> 材料可跨文件/章节映射；依据简明但完整，复杂理由在下方对应短段说明。此表不记录每个概念的详略、图形角色或局部标题。不为表格列数强拆学习单元。

## 正式知识点文件分工

| 文件/模块 | 主功能 | 与其他模块的边界 |
|---|---|---|

## 首次 B 的模块安排

- candidate_module: A 顺序中的第一个模块
- intended_validation_scope:
- unrepresented_content_types:
- user_override_if_any:

> 首模块未覆盖的知识类型留待后续学习检验，不要求用户提前阅读后续完整章节。旧项目沿用已确认参考文件。

## 待决事项

- 材料事实与设计推断的关键不确定处：
- 需要用户裁决的架构冲突：

## 待确认架构调整

- trigger_from_user:
- candidate_based_on_a_version:
- candidate_based_on_o_version:
- proposed_effective_from:

| 新依据 | 原模块/安排 | 候选模块/安排及理由 | 旧新对应与影响范围 |
|---|---|---|---|

> 首次 A 的正文是草案，pending_a_version 为 A-v1；后续修改仅放本区，不覆盖活动架构。复杂候选可在本区展开完整映射。确认后合并正文并清理已处理候选，不维护第二份活动地图。

## 当前批次与恢复点

- operation: produce-modules | audit-and-update
- authorized_units:
- execution_order:
- active_unit_and_step:
- pending_release_record:  # 仅发布中填写，链接本次内部版本、目标、备份及写前/拟写指纹记录
- active_unit_o_version:
- active_unit_a_version:
- active_unit_b_version:
- last_completed_unit:
- pending_issues:

| 模块 ID | 内部定版路径 | 展示路径 | 正文与附件指纹或清单链接 | 使用的 O/A/B | 验证记录与完成状态 |
|---|---|---|---|---|---|

> 完成表示已审核、落地并复核最终位置；无需修订的单元标“已核查、保留原稿”。未完成草稿不计完成。历史版本不因 O/A/B 更新反写。

## 简要架构历史

| A版本 | 确认依据与时间 | 所据 O | 主要变化及旧新模块对应 | 生效起点 |
|---|---|---|---|---|

> 只保存一个活动架构与简要历史；旧架构备份仅作恢复，不参与当前执行。首次确认时间与依据使用 architecture_approved_at / architecture_confirmation_basis，不重复维护另一组字段。
