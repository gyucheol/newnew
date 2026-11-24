"""report.md + data/*.csv -> index.html (self-contained, no external libs)."""
import csv, json, pathlib, re
import markdown

root = pathlib.Path(__file__).resolve().parent.parent
md = (root / "report.md").read_text(encoding="utf-8")

def rows(name):
    with open(root / "data" / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))

china = rows("china_implied_stockbuild.csv")
brent = rows("brent_month_end.csv")
rel = [r for r in rows("emergency_release_refill.csv") if r["country"] not in ("China (not IEA)",)]
tl = rows("refill_timeline.csv")

data = {
    "china": {"x": [r["month"].replace("20", "", 1) for r in china], "y": [float(r["implied_stockbuild_kbd"]) for r in china]},
    "brent": {"x": [r["date"][2:7].replace("-", ".") for r in brent], "y": [float(r["brent_usd"]) for r in brent]},
    "rel": {"x": ["미국 SPR", "유럽", "일본 국가비축", "한국", "IEA 합계", "세계 관측재고"],
            "s": [["방출(2월까지 예정 포함)", [float(r["released_mb"]) for r in rel]],
                  ["계약·목표상 우선 채울 양", [float(r["priority_refill_mb"]) for r in rel]]]},
    "speed": {"x": ["미국(설비)", "유럽(가정)", "일본", "한국(상환)", "IEA 전체(Kpler)"],
              "lo": [440, 170, 120, 7, 506], "hi": [672, 330, 200, 120, 664]},
    "tl": {"x": [r["month"] for r in tl],
           "s": [[k, [float(r[k]) for r in tl]] for k in tl[0] if k != "month"]},
}
names = {"IEA_china50": "IEA 경로(중국 50만)", "EIA_china50": "EIA 경로(중국 50만)",
         "2025supply_china0": "2025년 수준·중국 관망", "2025supply_china50": "2025년 수준·중국 50만",
         "2025supply_china110": "2025년 수준·중국 110만"}
data["tl"]["s"] = [[names[k], v] for k, v in data["tl"]["s"]]

charts = {
    "## 4. 2025년 과잉은 어디로 갔나": [
        ("c-china", "그래프 1. 중국 원유 비축 매입 추정 (수입+생산−정제, 천 배럴/일)",
         "의미: 중국은 유가가 쌀 때(2025년 4월, 11~12월) 크게 샀고, 전쟁 중에는 2025년 매입분의 약 18%만 꺼냈습니다. 전망: Brent가 60~70달러대로 내려가면 막대가 다시 크게 플러스로 돌아설 가능성이 높습니다(유추). 출처: Reuters Clyde Russell 계산."),
        ("c-brent", "그래프 2. Brent 월말 가격 (달러/배럴)",
         "의미: 2025년 중국의 대량 비축에도 Brent는 약 20% 내렸습니다. 2026년 10월 정점 뒤 11월에 89달러대로 내려왔습니다. 출처: FMP(BZUSD)."),
    ],
    "## 5. 비상 비축 방출과 재보충": [
        ("c-rel", "그래프 3. 비상 비축 방출량과 우선 채울 양 (백만 배럴)",
         "의미: IEA 회원국 방출은 2월까지 약 4억 2,000만 배럴, 세계 관측 재고는 4억 6,200만 배럴 비어 있습니다. 일본은 90일 목표까지 약 1,600만 배럴만 필요합니다(연역)."),
        ("c-speed", "그래프 4. 현실적인 하루 재보충 속도 (천 배럴/일, 하한~상한)",
         "의미: 미국이 재보충 수요의 중심입니다. 한국의 예산 매입은 하루 1만 배럴에도 못 미칩니다. 전망: 합산 평균 하루 60만~80만 배럴, 빠른 경우에만 약 120만 배럴입니다."),
    ],
    "## 6. 언제 다 채워지나": [
        ("c-tl", "그래프 5. 중국 밖 재고 구멍 중 남은 양 (백만 배럴, 월말)",
         "의미: IEA 경로는 2027년 4월 말, EIA 경로는 5월 중순, 2025년 수준 공급은 2027년 6월~2028년 4월에 0이 됩니다. 전망: 정부 탱크는 이보다 늦게 차므로 그사이 민간 재고가 넘쳐 콘탱고 조건이 됩니다(추론)."),
    ],
}

html_body = markdown.markdown(md, extensions=["extra", "sane_lists"])
html_body = re.sub(r'(https?://[^\s<]+)(?![^<]*</a>)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', html_body)
for head, items in charts.items():
    title = head.lstrip("# ").strip()
    m = re.search(r"<h2>" + re.escape(title) + r".*?</h2>", html_body)
    blocks = "".join(f'<figure class="card"><figcaption>{t}</figcaption><div class="chart" id="{i}"></div><p class="note">{n}</p></figure>' for i, t, n in items)
    html_body = html_body[:m.end()] + blocks + html_body[m.end():]

tpl = (root / "tools" / "template.html").read_text(encoding="utf-8")
out = tpl.replace("{{BODY}}", html_body).replace("{{DATA}}", json.dumps(data, ensure_ascii=False))
(root / "index.html").write_text(out, encoding="utf-8")
print("ok", len(out))
