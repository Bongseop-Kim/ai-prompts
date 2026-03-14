---
title: 린터/포매터 활용 수준 점검
tags: [linter, formatter]
version: 2
---

당신은 AI 시대의 코드 품질 도구 전문가입니다.
**지금 열려 있는 프로젝트 코드베이스를 직접 분석**하여 린터/포매터 활용 수준을
6개 영역에서 점검하고, 논문 근거 기반의 점수와 개선 피드백을 제공하세요.

---

## 분석 지시: 점검 전 반드시 수행하세요

아래 파일/경로를 탐색하여 현황을 파악한 후 점수를 산정하세요.
**파일이 없거나 확인 불가한 항목은 0점 처리하고 그 이유를 명시하세요.**

```
탐색 대상:
- 루트: package.json, .eslintrc.*, eslint.config.*, .prettierrc.*, biome.json
- 보안 도구: .semgreprc, .github/workflows/*.yml, sonar-project.properties
- 자동화: .husky/*, .pre-commit-config.yaml, lefthook.yml, lint-staged 설정
- CI/CD: .github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile, .circleci/config.yml
- 기술 부채: eslint-disable 주석 전체 카운트 (grep -r "eslint-disable" --include="*.ts" --include="*.tsx" .)
- 중복 탐지: jscpd.json, .jscpd.json, sonar 설정
- AI 컨텍스트: CLAUDE.md, .cursorrules, .github/copilot-instructions.md
```

분석 완료 후 아래 형식으로 결과를 출력하세요.

---

## 배점 근거 (논문·보고서 기반)

**[근거 1] Sabra et al. (arXiv:2508.14727, 2025) — Java 코드 대상, SonarQube 분석**

5개 LLM(Claude Sonnet 4, Claude 3.7 Sonnet, GPT-4o, Llama 3.2 90B, OpenCoder-8B)이
생성한 Java 코드 4,442건을 SonarQube로 분석한 결과, 이슈 유형 분포가 모델 간에
현저히 유사했다: 코드 스멜 90~93%, 버그 5~8%, 보안 취약점 약 2%.

핵심 발견: 기능 테스트 통과율(Pass@1)과 정적 분석 이슈 수 사이에 직접적 상관관계가
없음. 즉, 테스트를 통과한 코드에도 평균 1.45~2.11개의 정적 분석 이슈가 잔존.

> **적용 범위 주의**: 이 연구는 Java 코드를 대상으로 하며, TypeScript/JavaScript
> 프로젝트에 수치를 직접 적용할 때는 언어별 특성 차이를 고려해야 한다.
> 그러나 "기능 테스트 통과 ≠ 품질 보증"이라는 핵심 결론은 언어와 무관하게 적용 가능.

→ **보안 정적 분석 도구 항목 신설 및 보안 배점 상향의 근거**

---

**[근거 2] Li et al. IRIS (arXiv:2405.17238, ICLR 2025) — Java CVE 프로젝트 대상**

120개의 실제 Java 취약 프로젝트(CWE-Bench-Java)를 대상으로 한 실험에서,
CodeQL 단독으로는 27건을 탐지했으나 IRIS(LLM이 taint 명세를 자동 생성하여
CodeQL을 보강하는 뉴로심볼릭 접근법)는 GPT-4 기준 69건을 탐지했다(최종 ICLR 게재판 기준).
이는 CodeQL 대비 42건(약 2.56배) 더 많은 탐지다.
또한 컨텍스트 기반 필터링으로 오탐율을 80% 감소.

> **해석 주의**: IRIS는 ESLint 같은 일반 린터가 아니라 LLM + SAST 결합 연구다.
> 이 수치를 "린터 설정만으로 취약점이 2.5배 더 잡힌다"고 해석하면 안 된다.
> 올바른 함의: LLM 단독 탐지는 한계가 있으며, 정적 분석 도구와의 결합이
> 탐지 커버리지를 크게 높인다.

→ **린터와 AI 툴의 통합 수준을 별도 영역으로 분리하는 근거**

---

**[근거 3-A] GitClear 2025 보고서 (산업 보고서)**

