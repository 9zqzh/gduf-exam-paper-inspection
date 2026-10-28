#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从成绩单（xlsx / docx 表格）计算平均分、及格率、优秀率、标准差、分数段。

用法：
    python grade_stats.py "材料/学生成绩单.xlsx"
    python grade_stats.py "材料/学生成绩单.xlsx" --pass 60 --excellent 90
    python grade_stats.py "材料/学生成绩单.docx" --json --out 临时/成绩统计.json

说明：
- 自动识别表头行，优先统计“总评/总成绩/最终成绩”列，其次“期末/试卷/卷面”列，
  同时会统计“平时成绩”列。
- 缺考、缓考、免修、作弊等非数值记录不计入均值，但会在输出中单列，需在报告中说明。
- 标准差采用总体标准差；分数段按 [0,60)、[60,70)、[70,80)、[80,90)、[90,100]。
- 若表格结构特殊无法识别，会打印检测到的表头，请改用 --total-col 指定列名关键字。
"""

import argparse
import json
import os
import re
import statistics
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SPECIAL = ["缺考", "缓考", "免修", "作弊", "违纪", "取消", "未修", "休学", "退学", "免听", "通过", "不通过"]


def norm(v):
    return re.sub(r"[\s\u3000()（）\[\]【】]+", "", str(v or ""))


def is_blank(v):
    return str(v if v is not None else "").strip() == ""


def read_tables(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
        out = []
        for ws in wb.worksheets:
            rows = [list(r) for r in ws.iter_rows(values_only=True)]
            out.append({"name": f"工作表：{ws.title}", "rows": rows})
        wb.close()
        return out
    if ext in (".docx", ".doc"):
        if ext == ".doc":
            raise SystemExit("旧版 .doc 无法解析，请另存为 .docx。")
        import docx
        d = docx.Document(path)
        out = []
        for i, t in enumerate(d.tables, 1):
            rows = []
            for r in t.rows:
                cells, prev = [], None
                for c in r.cells:
                    txt = c.text.strip()
                    if txt != prev:
                        cells.append(txt)
                    prev = txt
                rows.append(cells)
            out.append({"name": f"表 {i}", "rows": rows})
        return out
    if ext == ".pdf":
        raise SystemExit("PDF 成绩单请先用 Read 工具按页查看，或从教务系统导出 xlsx 后重试。")
    raise SystemExit(f"不支持的成绩单格式：{ext}")


def find_header(rows):
    best = (-1, -1)
    for i, row in enumerate(rows[:25]):
        cells = [norm(c) for c in row]
        if not cells:
            continue
        score = 0
        if any("学号" in c for c in cells):
            score += 2
        if any("姓名" in c for c in cells):
            score += 1
        if any("成绩" in c or "总评" in c or "分数" in c for c in cells):
            score += 2
        if score >= 3 and score > best[0]:
            best = (score, i)
    return best[1] if best[1] >= 0 else None


def match_columns(headers):
    """返回 {kind: [(label, index)]}，kind 为 total/final/usual。"""
    groups = {
        "total": ["总评成绩", "总成绩", "最终成绩", "综合成绩", "总评", "最终", "总评分"],
        "final": ["期末成绩", "试卷成绩", "卷面成绩", "期末", "卷面", "试卷分"],
        "usual": ["平时成绩", "平时分", "过程性考核", "平时"],
    }
    found = {"total": [], "final": [], "usual": []}
    used = set()
    for kind, kws in groups.items():
        for j, h in enumerate(headers):
            n = norm(h)
            if not n or j in used:
                continue
            if any(k in n for k in kws):
                found[kind].append((str(headers[j]).strip(), j))
                used.add(j)
    return found


def parse_score(v):
    s = str(v if v is not None else "").strip()
    if not s:
        return None, ""
    for sp in SPECIAL:
        if sp in s:
            return None, sp
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    if not m:
        return None, s[:10]
    try:
        x = float(m.group())
    except ValueError:
        return None, s[:10]
    if x < 0 or x > 150:
        return None, s[:10]
    return x, ""


def stats_of(values, pass_line=60, excellent_line=90):
    n = len(values)
    if not n:
        return None
    mean = statistics.fmean(values)
    std = statistics.pstdev(values) if n > 1 else 0.0
    passed = sum(1 for v in values if v >= pass_line)
    excellent = sum(1 for v in values if v >= excellent_line)
    bands = {
        "0-59": sum(1 for v in values if v < 60),
        "60-69": sum(1 for v in values if 60 <= v < 70),
        "70-79": sum(1 for v in values if 70 <= v < 80),
        "80-89": sum(1 for v in values if 80 <= v < 90),
        "90-100": sum(1 for v in values if v >= 90),
    }
    return {
        "n": n,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
        "pass_rate": round(passed / n * 100, 2),
        "excellent_rate": round(excellent / n * 100, 2),
        "fail_rate": round((n - passed) / n * 100, 2),
        "bands": bands,
        "pass_line": pass_line,
        "excellent_line": excellent_line,
    }


def analyze_table(rows, table_name, pass_line, excellent_line, col_hint=None):
    hi = find_header(rows)
    if hi is None:
        return {"name": table_name, "ok": False, "error": "未识别到含“学号/姓名/成绩”的表头行", "sample": rows[:3]}

    headers = rows[hi]
    cols = match_columns(headers)
    if col_hint:
        for kind in cols:
            cols[kind] = [(h, j) for h, j in cols[kind] if col_hint in norm(h)]
    if not cols["total"] and not cols["final"]:
        # 只有一个含“成绩”的列时，视为总评
        cand = [(str(h).strip(), j) for j, h in enumerate(headers)
                if "成绩" in norm(h) and "平时" not in norm(h)]
        if len(cand) == 1:
            cols["total"] = cand
    targets = []
    for kind in ("total", "final", "usual"):
        for label, j in cols[kind]:
            targets.append((kind, label, j))

    if not targets:
        return {"name": table_name, "ok": False,
                "error": "未找到总评/期末/平时成绩列",
                "headers": [str(h) for h in headers if not is_blank(h)]}

    data_rows = rows[hi + 1:]
    result = {"name": table_name, "ok": True, "header_row": hi + 1,
              "headers": [str(h).strip() for h in headers], "columns": []}
    for kind, label, j in targets:
        values, specials = [], []
        for r in data_rows:
            if j >= len(r):
                continue
            v, sp = parse_score(r[j])
            if v is not None:
                values.append(v)
            elif sp:
                specials.append(sp)
        st = stats_of(values, pass_line, excellent_line)
        if not st:
            continue
        result["columns"].append({
            "kind": kind,
            "label": label,
            "index": j,
            "stats": st,
            "special_count": len(specials),
            "special_labels": sorted(set(specials)),
        })
    if not result["columns"]:
        result["ok"] = False
        result["error"] = "检测到成绩列，但没有可统计的数值"
    return result


def analyze(path, pass_line=60, excellent_line=90, col_hint=None):
    tables = read_tables(path)
    results = []
    for t in tables:
        r = analyze_table(t["rows"], t["name"], pass_line, excellent_line, col_hint)
        results.append(r)

    # 多表聚合：仅聚合各表中“总评”类的数值
    overall = None
    if sum(1 for r in results if r.get("ok")) > 1:
        vals = []
        for t, r in zip(tables, results):
            if not r.get("ok"):
                continue
            hi = r["header_row"] - 1
            total_cols = [c for c in r["columns"] if c["kind"] == "total"]
            if not total_cols:
                continue
            j = total_cols[0]["index"]
            for row in t["rows"][hi + 1:]:
                if j < len(row):
                    v, _ = parse_score(row[j])
                    if v is not None:
                        vals.append(v)
        overall = stats_of(vals, pass_line, excellent_line)
        if overall:
            overall["label"] = "各表总评合并"

    return {
        "file": os.path.abspath(path),
        "pass_line": pass_line,
        "excellent_line": excellent_line,
        "tables": results,
        "overall": overall,
    }


def print_md(res):
    print("# 成绩统计结果\n")
    print(f"- 文件：`{res['file']}`")
    print(f"- 及格线：{res['pass_line']}　优秀线：{res['excellent_line']}")
    print("- 标准差为总体标准差；缺考/缓考等非数值记录不计入均值。\n")
    kind_cn = {"total": "总评/最终成绩", "final": "期末/试卷成绩", "usual": "平时成绩"}
    for t in res["tables"]:
        print(f"## {t['name']}")
        if not t.get("ok"):
            print(f"未完成统计：{t.get('error')}")
            if t.get("headers"):
                print("检测到的表头：" + " | ".join(t["headers"]))
            if t.get("sample"):
                for row in t["sample"]:
                    print("  " + " | ".join("" if v is None else str(v) for v in row))
            print()
            continue
        print(f"表头位于第 {t['header_row']} 行。\n")
        print("| 统计口径 | 有效人数 | 平均分 | 标准差 | 最高 | 最低 | 及格率 | 优秀率 | 不及格率 |")
        print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for c in t["columns"]:
            s = c["stats"]
            print(f"| {kind_cn.get(c['kind'], c['kind'])}：{c['label']} | {s['n']} | {s['mean']} | {s['std']} | "
                  f"{s['max']} | {s['min']} | {s['pass_rate']}% | {s['excellent_rate']}% | {s['fail_rate']}% |")
        print()
        for c in t["columns"]:
            s = c["stats"]
            print(f"- {c['label']} 分数段：<60：{s['bands']['0-59']}；60-69：{s['bands']['60-69']}；"
                  f"70-79：{s['bands']['70-79']}；80-89：{s['bands']['80-89']}；90-100：{s['bands']['90-100']}")
            if c["special_count"]:
                print(f"  非数值记录 {c['special_count']} 条：{'、'.join(c['special_labels'])}（需在报告中说明）")
        print()
    if res["overall"]:
        s = res["overall"]
        print("## 各表合并（总评）\n")
        print(f"- 有效人数 {s['n']}，平均分 {s['mean']}，标准差 {s['std']}，及格率 {s['pass_rate']}%，"
              f"优秀率 {s['excellent_rate']}%，不及格率 {s['fail_rate']}%\n")
    print("> 提示：统计结果须与成绩单原件复核后再写入报告；若识别列有误，请用 --total-col 指定列名关键字重跑。")


def main():
    ap = argparse.ArgumentParser(description="计算成绩统计指标")
    ap.add_argument("path", help="成绩单 xlsx/docx")
    ap.add_argument("--pass", dest="pass_line", type=float, default=60, help="及格线，默认60")
    ap.add_argument("--excellent", dest="excellent_line", type=float, default=90, help="优秀线，默认90")
    ap.add_argument("--total-col", help="总评列名关键字（可选）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="写入结果文件")
    args = ap.parse_args()

    if not os.path.isfile(args.path):
        raise SystemExit(f"文件不存在：{args.path}")
    res = analyze(args.path, args.pass_line, args.excellent_line, args.total_col)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            if args.out.lower().endswith(".json") or args.json:
                json.dump(res, fh, ensure_ascii=False, indent=2)
            else:
                import io
                buf = io.StringIO()
                old = sys.stdout
                sys.stdout = buf
                try:
                    print_md(res)
                finally:
                    sys.stdout = old
                fh.write(buf.getvalue())
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_md(res)


if __name__ == "__main__":
    main()
