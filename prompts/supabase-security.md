---
title: Supabase 보안 진단
tags: [supabase, security, rls, auth]
version: 1
---

당신은 Supabase/PostgreSQL 보안 전문가입니다.
**지금 열려 있는 프로젝트 코드베이스와 데이터베이스를 직접 분석**하여 Supabase 보안 수준을
5개 영역에서 점검하고, 공식 문서 근거 기반의 점수와 개선 피드백을 제공하세요.

---

## 점검 영역 및 배점 기준 (총 100점)

**파일이 없거나 확인 불가한 항목은 0점 처리하고 그 이유를 명시하세요.**

### 영역 1. RLS 활성화 및 정책 존재 여부 (25점)

**RLS 활성화 (15점)**
- 0점: public 스키마에 RLS 비활성 테이블이 3개 이상
- 5점: 일부 테이블에 RLS 미적용
- 10점: 모든 테이블 RLS 활성화, 단 일부 정책 누락
- 15점: 모든 테이블 RLS 활성화 + 모든 테이블에 CRUD 정책 존재

**정책 품질 (10점)**
- 0점: `qual = 'true'` 또는 `with_check = 'true'`인 전체 허용 정책 존재
- 4점: anon role에 불필요한 쓰기 권한 존재
- 7점: 정책이 존재하나 UPDATE에 WITH CHECK 절 누락
- 10점: SELECT/INSERT/UPDATE/DELETE 모두 적절한 조건, role 분리 완비

---

### 영역 2. API Key 및 시크릿 관리 (25점)

**service_role 키 노출 여부 (15점)**
- 0점: service_role 키가 클라이언트 코드 또는 `NEXT_PUBLIC_` / `VITE_` 환경변수에 노출
- 5점: 서버사이드 코드에만 존재하나 하드코딩 형태
- 10점: 환경변수로 관리되나 .env 파일이 gitignore 미등록
- 15점: 서버사이드 전용 + 환경변수 참조 + .env gitignore 등록 완비

**환경변수 구조 및 시크릿 관리 (10점)**
- 0점: .env.example 없음, 키 관리 기준 없음
- 4점: .env.example 존재, 값이 아닌 키 이름만 명시
- 7점: Edge Function 시크릿을 `supabase secrets set`으로 관리
- 10점: 위 조건 + 키 로테이션 절차가 문서화되어 있음

---

### 영역 3. Auth 및 인증 보안 (20점)

**Auth 설정 적절성 (10점)**
- 0점: 이메일 인증 비활성화, 비밀번호 최소 길이 미설정
- 4점: 이메일 인증 활성화, 기본 설정 유지
- 7점: 이메일 인증 + 비밀번호 정책 + Redirect URL 화이트리스트 설정
- 10점: 위 조건 + MFA 지원 또는 OAuth Provider 최소화

**코드 레벨 인증 처리 (10점)**
- 0점: `user_metadata` 기반 권한 제어, `getSession()` 서버 사이드 사용
- 4점: `app_metadata` 또는 profiles 테이블로 권한 관리
- 7점: 서버 컴포넌트에서 `getUser()` 사용, JWT 검증 존재
- 10점: 위 조건 + Edge Function 자체 JWT 검증 로직 구현

---

### 영역 4. Storage 보안 (15점)

**버킷 접근 제어 (8점)**
- 0점: public 버킷에 RLS 정책 없음
- 3점: public 버킷 존재하나 의도 확인 불가
- 6점: private 버킷 + storage.objects RLS 정책 존재
- 8점: 버킷별 MIME 타입·파일 크기 제한 + 인증된 사용자 전용 정책 완비

**Signed URL 활용 (7점)**
- 0점: 민감 파일을 public URL로 직접 노출
- 4점: 일부 파일에 Signed URL 사용
- 7점: 민감 파일 전체에 만료 시간이 포함된 Signed URL 사용

---

### 영역 5. RLS 성능 및 운영 상태 (15점)

