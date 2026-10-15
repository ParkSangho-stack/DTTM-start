# DTTM 연구 시작 가이드

> ⚠️ **전제**: 저장소에 DTTM의 정의가 없어, 현재는 **DTTM = Digital Twin 기반 교통/관리(Traffic·Transport Management) 연구**로 가정했습니다.
> 의미가 다르면 [`config/keywords.md`](config/keywords.md)의 검색 키워드만 고치면 매일 논문 검색이 그 주제로 바뀝니다.

## 1. 연구 단계별 할 일

| 단계 | 기간(권장) | 할 일 | 산출물 |
|---|---|---|---|
| ① 용어·범위 정의 | 1주 | DTTM의 정확한 정의, 대상 시스템(도로·철도·항만·공장 등), 연구 질문(RQ) 1~3개 확정 | 1쪽 연구 범위 문서 |
| ② 문헌 조사 | 3~4주 | 서베이 논문 2~3편 정독 → 핵심 논문 30~50편 체계적 문헌고찰(PRISMA) | 문헌 매트릭스(저자·방법·데이터·한계) |
| ③ 갭 분석 | 1~2주 | 기존 연구의 한계(실시간 동기화, 데이터 품질, 확장성, 검증 방법) 정리 → 기여점 도출 | 연구 갭 표 + 가설 |
| ④ 데이터·도구 준비 | 2~4주 | 공개 데이터(METR-LA, PEMS-BAY, 국가교통정보센터, 공공데이터포털) 확보, 시뮬레이터(SUMO, CARLA) 및 모델 프레임워크(PyTorch) 구축 | 재현 가능한 실험 환경 |
| ⑤ 베이스라인 재현 | 2~3주 | 대표 논문 1~2편의 결과 재현 | 베이스라인 성능표 |
| ⑥ 제안 기법 개발 | 6~10주 | 모델링 → 실시간 미러링 → 예측/최적화(제어) → 검증의 DT 파이프라인 구현 | 프로토타입 + 실험 결과 |
| ⑦ 평가·논문화 | 4~6주 | 정량지표(MAE/RMSE, 지연시간, 동기화 오차), 어블레이션, 사례연구 → 투고 | 학회/저널 원고 |

## 2. 먼저 읽을 논문 (시작점)

1. **Digital Twin AI: Opportunities and Challenges from LLMs to World Models** (2026, 서베이) — https://arxiv.org/abs/2601.01321
2. **Architecting Digital Twins for Intelligent Transportation Systems** (2025) — https://arxiv.org/abs/2502.17646
3. **AI-Powered CPS-Enabled Vulnerable-User-Aware Urban Transportation Digital Twin** — https://arxiv.org/abs/2501.10396
4. **Autonomous Traffic Signal Optimization Using Digital Twin and Agentic AI** (2026) — https://arxiv.org/abs/2604.27753
5. **Semantic Edge-Cloud Communication for Real-Time Urban Traffic Digital Twins** (2026.10) — https://arxiv.org/abs/2610.14187

## 3. 투고 후보

- 저널: *IEEE Transactions on Intelligent Transportation Systems*, *Transportation Research Part C*, *IEEE Internet of Things Journal*, 한국ITS학회논문지
- 학회: IEEE ITSC, IEEE IV, TRB Annual Meeting

## 4. 매일 논문 알림

- 매일 **한국시간 새벽 1시경** 자동으로 최신 관련 논문을 검색해 `reports/YYYY-MM-DD.md`로 저장하고 이 브랜치에 커밋합니다.
- 검색 주제는 [`config/keywords.md`](config/keywords.md)에서 바꿀 수 있습니다.
