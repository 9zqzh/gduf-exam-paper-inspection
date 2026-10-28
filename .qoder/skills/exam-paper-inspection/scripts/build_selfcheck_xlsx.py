#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把核查发现的问题写入《试卷自查登记表》。

用法：
    python build_selfcheck_xlsx.py --payload 输出/issues.json --out "输出/高平安_试卷自查登记表.xlsx"

payload：
{
  "rows": [
    {"year":"2025-2026-2","course":"Java程序设计","type":"必修课",
     "class":"25清远计算机科学与技术-1～3班","teacher":"高平安",
     "students":"2025001、2025017","issue":"问题点及描述","note":"备注"}
  ]
}

列顺序与学院模板一致：序号、开课学年、课程名称、课程类型、专业班级、
任课/老师、涉及学生姓名或学号、问题点及描述、备注。
"""

import argparse
import json
import os
import sys

try:
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, Side
except ImportError:
    sys.stderr.write("ERROR: 缺少 openpyxl，请执行: python -m pip install openpyxl\n")
    sys.exit(2)

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(SKILL_DIR, "assets", "试卷自查登记表.xlsx")

HEADERS = ["序号", "开课学年", "课程名称", "课程类型", "专业班级", "任课/老师",
           "涉及学生姓名或学号", "问题点及描述", "备注"]
# 合计约 136 个字符宽，A4 横向按 100% 打印不再缩放
WIDTHS = [4, 11, 11, 6, 12, 5, 8, 46, 12]
KEYS = ["no", "year", "course", "type", "class", "teacher", "students", "issue", "note"]

# 问题分级自检：这些词通常意味着把系统/模板/纸质环节写成了教师问题
TRIAGE_BANNED = ["签字盖章", "答题册", "打印份数", "课程试卷及成绩分析表",
                 "XX列", "专业班级", "考试日期", "答题要求", "统计口径"]


def build(rows, out_path, template=TEMPLATE):
    wb = openpyxl.load_workbook(template)
    ws = wb.active
    if ws.max_row < 2:
        for j, h in enumerate(HEADERS, 1):
            ws.cell(row=1, column=j, value=h)

    thin = Side(style="thin", color="999999")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    body_font = Font(name="宋体", size=10.5)
    head_font = Font(name="宋体", size=10.5, bold=True)

    for j, (h, w) in enumerate(zip(HEADERS, WIDTHS), 1):
        c = ws.cell(row=1, column=j)
        c.font = head_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = border
        ws.column_dimensions[c.column_letter].width = w

    ws.row_dimensions[1].height = 42

    start = 2
    for i, item in enumerate(rows):
        vals = []
        for k in KEYS:
            if k == "no":
                vals.append(i + 1)
            else:
                vals.append(item.get(k, ""))
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=start + i, column=j, value=v)
            c.font = body_font
            c.border = border
            if j in (1, 2, 4, 6):
                c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            else:
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        issue_len = len(str(item.get("issue", "")))
        note_len = len(str(item.get("note", "")))
        lines = max(1, (issue_len + 21) // 22)
        note_lines = max(1, (note_len + 4) // 5)
        ws.row_dimensions[start + i].height = max(28, 14.2 * max(lines, note_lines) + 6)

    # 清空模板中多余的空白行边框
    for r in range(start + len(rows), ws.max_row + 1):
        for j in range(1, len(HEADERS) + 1):
            ws.cell(row=r, column=j).border = Border()

    ws.freeze_panes = "A2"
    ws.page_setup.orientation = "landscape"
    ws.page_margins.left = 1.0
    ws.page_margins.right = 1.0
    ws.page_margins.top = 0.9
    ws.page_margins.bottom = 0.9
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    # 宽度固定为一页；行数较多、超出 A4 横向一页时再整体缩放
    total_h = float(ws.row_dimensions[1].height or 42)
    for i in range(len(rows)):
        total_h += float(ws.row_dimensions[start + i].height or 28)
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 1 if total_h > 540 else 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "1:1"
    ws.print_area = f"A1:I{start + max(len(rows), 1) - 1}"
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    wb.save(out_path)
    return os.path.abspath(out_path)


def main():
    ap = argparse.ArgumentParser(description="生成试卷自查登记表")
    ap.add_argument("--payload", required=True, help="JSON 数据文件")
    ap.add_argument("--out", required=True, help="输出 xlsx 路径")
    ap.add_argument("--template", default=TEMPLATE, help="模板路径")
    args = ap.parse_args()

    with open(args.payload, encoding="utf-8") as fh:
        data = json.load(fh)
    rows = data.get("rows", data if isinstance(data, list) else [])
    if not rows:
        raise SystemExit("payload 中没有 rows，未生成登记表。")
    out = build(rows, args.out, args.template)
    print(f"[已生成] {out}")
    print(f"[条目数] {len(rows)}")

    hits = set()
    for item in rows:
        text = str(item.get("issue", "")) + " " + str(item.get("note", ""))
        hits.update(w for w in TRIAGE_BANNED if w in text)
    if hits:
        print("[提醒] 登记表疑似包含系统/模板/纸质环节事项（" + "、".join(sorted(hits)) +
              "）：按 references/issue-triage.md 只保留教师可改的硬性问题。", file=sys.stderr)


if __name__ == "__main__":
    main()
