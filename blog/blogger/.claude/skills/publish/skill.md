---
name: publish
description: "SEO 최적화된 마크다운 블로그 포스트를 HTML로 렌더링하여 사이트에 배포하고, 블로그 인덱스에 카드를 추가한다. 블로그 발행, HTML 변환, 퍼블리싱에 사용."
---

# Publish — 블로그 퍼블리싱 스킬

최종 마크다운 포스트를 사이트에 맞는 HTML로 변환하여 배포하고, 블로그 인덱스 페이지에 등록하는 스킬.

## 워크플로우

### 1. 입력 파싱

`blog/{slug}.md` 파일을 읽고 다음을 추출한다:

**YAML frontmatter:**
- `title`: 포스트 제목
- `description`: 메타 디스크립션
- `date`: 발행일 (YYYY-MM-DD)
- `tags`: 태그 목록
- `slug`: URL 슬러그
- `keywords`: SEO 키워드 목록

**마크다운 본문:** frontmatter 이후의 전체 내용

### 2. 참조 파일 읽기

사이트 디자인 일관성을 위해 다음을 읽는다:
- `../index.html` — 공통 header, footer, 스타일 시스템 확인
- 기존 HTML 포스트가 있으면 참조 (스타일 패턴 확인)

### 3. 마크다운 → HTML 변환

마크다운 본문을 시맨틱 HTML로 변환한다:

| Markdown | HTML |
|----------|------|
| `# 제목` | `<h1>` (포스트에서는 히어로에 표시하므로 본문에서 제거) |
| `## 소제목` | `<h2>` |
| `### 소제목` | `<h3>` |
| 문단 | `<p>` |
| `- 항목` | `<ul><li>` |
| `1. 항목` | `<ol><li>` |
| `**굵게**` | `<strong>` |
| `*기울임*` | `<em>` |
| `` `코드` `` | `<code>` |
| 코드 블록 | `<pre><code>` |
| `> 인용` | `<blockquote>` |
| `[텍스트](URL)` | `<a href="URL" target="_blank" rel="noopener">` |
| 테이블 | `<table>` with `<thead>`, `<tbody>` |
| `---` (수평선) | `<hr>` |

**주의사항:**
- 본문의 첫 번째 `# 제목`은 히어로 영역에 표시하므로 본문 HTML에서 제거한다
- 외부 링크에는 `target="_blank" rel="noopener"` 추가
- 코드 블록에 언어가 지정되어 있으면 `<code class="language-{lang}">` 적용

### 4. HTML 페이지 생성

