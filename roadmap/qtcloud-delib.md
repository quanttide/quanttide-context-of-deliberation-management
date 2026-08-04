# qtcloud-delib 核心功能规划

> 基于议事档案标本契约 v0.0.2、议事机构章程、议事管理工作手册、议事云产品理念及典型案例整理。

## 一、产品定位

以"议题"为核心的议事管理 SaaS——覆盖"议题创建 → 动议提出 → 附议扩散（可选）→ 决议形成（可选）→ 归档沉淀"五节点完整闭环，按年份+周次组织档案。无辩论区、附议/决议为柔性节点、"模型从资产中长出"（结构由类型模板驱动）。

## 二、领域模型

| 实体 | 要点 | 来源 |
|---|---|---|
| 议题 Issue | 九种类型：议事规则、议程、决策、计划、复盘研讨、提案审计、澄清评估、谈判报告、决议；共享同一生命周期 | contract.yaml |
| 动议区 Motion | 类型驱动的核心字段（决策→选项列表+准则+权衡；计划→目标+里程碑+责任人+时间线；…） | contract.yaml |
| 附议区 Second | 可选；表态、补充、支持 | contract.yaml |
| 决议区 Resolution | 可选；决议内容+投票结果；决策类含"决定"字段 | contract.yaml |
| 会议 Meeting | 时间、参与者、议程项（议程类型议题） | contract.yaml / handbook |
| 档案 Archive | 年份+周次组织；首页含议事活动和编号规则 | contract.yaml |
| 用户/角色 | 议长（主持人）、书记（记录人）、成员；治理层：创始人/上议院/下议院 | bylaw |

## 三、组件架构

按职责将系统分解为 11 个组件，定义见 [components/](./components/)：

| # | 组件 | 职责 | 分期 |
|---|---|---|---|
| 00 | [foundation](./components/00-foundation.md) | 基建：类型模板引擎、生命周期状态机、Markdown 编辑、持久化 | MVP |
| 01 | [issue](./components/01-issue.md) | 议题创建/编辑（动议/附议/决议三区）、类型模板、状态流转 | MVP |
| 02 | [meeting](./components/02-meeting.md) | 会议、议程编排（拖拽排序）、议程项关联议题 | MVP |
| 03 | [vote](./components/03-vote.md) | 电子表决：记名/不记名、支持/反对/弃权、结果统计 | V1 |
| 04 | [resolution](./components/04-resolution.md) | 决议案生成（做什么/谁负责/何时完成）、执行跟踪、逾期预警 | V1 |
| 05 | [archive](./components/05-archive.md) | 年份+周次归档、检索回溯、标本反推验证 | MVP |
| 06 | [role](./components/06-role.md) | 用户/角色/权限：议长、书记、成员、创始人/两院、三模流程 | V1 |
| 07 | [weekly](./components/07-weekly.md) | 周会三件套（进展+决议+审计）、周报引用规则 | V1 |
| 08 | [audit](./components/08-audit.md) | 会前/会中/会后三段式审计、客观评分 | V2 |
| 09 | [classroom](./components/09-classroom.md) | 课堂项目、轮值议长/秘书、过程性评价 | V2 |
| 10 | [ai-advisor](./components/10-ai-advisor.md) | AI 议事助手：议长/思考者/行动者三角色、模拟辩论 | V2 |

## 四、组件依赖关系

```
foundation(00)
  ├── issue(01) ──> meeting(02) ──> vote(03) ──> resolution(04)
  ├── issue(01) ──> archive(05)
  └── role(06) ──> meeting(02) / vote(03) / weekly(07)
audit(08) ──> meeting(02) / resolution(04)
classroom(09) ──> issue(01) / meeting(02) / vote(03)
ai-advisor(10) ──> issue(01) / foundation(00)
```

## 五、实施分期

| 分期 | 组件 | 与现状差距 |
|---|---|---|
| MVP | 00 foundation、01 issue、02 meeting、05 archive | 小——现有两屏骨架直接演进，补数据模型即可 |
| V1 | 03 vote、04 resolution、06 role、07 weekly | 中——需用户/会议/表决数据模型与权限体系 |
| V2 | 08 audit、09 classroom、10 ai-advisor | 大——AI 三角色模拟为核心差异化功能 |

## 六、与现有代码的映射

- `issue.dart` 的 `IssueContent`（内容/结论两栏）→ 01 issue 的动议区/决议区双栏编辑器
- `mettings.dart` 的 `ReorderableListView` → 02 meeting 的议程编排核心组件（50 条占位数据 → 真实议题数据源）
- 需新增：00 foundation（类型模板模型、生命周期状态机、归档服务、数据持久化）
