# ai-prompts

자주 사용하는 AI 프롬프트 저장소.

## 구조

```
ai-prompts/
├── prompts/        # 프롬프트 파일 (.md)
├── scripts/
│   └── gen-tags.py # TAGS.md 자동 생성 스크립트
├── .githooks/
│   └── pre-commit  # 커밋 시 TAGS.md 자동 재생성
├── TAGS.md         # 태그 인덱스 (자동 생성)
└── README.md
```

## 프롬프트 파일 형식

```markdown
---
title: 프롬프트 제목
tags: [tag1, tag2]
version: 1
---

(프롬프트 본문)
```

## 태그로 찾기

[TAGS.md](TAGS.md)에서 태그별 프롬프트 목록을 확인하세요.

또는 직접 검색:

```bash
grep -r "tags:.*security" prompts/
```

## 새 프롬프트 추가 방법

1. `prompts/` 에 `kebab-case.md` 파일 생성
2. frontmatter 작성 (`title`, `tags`, `version`)
3. Commit — TAGS.md는 자동 재생성됨

## 최초 셋업 (clone 후 1회)

```bash
git config core.hooksPath .githooks
```
