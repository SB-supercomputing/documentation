#!/usr/bin/env python3
"""Dress the built feeds after mkdocs runs.

mkdocs-rss-plugin writes the page feeds and offers no stylesheet hook and
no way to leave one page out, so this runs after the build: it points
each feed at its stylesheet (the human-readable view written beside it)
and removes the landing page's entry, which would otherwise top the
updated feed on every change because the generator dates it by the
newest source.

    python tools/style_feeds.py

No feeds is not an error: a build without a site address, as check.sh and
the a11y job run it, writes none, and there is nothing to dress.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "docs-site" / "site"
# Each feed's own view: the notices' channel carries its items' lines, so
# it gets the variant stylesheet; the page feeds keep the plain
# title-and-date view.
STYLESHEET = {"feed_rss_announcements.xml": "announcements.xsl"}


def pi(feed_name):
    """The stylesheet line a feed carries, pointing at its own view."""
    href = STYLESHEET.get(feed_name, "feed.xsl")
    return f'<?xml-stylesheet href="{href}" type="text/xsl"?>'


def site_root():
    """The address from the generated mkdocs.yml, with a trailing slash;
    the landing page's guid is exactly this."""
    cfg = (ROOT / "docs-site" / "mkdocs.yml").read_text(encoding="utf-8")
    m = re.search(r"^site_url:\s*(\S+)", cfg, re.M)
    return m.group(1).rstrip("/") + "/" if m else ""


def main():
    feeds = sorted(SITE.glob("feed_rss_*.xml"))
    if not feeds:
        print("style_feeds: no feeds to dress")
        return
    home = site_root()
    for feed in feeds:
        text = feed.read_text(encoding="utf-8")
        line = pi(feed.name)
        if line not in text:
            # The processing instruction belongs right after the XML
            # declaration, before anything a reader or validator parses.
            text = text.replace("?>", "?>\n" + line, 1)
        if home:
            def repl(m):
                return "" if f">{home}</guid>" in m.group(0) else m.group(0)
            text = re.sub(r"[ \t]*<item>.*?</item>\n?", repl, text, flags=re.S)
        kept = text.count("<item>")
        feed.write_text(text, encoding="utf-8")
        print(f"style_feeds: {feed.name}: stylesheet line, {kept} entries")


if __name__ == "__main__":
    main()
