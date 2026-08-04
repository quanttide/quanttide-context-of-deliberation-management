# CHANGELOG

所有显著变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [Unreleased]

### Added

- 新增议事云产品意图（intention/qtcloud-delib.md）：决议为中心的定位、自建系统与飞书单向导入的数据策略、决议子系统先行的实施路径

### Changed

- roadmap 分期调整：决议子系统（00/04/05）提前至 MVP 独立先行；议事子系统（01/02/03/06/07）为 V1

- 契约 v0.0.7 起决议统一治理补充可见性机制：治理视图、决议播报、周会决议汇总（解决"看不到决议"的管理困难）
- 契约升级 v0.0.7：生命周期扩充为七节点（新增辩论、投票环节）
- 契约升级 v0.0.6：议题收敛为两类模式——研讨（开放深度讨论）与提案（封闭决策）
- 契约升级 v0.0.5：议事规则、议程独立为实体（不混入议题类型）；议题类型 9 → 6 种
- 契约升级 v0.0.4：决议作为独立实体，脱离议题单独管理（统一治理——执行跟踪、审计、统计）
- 契约升级 v0.0.3：五环节固定骨架 + 各类型 stage_requirements 配置（required/optional/skipped）
- 治理内容迁出至 quanttide-org 领域（章程、设计意图、治理手册）
- 澄清无辩论区：真人议事简洁路径与 AI 模拟辩论分工

## [0.1.0] - 2026-08-04

### Added
- 初始化项目结构（README、LICENSE、CHANGELOG）
- 治理设计意图（design-intention.md）
- 议事云产品理念（delib-cloud.md）
- 议事流程（workflow.md）