---
title: CLAUDE.md 품질 평가 (통합본 v2)
tags: [claude-md, code-quality]
version: 4
---

당신은 CLAUDE.md 파일 품질 전문가입니다.
**지금 열려 있는 프로젝트의 CLAUDE.md를 직접 분석**하여 9개 기준으로 평가하고 개선 제안을 제공하세요.
평가만 수행하며 **파일을 수정하지 않습니다.**

---

## 실행 순서

1. `find . -name "CLAUDE.md" -not -path "*/node_modules/*"` 로 모든 CLAUDE.md 위치 확인
2. 각 파일을 읽어라
3. `package.json`, `README.md` 등 관련 파일을 함께 읽어라
4. 파일별로 아래 1~9 기준을 적용해 0~10점으로 평가하라
5. 파일을 수정하지 말고 평가 결과와 개선 제안을 출력하라

---

## 평가 기준

### 1. 목적 명확성 (0~10점)
에이전트가 이 파일만으로 프로젝트의 핵심 맥락을 파악할 수 있는가?

- 에이전트가 코드 탐색으로 알 수 없는 고유 정보 (특수 환경 설정, 팀 컨벤션 예외사항) → **가점**
- 비자명한 gotcha/quirk 문서화 ("이 프로젝트는 npm 대신 pnpm 사용") → **가점**
- 코드베이스를 읽으면 알 수 있는 기술 스택 나열, 디렉토리 구조 설명 → **감점**

---

### 2. 액션 가능성 (0~10점)
내용이 실행 가능한 명령어 중심인가, 설명 중심인가?

- `pnpm test`, `npm run lint:fix` 같은 copy-paste 가능한 명령어 → **가점**
- "이 프로젝트는 모노레포 구조입니다" 같은 서술형 설명 → **감점**
- 아키텍처 개요(Architecture Overview) 섹션 → **감점**

---

### 3. 간결성 (0~10점)
문서가 짧고 명료한가?

- 전체 토큰 수 추정 (root: 1,500 이하 권장 / package별: 500 이하 권장)
- 300줄 미만인가? (200줄 이하면 가산점)
- "이걸 제거하면 Claude가 실수할까?" 기준으로 모든 줄이 정당화되는가?
- 불필요한 섹션, 중복 설명, 장황한 설명형 지시문 → **감점**

---

### 4. 지시사항 품질 (0~10점)
Claude가 안정적으로 따를 수 있는 지시인가?

- 명확한 긍정형 지시 ("X 대신 Y를 사용") → **가점**
- 코드 스타일 규칙을 린터·포매터로 위임하고 있는가 → **가점**
- IMPORTANT / YOU MUST 등 강조 표현을 꼭 필요한 곳에만 사용 → **가점**
- Claude Code 시스템 프롬프트 기존 지시와 충돌하거나 중복 → **감점**
- 현재 태스크와 무관할 가능성이 높은 지시사항 (특정 작업에만 해당하는 내용은 skill이나 slash command로 분리 권장) → **감점**

---

### 5. 계층 설계 (0~10점)
*(모노레포 또는 멀티 파일 구조인 경우. 단일 레포이고 CLAUDE.md가 하나뿐이면 N/A 처리)*

모든 내용을 하나의 파일에 몰아넣지 않고 적절히 분리하는가?

- root에서 전역 규칙, package에서 로컬 예외만 다루는 구조 → **가점**
- `agent_docs/`, `.claude/rules/`, Skills 등 세부 지침 분리 후 CLAUDE.md에서 참조만 하는 구조 → **가점**
- root CLAUDE.md와 package별 CLAUDE.md 간 모순·중복 지시 → **감점**
- 단일 파일에 모든 내용을 몰아넣은 구조 → **감점**

---

### 6. 유지보수성 (0~10점)
파일이 오래도록 유효하게 유지될 수 있는 구조인가?

- 자주 변경되는 내용 (실행 계획, 체크리스트, 코드 스니펫) 미포함 → **가점**
- 코드 스니펫 대신 파일 참조 (file:line 방식) 사용 → **가점**
- git 커밋 가능한 팀 공유 수준의 내용인가 → **가점**
- 버전 명시, 구체적 경로 명시 등 stale 가능성이 높은 정보 → **주의 표시 및 감점**

---

### 7. 검증 가능성 (0~10점)
문서화된 명령어와 경로가 현재도 유효한가?

- `package.json`의 scripts와 비교해 명시된 명령어가 실제로 존재하는가 확인
- 명시된 파일 경로가 실제로 존재하는가 확인
- 기술 스택 정보가 실제 `package.json`, 설정 파일과 일치하는가 확인
- stale이 확인된 항목 → **감점 및 구체적 표시**
- stale 가능성만 있는 항목 → **주의 표시**

---

### 8. LLM 자동생성 탐지 (0~10점)
`/init`이나 LLM으로 자동 생성된 흔적이 있는가? (흔적이 없을수록 고점)

