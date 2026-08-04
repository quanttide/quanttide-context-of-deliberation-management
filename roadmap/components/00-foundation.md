# 00-foundation 基建组件

> 分期：MVP | 依赖：无

## 职责

提供所有组件共享的基础能力：议题类型模板引擎、生命周期状态机、Markdown 编辑基础与数据持久化。

## 功能点

- **类型模板引擎**：九种议题类型 → 动议区字段映射（决策→选项列表+准则+权衡；计划→目标+里程碑+责任人+时间线；复盘研讨→问题清单+解决方案+个人心得…），并读取各类型的 `stage_requirements` 配置（required/optional/skipped）决定环节流转
- **生命周期状态机**：议题创建 → 动议提出 → 附议扩散 → 决议形成 → 归档沉淀。**五节点为固定骨架**（`contract.yaml` lifecycle.fixed_skeleton），不可变；环节的必经/可选/跳过由类型配置驱动，不在状态机内硬编码
- **Markdown 编辑**：三区编辑器基础组件（编辑/预览），复用 `markdown_editor_plus`
- **数据持久化**：议题、会议、决议、档案的本地存储与同步接口
- **编号规则**：议事档案编号（年份+周次）生成

## 资料依据

- contract.yaml：九种类型 expected_fields、lifecycle 五节点
- 现有代码：`issue.dart` 已引入 `markdown_editor_plus`

## 代码映射

- 新增 `lib/models/issue_type.dart`（类型枚举与字段模板）
- 新增 `lib/models/lifecycle.dart`（状态机）
- 新增 `lib/services/storage.dart`（持久化接口）
