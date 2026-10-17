"""item_bank.csv를 읽어 검사하고 문항 설계표(마크다운)를 출력합니다.

사용법:
    python3 item_bank/render.py            # 검사 + 설계표 출력
    python3 item_bank/render.py --check    # 검사만
"""
import csv
import sys
from collections import Counter
from pathlib import Path

BANK = Path(__file__).with_name("item_bank.csv")

SCALES = {
    "L7": "7점 동의(1 전혀 그렇지 않다 ~ 7 매우 그렇다)",
    "YN": "예/아니오",
    "YN+day": "예/아니오 → 예: 요일",
    "YN3": "예/아니오/이전에 이미 함",
    "YN3+day": "예/아니오/이전에 이미 함 → 예: 요일+한 줄",
    "YN+text": "예/아니오 → 예: 이유 한 줄",
    "PCT5": "0%/1~25%/26~50%/51~75%/76~100%",
}
RECALL = {"7d": "지난 7일", "trait": "평소(성향)"}
SCHEDULE = {"weekly": "매주", "4-weekly": "0·4·8·12주", "0/4/8/12w": "0·4·8·12주", "—": "미사용"}
STATUSES = {"candidate", "active", "hold", "retired"}
BLOCKS = {"core": "공통", "student": "대학생", "worker": "직장인",
          "event": "공통(사건)", "cost": "공통(비용)", "inertia": "공통(관성)"}
PHASE_ORDER = ["S0", "S1", "S2", "S3", "E1", "S4", "COST"]


def load():
    with BANK.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(rows):
    errors = []
    ids = Counter(r["item_id"] for r in rows)
    errors += [f"중복 item_id: {i}" for i, n in ids.items() if n > 1]
    for r in rows:
        if r["status"] not in STATUSES:
            errors.append(f"{r['item_id']}: 알 수 없는 status {r['status']}")
        if r["scale"] not in SCALES:
            errors.append(f"{r['item_id']}: 알 수 없는 scale {r['scale']}")
        if r["block"] in ("core", "event", "cost", "inertia") and not (r["text_student"] and r["text_worker"]):
            errors.append(f"{r['item_id']}: 공통 문항인데 두 집단 문구가 모두 있지 않음")
        if r["block"] == "student" and r["text_worker"]:
            errors.append(f"{r['item_id']}: 대학생 맥락 문항에 직장인 문구가 있음")
        if r["block"] == "worker" and r["text_student"]:
            errors.append(f"{r['item_id']}: 직장인 맥락 문항에 대학생 문구가 있음")
    return errors


def text_cell(r):
    s, w = r["text_student"], r["text_worker"]
    if s and w and s != w:
        return f"[대] {s}<br>[직] {w}"
    return s or w


def table(rows, status=("candidate",)):
    out = []
    for phase in PHASE_ORDER:
        sel = [r for r in rows if r["phase"] == phase and r["status"] in status]
        if not sel:
            continue
        out.append(f"\n#### {phase}\n")
        out.append("| 문항 ID | 구분 | 측정 개념 | 문항 내용(개발 중인 예비문항) | 응답척도 | 회상기간 | 실시 주기 | 개발 근거 | 다른 국면과 중복 가능성 |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        for r in sel:
            out.append("| " + " | ".join([
                r["item_id"], BLOCKS[r["block"]], r["concept"], text_cell(r),
                r["scale"], RECALL[r["recall"]], SCHEDULE[r["schedule"]],
                r["basis"], r["overlap_risk"],
            ]) + " |")
    return "\n".join(out)


def summary(rows):
    c = Counter((r["phase"], r["block"], r["status"]) for r in rows)
    lines = ["| 국면 | 공통 | 대학생 맥락 | 직장인 맥락 | 대학생 응답 수 | 직장인 응답 수 | 보류 |", "|---|---|---|---|---|---|---|"]
    for p in ["S0", "S1", "S2", "S3", "S4"]:
        core, stu, wrk = c[(p, "core", "candidate")], c[(p, "student", "candidate")], c[(p, "worker", "candidate")]
        hold = sum(v for (ph, _, st), v in c.items() if ph == p and st == "hold")
        lines.append(f"| {p} | {core} | {stu} | {wrk} | {core + stu} | {core + wrk} | {hold} |")
    return "\n".join(lines)


if __name__ == "__main__":
    rows = load()
    errs = check(rows)
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    if "--check" in sys.argv:
        print(f"OK: {len(rows)}개 문항")
        sys.exit(0)
    print(summary(rows))
    print(table(rows))
