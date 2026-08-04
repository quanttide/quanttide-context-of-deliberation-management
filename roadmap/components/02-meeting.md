# 02-meeting 会议与议程组件

> 分期：MVP | 依赖：00-foundation、01-issue、06-role

## 职责

会议的组织与议程编排：会议创建、议程项排序、议程与议题关联、决议执行播报。

## 功能点

- **会议创建**：时间、参与者、议程项（议程类型议题）
- **议程编排**：议程项拖拽排序（ReorderableListView）
- **议程关联**：议程项关联议题，@提及行动项（议事规则类型）
- **决议执行播报**：开场自动播报上次会议决议执行情况，未结事项置顶（周会案例）
- **程序动议**：修改议程、立刻表决、休息等优先处理

## 资料依据

- contract.yaml：议程类型 expected_fields（时间、参与者、议程项）
- 案例一：会前议程生成、会中程序动议
- 现有代码：`mettings.dart`（IssueList 可拖拽排序，50 条占位数据）

## 代码映射

- `mettings.dart` 的 `ReorderableListView` 演进为议程编排核心组件
- 新增 `lib/screens/meeting_create.dart`（会议创建）
- 新增 `lib/widgets/agenda_item.dart`（议程项：关联议题 + @提及）