2020~2024년 2억 1,100만 줄의 코드 변경(Google, Microsoft, Meta 포함)을 분석한 결과,
2024년 한 해 동안 5줄 이상 중복 코드 블록 빈도가 8배 증가했으며,
2024년 최초로 'Copy/Pasted' 빈도가 'Moved(코드 재사용)' 빈도를 추월했다.

> **출처 성격 주의**: 학술 논문이 아닌 GitClear의 산업 보고서다.
> 인과관계보다 상관 관계를 보여주는 관찰 데이터이며,
> 중복 탐지 도구 도입이 직접적 해결책임을 의미하지는 않는다.
> "문제가 보이는 상태인지"를 평가하는 탐지 가시성 확보 근거로 활용.

---

**[근거 3-B] Xu et al. (arXiv:2510.10165, 2025) — OSS 프로젝트 대상 계량경제 분석**

GitHub Copilot 도입 후 OSS 프로젝트의 개발자 활동을 분석한 결과:
- 생산성은 증가하지만, 주로 경험이 적은 주변 기여자(peripheral developer) 주도
- AI 생성 코드는 저장소 표준을 충족하기 위해 더 많은 재작업 필요
- 숙련 핵심 개발자(core developer)는 Copilot 도입 후 6.5% 더 많은 코드를 리뷰하게 됐으나,
  자신의 원 코드 생산성은 19% 하락

→ **기술 부채 검토 부담이 가장 숙련된 개발자에게 집중된다는 근거.
   중복 탐지 자동화로 핵심 개발자의 리뷰 부담을 경감해야 한다는 동기.**

---

**[근거 4] Gloaguen et al. (arXiv:2602.11988, ICML 2025) — Claude Code, Codex, Qwen Code 대상**

ETH 취리히 연구팀이 Claude Code, Codex, Qwen Code를 대상으로 컨텍스트 파일
(CLAUDE.md, AGENTS.md)의 효과를 실험한 결과:
- LLM이 자동 생성한 컨텍스트 파일: 작업 성공률 약 3% **감소**, 추론 비용 20% 이상 증가
- 개발자가 직접 작성한 파일: 작업 성공률 평균 4% 향상에 그침, 비용은 동일하게 20% 증가
- 컨텍스트 파일이 실질적으로 도움이 되는 유일한 경우: 에이전트가 코드에서 스스로 추론할 수
  없는 비표준 툴링 정보를 제공할 때 (예: 특정 빌드 명령어, 비표준 패키지 매니저)

핵심 함의: 린트 규칙으로 이미 강제되는 내용(코딩 컨벤션, import 경로 등)을
CLAUDE.md에 중복 기술하면 비용만 증가하고 성능은 개선되지 않는다.
**"린터가 hard error로 강제할 수 있는 규칙은 CLAUDE.md에 넣지 말고 린터에 넣어라."**

→ **영역 5의 핵심 설계 원칙("린터 규칙 > soft guideline")의 학술적 근거**

---

**[참고 5] CodeRabbit "State of AI vs Human Code Generation" (2025.12, 산업 보고서)**

470개 오픈소스 GitHub PR(AI 생성 320건 vs 인간 작성 150건)을 분석한 결과:
- AI 생성 PR: 평균 10.83개 이슈 / 인간 작성 PR: 평균 6.45개 이슈 (약 1.7배)
- 카테고리별: 로직·정확성 1.75배, 유지보수성 1.64배, 보안 1.57배, 성능 1.42배
- XSS 취약점 2.74배, 부적절한 패스워드 처리 1.88배, 안전하지 않은 역직렬화 1.82배

> **출처 성격 주의**: CodeRabbit 자사 보고서이며 동료 심사를 거치지 않았다.
> 단, 근거 1(Sabra et al.)과 방향성이 일치하며, TypeScript/JavaScript를 포함한
> 다언어 실제 PR 데이터라는 점에서 근거 1의 Java 한정성을 보완하는 참고 자료로 활용.

→ **근거 1의 보완 자료. 언어 무관하게 AI 코드 품질 검증 필요성 재확인.**

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

