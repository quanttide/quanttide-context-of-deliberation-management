# qtcloud-delib 核心功能规划

> 基于议事档案标本契约 v0.0.7、议事管理工作手册、议事云产品理念及典型案例整理。产品意图见 [intention/qtcloud-delib.md](../intention/qtcloud-delib.md)。

## 一、产品定位

以**决议为中心**、以议题为过程的议事管理 SaaS——先做决议治理（决议档案、治理视图、执行跟踪），再做议事闭环（七节点完整流程）。研讨/提案两类模式、辩论与投票环节、"模型从资产中长出"（结构由模式模板驱动）。

## 二、领域模型

| 实体 | 要点 | 来源 |
|---|---|---|
| 议事规则 Rule | 常驻规则配置（版本化、修订记录、生效状态），非议题类型 | contract.yaml |
| 议程 Agenda | 会议骨架（时间、参与者、议程项[关联议题]），非议题类型 | contract.yaml |
| 议题 Issue | 两类模式：研讨（开放深度讨论）、提案（封闭决策）；共享同一生命周期 | contract.yaml |
| 动议区 Motion | 模式驱动的核心字段（研讨→主题/框架；提案→内容/选项/准则） | contract.yaml |
| 附议区 Second | 研讨为参与确认；提案为封闭表态（附议/反对/弃权） | contract.yaml |
| 辩论区 Debate | 研讨必经（开放深度讨论）；提案冲突时启用（观点交锋） | contract.yaml |
| 投票区 Vote | 提案必经（支持/反对/弃权）；研讨不适用 | contract.yaml |
| 决议 Resolution | 独立实体：决议内容+投票结果+责任人+完成期限+执行状态；统一治理（跟踪/审计/统计） | contract.yaml |
| 会议 Meeting | 时间、参与者、议程项（议程实体） | contract.yaml / handbook |
| 档案 Archive | 年份+周次组织；首页含议事活动和编号规则 | contract.yaml |
| 用户/角色 | 议长（主持人）、书记（记录人）、成员；治理层：创始人/上议院/下议院 | bylaw（org 领域） |

## 三、组件架构

按职责将系统分解为 11 个组件，定义见 [components/](./components/)：

| # | 组件 | 职责 | 分期 |
|---|---|---|---|
| 00 | [foundation](./components/00-foundation.md) | 基建：类型模板引擎、生命周期状态机、Markdown 编辑、持久化 | MVP |
| 04 | [resolution](./components/04-resolution.md) | 决议独立档案、治理视图、执行跟踪、逾期预警、治理审计 | MVP |
| 05 | [archive](./components/05-archive.md) | 年份+周次归档、检索回溯、标本反推验证 | MVP |
| 01 | [issue](./components/01-issue.md) | 议题创建/编辑（动议/附议/辩论/投票/决议区）、模式模板、状态流转 | V1 |
| 02 | [meeting](./components/02-meeting.md) | 会议、议程编排（拖拽排序）、议程项关联议题 | V1 |
| 03 | [vote](./components/03-vote.md) | 电子表决：记名/不记名、支持/反对/弃权、结果统计 | V1 |
| 06 | [role](./components/06-role.md) | 用户/角色/权限：议长、书记、成员、创始人/两院、三模流程 | V1 |
| 07 | [weekly](./components/07-weekly.md) | 周会三件套（进展+决议+审计）、周报引用规则 | V1 |
| 08 | [audit](./components/08-audit.md) | 会前/会中/会后三段式审计、客观评分 | V2 |
| 09 | [classroom](./components/09-classroom.md) | 课堂项目、轮值议长/秘书、过程性评价 | V2 |
| 10 | [ai-advisor](./components/10-ai-advisor.md) | AI 议事助手：议长/思考者/行动者三角色、模拟辩论 | V2 |

## 四、组件依赖关系

```
foundation(00)
  ├── resolution(04) ──> archive(05)     # 决议子系统（MVP，独立闭环）
  ├── issue(01) ──> meeting(02) ──> vote(03) ──> resolution(04)   # 议事子系统（V1）
  ├── issue(01) ──> archive(05)
  └── role(06) ──> meeting(02) / vote(03) / weekly(07)
audit(08) ──> meeting(02) / resolution(04)
classroom(09) ──> issue(01) / meeting(02) / vote(03)
ai-advisor(10) ──> issue(01) / foundation(00)
```

决议子系统（00 → 04 → 05）不依赖议题/会议/表决，可独立先行；议事子系统产出决议后汇入决议档案。

## 五、实施分期

| 分期 | 组件 | 与现状差距 |
|---|---|---|
| MVP（决议子系统） | 00 foundation、04 resolution、05 archive | 小——决议档案 + 治理视图 + 执行跟踪，决议可直接创建/导入（飞书导出），不依赖议事流程 |
| V1（议事子系统） | 01 issue、02 meeting、03 vote、06 role、07 weekly | 中——七节点流程、会议议程、表决与权限体系；决议从议题决议形成节点自动汇入档案 |
| V2（AI 与组织学习） | 08 audit、09 classroom、10 ai-advisor | 大——AI 三角色模拟为核心差异化功能 |

## 六、与现有代码的映射

- `issue.dart` 的 `IssueContent`（内容/结论两栏）→ 01 issue 的动议区/决议区双栏编辑器
- `mettings.dart` 的 `ReorderableListView` → 02 meeting 的议程编排核心组件（50 条占位数据 → 真实议题数据源）
- 需新增：00 foundation（类型模板模型、生命周期状态机、归档服务、数据持久化）
