#!/usr/bin/env python3
"""Check every address the built site ships.

Internal links and images must resolve to files in the build; an anchor
must name an id that exists in the page it points at; an external
address must answer with redirects followed. The feeds ride along:
an absolute address carrying the site's own URL maps back onto the
build instead of the network, so a feed entry is checked against the
pages it was just built with.

    python tools/check_links.py [--site docs-site/site]

Nothing here knows about Markdown: it reads the built HTML and the
feeds, which is what a browser sees. Exits nonzero after listing every
break, so CI refuses to ship one.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (compatible; sbsc-docs-linkcheck/1.0)"}
# Some sites answer a script with 404 or 5xx and a browser with the page;
# an address is called broken only after it fails a browser's request too.
BROWSER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
SKIPPED = ("mailto:", "tel:", "data:", "javascript:")
# Hosts reachable only from inside the hospital network (ClinWulf's
# portal, linked from the ported RCI pages); from anywhere else they
# never answer, so the check reports them instead of failing on them.
PRIVATE = (".uhmc.sbuh.stonybrook.edu",)


class Collector(HTMLParser):
    """Every href and src a page carries, in document order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.values = []

    def handle_starttag(self, tag, attrs):
        wanted = "href" if tag == "a" else "src"
        for name, value in attrs:
            if name == wanted and value:
                self.values.append(value)


def configured_site_url():
    """The site's own address from the generated config, if the build
    knows one; links carrying it belong to this build, not the network."""
    cfg = ROOT / "docs-site" / "mkdocs.yml"
    if not cfg.exists():
        return ""
    m = re.search(r"^site_url:\s*(\S+)", cfg.read_text(encoding="utf-8"), re.M)
    return m.group(1).rstrip("/") if m else ""


def ids_of(html_text):
    return set(re.findall(r'\bid="([^"]+)"', html_text))


def file_for(site: pathlib.Path, base: pathlib.Path, value: str):
    """The file an address lands on, directory URLs and all, resolved
    from base (the page's own directory, or the site root for absolute
    tails). None when it leaves the build or matches nothing."""
    tail = urllib.parse.unquote(value.split("#", 1)[0].split("?", 1)[0]).lstrip("/")
    if not tail:
        return None
    path = (base / tail).resolve()
    try:
        path.relative_to(site.resolve())
    except ValueError:
        return None
    if path.is_dir():
        return path / "index.html"
    return path if path.is_file() else None


def fetch(url, headers=UA, methods=("HEAD", "GET")):
    """One address's status, HEAD first and GET when refused. None when
    the network never answers, which is a retry, not a verdict."""
    for method in methods:
        req = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.status
        except urllib.error.HTTPError as err:
            if method == "HEAD" and err.code in (403, 405, 501):
                continue
            return err.code
        except (urllib.error.URLError, TimeoutError, OSError):
            return None
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="docs-site/site",
                    help="the built tree to read (default: docs-site/site)")
    args = ap.parse_args()
    site = (ROOT / args.site).resolve()
    if not site.is_dir():
        sys.exit(f"check_links: {site} does not exist; build first")

    home = configured_site_url()
    broken = []
    seen_external = {}

    pages = sorted(site.rglob("*.html"))
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        ids = ids_of(text)
        parser = Collector()
        parser.feed(text)
        for value in parser.values:
            if value.startswith(SKIPPED):
                continue
            if value.startswith("#"):
                frag = value[1:]
                if frag and frag not in ids:
                    broken.append((page, f"anchor #{frag} names nothing on the page"))
                continue
            if value.startswith(("http://", "https://")):
                if home and value.startswith(home + "/"):
                    target = file_for(site, site, value[len(home):])
                    if target is None:
                        broken.append((page, f"site address with no file behind it: {value}"))
                    continue
                url = value.split("#", 1)[0]
                if url not in seen_external:
                    seen_external[url] = None
                continue
            # A relative address: it must land on a file, and its anchor,
            # when it carries one, must exist there. Root-relative ones
            # (a leading slash) carry the deployment's path prefix when
            # the build knows one.
            if value.startswith("/"):
                prefix = "/" + home.rstrip("/").split("/", 3)[-1] if home.count("/") >= 3 else ""
                if prefix and value.startswith(prefix):
                    value = value[len(prefix):]
                target = file_for(site, site, value.lstrip("/"))
            else:
                target = file_for(site, page.parent, value)
            if target is None:
                broken.append((page, f"no file at {value}"))
                continue
            frag = value.split("#", 1)[1] if "#" in value else ""
            if frag and frag not in ids_of(target.read_text(encoding="utf-8", errors="replace")):
                broken.append((page, f"anchor #{frag} names nothing in {value}"))

    feeds = sorted(site.glob("*.xml"))
    for feed in feeds:
        text = feed.read_text(encoding="utf-8", errors="replace")
        for url in sorted(set(re.findall(r"https?://[^<>\"\s]+", text))):
            if home and url.rstrip("/") == home:
                continue
            if home and url.startswith(home + "/"):
                if file_for(site, site, url[len(home):]) is None:
                    broken.append((feed, f"site address with no file behind it: {url}"))
                continue
            if url not in seen_external:
                seen_external[url] = None

    checked = 0
    refused, signin, private = [], [], []
    for url in sorted(seen_external):
        host = urllib.parse.urlsplit(url).hostname or ""
        if host.endswith(PRIVATE):
            private.append(url)
            continue
        status = None
        for attempt in (1, 2):
            status = fetch(url)
            if status is not None and status < 500 and status != 429:
                break
            time.sleep(2 * attempt)
        if status is None or (status >= 400 and status not in (401, 403)):
            status = fetch(url, BROWSER, ("GET",)) or status
        checked += 1
        # Some sites (MathWorks, ACM, and the journal publishers among
        # them) turn away any scripted client, live or dead alike, with
        # 403, 405, or 429; that is a refusal to say, not a no.
        if status in (403, 405, 429, 999):
            refused.append(url)
        # A portal behind a sign-in (the OnDemand sites) answers 401: the
        # server is there and the address is its own, which is all a link
        # can promise a reader who is not signed in yet.
        elif status == 401:
            signin.append(url)
        elif status is None or status >= 400:
            broken.append((None, f"external address answers {status}: {url}"))

    for page, why in broken:
        if page is None:
            where = "network"
        else:
            try:
                where = str(page.relative_to(ROOT))
            except ValueError:
                where = str(page)
        print(f"check_links: BROKEN {where}: {why}")
    for url in refused:
        print(f"check_links: not machine-checkable (server refuses scripts): {url}")
    for url in signin:
        print(f"check_links: not machine-checkable (sign-in required): {url}")
    for url in private:
        print(f"check_links: not machine-checkable (private network): {url}")
    print(f"check_links: {len(pages)} pages, {len(feeds)} feeds, "
          f"{checked} external addresses checked, {len(broken)} broken")
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
