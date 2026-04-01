# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blogger is an AI-powered blog post generation pipeline. It uses a harness of four specialized agents to produce SEO-optimized blog posts, render them as HTML, and deploy to the site.

## Architecture

**Pipeline pattern (sub-agent mode):**

```
User topic → [Searcher] → [Post Writer] → [SEO Writer] → [Publisher] → ../{slug}.html
```

1. **Searcher** — performs web research, collects sources, keywords, and trends
2. **Post Writer** — transforms research into a reader-friendly blog post draft
3. **SEO Writer** — optimizes the draft for search engines and produces the final markdown
4. **Publisher** — renders markdown to HTML, deploys to `../`, and registers in `../index.html`

Intermediate artifacts are stored in `_workspace/`. Final markdown goes to `blog/`. Published HTML goes to `../` (parent blog directory).

## Harness Structure

- `.claude/agents/` — agent definitions (searcher, post-writer, seo-writer, publisher)
- `.claude/skills/` — skill definitions (search, write-post, seo-optimize, publish, blog-orchestrator)
- `blog-orchestrator` is the entry-point skill that coordinates the full pipeline

## Usage

Trigger the pipeline by mentioning blog writing (e.g., "블로그 써줘: {topic}"). The `blog-orchestrator` skill will run the four agents sequentially with `model: "opus"`.
