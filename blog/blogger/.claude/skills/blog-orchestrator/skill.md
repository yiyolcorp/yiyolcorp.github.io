---
name: blog-orchestrator
description: "블로그 포스트 작성 파이프라인을 조율하는 오케스트레이터. 사용자가 블로그 주제를 제시하면 리서치 → 포스트 작성 → SEO 최적화 → HTML 퍼블리싱 순서로 에이전트를 실행하여 최종 HTML 블로그 포스트를 생성한다. '블로그 작성', '블로그 써줘', '포스트 작성', '글 써줘', '블로그 주제' 등을 언급하면 반드시 이 스킬을 사용할 것."
---

# Blog Orchestrator

블로그 포스트 작성 에이전트 파이프라인을 조율하여 최종 SEO 최적화된 HTML 포스트를 생성하고 사이트에 배포하는 통합 스킬.

## 실행 모드: 서브 에이전트

순차 의존이 강한 파이프라인이므로 서브 에이전트 모드를 사용한다. 각 에이전트의 출력이 다음 에이전트의 입력이 되며, 에이전트 간 실시간 통신은 불필요하다.

## 에이전트 구성

| 에이전트 | subagent_type | 역할 | 스킬 | 출력 |
|---------|--------------|------|------|------|
| searcher | searcher | 웹 리서치 | search | `_workspace/01_searcher_results.md` |
| post-writer | post-writer | 포스트 작성 | write-post | `_workspace/02_post-writer_draft.md` |
| seo-writer | seo-writer | SEO 최적화 | seo-optimize | `blog/{slug}.md` |
| publisher | publisher | HTML 퍼블리싱 | publish | `../{slug}.html` + `../index.html` 업데이트 |

## 워크플로우

### Phase 1: 준비
1. 사용자 입력에서 블로그 주제를 파악한다
2. 프로젝트 루트에 `_workspace/` 디렉토리를 생성한다
3. `blog/` 디렉토리가 없으면 생성한다

### Phase 2: 리서치 (Searcher)

Searcher 에이전트를 실행하여 주제에 대한 웹 리서치를 수행한다.

```
Agent(
  description: "블로그 리서치 수행",
  prompt: "당신은 블로그 리서치 전문가입니다.
    에이전트 정의: .claude/agents/searcher.md를 읽고 역할과 원칙을 따르라.
    스킬: .claude/skills/search/skill.md를 읽고 워크플로우를 따르라.
    주제: {사용자가 제시한 주제}
    출력: _workspace/01_searcher_results.md에 리서치 결과를 저장하라.",
  subagent_type: "searcher",
  model: "opus"
)
```

**완료 확인:** `_workspace/01_searcher_results.md` 파일이 생성되었는지 확인. 파일이 없거나 내용이 부족하면 1회 재시도.

### Phase 3: 포스트 작성 (Post Writer)

Post Writer 에이전트를 실행하여 리서치 결과 기반 포스트를 작성한다.

```
Agent(
  description: "블로그 포스트 작성",
  prompt: "당신은 블로그 콘텐츠 작성 전문가입니다.
    에이전트 정의: .claude/agents/post-writer.md를 읽고 역할과 원칙을 따르라.
    스킬: .claude/skills/write-post/skill.md를 읽고 워크플로우를 따르라.
    리서치 결과: _workspace/01_searcher_results.md를 읽어라.
    출력: _workspace/02_post-writer_draft.md에 포스트 초안을 저장하라.",
  subagent_type: "post-writer",
  model: "opus"
)
```

**완료 확인:** `_workspace/02_post-writer_draft.md` 파일이 생성되었는지 확인.

### Phase 4: SEO 최적화 (SEO Writer)

SEO Writer 에이전트를 실행하여 포스트를 최적화하고 최종 파일을 생성한다.

```
Agent(
  description: "SEO 최적화 수행",
  prompt: "당신은 SEO 최적화 전문가입니다.
    에이전트 정의: .claude/agents/seo-writer.md를 읽고 역할과 원칙을 따르라.
    스킬: .claude/skills/seo-optimize/skill.md를 읽고 워크플로우를 따르라.
    리서치 결과: _workspace/01_searcher_results.md를 읽어라 (키워드, 트렌드 정보).
    포스트 초안: _workspace/02_post-writer_draft.md를 읽어라.
    출력: blog/{slug}.md에 최종 SEO 최적화된 포스트를 저장하라.
    blog/ 디렉토리가 없으면 생성하라.",
  subagent_type: "seo-writer",
  model: "opus"
)
```