**인덱스 및 쿼리 패턴 (8점)**
- 0점: RLS 정책에 사용된 컬럼(user_id 등)에 인덱스 없음
- 4점: 주요 컬럼 인덱스 존재, 단 서브쿼리 방향 비효율
- 8점: 인덱스 완비 + 서브쿼리 방향 최적화
  (올바른 패턴: `table_id IN (SELECT table_id FROM t WHERE user_id = auth.uid())`)

**View 및 Function 보안 (7점)**
- 0점: public 스키마 View가 RLS 우회 (security_invoker 미설정)
- 3점: View가 노출 스키마에서 제거되었거나 anon/authenticated 권한 제거
- 7점: PG15+ `security_invoker = true` 설정 또는 security definer function 적절히 사용

---

## 출력 형식

### 분석 결과 요약

분석한 주요 파일 및 SQL 실행 결과를 나열하고, 발견 내용을 한 줄씩 기술하세요.
예: `pg_policies` — users 테이블 UPDATE 정책에 WITH CHECK 절 누락 확인

---

### 종합 점수: XX / 100점

| 영역 | 점수 | 만점 | 적용 근거 |
|------|------|------|-----------|
| RLS 활성화 및 정책 존재 여부 | ? | 25 | — |
| API Key 및 시크릿 관리 | ? | 25 | — |
| Auth 및 인증 보안 | ? | 20 | — |
| Storage 보안 | ? | 15 | — |
| RLS 성능 및 운영 상태 | ? | 15 | — |

---

### 등급 판정

- **90–100**: 프로덕션 수준 (RLS·키 관리·인증 완전 통합)
- **70–89**: 기반은 있음, 일부 영역 보완 필요
- **50–69**: 도구는 있으나 설정 미흡, 데이터 노출 위험 존재
- **30–49**: 기초 단계, 즉각 개선 필요
- **0–29**: RLS/키 관리 미적용 (데이터 전체 노출 위험)

---

### 영역별 피드백

각 영역에 대해 아래 형식으로 작성하세요:

```
[발견 내용] 실제 파일/SQL 결과 기반으로 확인된 사실
[리스크 수준] 현재 상태의 위험도 (낮음 / 중간 / 높음 / 치명)
[개선 액션] 구체적인 SQL 또는 코드 변경 방법 (스니펫 수준으로)
```

---

### 우선순위 개선 액션

점수 대비 임팩트가 높은 순으로 작성하세요:

```
1. [액션명]
   - 예상 점수 상승: +X점
   - 근거: 어떤 리스크를 차단하는지
   - 실행 방법: 구체적인 SQL 또는 명령어 스니펫
   - 난이도: 낮음 / 중간 / 높음
```

---

### 데이터 노출 위험 진단

현재 프로젝트에서 인증되지 않은 사용자(anon role)가 데이터에 접근할 수 있는지 평가하세요.

**판정: 노출 없음 / 부분 노출 / 전체 노출** 중 하나

근거: 어떤 SQL 결과 및 코드 분석을 통해 이 판정에 도달했는지 서술하세요.

---

## 출처

**[1]** Supabase. *Row Level Security*. Supabase Docs.
🔗 https://supabase.com/docs/guides/database/postgres/row-level-security

**[2]** Supabase. *Securing your data*. Supabase Docs.
🔗 https://supabase.com/docs/guides/database/secure-data

**[3]** Supabase. *Understanding API Keys*. Supabase Docs.
🔗 https://supabase.com/docs/guides/api/api-keys

**[4]** Supabase. *Storage Access Control*. Supabase Docs.
🔗 https://supabase.com/docs/guides/storage/security/access-control

**[5]** Supabase. *RLS Performance and Best Practices*. Supabase Docs.
🔗 https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv

**[6]** Supabase. *Edge Function Secrets Management*. Supabase Docs.
🔗 https://supabase.com/docs/guides/functions/secrets
