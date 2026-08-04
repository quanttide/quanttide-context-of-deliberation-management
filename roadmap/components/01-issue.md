# 01-issue 议题组件

> 分期：MVP | 依赖：00-foundation

## 职责

议题的全生命周期管理：按类型模板创建、三区编辑（动议/附议/决议）、状态流转。

## 功能点

- **类型化创建**：按六种类型（决策、计划、复盘研讨、提案审计、澄清评估、谈判报告）选择模板创建；议事规则、议程、决议为独立实体
- **三区编辑**：动议区（类型驱动字段）、附议区（可选：表态/补充/支持）、决议区（记录本议题最终决定，可选；决议实体同时进入决议档案）
- **状态流转**：草稿 → 动议 → 附议 → 决议 → 已归档，环节必经/可选/跳过由类型 stage_requirements 配置驱动
- **Markdown 预览**：双栏编辑（内容/结论）

## 资料依据

- contract.yaml：九种类型与 expected_fields、validation（required：议题、动议区；optional：附议区、决议区）
- 现有代码：`issue.dart`（IssueContent 内容/结论双栏）

## 代码映射

- `issue.dart` 的 `IssueContent` 演进为动议区/决议区双栏编辑器
- 新增 `lib/screens/issue_edit.dart`（类型化创建与三区编辑）
- 新增 `lib/widgets/motion_section.dart`、`second_section.dart`、`resolution_section.dart`