**완료 확인:** `blog/` 디렉토리에 새 `.md` 파일이 생성되었는지 확인. 생성된 파일의 slug를 기록한다.

### Phase 5: HTML 퍼블리싱 (Publisher)

Publisher 에이전트를 실행하여 마크다운을 HTML로 렌더링하고 블로그 인덱스에 등록한다.

```
Agent(
  description: "블로그 HTML 퍼블리싱",
  prompt: "당신은 블로그 퍼블리싱 전문가입니다.
    에이전트 정의: .claude/agents/publisher.md를 읽고 역할과 원칙을 따르라.
    스킬: .claude/skills/publish/skill.md를 읽고 워크플로우를 따르라.
    대상 파일: blog/{slug}.md를 읽어라.
    참조: ../index.html을 읽어 사이트 구조와 기존 카드 패턴을 확인하라.
    출력:
      1. ../{slug}.html에 HTML로 렌더링된 블로그 포스트를 저장하라.
      2. ../index.html의 .blog-grid 맨 위에 새 카드를 추가하라.
      3. ../md/{slug}.md에 마크다운 원본을 복사하라.",
  subagent_type: "publisher",
  model: "opus"
)
```

**완료 확인:** `../{slug}.html` 파일이 생성되었는지, `../index.html`에 새 카드가 추가되었는지, `../md/{slug}.md`가 복사되었는지 확인.

### Phase 6: 정리 및 보고
1. `_workspace/` 디렉토리 보존 (중간 산출물은 삭제하지 않음 — 사후 검증용)
2. 사용자에게 결과 요약 보고:
   - 마크다운 파일 경로: `blog/{slug}.md`
   - HTML 파일 경로: `../{slug}.html`
   - 마크다운 원본 보관: `../md/{slug}.md`
   - 포스트 제목
   - 타겟 키워드
   - 글자 수 / 예상 읽기 시간
   - 사이트 URL: `https://yiyol.com/blog/{slug}.html`
   - 인덱스 등록 여부

## 데이터 흐름

```
사용자 입력 (주제)
       ↓
  [Searcher] → _workspace/01_searcher_results.md
       ↓                    ↓
  [Post Writer]              ↓
       ↓                    ↓
  _workspace/02_post-writer_draft.md
       ↓                    ↓
  [SEO Writer] ←────────────┘
       ↓
  blog/{slug}.md
       ↓
  [Publisher]
       ↓
  ../{slug}.html + ../index.html 업데이트 + ../md/{slug}.md (최종 산출물)
```

## 에러 핸들링

| 상황 | 전략 |
|------|------|
| Searcher 실패 | 1회 재시도. 재실패 시 사용자에게 주제 변경 또는 직접 자료 제공 요청 |
| Post Writer 실패 | 1회 재시도. 재실패 시 리서치 결과만으로 간략한 포스트 직접 생성 |
| SEO Writer 실패 | 1회 재시도. 재실패 시 포스트 초안을 그대로 blog/에 저장 (SEO 미적용 명시) |
| Publisher 실패 | 1회 재시도. 재실패 시 마크다운 파일만 전달하고 HTML 미생성 명시 |
| 중간 파일 누락 | 해당 Phase 재실행 |
| blog/ 디렉토리 생성 실패 | 사용자에게 권한 확인 요청 |
| ../index.html 누락 | 사용자에게 경로 확인 요청 |

## 테스트 시나리오

### 정상 흐름
1. 사용자가 "Python 웹 스크래핑 입문 가이드" 주제 제시
2. Phase 1: `_workspace/` 생성
3. Phase 2: Searcher가 웹 스크래핑 관련 5개+ 소스에서 정보 수집 → `01_searcher_results.md`
4. Phase 3: Post Writer가 리서치 기반 1,500~3,000단어 포스트 작성 → `02_post-writer_draft.md`
5. Phase 4: SEO Writer가 키워드 최적화 + 메타 데이터 완성 → `blog/python-web-scraping-guide.md`
6. Phase 5: Publisher가 HTML 렌더링 → `../python-web-scraping-guide.html` + `../index.html` 카드 추가 + `../md/python-web-scraping-guide.md` 복사
7. Phase 6: 사용자에게 파일 경로, 제목, 키워드, 글자 수, 사이트 URL 보고

### 에러 흐름
1. Phase 2에서 Searcher가 검색 API 오류로 실패
2. 1회 재시도 → 성공
3. 나머지 Phase 정상 진행
4. 만약 재시도도 실패 → 사용자에게 "검색이 실패했습니다. 주제를 구체화하거나 참고 자료를 직접 제공해 주세요." 안내
