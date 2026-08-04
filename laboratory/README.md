# 决议子系统结构实验

> 实验目的：验证"一决议一文件 + 索引 + 逾期推导"的决议档案结构是否可行，以及它能否支撑治理视图、执行跟踪与周会汇总。

## 实验结构

```
laboratory/
├── README.md                    # 本文件：实验说明
├── resolutions/                 # 决议档案实验区
│   ├── schema.yaml              # 决议 schema（结构契约）
│   ├── 2026-W31-001.yaml        # 示例决议：进行中
│   ├── 2026-W31-002.yaml        # 示例决议：逾期
│   ├── 2026-W31-003.yaml        # 示例决议：已完成
│   └── index.yaml               # 决议索引（由脚本生成：状态聚合、逾期推导）
└── scripts/
    └── gen_index.py             # 索引生成脚本：扫描决议 → 生成 index.yaml + 治理视图
```

## 实验方法

1. 手写 3 条示例决议（覆盖进行中/逾期/已完成三种状态）
2. 运行 `scripts/gen_index.py`：扫描决议文件，推导逾期状态，生成索引与治理视图
3. 观察输出：状态统计、逾期列表、责任人分布——回答"治理层能不能一屏看到决议全貌"

## 运行

```bash
python3 scripts/gen_index.py
```

## 待验证问题

- [x] 一决议一文件的粒度是否方便增删改（责任人改状态 = 改一个字段）
- [x] 逾期推导规则（due < 今天 且 status ≠ 已完成）是否合理
- [x] 索引能否直接支撑周会汇总与治理视图
- [x] 飞书导出的决议能否映射到这个 schema（见 import_feishu.py 实验）

## 飞书导入实验（2026-08-04，真实数据）

用 lark-cli 从飞书"议事档案"知识库导出 3 个真实文档，映射为决议 YAML：

| 飞书文档 | 导入结果 | 关键字段 |
|---------|---------|---------|
| 2026年第28周-提案1-人员晋升 | `imported/2026-W28-001.yaml` | owner=涂雅芳/刘婧怡, vote.present=true |
| 2026年第3周-提案2-数据契约 | `imported/2026-W03-002.yaml` | 提及 5 人, vote.present=true |
| 【已废止】建立各部门GTD清单 | `imported/import-000.yaml` | **status=已废止**（标题前缀识别） |

**真实数据发现**（影响 schema 设计）：
1. 飞书决议/提案无"完成期限"字段 → `due` 缺失（逾期推导跳过）
2. 状态用【已废止】标题前缀表达（非枚举字段）→ 导入时映射为 status
3. 投票是 `<poll>` 块 → 映射为 `vote.present`
4. 文档标题格式不一（`# ` 或 `<title>`）→ 解析需兼容两种

**导入命令**：
```bash
uv run --with pyyaml python3 scripts/import_feishu.py <导出md文件...>
uv run --with pyyaml python3 scripts/gen_index.py   # 重新生成治理视图
```
