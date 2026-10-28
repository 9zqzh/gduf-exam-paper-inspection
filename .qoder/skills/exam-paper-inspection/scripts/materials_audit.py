#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""对照《本科课程考试试卷档案归档目录》清点教师上传的试卷材料。

用法：
    python materials_audit.py --dir "试卷材料/Java程序设计" --checklist paper
    python materials_audit.py --dir ... --checklist cbt --classes 3 --students 167
    python materials_audit.py --dir ... --json

说明：
- 依据文件名归类，不能替代人工核对；输出会明确标注“需人工确认”的项。
- 扫描件、签章、学号排序、分析表字数等无法仅凭文件名判断，统一列入人工核对项。
- 缺失必需材料或必需材料为 0 字节空文件时 complete=false，上层 Agent 应暂停写报告，先引导教师补传。
"""

import argparse
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHECKLISTS = {
    "paper": {
        "title": "《本科课程考试试卷档案归档目录》（纸质版）",
        "items": [
            {"no": "1", "name": "期末考试试题", "required": True, "hint": "A4版本原稿（A或B卷一套）"},
            {"no": "2", "name": "标准答案及评分标准", "required": True, "hint": "与试题配套，评分标准完整规范"},
            {"no": "3", "name": "学生成绩单", "required": True, "hint": "教务系统导出，含考试简况/实到人数"},
            {"no": "4", "name": "学生平时成绩登记表", "required": True, "hint": "2025年教务处制，注明分数来源"},
            {"no": "5", "name": "班级成绩分析表", "required": True, "hint": "按班级填写"},
            {"no": "6", "name": "课程试卷及成绩分析表（试卷类）", "required": True, "hint": "试卷情况等四段各约200字"},
            {"no": "7", "name": "期末考试专用答题册", "required": True, "hint": "按学号由小到大排列"},
            {"no": "8", "name": "试卷审核表（复印件）", "required": True, "hint": "2025年教务处制"},
            {"no": "9", "name": "其他材料", "required": False, "hint": "如《归档材料补充说明》"},
        ],
    },
    "cbt": {
        "title": "《本科课程考试试卷档案归档目录（机考）》",
        "items": [
            {"no": "1", "name": "期末考试试题", "required": True, "hint": "电子版"},
            {"no": "2", "name": "标准答案及评分标准", "required": True, "hint": "电子版"},
            {"no": "3", "name": "学生成绩单", "required": True, "hint": "签名处需电子签章或签字盖章后扫描"},
            {"no": "4", "name": "学生平时成绩登记表", "required": True, "hint": "2025年教务处制，打印盖学院公章再扫描/拍照"},
            {"no": "5", "name": "班级成绩分析表", "required": True, "hint": "四段各约200字"},
            {
                "no": "6",
                "name": "课程试卷及成绩分析表（试卷类）/课程考核成绩分析表（非试卷类）",
                "required": True,
                "hint": "按考试类型二选一；非试卷类由教师自行计算数据填写；每班一份复核说明",
            },
            {"no": "7", "name": "期末考试专用答题册", "required": True, "hint": "系统导出电子版，每位学生一份"},
            {"no": "8", "name": "试卷审核表", "required": True, "hint": "打印盖学院公章再扫描/拍照"},
            {"no": "9", "name": "其他材料", "required": False, "hint": "如复核说明、补充说明"},
        ],
    },
}

# 顺序敏感：先匹配更具体的类别
RULES = [
    ("8", ["试卷审核", "审核表"]),
    ("2", ["标准答案", "参考答案", "答案及评分", "评分标准", "答案"]),
    ("4", ["平时成绩", "平时分"]),
    ("5", ["班级成绩分析", "班级分析"]),
    ("6a", ["试卷及成绩分析", "课程试卷及成绩分析", "试卷分析", "课程考试成绩分析", "质量分析"]),
    ("6b", ["考核成绩分析", "非试卷", "课程考核成绩分析"]),
    ("7", ["答题册", "答题纸", "学生答卷", "答卷"]),
    ("3", ["成绩单", "学生成绩", "成绩登记"]),
    ("9", ["补充说明", "归档材料补充", "复核说明", "其他材料", "情况说明"]),
    ("1", ["期末试题", "期末考试试题", "试题", "试卷", "A卷", "B卷", "AB卷"]),
]

DOC_EXT = {".docx", ".doc", ".pdf", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".md", ".wps", ".zip", ".rar", ".7z", ".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def norm(s):
    return re.sub(r"[\s_\-—（）()【】\[\]{}·.]+", "", str(s or "")).lower()


def classify(filename):
    n = norm(filename)
    for key, kws in RULES:
        if any(k.lower() in n for k in kws):
            return key
    return None


def item_key_map(checklist):
    """把 6a/6b 映射到清单条目编号 6。"""
    return {"6a": "6", "6b": "6"}


def scan_files(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        for f in filenames:
            if f.startswith("~$") or f.startswith("."):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext and ext not in DOC_EXT:
                continue
            path = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(path)
            except OSError:
                size = 0
            out.append({"name": f, "path": path, "rel": os.path.relpath(path, root), "size": size, "ext": ext})
    return sorted(out, key=lambda x: x["rel"])


def audit(root, checklist="paper", classes=None, students=None, actual=None):
    if not os.path.isdir(root):
        raise SystemExit(f"目录不存在：{root}")
    spec = CHECKLISTS[checklist]
    files = scan_files(root)
    kmap = item_key_map(checklist)

    buckets = {it["no"]: [] for it in spec["items"]}
    unrecognized = []
    for f in files:
        key = classify(f["name"])
        no = kmap.get(key, key)
        if no and no in buckets:
            buckets[no].append(f)
        else:
            unrecognized.append(f)

    items = []
    for it in spec["items"]:
        fs = buckets[it["no"]]
        empty = [f for f in fs if f["size"] == 0]
        if not fs:
            status = "optional_absent" if not it["required"] else "missing"
        elif len(empty) == len(fs):
            status = "empty"
        elif empty:
            status = "partial_empty"
        else:
            status = "found"
        items.append({**it, "status": status, "files": fs, "count": len(fs), "empty": empty})

    missing = [it["name"] for it in items if it["status"] in ("missing", "empty")]
    empty_names = [it["name"] for it in items if it["status"] in ("empty", "partial_empty")]

    checks = []

    def check(level, text):
        checks.append({"level": level, "text": text})

    # 试题 A/B 卷
    exam_files = buckets.get("1", [])
    names = " ".join(f["name"] for f in exam_files)
    has_a = bool(re.search(r"(?<![A-Za-z])A卷|A卷", names, re.I))
    has_b = bool(re.search(r"(?<![A-Za-z])B卷|B卷", names, re.I))
    if exam_files:
        if has_a and has_b:
            check("ok", "试题文件中同时检测到 A 卷与 B 卷。")
        elif has_a or has_b:
            check("warn", f"仅检测到 {'A' if has_a else 'B'} 卷；请确认另一套卷是否按规定归档（共性检查要求 A/B 卷齐全且不雷同）。")
        else:
            check("manual", "试题文件未标注 A/B 卷，无法自动判断套数；请人工确认 A/B 卷是否齐全。")
    else:
        check("error", "未找到期末考试试题文件。")

    # 分析表
    analysis = buckets.get("6", [])
    if analysis:
        check("manual", "分析表中的“试卷情况、改进措施、考试结果分析、改进教学建议”应各约200字；请用 extract_text.py 提取后核对字数与内容真实性。")
    # 机考复核说明
    if checklist == "cbt":
        review_files = [f for f in files if "复核" in f["name"]]
        if review_files:
            check("ok", f"检测到复核说明类文件 {len(review_files)} 个。")
        else:
            check("warn", "未检测到“复核说明”；机考/考查课程要求每个班级写一份复核说明。")
        check("manual", "机考材料需核对：成绩单、分析表签名处是否有电子签章或签字盖章扫描件；非试卷类分析表数据是否由任课教师自行计算填写。")

    # 人数与答题册
    answerbooks = buckets.get("7", [])
    if students and answerbooks:
        per_student = len(answerbooks) >= max(5, int(students * 0.5)) if students else False
        if per_student:
            if len(answerbooks) == students:
                check("ok", f"答题册文件数（{len(answerbooks)}）与选课人数（{students}）一致。")
            else:
                check("warn", f"答题册文件数（{len(answerbooks)}）与选课人数（{students}）不一致；请核对是否缺考、缓考、作弊上缴等情况，必要时填写《归档材料补充说明》。")
        else:
            check("warn", f"答题册仅 {len(answerbooks)} 个文件，明显少于选课人数 {students}。请确认是合并扫描件，还是存在缺传；若为合并件需打开核对实际份数是否等于实到人数（{actual or '未提供'}）。")
    elif students and not answerbooks:
        check("error", "未找到答题册/学生答卷文件，无法核对实到人数。")
    if actual and students and actual != students:
        check("warn", f"实到人数（{actual}）与选课人数（{students}）不一致，请按《归档材料补充说明》说明原因。")

    # 班级数
    if classes:
        for no, label in (("3", "成绩单"), ("4", "平时成绩登记表"), ("5", "班级成绩分析表")):
            fs = buckets.get(no, [])
            if fs and len(fs) not in (1, classes):
                check("warn", f"{label}文件数为 {len(fs)}，与班级数 {classes} 不一致（合并文件可忽略此项）。")
    # 零字节文件：文件存在但内容为空，等同于未提供，不能进入核查
    zero = [f["rel"] for f in files if f["size"] == 0]
    if zero:
        check("error", "以下文件为 0 字节（空文件），无法核验，请重新上传：" + "；".join(zero[:8]) + ("…" if len(zero) > 8 else ""))
    if empty_names:
        check("error", "存在空文件的必需材料：" + "；".join(empty_names) + "。请重新上传后再核查。")
    if unrecognized:
        check("manual", f"有 {len(unrecognized)} 个文件未能按文件名归类，请人工确认归属：")
    check("manual", "以下项目无法自动核验，需逐份查看：成绩单“考试简况”实到人数、平时成绩分数来源标注、阅卷统分准确性、答题册学号顺序、签名/盖章完整性。")

    complete = not missing and not any(it["status"] == "partial_empty" for it in items)
    return {
        "dir": os.path.abspath(root),
        "checklist": checklist,
        "checklist_title": spec["title"],
        "file_count": len(files),
        "items": items,
        "missing": missing,
        "empty_items": empty_names,
        "unrecognized": unrecognized,
        "checks": checks,
        "complete": complete,
        "inputs": {"classes": classes, "students": students, "actual": actual},
    }


def print_md(res):
    print(f"# 材料清点结果\n")
    print(f"- 清点目录：`{res['dir']}`")
    print(f"- 对照清单：{res['checklist_title']}")
    print(f"- 文件总数：{res['file_count']}")
    print(f"- 结论：{'材料齐全，可进入核查' if res['complete'] else '材料不齐或存在空文件，需补传/重新上传'}\n")
    print("| 序号 | 归档材料 | 要求 | 状态 | 文件数 |")
    print("| --- | --- | --- | --- | --- |")
    status_cn = {
        "found": "已提供",
        "missing": "缺失",
        "empty": "文件为空（0字节）",
        "partial_empty": "部分文件为空",
        "optional_absent": "未提供（可选）",
    }
    for it in res["items"]:
        print(f"| {it['no']} | {it['name']} | {it['hint']} | {status_cn[it['status']]} | {it['count']} |")
    print()
    if res["missing"]:
        print("## 待补传/重新上传\n")
        for m in res["missing"]:
            print(f"- {m}")
        print()
    if res["unrecognized"]:
        print("## 未识别文件（请确认归属）\n")
        for f in res["unrecognized"]:
            print(f"- {f['rel']}")
        print()
    print("## 自动核查与人工核对项\n")
    icon = {"ok": "✅", "warn": "⚠️", "error": "❌", "manual": "👁️"}
    for c in res["checks"]:
        print(f"- {icon.get(c['level'], '·')} {c['text']}")
    print()
    print("> 提示：本结果基于文件名自动归类，不能替代逐份翻阅。请把“人工核对项”在报告中如实体现。")


def main():
    ap = argparse.ArgumentParser(description="对照归档目录清点试卷材料")
    ap.add_argument("--dir", required=True, help="材料所在目录")
    ap.add_argument("--checklist", choices=["paper", "cbt"], default="paper", help="paper=纸质版，cbt=机考/考查版")
    ap.add_argument("--classes", type=int, help="班级数")
    ap.add_argument("--students", type=int, help="选课人数")
    ap.add_argument("--actual", type=int, help="实到人数（成绩单考试简况）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--json-out", help="同时写入 JSON 文件")
    args = ap.parse_args()

    res = audit(args.dir, args.checklist, args.classes, args.students, args.actual)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print_md(res)
    sys.exit(0)


if __name__ == "__main__":
    main()
