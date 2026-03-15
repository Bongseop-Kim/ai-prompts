---
title: Vitest 도입 수준 감사 프롬프트
tags: [vitest, testing, code-quality]
version: 1
---

# Vitest 도입 수준 감사 프롬프트

> Claude Code에서 실행하는 React 프로젝트 Vitest 도입 수준 자동 감사 프롬프트.
> 점수(100점 만점) + 개선 항목 리스트를 출력한다.

---

## 실행 순서

1. `vitest.config.ts` 또는 `vite.config.ts` 내 `test` 블록을 읽어라
2. `package.json`의 `dependencies`, `scripts`를 읽어라
3. `src/**/*.test.{ts,tsx}` 또는 `src/**/*.spec.{ts,tsx}` 파일 전체를 탐색해라
4. `setupTests.ts` 또는 `setupFiles`로 지정된 파일을 읽어라
5. `coverage/coverage-summary.json`이 존재하면 읽어라. 없으면 ⑤ 커버리지 기준점 달성 항목은 "측정 불가 — 0점"으로 처리하고 그 이유를 결과에 명시해라
6. 파일이 없는 항목은 "미존재"로 표시하고 해당 항목 점수는 0점으로 처리해라
7. 아래 ①~⑤ 기준을 적용해 채점하고, 정해진 형식으로 결과를 출력해라
8. 파일을 수정하지 말 것

---

## 공통 감점 규칙

> **모든 항목에 적용**: 감점 적용 후 해당 항목 점수는 최소 0점으로 처리한다. 음수가 되지 않는다.

---

## 평가 기준 (총 100점)

### ① 설정 & 구성 (20점)

`vitest.config.ts` 또는 `vite.config.ts`의 `test` 블록을 검토한다.

| 항목 | 점수 | 합격 기준 |
|------|------|-----------|
| environment | 5점 | `jsdom` 또는 `happy-dom` 설정 여부 |
| setupFiles | 5점 | `@testing-library/jest-dom` extend 포함 여부 |
| coverage.provider | 4점 | `v8` 또는 `istanbul` 명시 여부 |
| coverage.thresholds | 6점 | lines/branches/functions/statements 모두 80 이상 설정 여부 |
| transform / plugin | 0점 (감점 항목) | `@vitejs/plugin-react` 또는 `transform` 설정 미존재 시 -3점 (React+TS 환경에서 테스트 실행 불가 신호) |

감점 조건:
- `globals: true` 미설정 시 -1점 (describe/it을 매 파일 import해야 해서 불편). 단, 팀 컨벤션상 명시적 import를 선호하는 경우 이 감점을 제외할 수 있다.
- include/exclude 패턴 미설정 시 -1점

> 근거: jsdom 없이는 React 컴포넌트 렌더링 자체가 불가능하다. coverage threshold를 설정하지 않으면 CI가 커버리지 하락을 감지하지 못한다. `@vitejs/plugin-react` 미설정 시 JSX 변환이 되지 않아 테스트 파일 자체가 parse 에러를 낸다. [^1]

---

### ② 테스트 구조 (20점)

테스트 파일 전체를 읽어 구조를 평가한다.

| 항목 | 점수 | 합격 기준 |
|------|------|-----------|
| describe/it 계층 | 5점 | describe로 기능/컴포넌트 단위 그룹화, it은 단일 동작 검증 |
| 테스트 네이밍 | 5점 | "동작을 설명하는 문장" 형식 (예: "버튼 클릭 시 모달이 열린다") |
| 테스트 격리 | 5점 | beforeEach/afterEach에서 상태 초기화, 전역 오염 없음 |
| 테스트 분포 | 5점 | Unit + Integration 테스트가 모두 존재하고, E2E만 있거나 단위 테스트만 있지 않음. 소스 파일 대비 테스트 파일 비율이 현저히 낮은 경우(예: 테스트 파일 1개 미만/소스 파일 10개) 최대 -3점 감점 |

감점 조건:
- 테스트 파일이 전혀 없으면 이 항목 전체 0점
- it 설명이 "test 1", "should work" 수준이면 네이밍 항목 0점

