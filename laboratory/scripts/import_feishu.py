#!/usr/bin/env python3
"""飞书导出 → 决议 YAML 导入实验

输入：飞书导出的 Markdown 文件（lark-cli drive +export --file-extension markdown）
输出：决议 YAML 文件（对齐 laboratory/resolutions/schema.yaml）

映射规则（从真实文档形态反推）：
- 第一行 "# 标题" → title；从标题提取周次 → id（2026年第N周 → 2026-WNN）
- "【已废止】" 标题前缀 → status=已废止
- <cite user-name="X"> → 提及人（owner 候选）
- <poll name="同意否"> → 投票标记（vote.present）
- "元数据区"/"决议区" 小节 → 结构段落
- 其余段落 → content

用法：python3 import_feishu.py <导出的md文件...> [--output-dir DIR]
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml


def extract_week(title: str) -> str | None:
    """2026年第28周 → 2026-W28"""
    m = re.search(r"(\d{4})年第(\d+)周", title)
    if m:
        return f"{m.group(1)}-W{int(m.group(2)):02d}"
    return None


def extract_proposal_no(title: str) -> int:
    """提案1 → 1；默认 0"""
    m = re.search(r"提案(\d+)", title)
    return int(m.group(1)) if m else 0


def parse_markdown(md: str) -> dict:
    lines = md.splitlines()
    title = ""
    m = re.search(r"<title>(.*?)</title>", md)
    if m:
        title = m.group(1).strip()
    if not title:
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

    status = "已废止" if "已废止" in title else "待执行"
    mentions: list[str] = []
    for name in re.findall(r'<cite[^>]*user-name="([^"]+)"', md):
        if name not in mentions:
            mentions.append(name)
    has_poll = "<poll" in md

    # 提取决议区内容（若有），否则用全文正文
    body_lines = []
    for line in lines:
        if line.startswith("#") or line.startswith("<cite") or line.startswith("<poll"):
            continue
        if line.strip():
            body_lines.append(re.sub(r"<[^>]+>", "", line).strip())
    content = "\n".join(body_lines)[:500]

    week = extract_week(title)
    seq = extract_proposal_no(title)
    res_id = f"{week}-{seq:03d}" if week else f"import-{seq:03d}"

    return {
        "id": res_id,
        "title": title,
        "content": content,
        "owner": mentions[0] if mentions else "",
        "mentions": mentions,
        "status": status,
        "vote_present": has_poll,
        "source": "飞书议事档案导入（实验）",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", help="飞书导出的 markdown 文件")
    ap.add_argument("--output-dir", default=str(
        Path(__file__).resolve().parent.parent / "resolutions" / "imported"))
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for f in args.files:
        md = Path(f).read_text(encoding="utf-8")
        res = parse_markdown(md)
        # 组装 schema 化决议
        resolution = {
            "id": res["id"],
            "title": res["title"],
            "content": res["content"],
            "owner": res["owner"],
            "due": None,
            "status": res["status"],
            "vote": {"present": res["vote_present"]},
            "source": {"imported_from": Path(f).name, "meeting": None},
            "evidence": [],
            "created_at": date.today().isoformat(),
            "history": [{"at": date.today().isoformat(), "by": "导入", "action": "飞书导入"}],
        }
        out = out_dir / f"{res['id']}.yaml"
        with open(out, "w", encoding="utf-8") as fh:
            yaml.safe_dump(resolution, fh, allow_unicode=True, sort_keys=False)
        print(f"✓ {res['id']} | {res['title']} | 状态={res['status']} | "
              f"提及={res['mentions']} | poll={res['vote_present']}")
    print(f"输出目录: {out_dir}")


if __name__ == "__main__":
    main()