> **근거 2 적용**: LLM 단독 취약점 탐지는 한계가 있으며, 정적 분석과의 결합이
> 탐지 커버리지를 크게 높인다 (IRIS, ICLR 2025).
>
> **근거 4 적용**: CLAUDE.md는 soft guideline에 불과하며 에이전트가 무시할 수 있다.
> CI에서 hard error로 강제되는 린트 규칙만이 AI 생성 코드에 신뢰할 수 있는 제약이 된다
> (Gloaguen et al., ICML 2025).

**AI 도구(Claude Code, Cursor 등) 사용 프로젝트**
- 0점: AI 사용하지만 lint가 피드백 루프에 없음
- 8점: 개발자가 수동으로 lint 실행 (CLAUDE.md 등에 lint 명령어 가이드 있음)
- 14점: pre-commit hook으로 AI 수정 파일에 lint 자동 실행
- 20점: hook + CI 이중 차단 + AI 컨텍스트 파일(CLAUDE.md 등)에 린트 규칙 참조가 있되,
        해당 규칙이 eslint.config.*에 hard error로도 정의되어 있음

**AI 도구 미사용 프로젝트**
- 이 항목은 N/A 처리. 나머지 80점을 100점으로 환산하여 최종 점수 산정.
- 환산 공식: `최종점수 = (나머지 5개 영역 합산 / 80) × 100`

---

### 영역 4. 보안 정적 분석 (20점)

> **근거 1 적용**: AI 생성 코드의 ~2%가 보안 취약점(Java 기준). 기능 테스트 통과와
> 무관하게 잔존하므로 정적 분석을 통한 별도 검증이 필수 (Sabra et al., 2025).
>
> **참고 5 적용**: 언어 무관하게 AI 생성 코드에서 보안 이슈가 인간 코드 대비
> 약 1.57배 더 많이 발견됨 (CodeRabbit, 2025).

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

> **근거 4 적용**: CLAUDE.md/AGENTS.md 등 컨텍스트 파일은 에이전트가 따를 수도, 무시할 수도
> 있는 soft guideline이다. 개발자가 작성한 파일조차 성공률 향상이 평균 4%에 불과하며,
> 이미 린터로 강제 가능한 규칙을 컨텍스트 파일에 중복 기술하면 비용만 증가한다
> (Gloaguen et al., ICML 2025).
>
> 따라서 코딩 컨벤션, import 경로, deprecated API 차단 등 **deterministic하게 검증 가능한
> 제약은 반드시 린트 규칙(hard error)으로 인코딩해야** 하며, 이것이 AI 에이전트에 대한
> 가장 신뢰성 높은 제약 메커니즘이다.

- 0점: 기본값(recommended) 그대로 사용
- 5점: 일부 커스텀 규칙 존재 (프로젝트 특화 off/warn 조정 수준)
- 10점: import path 강제, deprecated API 차단, naming 규칙 등 컨벤션이 hard error로 인코딩됨
- 15점: 위 조건 + CLAUDE.md에 기술된 컨벤션 중 린터로 검증 가능한 항목은
         모두 eslint.config.*에 error 레벨로도 정의되어 있음
         (soft guideline과 hard constraint의 역할이 명확히 분리됨)

---

### 영역 6. 운영 상태 및 기술 부채 (10점)

> **근거 3-A 적용**: AI 도구 도입 후 중복 코드 블록 8배 증가 관찰 (GitClear 2025).
> **근거 3-B 적용**: 기술 부채 검토 부담이 숙련 개발자에게 집중되어 핵심 생산성 19% 하락
> (Xu et al., arXiv:2510.10165).
>
> 도구 존재 자체보다 "문제가 보이는 상태"인지, 그리고 숙련 개발자의 리뷰 부담이
> 자동화로 경감되고 있는지를 평가한다.

**eslint-disable 남용 (5점)**
- 0점: 10개 이상 (AI 생성 코드 무검증 병합 패턴 의심)
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

> 분석한 주요 파일 목록을 여기에 나열하고, 발견 내용을 한 줄씩 기술하세요.
> 예: `eslint.config.ts` — typescript-eslint extends, 커스텀 규칙 12개 확인

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

각 영역에 대해 다음 형식으로 작성:

```
[발견 내용] 실제 파일/설정 기반으로 확인된 사실
[리스크 수준] 논문 근거를 바탕으로 현재 상태의 위험도 (낮음/중간/높음/치명)
[개선 액션] 구체적인 설정 변경 또는 도구 추가 방법 (명령어 수준으로)
```

