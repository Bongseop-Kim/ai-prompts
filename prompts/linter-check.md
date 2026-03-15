---
title: 린터/포매터 활용 수준 점검
tags: [linter, formatter]
version: 3
---

당신은 AI 시대의 코드 품질 도구 전문가입니다.
**지금 열려 있는 프로젝트 코드베이스를 직접 분석**하여 린터/포매터 활용 수준을
6개 영역에서 점검하고, 논문 근거 기반의 점수와 개선 피드백을 제공하세요.

---

## 분석 지시

아래 파일/경로를 탐색하여 현황을 파악한 후 점수를 산정하세요.
**파일이 없거나 확인 불가한 항목은 0점 처리하고 그 이유를 명시하세요.**

```
탐색 대상:
- 루트: package.json, .eslintrc.*, eslint.config.*, .prettierrc.*, biome.json
- 보안 도구: .semgreprc, .github/workflows/*.yml, sonar-project.properties
- 자동화: .husky/*, .pre-commit-config.yaml, lefthook.yml, lint-staged 설정
- CI/CD: .github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile, .circleci/config.yml
- 기술 부채: eslint-disable 주석 전체 카운트
  grep -r "eslint-disable" --include="*.ts" --include="*.tsx" .
- 중복 탐지: jscpd.json, .jscpd.json, sonar 설정
- AI 컨텍스트: CLAUDE.md, .cursorrules, .github/copilot-instructions.md
```

---

## 점검 영역 및 배점 기준 (총 100점)

### 영역 1. 도구 설치 및 기본 설정 (15점)

**린터 설치 및 규칙 파일 (8점)**
- 0점: 린터 없음
- 5점: 린터 설치됨, 규칙 파일 존재
- 8점: 린터 설치됨, 규칙 파일 존재 + extends 또는 plugins로 기본값 이상 확장됨

**포매터 설치 및 설정 파일 (7점)**
- 0점: 포매터 없음
- 4점: 포매터 설치됨, 설정 파일 존재
- 7점: 포매터 설치됨, 설정이 팀 컨벤션(print width, tab 등)을 명시적으로 정의함

---

### 영역 2. 자동화 수준 (20점)

**pre-commit hook (13점)**
- 0점: hook 없음
- 6점: hook 존재하지만 lint 또는 format 중 하나만 포함
- 10점: lint + format 모두 자동 실행
- 13점: lint + format + type-check 또는 test까지 포함

**CI/CD 파이프라인 lint 강제 (7점)**
- 0점: CI 없거나 lint 미포함
- 4점: CI에 lint 포함되지만 실패 시 통과 가능 (warn 수준)
- 7점: CI에서 lint 실패 시 머지 차단

---

### 영역 3. AI 코딩 도구 통합 (20점)

**AI 도구(Claude Code, Cursor 등) 사용 프로젝트**
- 0점: AI 사용하지만 lint가 피드백 루프에 없음
- 8점: 개발자가 수동으로 lint 실행 (CLAUDE.md 등에 lint 명령어 가이드 있음)
- 14점: pre-commit hook으로 AI 수정 파일에 lint 자동 실행
- 20점: hook + CI 이중 차단 + AI 컨텍스트 파일(CLAUDE.md 등)에 린트 규칙 참조가 있되,
        해당 규칙이 eslint.config.*에 hard error로도 정의되어 있음

**AI 도구 미사용 프로젝트**
- N/A 처리. 나머지 5개 영역 합산을 100점으로 환산.
- 환산 공식: `최종점수 = (나머지 5개 영역 합산 / 80) × 100`

---

### 영역 4. 보안 정적 분석 (20점)

**보안 전용 정적 분석 도구 존재 여부 (10점)**
- 0점: 없음
- 4점: eslint-plugin-security 수준 (규칙 기반, 경고 위주)
- 7점: Semgrep OSS 등 패턴 매칭 SAST 도구
- 10점: CodeQL 또는 상용 SAST 도구 (Snyk, SonarQube 포함)

**보안 규칙의 적용 범위 (10점)**
- 0점: 로컬에서만 실행되거나 AI 생성 코드에 적용 안 됨
- 5점: PR 단계에서 수동 실행 또는 부분 적용
- 10점: CI에서 모든 커밋/PR에 자동 SAST 실행, 실패 시 머지 차단

---

### 영역 5. 규칙의 전략적 설계 (15점)

- 0점: 기본값(recommended) 그대로 사용
- 5점: 일부 커스텀 규칙 존재 (프로젝트 특화 off/warn 조정 수준)
- 10점: import path 강제, deprecated API 차단, naming 규칙 등 컨벤션이 hard error로 인코딩됨
- 15점: 위 조건 + CLAUDE.md에 기술된 컨벤션 중 린터로 검증 가능한 항목은
        모두 eslint.config.*에 error 레벨로도 정의되어 있음
        (soft guideline과 hard constraint의 역할이 명확히 분리됨)

---

### 영역 6. 운영 상태 및 기술 부채 (10점)

**eslint-disable 남용 (5점)**
- 0점: 10개 이상
- 2점: 5~9개
- 4점: 1~4개
- 5점: 0개

**중복 코드 탐지 도구 (5점)**
- 0점: 없음
- 2점: jscpd / SonarQube 등 설정 존재하지만 CI 미연동
- 5점: CI에서 자동 실행, 임계값 초과 시 경고 또는 차단

---

## 출력 형식

### 분석 결과 요약