> 근거: Testing Trophy 구조(Static → Unit → Integration → E2E)에 따르면 Integration 테스트 비중이 가장 높아야 ROI가 좋다. describe 계층 없이 평탄한 구조는 테스트 의도를 읽기 어렵게 만든다. [^2]

---

### ③ React 테스트 패턴 (25점)

React Testing Library 사용 방식을 평가한다.

| 항목 | 점수 | 합격 기준 |
|------|------|-----------|
| 쿼리 우선순위 준수 | 8점 | getByRole > getByLabelText > getByText 순서 준수. getByTestId 남용 없음 |
| userEvent 사용 | 7점 | 클릭·입력 등 사용자 인터랙션에 `userEvent.setup()` 사용 (fireEvent 단독 사용 지양) |
| 비동기 처리 | 5점 | `waitFor`, `findBy*` 쿼리로 비동기 상태 검증 |
| 커스텀 훅 테스트 | 5점 | `renderHook` 또는 래퍼 컴포넌트로 훅 단독 테스트 존재 여부 |

감점 조건 (각 항목 최소 0점 보장):
- 구현 세부사항 테스트 발견 시 (내부 state 직접 검증, 클래스명 단독 assertion) -2점/건, 최대 -6점
- `screen` 대신 `container.querySelector` 남용 시 -2점

> 근거: "The more your tests resemble the way your software is used, the more confidence they can give you." — RTL Guiding Principle. getByRole은 실제 접근성 트리를 기준으로 쿼리하므로 마크업 변경에 덜 취약하다. [^3]

---

### ④ Mock 전략 (20점)

`vi.*` API 사용 방식을 평가한다.

| 항목 | 점수 | 합격 기준 |
|------|------|-----------|
| vi.mock 사용 | 6점 | 외부 모듈(API, router 등)을 `vi.mock()`으로 격리 |
| vi.importActual 활용 | 4점 | 일부만 mock 필요한 경우 `vi.importActual`로 원본 유지 |
| mock 클린업 | 6점 | `afterEach`에서 `vi.clearAllMocks()` 또는 `vi.restoreAllMocks()` 호출 |
| 과도한 mocking 없음 | 4점 | 테스트 대상 외 불필요한 모든 것을 mock하지 않음 |

감점 조건 (각 항목 최소 0점 보장):
- `vi.mock`을 쓰되 클린업 없이 테스트 간 mock 상태가 오염될 가능성 있으면 -3점
- `jest.mock` 잔존 코드 발견 시 -2점 (Jest → Vitest 미완 마이그레이션 신호)

> 근거: afterEach 클린업 없이 vi.mock을 사용하면 테스트 실행 순서에 따라 결과가 달라지는 flaky test가 발생한다. jest.mock 잔존은 일부 환경에서 런타임 오류를 유발한다. [^4]

---

### ⑤ 커버리지 & CI 통합 (15점)

| 항목 | 점수 | 합격 기준 |
|------|------|-----------|
| 커버리지 수집 설정 | 5점 | `coverage.provider` + `reporter(['text','html','json'])` 설정 |
| 커버리지 기준점 달성 | 5점 | `coverage/coverage-summary.json`이 존재하고 설정된 threshold 이상. 파일이 없으면 "측정 불가 — 0점"으로 처리 |
| CI 스크립트 존재 | 5점 | `package.json` scripts에 `test:ci` 또는 `test --run` 형태의 CI용 명령어 존재 |

감점 조건:
- threshold 설정은 있으나 CI에서 `--coverage` 플래그 없이 실행 시 -2점

> 근거: 커버리지 80% 기준은 업계 표준으로 널리 인용된다. CI에서 `--coverage` 없이 실행하면 threshold가 있어도 기준점 미달을 감지하지 못한다. [^5]

---

## 출력 형식

감사를 마친 후 아래 형식으로 출력하라. 형식을 변경하지 말 것.

### Vitest 도입 수준 감사 결과

#### 종합 점수

> 상태 기준: 🟢 해당 차원 80% 이상 / 🟡 50~79% / 🔴 50% 미만

