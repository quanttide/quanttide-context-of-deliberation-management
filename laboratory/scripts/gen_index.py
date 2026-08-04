#!/usr/bin/env python3
"""决议索引生成脚本（实验）

扫描 resolutions/ 下的决议 YAML 文件：
1. 推导逾期状态（due < today 且 status != 已完成）
2. 生成 index.yaml（聚合统计）
3. 输出治理视图（控制台打印，模拟"治理层一屏看决议"）

用法：python3 gen_index.py [--today YYYY-MM-DD]（--today 用于实验固定日期）
"""
import argparse
import sys
import yaml
from datetime import date, datetime
from pathlib import Path

RESOLUTIONS_DIR = Path(__file__).resolve().parent.parent / "resolutions"


def parse_date(s) -> date:
    if isinstance(s, date):
        return s
    return datetime.strptime(s, "%Y-%m-%d").date()


def load_resolutions() -> list[dict]:
    items = []
    for f in sorted(RESOLUTIONS_DIR.glob("*.yaml")):
        if f.name in ("schema.yaml", "index.yaml"):
            continue
        with open(f, encoding="utf-8") as fh:
            items.append(yaml.safe_load(fh))
    return items


def derive_status(res: dict, today: date) -> str:
    """逾期为推导状态：due < today 且未完成"""
    if res.get("status") == "已完成":
        return "已完成"
    if parse_date(res["due"]) < today:
        return "逾期"
    return res.get("status", "待执行")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=date.today().isoformat())
    args = ap.parse_args()
    today = parse_date(args.today)

    resolutions = load_resolutions()
    for res in resolutions:
        res["_derived_status"] = derive_status(res, today)

    # 聚合统计
    stats = {"总数": len(resolutions)}
    for st in ("待执行", "执行中", "已完成", "逾期"):
        stats[st] = sum(1 for r in resolutions if r["_derived_status"] == st)

    # 生成 index.yaml
    index = {
        "generated_at": today.isoformat(),
        "stats": stats,
        "resolutions": [
            {
                "id": r["id"],
                "title": r["title"],
                "owner": r["owner"],
                "due": r["due"],
                "status": r["_derived_status"],
            }
            for r in resolutions
        ],
    }
    with open(RESOLUTIONS_DIR / "index.yaml", "w", encoding="utf-8") as fh:
        yaml.safe_dump(index, fh, allow_unicode=True, sort_keys=False)

    # 治理视图（控制台）
    print("═" * 46)
    print(f"  决议治理视图  [{today}]")
    print("═" * 46)
    print(f"  统计: 总数 {stats['总数']} | 待执行 {stats['待执行']} | "
          f"执行中 {stats['执行中']} | 已完成 {stats['已完成']} | 逾期 {stats['逾期']}")
    print("─" * 46)
    overdue = [r for r in resolutions if r["_derived_status"] == "逾期"]
    if overdue:
        print("  ⚠ 逾期决议:")
        for r in overdue:
            print(f"    - {r['id']} {r['title']} (责任人: {r['owner']}, 期限: {r['due']})")
    print("─" * 46)
    print("  按责任人分布:")
    by_owner: dict[str, int] = {}
    for r in resolutions:
        by_owner[r["owner"]] = by_owner.get(r["owner"], 0) + 1
    for owner, cnt in by_owner.items():
        print(f"    - {owner}: {cnt} 项")
    print("═" * 46)


if __name__ == "__main__":
    main()
