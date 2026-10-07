.PHONY: run sync-api en-blog

# NOX 저장소 위치. 다른 곳에 있으면 make sync-api NOX_DIR=... 로 덮어쓴다.
NOX_DIR ?= ../nox/nox

run:
	python3 -m http.server 18000

# NOX API 문서를 사이트의 /api/ 로 동기화한다.
# 문서를 새로 뽑을 때는 NOX 저장소에서 SITE_URL 을 반드시 준다. 안 주면 canonical·
# OpenGraph·JSON-LD 같은 검색 메타가 빠진 오프라인용 산출물이 그대로 덮인다.
#
#   cd $(NOX_DIR) && make apidoc SITE_URL=https://yiyol.com/api/
#   make sync-api
sync-api:
	rsync -a --delete $(NOX_DIR)/dist/api-docs/ api/
	@grep -q 'rel="canonical" href="https://yiyol.com/api/"' api/index.html \
	  || { echo "오류: 동기화된 문서에 canonical 이 없다. NOX 저장소에서"; \
	       echo "      make apidoc SITE_URL=https://yiyol.com/api/ 로 다시 뽑아라."; exit 1; }
	@echo "동기화 완료 — 검색 메타 확인됨. sitemap.xml 의 API 항목 lastmod 도 함께 갱신할 것."

# 블로그 영어판(/en/blog/)·hreflang·sitemap 을 한국어 원본에서 다시 만든다.
# 글을 고치거나 새 글을 추가하면 scripts/blog-en-meta.json 을 채우고 돌릴 것.
en-blog:
	python3 scripts/build_en_blog.py
