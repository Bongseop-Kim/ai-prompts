---
title: 리팩토링 점검
tags: [refactor]
version: 2
---

당신은 AI 시대의 코드 리팩토링 전문가입니다.
**지금 열려 있는 프로젝트 코드베이스를 직접 분석**하여 아래 지시에 따라 리팩토링을 수행하세요.

---

## 목표

아래 타입 중 해당하는 항목을 선택하거나 직접 기술하세요.
**파일을 먼저 탐색한 후, 실제로 발견된 문제 타입만 체크하세요.**

- [ ] rename — 의도를 드러내는 네이밍으로 변경
- [ ] extract function / extract component — 단일 책임 원칙 적용
- [ ] smell 제거 — Long Method / Magic Number / Dead Code / God Object
- [ ] duplicate 제거 — 중복 로직을 공통 함수/훅으로 추출
- [ ] conditional 단순화 — 중첩 if → early return, switch → 전략 패턴
- [ ] import 정리 — 절대 경로(@/) 통일, 순환 참조 제거
- [ ] type 강화 — any 제거, 좁은 타입으로 교체

---

## 제약

- **동작 변경 금지**: 기존 단위 테스트 및 통합 테스트 모두 통과 유지
- **공개 API 변경 금지**: export된 함수/컴포넌트 시그니처 유지
- 파일 범위: [대상 파일 또는 디렉터리]
- 적용 제외: [\_\_tests\_\_/, \*.spec.ts, \*.test.tsx 등]

---

## 기준 예시 (one-shot)

팀 컨벤션에 맞는 실제 코드 패턴을 아래에 제공합니다.
에이전트가 코드에서 스스로 추론할 수 없는 비표준 규칙을 우선 기술하세요.

**Before:**
```ts
// [나쁜 예 — 실제 코드베이스에서 발췌]
```

**After:**
```ts
// [좋은 예 — 원하는 패턴]
```

---

## 검증

리팩토링 완료 후 **반드시 아래 순서로 실행**하고 결과를 보고하세요.
각 단계 실패 시 수정 후 재실행. 수정 불가한 경우 이유를 명시하세요.

1. `npx tsc --noEmit`
2. `npx eslint src/ --max-warnings 0`
3. `npx vitest run` (또는 `jest --ci`)

---

## 출력

리팩토링 결과와 변경 이유 한 줄 요약을 아래 형식으로 출력하세요.

### 변경 파일 목록

| 파일 | 변경 타입 | 변경 이유 (한 줄) |
|------|-----------|-------------------|
| src/components/X.tsx | smell 제거 | Magic Number → Named Constant |

### 검증 결과

| 검사 | 결과 | 비고 |
|------|------|------|
| tsc --noEmit | ✅ 0 errors | — |
| eslint | ✅ 0 warnings | — |
| vitest | ✅ 24/24 pass | — |

### eslint-disable 사용 여부

- 새로 추가된 eslint-disable 주석: X개 (0개가 이상적)
- 추가한 경우 각 위치와 이유를 명시

---

## 출처

**[1]** Abbas Sabra, Olivier Schmitt, Joseph Tyler.
*Assessing the Quality and Security of AI-Generated Code: A Quantitative Analysis.*
arXiv:2508.14727 [cs.SE], 20 Aug 2025. Sonar 소속 연구진. Java 코드 4,442건 대상.
🔗 https://arxiv.org/abs/2508.14727

**[2]** Ziyang Li, Saikat Dutta, Mayur Naik.
*IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities.*
arXiv:2405.17238 [cs.CR]. ICLR 2025. Cornell University & University of Pennsylvania.
🔗 https://arxiv.org/abs/2405.17238

**[3-A]** GitClear.
*AI Copilot Code Quality 2025: 4x More Code Cloning.*
산업 보고서, 2025. 동료 심사 없음. 관찰 데이터.
🔗 https://www.gitclear.com/ai_assistant_code_quality_2025_research

**[3-B]** Feiyang Xu et al.
*AI-Assisted Programming Decreases the Productivity of Experienced Developers.*
arXiv:2510.10165 [econ.GN]. v3 Jan 2026.
🔗 https://arxiv.org/abs/2510.10165

**[4]** Thibault Gloaguen et al. (ETH Zurich).
*Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*
arXiv:2602.11988 [cs.SE]. ICML 2025.
🔗 https://arxiv.org/abs/2602.11988

**[5]** CodeRabbit.
*State of AI vs Human Code Generation.*
산업 보고서, Dec 2025. 동료 심사 없음. CodeRabbit 자사 보고서.
🔗 https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
