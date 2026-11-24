# 2027년 원유 공급 과잉 논제 검증 노트

작성 기준일: 2026년 11월 24일 (KST)

이 저장소는 이란 전쟁 이후 원유 시장을 두고 나눈 일련의 질문과 분석을 정리한 것입니다. 핵심 질문은 "IEA·EIA가 말하는 2027년 원유 공급 과잉은 실제로 오는가, 그리고 줄어든 국가 비축유는 언제 다 채워지는가"입니다.

투자 권유가 아닌 판단 기준입니다. 추론에는 유형(연역·귀납·유추)을 표시했고, 확인하지 못한 수치는 그렇다고 적었습니다.

---

## 파일 구성

0. [index.html](index.html): 본문과 그래프 5개를 한 페이지로 보는 HTML (GitHub Pages 주소: https://gyucheol.github.io/newnew/ , Pages 활성화 필요). `python3 tools/build_html.py`로 다시 만듭니다.
1. [report.md](report.md): 전체 분석 본문 (결론 → 근거 → 반대 의견 → 시사점)
2. [data/china_implied_stockbuild.csv](data/china_implied_stockbuild.csv): 중국 원유 비축 매입 추정치, 2025년 1월~2026년 10월 (Reuters Clyde Russell 계산)
3. [data/brent_month_end.csv](data/brent_month_end.csv): Brent 월말 가격, 2025년 1월~2026년 11월 23일 (FMP)
4. [data/emergency_release_refill.csv](data/emergency_release_refill.csv): 나라별 비상 비축 방출량·채울 양·하루 재보충 속도
5. [data/refill_timeline.csv](data/refill_timeline.csv): 공급 경로별 중국 밖 재고 구멍이 메워지는 월별 경로
6. [model/refill_model.py](model/refill_model.py): 위 경로를 계산한 스크립트

---

## 한 줄 결론

1. 수급표상 2027년 과잉이 생길 확률은 약 75%, 정부 재보충과 중국 매입을 빼고도 가격을 누르는 과잉이 남을 확률은 약 60%로 봅니다 (주관적 판단).
2. 중국 밖 재고 4억 6,200만 배럴의 구멍은 IEA 경로로 2027년 4월 말, EIA 경로로 2027년 5월 중순, 2025년 수준 공급이면 2027년 6월~2028년 4월(중국 매입량에 따라)에 메워집니다.
3. 정부 비축 탱크는 더 늦게 찹니다. 미국 SPR은 2027년 9월~2028년 9월입니다.
4. 원유는 과잉으로 가도 석유제품(디젤)은 부족이 이어질 수 있어, 원유 과잉이 곧 물가 안정을 뜻하지는 않습니다.