| 차원 | 점수 | 만점 | 상태 |
|------|------|------|------|
| ① 설정 & 구성 | X | 20 | 🟢 양호 / 🟡 주의 / 🔴 미흡 |
| ② 테스트 구조 | X | 20 | 🟢 / 🟡 / 🔴 |
| ③ React 패턴 | X | 25 | 🟢 / 🟡 / 🔴 |
| ④ Mock 전략 | X | 20 | 🟢 / 🟡 / 🔴 |
| ⑤ 커버리지 & CI | X | 15 | 🟢 / 🟡 / 🔴 |
| **총점** | **XX / 100** | | |

---

#### 발견된 문제점

**🔴 즉시 수정 필요 (점수 영향 큰 항목)**
- (발견된 항목 없으면 "없음"으로 표시)

**🟡 개선 권장 (베스트 프랙티스 미준수)**
- (발견된 항목 없으면 "없음"으로 표시)

**ℹ️ 참고 사항 (점수 영향 없는 관찰)**
- (발견된 항목 없으면 "없음"으로 표시)

---

#### 개선 우선순위

**Priority 1 — Quick Win (1일 이내 적용 가능)**
1. [항목]: [현재 상태] → [목표 상태]

**Priority 2 — 단기 (1주 이내)**
1. [항목]: [현재 상태] → [목표 상태]

**Priority 3 — 중장기 (1달 이내)**
1. [항목]: [현재 상태] → [목표 상태]

---

#### 차원별 핵심 근거

> 각 점수의 판단 근거를 파일명과 라인 번호(또는 코드 스니펫)로 명시하라.

**① 설정 & 구성**
- 근거: `vitest.config.ts` L{N} — {내용}

**② 테스트 구조**
- 근거: `src/{파일명}.test.tsx` — {내용}

**③ React 패턴**
- 근거: `src/{파일명}.test.tsx` — {내용}

**④ Mock 전략**
- 근거: `src/{파일명}.test.tsx` — {내용}

**⑤ 커버리지 & CI**
- 근거: `package.json scripts` — {내용}

---

## 주의사항

- 파일을 수정하지 말 것
- 각 판단은 파일의 실제 내용을 인용해서 구체적으로 근거를 제시할 것
- `package.json`, `vitest.config.ts` 등 관련 파일을 참조해서 stale 여부를 검증할 것
- 점수는 항목별 설명의 가점/감점 기준을 엄격히 적용할 것. 관대하게 주지 말 것
- 감점 적용 후 각 항목 점수는 최소 0점이며 음수가 되지 않는다

---

## 참고 문헌

[^1]: Vitest, **"Test Environment"**, Official Documentation.
- 원문: https://vitest.dev/guide/environment.html
- 주요 발견: jsdom/happy-dom 없이는 DOM API가 존재하지 않아 React 컴포넌트 테스트 불가. coverage.thresholds 미설정 시 기준점 미달 감지 불가. @vitejs/plugin-react 미설정 시 JSX 파싱 불가.

[^2]: Kent C. Dodds, **"The Testing Trophy"**, Blog, 2018.
- 원문: https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications
- 주요 발견: Static → Unit → Integration → E2E 계층에서 Integration 테스트 비중이 가장 높을 때 ROI가 좋다.

[^3]: Kent C. Dodds, **"Testing Library — Guiding Principles"**, Testing Library Docs.
- 원문: https://testing-library.com/docs/guiding-principles
- 주요 발견: 소프트웨어 사용 방식을 닮은 테스트일수록 신뢰도가 높다. getByRole은 실제 접근성 트리를 기준으로 쿼리하므로 마크업 변경에 덜 취약하다.

[^4]: Vitest, **"Mock Lifecycle"**, Official Documentation.
- 원문: https://vitest.dev/guide/mocking.html
- 주요 발견: afterEach 클린업 없이 vi.mock을 사용하면 테스트 순서에 따라 결과가 달라지는 flaky test 발생. clearAllMocks/restoreAllMocks 중 프로젝트 정책에 맞는 하나를 전역 설정 권장.

[^5]: Atlassian, **"Code Coverage — A Guide to Understanding What It Is and How It's Used"**, Atlassian Engineering Blog.
- 원문: https://www.atlassian.com/continuous-delivery/software-testing/code-coverage
- 주요 발견: 커버리지 80%는 업계 표준으로 널리 인용되는 기준점. 단, 숫자보다 critical path 커버 여부가 더 중요하다.
