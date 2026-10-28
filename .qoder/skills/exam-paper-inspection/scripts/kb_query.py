#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按教师姓名 / 课程查询课程归属表与试卷归档清单。

用法：
    python kb_query.py --teacher 高平安
    python kb_query.py --teacher 高平安 --course Java --term 2025-2026-2
    python kb_query.py --teacher 高平安 --json
    python kb_query.py --list-teachers
    python kb_query.py --list-courses --teacher 周宇才

数据源：references/kb/ 下的 *课程归属表*.xlsx 与 *归档清单*.xlsx。
输出：默认人类可读摘要；--json 输出结构化结果供上层 Agent 使用。
"""

import argparse
import glob
import json
import os
import re
import sys
from difflib import get_close_matches

try:
    import openpyxl
except ImportError:
    sys.stderr.write("ERROR: 缺少 openpyxl，请先执行: python -m pip install openpyxl\n")
    sys.exit(2)

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_KB = os.path.join(SKILL_DIR, "references", "kb")

DEPT_MAP = [
    (("计算机科学与技术", "软件工程"), "计算机与科学系", "梁耀坤"),
    (("数据科学与大数据技术", "应用统计学"), "数据科学与大数据技术系", "徐鹏程"),
    (("人工智能",), "人工智能系", "吴振清"),
]


def norm(v):
    return re.sub(r"\s+", "", str(v if v is not None else ""))


def split_names(v):
    return [x for x in re.split(r"[,，、/;；\s]+", str(v or "")) if x.strip()]


def split_ids(v):
    return {x for x in re.split(r"[,，、/;；\s]+", str(v or "")) if x.strip()}


def term_from_filename(name):
    m = re.search(r"(\d{4})-(\d{4})-([12])学期", name)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else ""


def load_sheet(path):
    """返回 (rows, source_name)。rows 为 dict 列表，已按表头映射。"""
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb.active
    all_rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()

    header_idx = None
    headers = []
    for i, row in enumerate(all_rows[:6]):
        cells = [norm(c) for c in row]
        if "授课教师" in cells and ("课程名称" in cells or "课程编号" in cells):
            header_idx, headers = i, cells
            break
    if header_idx is None:
        return []

    def col(*keys, startswith=None):
        for j, h in enumerate(headers):
            if startswith and h.startswith(startswith):
                return j
            if h in keys:
                return j
        return None

    idx = {
        "archive_no": col("归档编号"),
        "course_code": col("课程编号", "课程代码"),
        "course_name": col("课程名称"),
        "major": col("专业名称"),
        "teacher_id": col("教师编号"),
        "teacher": col("授课教师"),
        "class_id": col("班级编号"),
        "class_name": col("班级名称"),
        "students": col("选课人数", "人数"),
        "campus": col("校区"),
        "course_attr": col("课程属性"),
        "course_nature": col("课程性质"),
        "exam_method": col("考试方式", "考核方式"),
        "exam_type": col("考试分类"),
        "cbt": col(startswith="是否申请融智"),
        "archived": col(startswith="是否归档"),
        "note": col("备注"),
        "dept": col("开课单位"),
    }

    out = []
    for row in all_rows[header_idx + 1:]:
        if not any(norm(c) for c in row):
            continue
        rec = {}
        for key, j in idx.items():
            rec[key] = row[j] if j is not None and j < len(row) else None
        if not norm(rec.get("teacher")) and not norm(rec.get("course_name")):
            continue
        out.append(rec)
    return out


def load_kb(kb_dir):
    ownership, archive = [], []
    files = sorted(glob.glob(os.path.join(kb_dir, "*.xlsx")))
    for path in files:
        name = os.path.basename(path)
        if "登记表" in name or "互查" in name or name.startswith("~$"):
            continue
        term = term_from_filename(name)
        recs = load_sheet(path)
        for r in recs:
            r["_term"] = term
            r["_source"] = name
        if "课程归属表" in name:
            ownership.extend(recs)
        elif "归档清单" in name:
            archive.extend(recs)
    return ownership, archive, files


def map_course_type(course_name, nature, exam_method):
    name = norm(course_name)
    nat = norm(nature)
    if "论文" in name and "分析" not in name:
        return "课程论文", "课程名称含“论文”"
    if any(k in name for k in ("实验", "实践", "实训", "课程设计")):
        return "实验（实践）课", "课程名称含实验/实践类字样"
    if "必修" in nat:
        return "必修课", f"课程性质为“{nature}”"
    if "选修" in nat:
        return "选修课", f"课程性质为“{nature}”"
    if norm(exam_method) == "考查":
        return "选修课", "考核方式为考查且性质未明，暂按选修课归类，需教师确认"
    return "必修课", "课程性质未明，暂按必修课归类，需教师确认"


def map_department(major):
    for keys, dept, director in DEPT_MAP:
        if any(k in norm(major) for k in keys):
            return dept, director
    return "待确认", ""


def num(v):
    try:
        return int(float(str(v).strip()))
    except (TypeError, ValueError):
        return 0


def has_num(v):
    return str(v).strip() not in ("", "None")


def clean_class_name(v):
    s = str(v or "").replace("\r", "").replace("\n", "、").replace("/", "、")
    return re.sub(r"[、\s]+", "、", s).strip("、")


def pick_class_rows(recs):
    """归属表中同时存在合班行与单班行，需去重，避免人数翻倍。

    优先使用单班行（每班独立成绩单/答题册）；未被单班行覆盖的班级，
    再用覆盖它的最小合班行，并按残差计人数。
    返回 [(记录, 覆盖的班级ID集合, 人数)]。
    """
    ids_of = {id(r): split_ids(r.get("class_id")) for r in recs}
    all_ids = set().union(*ids_of.values()) if recs else set()

    singles = {}
    for r in recs:
        s = ids_of[id(r)]
        if len(s) == 1:
            cid = next(iter(s))
            # 同一班级若有多条，取人数最大的一条，避免 0 人记录
            if cid not in singles or num(r.get("students")) > num(singles[cid].get("students")):
                singles[cid] = r

    if not all_ids:
        seen, out = set(), []
        for r in recs:
            key = norm(r.get("class_name")) or norm(r.get("class_id"))
            if key in seen:
                continue
            seen.add(key)
            out.append((r, set(), num(r.get("students")), has_num(r.get("students"))))
        return out

    if not singles:
        # 只有合班行：原样保留，按班级集合/名称去重，不拆人数
        seen, out = set(), []
        for r in recs:
            key = tuple(sorted(ids_of[id(r)])) or norm(r.get("class_name"))
            if key in seen:
                continue
            seen.add(key)
            out.append((r, ids_of[id(r)], num(r.get("students")), has_num(r.get("students"))))
        return out

    out = []
    covered = set()
    for cid in sorted(all_ids):
        if cid in singles:
            r = singles[cid]
            out.append((r, {cid}, num(r.get("students")), has_num(r.get("students"))))
            covered.add(cid)

    # 未被单班行覆盖的班级：找包含它们的最小合班行。
    # 若与已列班级无重叠，直接按原人数整行保留；若有重叠，才扣除已知人数取残差。
    missing = all_ids - covered
    used = set()
    while missing:
        cands = [r for r in recs if ids_of[id(r)] and len(ids_of[id(r)]) > 1
                 and (ids_of[id(r)] & missing) and id(r) not in used]
        if not cands:
            break
        r = min(cands, key=lambda x: (len(ids_of[id(x)]), -num(x.get("students"))))
        s = ids_of[id(r)]
        target = s & missing
        overlap = s & covered
        if not overlap:
            out.append((r, target, num(r.get("students")), has_num(r.get("students"))))
        else:
            known = sum(c[2] for c in out if c[1] and c[1] <= overlap)
            residual = max(num(r.get("students")) - known, 0)
            out.append((r, target, residual, True))
        used.add(id(r))
        missing -= target
        covered |= target

    return out


def archive_match(rec_row, ids, term, code, cname, tname, archive):
    """在归档清单中匹配条目，返回 (匹配列表, 提示)。

    归档清单与课程归属表偶尔存在教师姓名、课程名称/编号不一致，
    因此按 严格 → 课程编号 → 课程名称 → 教师+班级+人数 四级容错匹配，
    并在提示中说明不一致点，供报告与教师核对。
    """
    pool = [a for a in archive if a["_term"] == term]
    if not pool:
        return [], ""

    def class_hit(a):
        aid = split_ids(a.get("class_id"))
        aname = norm(a.get("class_name"))
        if ids and aid:
            return bool(ids & aid) or ids <= aid or aid <= ids
        return bool(aname) and aname == norm(rec_row.get("class_name"))

    def pick(cands, how, note=""):
        if not cands:
            return [], ""
        scored = []
        for a in cands:
            aid = split_ids(a.get("class_id"))
            diff = len(ids ^ aid) if (ids and aid) else 0
            scored.append((diff, a))
        best = min(s[0] for s in scored)
        return [(a, how) for d, a in scored if d == best], note

    # 1) 严格：课程编号 + 课程名称 + 教师 + 班级
    hits = [a for a in pool
            if (not code or norm(a.get("course_code")) == code)
            and norm(a.get("course_name")) == cname
            and (not tname or tname in [norm(n) for n in split_names(a.get("teacher"))])
            and class_hit(a)]
    if hits:
        return pick(hits, "class")

    # 2) 课程编号 + 班级，忽略教师姓名
    hits = [a for a in pool
            if code and norm(a.get("course_code")) == code and class_hit(a)]
    if hits:
        names = sorted({str(a.get("teacher") or "").strip() for a in hits if a.get("teacher")})
        note = f"《试卷归档清单》中该课程的授课教师为“{'、'.join(names)}”，与归属表不一致，已按课程编号+班级匹配，请人工核对。" if names else ""
        return pick(hits, "code+class", note)

    # 3) 课程名称 + 班级，忽略课程编号
    hits = [a for a in pool
            if norm(a.get("course_name")) == cname and class_hit(a)]
    if hits:
        codes = sorted({str(a.get("course_code") or "").strip() for a in hits if a.get("course_code")})
        note = f"《试卷归档清单》中该课程编号为“{'、'.join(codes)}”，与归属表不一致，已按课程名称+班级匹配，请人工核对。"
        return pick(hits, "name+class", note)

    # 4) 教师 + 班级 + 人数一致，且课程名称相近
    from difflib import SequenceMatcher
    cands = []
    for a in pool:
        if tname and tname not in [norm(n) for n in split_names(a.get("teacher"))]:
            continue
        if not class_hit(a):
            continue
        sim = SequenceMatcher(None, norm(a.get("course_name")), cname).ratio()
        same_n = has_num(a.get("students")) and num(a.get("students")) == num(rec_row.get("students"))
        if sim >= 0.5 or same_n:
            cands.append(a)
    if cands:
        names = sorted({str(a.get("course_name") or "").strip() for a in cands})
        note = f"归档清单中的课程名称为“{'、'.join(names)}”，与归属表“{rec_row.get('course_name')}”不一致，已按教师+班级+人数匹配，请人工核对课程对应关系。"
        return pick(cands, "teacher+class+similar", note)

    return [], ""


def storage_of(rec, archive_nos):
    archived = norm(rec.get("archived"))
    method = norm(rec.get("exam_method"))
    # 考查课无论是否标注归档，均以电子版材料自查
    if method == "考查":
        return "电子版材料（教师自查后交教研室与学院教学秘书备份）"
    if archived == "是":
        suffix = f"（归档编号：{'、'.join(archive_nos)}）" if archive_nos else "（尚未在归档清单中匹配到归档编号，需核对）"
        return "清远校区行政楼202试卷档案室" + suffix
    if archived == "否":
        return "敏学楼514"
    return "待确认（课程归属表未标注是否归档）"


def query(teacher=None, teacher_id=None, course=None, term=None, kb_dir=DEFAULT_KB):
    ownership, archive, files = load_kb(kb_dir)
    if not ownership:
        raise SystemExit(f"未在 {kb_dir} 找到可解析的课程归属表，请检查文件。")

    tname = norm(teacher)
    tid = norm(teacher_id)
    ckw = norm(course)

    def teacher_hit(rec):
        if tid and tid == norm(rec.get("teacher_id")):
            return True
        if not tname:
            return True
        names = [norm(n) for n in split_names(rec.get("teacher"))]
        return tname in names or any(tname == n for n in names)

    rows = [r for r in ownership if teacher_hit(r)]
    if ckw:
        rows = [r for r in rows if ckw in norm(r.get("course_code")) or ckw in norm(r.get("course_name"))]
    if term:
        rows = [r for r in rows if norm(r.get("_term")).startswith(norm(term)) or norm(term) in norm(r.get("_term"))]

    # 按 学期 + 课程编号 + 课程名称 聚合
    groups = {}
    for r in rows:
        key = (r["_term"], norm(r.get("course_code")), norm(r.get("course_name")))
        groups.setdefault(key, []).append(r)

    matches = []
    for (tm, code, cname), recs in sorted(groups.items(), key=lambda x: (x[0][0], x[0][2])):
        base = recs[0]
        classes, archive_records, warnings = [], [], []
        seen_archive = set()

        unknown_students = False
        for r, ids, students, known in pick_class_rows(recs):
            unknown_students = unknown_students or not known
            row_archives = []
            is_kaocha = norm(base.get("exam_method")) == "考查"
            ahits, anote = ([], "") if is_kaocha else archive_match(r, ids, tm, code, cname, tname, archive)
            if anote and anote not in warnings:
                warnings.append(anote)
            for a, how in ahits:
                arc = {
                    "archive_no": str(a.get("archive_no") or "").strip(),
                    "class_name": str(a.get("class_name") or "").strip(),
                    "class_id": str(a.get("class_id") or "").strip(),
                    "students": a.get("students"),
                    "source": a["_source"],
                    "matched_by": how,
                }
                row_archives.append(arc["archive_no"])
                if arc["archive_no"] and arc["archive_no"] not in seen_archive:
                    seen_archive.add(arc["archive_no"])
                    archive_records.append(arc)
            classes.append({
                "class_id": ",".join(sorted(ids)),
                "class_name": clean_class_name(r.get("class_name")),
                "students": students,
                "students_known": known,
                "teachers": str(r.get("teacher") or "").strip(),
                "teacher_id": str(r.get("teacher_id") or "").strip(),
                "campus": str(r.get("campus") or "").strip(),
                "archive_hits": row_archives,
            })

        archive_nos = [x["archive_no"] for x in archive_records if x["archive_no"]]
        total_students = sum(c["students"] for c in classes)

        archived = norm(base.get("archived"))
        if unknown_students:
            warnings.append("部分班级在《课程归属表》中未标注选课人数，人数需教师确认或从成绩单核实。")
        if norm(base.get("exam_method")) == "考查":
            if archived == "是":
                warnings.append("归属表标注“已归档”，但按方案考查课程以电子版材料自查，归档编号不参与材料清点；如需调阅纸质档案请人工核对。")
        elif archived == "是" and not archive_nos:
            warnings.append("课程归属表标注为已归档，但未在归档清单中匹配到归档编号，请人工核对班级与归档记录。")
        if archived == "否" and norm(base.get("exam_method")) == "考试":
            warnings.append("未归档三校区试卷库，按方案到敏学楼514检查纸质材料。")
        all_teachers = sorted({n for r in recs for n in split_names(r.get("teacher"))})
        if len(all_teachers) > 1:
            warnings.append("该课程记录含多位授课教师（" + "、".join(all_teachers) + "），请确认本人所授班级。")

        dept, director = map_department(base.get("major"))
        ctype, ctype_note = map_course_type(base.get("course_name"), base.get("course_nature"), base.get("exam_method"))
        is_cbt = norm(base.get("cbt")) == "是"
        checklist = "cbt" if (is_cbt or norm(base.get("exam_method")) == "考查") else "paper"
        checklist_reason = (
            "课程申请了融智机考" if is_cbt else
            "考核方式为考查，按机考版目录检查电子材料" if norm(base.get("exam_method")) == "考查" else
            "笔试类课程，按纸质版目录检查"
        )

        matches.append({
            "term": tm,
            "course_code": str(base.get("course_code") or "").strip(),
            "course_name": str(base.get("course_name") or "").strip(),
            "course_attribute": str(base.get("course_attr") or "").strip(),
            "course_nature": str(base.get("course_nature") or "").strip(),
            "report_course_type": ctype,
            "course_type_note": ctype_note,
            "exam_method": str(base.get("exam_method") or "").strip(),
            "exam_type": str(base.get("exam_type") or "").strip(),
            "cbt": is_cbt,
            "archived": archived,
            "campus": str(base.get("campus") or "").strip(),
            "major": str(base.get("major") or "").strip(),
            "department": dept,
            "director": director,
            "classes": classes,
            "class_count": len(classes),
            "total_students": total_students,
            "co_teachers": all_teachers,
            "archive_records": archive_records,
            "archive_nos": archive_nos,
            "storage": storage_of(base, archive_nos),
            "checklist": checklist,
            "checklist_reason": checklist_reason,
            "notes": [str(base.get("note") or "").strip()] if norm(base.get("note")) else [],
            "warnings": warnings,
            "source_files": sorted({r["_source"] for r in recs} | {x["source"] for x in archive_records}),
        })

    result = {
        "query": {"teacher": teacher, "teacher_id": teacher_id, "course": course, "term": term},
        "kb_dir": kb_dir,
        "kb_files": [os.path.basename(f) for f in files],
        "matches": matches,
    }
    if not matches:
        all_names = sorted({n for r in ownership for n in split_names(r.get("teacher"))})
        close = get_close_matches(teacher or "", all_names, n=6, cutoff=0.55)
        result["suggestions"] = close
        result["all_teachers_count"] = len(all_names)
    return result


def fmt_classes(m):
    parts = []
    for c in m["classes"]:
        name = c["class_name"] or c["class_id"] or "未标注班级"
        parts.append(name + (f"（{c['students']}人）" if c.get("students_known") else "（人数未标注）"))
    return "；".join(parts)


def print_human(res):
    if not res["matches"]:
        print(f"未查询到教师“{res['query'].get('teacher') or ''}”的课程记录。")
        if res.get("suggestions"):
            print("相近姓名：" + "、".join(res["suggestions"]))
        print("请核对姓名是否与《课程归属表》一致，或补充课程名称重新查询。")
        return
    print(f"共命中 {len(res['matches'])} 门课程记录（按学期-课程聚合）：\n")
    for i, m in enumerate(res["matches"], 1):
        print(f"[{i}] {m['term']}学期 | {m['course_name']}（{m['course_code']}）")
        print(f"    课程性质：{m['course_nature']}（{m['course_attribute']}） → 报告课程类型：{m['report_course_type']}")
        print(f"    考核方式：{m['exam_method']} / {m['exam_type']}" + ("（融智机考）" if m["cbt"] else ""))
        print(f"    专业：{m['major']} | 校区：{m['campus']} | 教研室：{m['department']}" + (f"（主任：{m['director']}）" if m["director"] else ""))
        print(f"    班级：{fmt_classes(m)}" + (f" | 合计 {m['total_students']} 人" if m["total_students"] else ""))
        print(f"    归档：{m['archived'] or '未标注'} | 归档编号：{'、'.join(m['archive_nos']) or '未匹配到'}")
        print(f"    材料存放：{m['storage']}")
        print(f"    检查清单：{m['checklist']}（{m['checklist_reason']}）")
        if m["notes"]:
            print("    备注：" + "；".join(m["notes"]))
        for w in m["warnings"]:
            print(f"    ⚠ {w}")
        print()
    if len(res["matches"]) > 1:
        print("提示：命中多门课程或多学期记录，请让教师确认本次检查的具体课程与学期，再继续。")


def main():
    ap = argparse.ArgumentParser(description="查询课程归属表与试卷归档清单")
    ap.add_argument("--teacher", help="教师姓名，如 高平安")
    ap.add_argument("--teacher-id", help="教师编号（可选）")
    ap.add_argument("--course", help="课程名称或课程编号关键字（可选）")
    ap.add_argument("--term", help="学期，如 2025-2026-2（可选）")
    ap.add_argument("--kb", default=DEFAULT_KB, help="知识库目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--list-teachers", action="store_true", help="列出知识库中的全部教师姓名")
    ap.add_argument("--list-courses", action="store_true", help="列出某教师的全部课程")
    args = ap.parse_args()

    if args.list_teachers:
        ownership, _, _ = load_kb(args.kb)
        names = sorted({n for r in ownership for n in split_names(r.get("teacher"))})
        print(f"共 {len(names)} 位教师：")
        print("、".join(names))
        return

    if not args.teacher and not args.teacher_id:
        ap.error("请提供 --teacher 或 --teacher-id；如需查看全部教师，使用 --list-teachers")

    res = query(args.teacher, args.teacher_id, args.course, args.term, args.kb)
    if args.list_courses:
        if not res["matches"]:
            print("未找到该教师的课程。")
            return
        for m in res["matches"]:
            print(f"{m['term']} | {m['course_name']} | {m['course_code']} | {m['report_course_type']} | {m['exam_method']}")
        return
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2, default=str))
    else:
        print_human(res)


if __name__ == "__main__":
    main()