분석한 주요 파일 목록을 나열하고, 발견 내용을 한 줄씩 기술하세요.
예: `eslint.config.ts` — typescript-eslint extends, 커스텀 규칙 12개 확인

---

### 종합 점수: XX / 100점

| 영역 | 점수 | 만점 | 적용 근거 |
|------|------|------|-----------|
| 도구 설치 및 기본 설정 | ? | 15 | — |
| 자동화 수준 | ? | 20 | — |
| AI 코딩 도구 통합 | ? | 20 (또는 N/A) | IRIS (arXiv:2405.17238) · Gloaguen et al. (arXiv:2602.11988) |
| 보안 정적 분석 | ? | 20 | Sabra et al. (arXiv:2508.14727) · CodeRabbit 2025 |
| 규칙의 전략적 설계 | ? | 15 | Gloaguen et al. (arXiv:2602.11988) |
| 운영 상태 및 기술 부채 | ? | 10 | GitClear 2025 · Xu et al. (arXiv:2510.10165) |

*AI 도구 미사용 시: 5개 영역 합산 점수 기재 후 80점 만점 환산값을 최종 점수로 명시*

---

### 등급 판정

- **90–100**: AI 시대 모범 수준 (보안·자동화 완전 통합, 린터가 hard constraint 역할)
- **70–89**: 기반은 있음, 보안 정적 분석 또는 AI 통합 미흡
- **50–69**: 도구는 있으나 AI 워크플로우 미통합, 기술 부채 누적 위험
- **30–49**: 기초 단계, 즉각 개선 필요
- **0–29**: 린터/포매터 미사용 (AI 생성 코드 품질 보증 불가)

---

### 영역별 피드백

각 영역에 대해 아래 형식으로 작성하세요:

```
[발견 내용] 실제 파일/설정 기반으로 확인된 사실
[리스크 수준] 현재 상태의 위험도 (낮음 / 중간 / 높음 / 치명)
[개선 액션] 구체적인 설정 변경 또는 도구 추가 방법 (명령어 수준으로)
```

---

### 우선순위 개선 액션 TOP 3

점수 대비 임팩트가 높은 순으로 작성하세요:

```
1. [액션명]
   - 예상 점수 상승: +X점
   - 근거: 어떤 리스크를 차단하는지
   - 실행 방법: 구체적인 명령어 또는 설정 스니펫
   - 난이도: 낮음 / 중간 / 높음
```

---

### AI 코드 품질 리스크 진단

현재 프로젝트에서 AI 생성 코드의 보안 취약점이 CI 이전에 차단될 확률을 평가하세요.

**판정: 차단 가능 / 차단 불가 / 부분 차단** 중 하나

근거: 어떤 파일/설정 분석을 통해 이 판정에 도달했는지 서술하세요.

---

## 출처

**[1]** Abbas Sabra, Olivier Schmitt, Joseph Tyler.
*Assessing the Quality and Security of AI-Generated Code: A Quantitative Analysis.*
arXiv:2508.14727 [cs.SE], 20 Aug 2025.
Sonar 소속 연구진. Java 코드 4,442건 대상, SonarQube(SonarWay Java ~550 rules) 분석.
🔗 https://arxiv.org/abs/2508.14727

**[2]** Ziyang Li, Saikat Dutta, Mayur Naik.
*IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities.*
arXiv:2405.17238 [cs.CR]. ICLR 2025 게재.
Cornell University & University of Pennsylvania.
CWE-Bench-Java(실제 CVE 취약 Java 프로젝트 120건) 대상 실험.
CodeQL 단독 27건 → IRIS+GPT-4 69건 탐지 (최종 ICLR 게재판 기준).
🔗 https://arxiv.org/abs/2405.17238

**[3-A]** GitClear.
*AI Copilot Code Quality 2025: 4x More Code Cloning, "Copy/Paste" Exceeds "Moved" Code for First Time in History.*
산업 보고서, 2025. 동료 심사 없음. 관찰 데이터.
2020~2024년 2억 1,100만 변경 라인(Google, Microsoft, Meta 포함) 분석.
🔗 https://www.gitclear.com/ai_assistant_code_quality_2025_research

**[3-B]** Feiyang Xu, Poonacha K. Medappa, Murat M. Tunc, Martijn Vroegindeweij, Jan C. Fransoo.
*AI-Assisted Programming Decreases the Productivity of Experienced Developers by Increasing the Technical Debt and Maintenance Burden.*
arXiv:2510.10165 [econ.GN]. 최초 제출 Oct 2025, v3 Jan 2026.
GitHub Copilot 도입 전후 OSS 프로젝트 개발자 활동 차이분석(Difference-in-Differences).
🔗 https://arxiv.org/abs/2510.10165

**[4]** Thibault Gloaguen et al. (ETH Zurich).
*Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*
arXiv:2602.11988 [cs.SE]. ICML 2025.
Claude Code(Sonnet-4.5), Codex(GPT-5.2/5.1 mini), Qwen Code 대상.
SWE-bench Lite + 신규 벤치마크 AGENTbench(실제 CLAUDE.md 보유 저장소 138개 태스크) 평가.
🔗 https://arxiv.org/abs/2602.11988

**[5]** CodeRabbit.
*State of AI vs Human Code Generation.*
산업 보고서, Dec 2025. 동료 심사 없음. CodeRabbit 자사 보고서.
오픈소스 GitHub PR 470건(AI 생성 320건 vs 인간 작성 150건) 분석.
Poisson rate ratio / 95% CI 통계 검정 적용.
🔗 https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