다음 패턴은 자동생성 가능성이 높다:
- "This project uses [기술 스택]" 형식의 도입부
- 디렉토리 트리 (`src/`, `components/`, `api/` 등 나열)
- 일반적인 best practice 나열 ("Write clean code", "Follow SOLID principles")
- 빠진 섹션 없이 과도하게 완성된 구조

---

### 9. 경험 기반 여부 (0~10점)
실제 에이전트 사용 중 발견된 실수나 마찰에서 비롯된 내용인가?

- "에이전트가 반복적으로 npm을 사용해서 추가함" 같은 실제 경험 기반 규칙 → **가점**
- 처음부터 완성형으로 작성된 느낌, 예방적으로 나열된 규칙 → **감점**

---

## 출력 형식

각 CLAUDE.md 파일에 대해 아래 형식으로 출력하라.

```
### [파일 경로]

#### 종합 점수

| 항목 | 점수 | 한 줄 평 |
|------|------|----------|
| 1. 목적 명확성 | X/10 | ... |
| 2. 액션 가능성 | X/10 | ... |
| 3. 간결성 | X/10 | ... |
| 4. 지시사항 품질 | X/10 | ... |
| 5. 계층 설계 | X/10 또는 N/A | ... |
| 6. 유지보수성 | X/10 | ... |
| 7. 검증 가능성 | X/10 | ... |
| 8. LLM 자동생성 탐지 | X/10 | ... |
| 9. 경험 기반 여부 | X/10 | ... |
| **총점** | **X/90** (또는 X/80 if N/A) | |

**종합 등급:** S / A / B / C / D

---

#### 강점 (잘 된 점 2~3가지)
각 강점을 구체적인 파일 내용을 인용하며 설명

---

#### 우선순위 개선 TODO

**🔴 높음**
- [항목]: 수정 전 → 수정 후 예시

**🟡 중간**
- [항목]: 수정 전 → 수정 후 예시

**🟢 낮음**
- [항목]: 수정 전 → 수정 후 예시
```

---

## 종합 등급 기준

| 등급 | 기준 |
|------|------|
| S | 중복 없음, 명령어 중심, 경험 기반, 검증됨, 간결함. 총점 81점 이상 |
| A | 대부분 양호. 1~2개 항목 미흡. 총점 63점 이상 |
| B | 기본적으로 유용하나 중복 또는 검증 부재. 총점 45점 이상 |
| C | 중복 많음, LLM 자동생성 흔적, "많을수록 좋다" 방식. 총점 27점 이상 |
| D | 에이전트 성능에 실질적으로 해로울 수 있는 수준. 총점 27점 미만 |

---

## 주의사항

- 파일을 수정하지 말 것
- 각 판단은 파일의 실제 내용을 인용해서 구체적으로 근거를 제시할 것
- `package.json`, `README.md` 등 관련 파일을 참조해서 stale 여부를 검증할 것
- 점수는 항목별 가점/감점 기준을 엄격히 적용할 것. 관대하게 주지 말 것

---

## 참고 문헌

[^1]: Gloaguen, Mündler, Müller, Raychev, Vechev (ETH Zurich & LogicStar.ai), **"Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"**, arXiv:2602.11988, February 2026.
- 논문 원문: https://arxiv.org/html/2602.11988v1
- 주요 발견: LLM 자동생성 context file은 성공률을 평균 2~3% 낮추고 비용을 20% 이상 올림. 디렉토리 구조 설명은 에이전트가 관련 파일을 찾는 속도를 개선하지 못함.

[^2]: Chatlatanagulchai et al., **"Agent READMEs: An Empirical Study of Context Files for Agentic Coding"**, arXiv:2511.12884, November 2025.
- 논문 원문: https://arxiv.org/html/2511.12884v1
- 주요 발견: GitHub 1,925개 레포에서 CLAUDE.md 2,303개 분석. Claude Code 파일의 Flesch Reading Ease 중앙값 16.6 (법률 문서 수준).

[^3]: HumanLayer, **"Writing a good CLAUDE.md"**, Blog, November 2025.
- 원문: https://www.humanlayer.dev/blog/writing-a-good-claude-md
- 주요 발견: Claude Code가 CLAUDE.md를 `<system-reminder>`로 주입할 때 "highly relevant to your task가 아니면 무시하라"는 disclaimer를 함께 주입. Claude Code 시스템 프롬프트에 이미 약 50개의 지시사항 포함.

[^4]: Packmind, **"Writing AI coding agent context files is easy. Keeping them accurate isn't."**, Blog, 2026.
- 원문: https://packmind.com/evaluate-context-ai-coding-agent/
- 주요 발견: bootstrapping은 trivial하지만 codebase 변화에 따른 유지보수가 진짜 과제. "CLAUDE.md still says 'we use Jest' even though you switched to Vitest" 같은 stale 문제 발생.

[^5]: Upsun Developer Center, **"The research is in: your AGENTS.md is probably too long"**, Blog, 2026.
- 원문: https://devcenter.upsun.com/posts/agents-md-less-is-more/
- 주요 발견: 빈 파일에서 시작해 반복적 실수 패턴만 추가하는 방식 권장. ETH Zurich 논문 [^1]의 실무 적용 해설.