`../{slug}.html`에 다음 구조의 완전한 HTML 페이지를 Write한다:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <!-- Google Analytics (G-CKJ4GX2KHS) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-CKJ4GX2KHS"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-CKJ4GX2KHS');
  </script>

  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>{title} - YIYOL Blog</title>

  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords를 쉼표로 연결}" />

  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://yiyol.com/blog/{slug}.html" />
  <meta property="og:title" content="{title} — YIYOL" />
  <meta property="og:description" content="{description}" />
  <meta property="og:site_name" content="YIYOL" />

  <link rel="canonical" href="https://yiyol.com/blog/{slug}.html" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />

  <!-- Fonts & CSS -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <link rel="stylesheet" href="/assets/css/style.css" />

  <style>
    /* Post Hero */
    .post-hero {
      padding: 130px 0 50px;
      background: radial-gradient(circle at top right, #1e293b, #0f172a);
      color: white;
      text-align: center;
      position: relative;
      overflow: hidden;
    }
    .post-hero::before {
      content: '';
      position: absolute;
      top: -50%; right: -20%;
      width: 80%; height: 200%;
      background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 60%);
      pointer-events: none;
    }
    .post-hero-content {
      position: relative;
      z-index: 1;
      max-width: 800px;
      margin: 0 auto;
      padding: 0 2rem;
    }
    .post-breadcrumb {
      margin-bottom: 1rem;
      font-size: 0.85rem;
    }
    .post-breadcrumb a {
      color: #60a5fa;
      text-decoration: none;
    }
    .post-breadcrumb a:hover { text-decoration: underline; }
    .post-breadcrumb span { color: #64748b; margin: 0 0.4rem; }
    .post-hero h1 {
      font-family: 'Poppins', sans-serif;
      font-size: clamp(1.5rem, 3.5vw, 2.2rem);
      font-weight: 800;
      color: #fff;
      margin-bottom: 1rem;
      line-height: 1.4;
    }
    .post-meta {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 1rem;
      flex-wrap: wrap;
      font-size: 0.85rem;
      color: #94a3b8;
    }
    .post-meta-date { display: inline-flex; align-items: center; gap: 0.4rem; }
    .post-meta-date i { font-size: 0.8rem; }
    .post-tags { display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center; }
    .post-tag {
      font-size: 0.7rem;
      font-weight: 600;
      letter-spacing: 0.03em;
      color: #60a5fa;
      background: rgba(59,130,246,0.15);
      padding: 0.2rem 0.6rem;
      border-radius: 4px;
    }

    /* Post Content */
    .post-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 50px 2rem 100px;
    }
    .post-article {
      font-size: 1.05rem;
      line-height: 1.85;
      color: var(--text-color, #1e293b);
    }
    .post-article h2 {
      font-family: 'Poppins', sans-serif;
      font-size: 1.5rem;
      font-weight: 700;
      color: var(--primary-color, #0f172a);
      margin: 2.5rem 0 1rem;
      padding-bottom: 0.4rem;
      border-bottom: 2px solid var(--border-color, #e2e8f0);
    }
    .post-article h3 {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--primary-color, #0f172a);
      margin: 2rem 0 0.75rem;
    }
    .post-article p {
      margin-bottom: 1.2rem;
    }
    .post-article a {
      color: var(--accent-color, #3b82f6);
      text-decoration: underline;
      text-underline-offset: 2px;
    }
    .post-article a:hover { color: #2563eb; }
    .post-article ul, .post-article ol {
      margin: 1rem 0 1.5rem 1.5rem;
    }
    .post-article li {
      margin-bottom: 0.5rem;
    }
    .post-article table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.5rem 0;
      font-size: 0.95rem;
    }
    .post-article thead th {
      background: var(--bg-accent, #f8fafc);
      font-weight: 600;
      text-align: left;
      padding: 0.75rem 1rem;
      border-bottom: 2px solid var(--border-color, #e2e8f0);
    }
    .post-article tbody td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color, #e2e8f0);
    }
    .post-article pre {
      background: #0f172a;
      color: #e2e8f0;
      border-radius: 8px;
      padding: 1.25rem 1.5rem;
      overflow-x: auto;
      margin: 1.5rem 0;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .post-article code {
      font-family: 'SF Mono', 'Fira Code', monospace;
      font-size: 0.88em;
    }
    .post-article :not(pre) > code {
      background: rgba(59,130,246,0.08);
      color: #1e40af;
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
    }
    .post-article blockquote {
      border-left: 4px solid var(--accent-color, #3b82f6);
      background: var(--bg-accent, #f8fafc);
      margin: 1.5rem 0;
      padding: 1rem 1.5rem;
      border-radius: 0 8px 8px 0;
      color: var(--text-secondary, #475569);
    }
    .post-article blockquote p { margin-bottom: 0; }
    .post-article hr {
      border: none;
      border-top: 1px solid var(--border-color, #e2e8f0);
      margin: 2rem 0;
    }
    .post-article img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      margin: 1.5rem 0;
    }

    @media (max-width: 640px) {
      .post-container { padding: 30px 1rem 60px; }
      .post-article { font-size: 1rem; }
      .post-article h2 { font-size: 1.3rem; }
    }
  </style>
</head>
<body>
  <!-- Header: ../index.html에서 동일한 header 사용 -->
  <!-- Hero -->
  <section class="post-hero">
    <div class="post-hero-content">
      <nav class="post-breadcrumb">
        <a href="/">YIYOL</a><span>›</span><a href="/blog/">블로그</a><span>›</span> 현재 글
      </nav>
      <h1>{title}</h1>
      <div class="post-meta">
        <span class="post-meta-date"><i class="far fa-calendar-alt"></i> {YYYY.MM.DD}</span>
        <div class="post-tags">
          {태그별 <span class="post-tag">{tag}</span>}
        </div>
      </div>
    </div>
  </section>
  <!-- Main -->
  <main class="post-container">
    <article class="post-article">
      {변환된 HTML 본문}
    </article>
  </main>
  <!-- Footer: ../index.html에서 동일한 footer 사용 -->
</body>
</html>
```

### 5. 마크다운 원본 보관

`../md/` 디렉토리에 `{slug}.md`를 복사한다. 디렉토리가 없으면 생성한다.

### 6. 인덱스 카드 추가

`../index.html`을 읽고 `.blog-grid` 내부의 **첫 번째 위치**에 새 블로그 카드를 삽입한다.

**카드 삽입 위치:** `<div class="blog-grid">` 바로 다음 줄

**아이콘 선택 기준:**
포스트 주제의 키워드를 분석하여 적절한 Font Awesome 아이콘을 선택한다:
- 보안/인증: `fa-shield-halved`
- 개발/코딩: `fa-code`
- 네트워크: `fa-network-wired`
- 데이터/분석: `fa-chart-line`
- 가이드/튜토리얼: `fa-book`
- 클라우드: `fa-cloud`
- AI/머신러닝: `fa-brain`
- 도구/유틸리티: `fa-wrench`
- 기타: `fa-file-lines`

**카드 HTML:**
```html
<!-- Post: {title} -->
<a href="/blog/{slug}.html" class="blog-card" style="text-decoration:none;">
  <div class="blog-card-icon">
    <i class="fas {icon}"></i>
  </div>
  <div class="blog-card-body">
    <span class="blog-card-tag">{tags[0]}</span>
    <h2 class="blog-card-title ko-only">{title}</h2>
    <p class="blog-card-desc ko-only">{description}</p>
    <div class="blog-card-meta">
      <span>{YYYY.MM.DD}</span>
      <span class="blog-card-link">
        <span class="ko-only">읽기</span>
        <span class="en-only">Read</span>
        <i class="fas fa-arrow-right"></i>
      </span>
    </div>
  </div>
</a>
```

**중복 방지:** 삽입 전에 `../index.html`에 동일한 `{slug}.html` 링크가 이미 있는지 확인한다. 있으면 기존 카드를 새 카드로 교체한다.

### 7. 최종 검증

- `../{slug}.html` 파일이 생성되었는지 확인
- `../md/{slug}.md` 파일이 복사되었는지 확인
- `../index.html`에 새 카드가 추가되었는지 확인
- HTML이 올바른 구조인지 확인 (DOCTYPE, 닫는 태그 등)

## 품질 기준
- HTML이 `../index.html` 및 기존 HTML 포스트와 시각적 일관성을 유지
- Google Analytics 태그가 포함됨
- Open Graph 메타 태그가 올바르게 설정됨
- canonical URL이 `https://yiyol.com/blog/{slug}.html`로 설정됨
- 모든 외부 링크에 `target="_blank" rel="noopener"` 적용
- 반응형 디자인이 적용됨 (모바일 대응)
- 인덱스 카드의 날짜 형식이 기존 카드와 동일 (YYYY.MM.DD)
