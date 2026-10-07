#!/usr/bin/env python3
"""블로그 영어판(/en/blog/)을 한국어 원본(/blog/)에서 생성한다.

원본 글은 한 파일 안에 .ko-only / .en-only 를 함께 담고 있다. 검색엔진은 URL 하나를
한 언어로만 색인하므로, 영어판은 별도 URL 로 떼어 낸다.

  - .ko-only 요소를 제거하고 <html lang="en" data-lang-fixed="en"> 으로 고정
  - <head> 의 title·description·OG·canonical·JSON-LD 를 영어로 교체
    (영어 문구는 scripts/blog-en-meta.json)
  - 내부 블로그 링크를 /en/blog/ 로 바꿈
  - 원본·영어판 양쪽에 hreflang(ko/en/x-default) 을 넣고, sitemap.xml 에 영어판 URL 추가

글을 고치거나 새 글을 추가하면 blog-en-meta.json 을 채운 뒤 `make en-blog` 를 다시 돌린다.
"""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://yiyol.com"
META = json.loads((ROOT / "scripts/blog-en-meta.json").read_text(encoding="utf-8"))

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "source", "track", "wbr"}


def ko_url(slug):
    return f"{SITE}/blog/" if slug == "index" else f"{SITE}/blog/{slug}.html"


def en_url(slug):
    return f"{SITE}/en/blog/" if slug == "index" else f"{SITE}/en/blog/{slug}.html"


def slug_of(url):
    m = re.match(re.escape(SITE) + r"/blog/(?:([\w-]+)\.html)?$", url)
    return (m.group(1) or "index") if m else None