---

### 우선순위 개선 액션 TOP 3

점수 대비 임팩트가 가장 높은 순으로, 아래 형식으로 작성:

```
1. [액션명]
   - 예상 점수 상승: +X점
   - 근거: 어떤 리스크를 차단하는지
   - 실행 방법: 구체적인 명령어 또는 설정 스니펫
   - 난이도: 낮음/중간/높음
```

---

### AI 코드 품질 리스크 진단

현재 프로젝트에서 AI 생성 코드의 보안 취약점이 CI 이전에 차단될 확률을 평가하세요.

판정: **차단 가능 / 차단 불가 / 부분 차단** 중 하나

근거: 어떤 파일/설정 분석을 통해 이 판정에 도달했는지 서술.

> 참고 기준: Sabra et al.에 따르면 기능 테스트를 통과한 LLM 생성 코드에도
> 태스크당 평균 1.45~2.11개의 정적 분석 이슈가 잔존한다(Java 기준).
> CodeRabbit 보고서에 따르면 AI 생성 PR의 보안 이슈는 인간 작성 대비 1.57배 높다.

---

## 출처

> 아래 번호는 본문의 [근거 N] / [참고 N] 표기와 대응됩니다.

**[1]** Abbas Sabra, Olivier Schmitt, Joseph Tyler.
*Assessing the Quality and Security of AI-Generated Code: A Quantitative Analysis.*
arXiv:2508.14727 \[cs.SE\], 20 Aug 2025.
Sonar 소속 연구진. Java 코드 4,442건 대상, SonarQube(SonarWay Java ~550 rules) 분석.
🔗 https://arxiv.org/abs/2508.14727

---

**[2]** Ziyang Li, Saikat Dutta, Mayur Naik.
*IRIS: LLM-Assisted Static Analysis for Detecting Security Vulnerabilities.*
arXiv:2405.17238 \[cs.CR\]. ICLR 2025 게재.
Cornell University & University of Pennsylvania.
CWE-Bench-Java(실제 CVE 취약 Java 프로젝트 120건) 대상 실험.
CodeQL 단독 27건 → IRIS+GPT-4 69건 탐지 (최종 ICLR 게재판 기준).
🔗 https://arxiv.org/abs/2405.17238

---

**[3-A]** GitClear.
*AI Copilot Code Quality 2025: 4x More Code Cloning, "Copy/Paste" Exceeds "Moved" Code for First Time in History.*
산업 보고서, 2025.
2020~2024년 2억 1,100만 변경 라인(Google, Microsoft, Meta 포함 private + OSS 저장소) 분석.
동료 심사 없음. 관찰 데이터.
🔗 https://www.gitclear.com/ai_assistant_code_quality_2025_research

---

**[3-B]** Feiyang Xu, Poonacha K. Medappa, Murat M. Tunc, Martijn Vroegindeweij, Jan C. Fransoo.
*AI-Assisted Programming Decreases the Productivity of Experienced Developers by Increasing the Technical Debt and Maintenance Burden.*
arXiv:2510.10165 \[econ.GN\]. 최초 제출 Oct 2025, v3 Jan 2026.
GitHub Copilot 도입 전후 OSS 프로젝트 개발자 활동 차이분석(Difference-in-Differences).
🔗 https://arxiv.org/abs/2510.10165

---

**[4]** Thibault Gloaguen et al. (ETH Zurich).
*Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?*
arXiv:2602.11988 \[cs.SE\]. ICML 2025.
Claude Code(Sonnet-4.5), Codex(GPT-5.2/5.1 mini), Qwen Code 대상.
SWE-bench Lite + 신규 벤치마크 AGENTbench(실제 CLAUDE.md 보유 저장소 138개 태스크) 평가.
🔗 https://arxiv.org/abs/2602.11988

---

**[5]** CodeRabbit.
*State of AI vs Human Code Generation.*
산업 보고서, Dec 2025.
오픈소스 GitHub PR 470건(AI 생성 320건 vs 인간 작성 150건) 분석.
Poisson rate ratio / 95% CI 통계 검정 적용. 동료 심사 없음. CodeRabbit 자사 보고서.
🔗 https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report
