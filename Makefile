.PHONY: run sync-api

# NOX 저장소 위치. 다른 곳에 있으면 make sync-api NOX_DIR=... 로 덮어쓴다.
NOX_DIR ?= ../nox/nox

run:
	python3 -m http.server 18000

# NOX API 문서를 사이트의 /api/ 로 동기화한다.
# 문서를 새로 뽑으려면 NOX 저장소에서 먼저 `make apidoc` 을 실행할 것.
sync-api:
	rsync -a --delete $(NOX_DIR)/dist/api-docs/ api/