class StripKoOnly(HTMLParser):
    """class 에 ko-only 가 있는 요소를 통째로 지우고 나머지는 원문 그대로 다시 쓴다."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.skip = 0  # ko-only 요소 안에서의 열린 태그 깊이

    def emit(self, s):
        if not self.skip:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag not in VOID:
                self.skip += 1
            return
        classes = (dict(attrs).get("class") or "").split()
        if "ko-only" in classes:
            if tag not in VOID:
                self.skip = 1
            return
        self.out.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if not self.skip and "ko-only" not in (dict(attrs).get("class") or "").split():
            self.out.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.skip:
            if tag not in VOID:
                self.skip -= 1
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, d): self.emit(d)
    def handle_entityref(self, n): self.emit(f"&{n};")
    def handle_charref(self, n): self.emit(f"&#{n};")
    def handle_comment(self, d): self.emit(f"<!--{d}-->")
    def handle_decl(self, d): self.emit(f"<!{d}>")
    def handle_pi(self, d): self.emit(f"<?{d}>")


def strip_ko_only(html):
    p = StripKoOnly()
    p.feed(html)
    p.close()
    return "".join(p.out)


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def hreflang_block(slug, indent):
    lines = [
        "<!-- hreflang:start -->",
        f'<link rel="alternate" hreflang="ko" href="{ko_url(slug)}" />',
        f'<link rel="alternate" hreflang="en" href="{en_url(slug)}" />',
        f'<link rel="alternate" hreflang="x-default" href="{ko_url(slug)}" />',
        "<!-- hreflang:end -->",
    ]
    return ("\n" + indent).join(lines)


def put_hreflang(html, slug):
    html = re.sub(r"[ \t]*<!-- hreflang:start -->.*?<!-- hreflang:end -->\n", "", html, flags=re.S)
    m = re.search(r"\n([ \t]*)<link rel=\"canonical\"", html)
    indent = m.group(1)
    return html[:m.start() + 1] + indent + hreflang_block(slug, indent) + "\n" + html[m.start() + 1:]


def set_meta(html, attr, name, value):
    pat = re.compile(rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*(")')
    if not pat.search(html):
        return html
    return pat.sub(lambda m: m.group(1) + esc(value) + m.group(2), html, count=1)


def translate_ld(d, slug, meta):
    t = d.get("@type")
    if t in ("BlogPosting", "WebApplication"):
        d["headline" if t == "BlogPosting" else "name"] = meta["title"]
        d["description"] = meta["description"]
        d["url"] = en_url(slug)
        if "keywords" in d:
            d["keywords"] = meta["keywords"]
        d["inLanguage"] = "en"
        d["translationOfWork"] = {"@id": ko_url(slug)}
    elif t == "BreadcrumbList":
        items = d["itemListElement"]
        for it in items:
            s = slug_of(it.get("item", ""))
            if s:
                it["item"] = en_url(s)
            if s == "index":
                it["name"] = "Blog"
        if slug != "index":
            items[-1]["name"] = meta["title"]
    elif t == "FAQPage":
        d["mainEntity"] = [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in meta["faq"]
        ]
    elif t == "Blog":
        d["name"] = "YIYOL Blog"
        d["description"] = meta["description"]
        d["url"] = en_url("index")
        d["inLanguage"] = "en"
        for p in d.get("blogPost", []):
            s = slug_of(p.get("url", ""))
            if s in META:
                p["headline"] = META[s]["title"]
                p["description"] = META[s]["description"]
                p["url"] = en_url(s)
                if "inLanguage" in p:
                    p["inLanguage"] = "en"
                if "keywords" in p:
                    p["keywords"] = META[s]["keywords"]
    elif t == "ItemList":
        d["name"] = "YIYOL Blog posts"
        for it in d["itemListElement"]:
            s = slug_of(it.get("url", "") or it.get("item", {}).get("url", ""))
            if s in META:
                if "url" in it:
                    it["url"] = en_url(s)
                if "name" in it:
                    it["name"] = META[s]["title"]
                if isinstance(it.get("item"), dict):
                    it["item"]["url"] = en_url(s)
                    for k in ("name", "headline"):
                        if k in it["item"]:
                            it["item"][k] = META[s]["title"]
    return d


def replace_ld(html, slug, meta):
    def sub(m):
        d = translate_ld(json.loads(m.group(2)), slug, meta)
        body = json.dumps(d, ensure_ascii=False, indent=2)
        ind = m.group(1)
        return f'{ind}<script type="application/ld+json">\n' + "\n".join(
            ind + "  " + line for line in body.splitlines()) + f"\n{ind}</script>"
    return re.sub(r'([ \t]*)<script type="application/ld\+json">(.*?)</script>', sub, html, flags=re.S)


def build_en(src_html, slug):
    meta = META[slug]
    html = strip_ko_only(src_html)
    html = re.sub(r'<html lang="ko"[^>]*>', '<html lang="en" data-lang-fixed="en">', html, count=1)

    suffix = "" if slug == "index" else " - YIYOL Blog"
    title = meta["title"] + suffix
    social_title = meta["title"] if slug == "index" else meta["title"] + " — YIYOL"
    html = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(title)}</title>", html, count=1, flags=re.S)
    html = set_meta(html, "name", "description", meta["description"])
    html = set_meta(html, "name", "keywords", ",".join(meta["keywords"]))
    html = set_meta(html, "property", "og:url", en_url(slug))
    html = set_meta(html, "property", "og:title", social_title)
    html = set_meta(html, "property", "og:description", meta["description"])
    html = set_meta(html, "name", "twitter:title", social_title)
    html = set_meta(html, "name", "twitter:description", meta["description"])
    html = re.sub(r'(<link rel="canonical" href=")[^"]*(")', rf"\g<1>{en_url(slug)}\2", html, count=1)
    if 'property="og:locale"' not in html:
        html = re.sub(r'(\n([ \t]*)<meta property="og:site_name"[^>]*>)',
                      r'\1\n\2<meta property="og:locale" content="en_US" />\n\2<meta property="og:locale:alternate" content="ko_KR" />',
                      html, count=1)
    html = replace_ld(html, slug, meta)
    html = html.replace('href="/blog/', 'href="/en/blog/')
    html = html.replace('<span class="lang-current">한국어</span>', '<span class="lang-current">English</span>')
    # 계산기의 <option> 은 JS 가 data-ko/data-en 으로 바꿔 끼운다. 정적 HTML 에도 영어가 보이게 한다.
    html = re.sub(r'(<option [^>]*data-en="([^"]*)"[^>]*>)[^<]*(</option>)', r'\1\2\3', html)
    return put_hreflang(html, slug)


def update_sitemap(slugs):
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    for slug in slugs:
        ko, en = ko_url(slug), en_url(slug)
        alts = (f'    <xhtml:link rel="alternate" hreflang="ko" href="{ko}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ko}"/>\n')
        # 기존 대체 링크를 지우고 다시 넣어 여러 번 돌려도 같은 결과가 나오게 한다.
        xml = re.sub(rf"(  <url>\n    <loc>({re.escape(ko)}|{re.escape(en)})</loc>\n(?:(?!</url>).)*?)"
                     r"(?:    <xhtml:link[^\n]*\n)+(  </url>)", r"\1\3", xml, flags=re.S)
        m = re.search(rf"  <url>\n    <loc>{re.escape(ko)}</loc>\n(.*?)  </url>\n", xml, re.S)
        if not m:
            raise SystemExit(f"sitemap.xml 에 {ko} 항목이 없다. 먼저 추가할 것.")
        ko_block = f"  <url>\n    <loc>{ko}</loc>\n{m.group(1)}{alts}  </url>\n"
        xml = xml[:m.start()] + ko_block + xml[m.end():]
        en_pat = re.compile(rf"  <url>\n    <loc>{re.escape(en)}</loc>\n.*?  </url>\n", re.S)
        en_block = f"  <url>\n    <loc>{en}</loc>\n{m.group(1)}{alts}  </url>\n"
        if en_pat.search(xml):
            xml = en_pat.sub(lambda _: en_block, xml, count=1)
        else:
            i = xml.index(ko_block) + len(ko_block)
            xml = xml[:i] + en_block + xml[i:]
    path.write_text(xml, encoding="utf-8")


def main():
    out_dir = ROOT / "en/blog"
    out_dir.mkdir(parents=True, exist_ok=True)
    for slug in META:
        src = ROOT / "blog" / f"{slug}.html"
        html = src.read_text(encoding="utf-8")
        # 한국어 URL 은 한국어로 고정한다. 영어 브라우저로 렌더링하는 검색 봇이
        # 한국어 URL 을 영어 페이지로 색인하지 않게 하기 위해서다.
        ko_html = re.sub(r'<html lang="ko"[^>]*>', '<html lang="ko" data-lang-fixed="ko">', html, count=1)
        ko_html = put_hreflang(ko_html, slug)
        if ko_html != html:
            src.write_text(ko_html, encoding="utf-8")
        (out_dir / f"{slug}.html").write_text(build_en(ko_html, slug), encoding="utf-8")
        print(f"en/blog/{slug}.html")
    update_sitemap(list(META))
    print("sitemap.xml")


if __name__ == "__main__":
    main()
