#!/usr/bin/env python3
"""Build the documentation site.

site.yaml decides what publishes and in what order; this script turns it
into an MkDocs (Material) site under docs-site/:

    python tools/build_docs.py [--site-url https://...]

GitHub alerts ("> [!NOTE]") become Material admonitions, and a link whose
target never publishes keeps its words and loses the link, so the strict
build never fails on a page still being written. The RSS feed dates come
from each source file's git history, stamped onto the generated copy as
frontmatter, because the copies themselves are never tracked. The
announcements under announcements/ carry their own dates, and their feed
is written here, since the plugin emits exactly the two page feeds.
"""
from __future__ import annotations

import argparse
import datetime
import pathlib
import re
import shutil
import subprocess
import sys
from email.utils import format_datetime
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs-site"
EASTERN = ZoneInfo("America/New_York")
HOME_LABEL = "SBSC Home"
ALERTS = {"NOTE": "note", "TIP": "tip", "IMPORTANT": "info", "WARNING": "warning", "CAUTION": "danger"}
ALERT_RE = re.compile(r"> \[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\n((?:>[^\n]*\n?)+)")
LINK_RE = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


class Node:
    """A page, or a heading over the pages under it (rel is None)."""

    def __init__(self, title, menu, rel, children):
        self.title, self.menu, self.rel, self.children = title, menu, rel, children


def read_tree():
    """site.yaml's settings and its tree of pages, in order, groups in
    place. The tree's first entry is the site's front page; it carries no
    source, since the build writes the landing from the tree itself."""
    site = yaml.safe_load((ROOT / "site.yaml").read_text(encoding="utf-8"))

    def walk(entries):
        nodes = []
        for entry in entries or []:
            if "group" in entry:
                nodes.append(Node(entry["group"], entry["group"], None, walk(entry.get("pages"))))
            elif "link" not in entry:
                source = entry.get("source")
                nodes.append(Node(entry["title"], entry.get("menu") or entry["title"],
                                  pathlib.PurePosixPath(source) if source else None,
                                  walk(entry.get("pages"))))
        return nodes

    return site, walk(site.get("pages"))


def all_pages(nodes):
    for node in nodes:
        if node.rel is not None:
            yield node
        yield from all_pages(node.children)


def page_url(page):
    """A page's local address in mkdocs's directory-URL form. An index or
    README stem names its directory, not a page of its own."""
    parts = page.rel.parts
    stem = parts[-1][:-3]
    if stem in ("index", "README"):
        return "/" + "/".join(parts[:-1]) + "/"
    return "/" + "/".join(parts[:-1] + (stem,)) + "/"


def git_dates():
    """Each source file's newest and oldest commit date, from one pass
    over the git log. The pages mkdocs compiles are generated copies that
    git never tracks, so their history is read here, from the sources, and
    stamped onto the copies as frontmatter for the feed plugin."""
    log = subprocess.run(
        ["git", "log", "--format=%x1e%aI", "--name-only", "--no-renames"],
        cwd=ROOT, capture_output=True, text=True)
    dates = {}
    if log.returncode != 0:
        return dates
    for chunk in log.stdout.split("\x1e")[1:]:
        lines = chunk.strip().splitlines()
        if not lines:
            continue
        iso = lines[0].strip()
        for path in lines[1:]:
            if path.strip():
                # The log runs newest first: the first sighting of a path
                # fixes its newest date, and the oldest wins the other slot.
                entry = dates.setdefault(path.strip(), [iso, iso])
                entry[1] = iso
    return dates


def as_yaml_scalar(text):
    """A sentence as a YAML double-quoted scalar, whatever finds its way
    into it. A colon in a plain scalar reads as a second key."""
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def with_dates(text, entry, blurb=""):
    """A copy's feed dates and description as frontmatter: the dates order
    the feeds, and the description keeps the feed items reading as prose
    instead of the page's raw markup. A page that arrives with its own
    frontmatter, or a checkout without git history, keeps its text as is."""
    if entry is None or text.startswith("---"):
        return text
    updated, created = entry
    desc = (f"description: {as_yaml_scalar(blurb)}\n"
            if blurb else "")
    return f"---\ndate: {created}\nupdated: {updated}\n{desc}---\n\n{text}"


def as_instant(value):
    """One comparable instant per notice: a date alone publishes at
    midnight Eastern, the center's own clock (and the plugin's
    default_timezone below); a timestamp keeps the offset it was
    written with."""
    if isinstance(value, datetime.datetime):
        return value
    return datetime.datetime(value.year, value.month, value.day,
                             tzinfo=EASTERN)


def parse_announcements():
    """The notices under announcements/, newest first: one file each,
    titled and dated by its frontmatter, because git history cannot
    know when a maintenance window is scheduled. Anything malformed
    stops the build naming the file."""
    items = []
    for path in sorted((ROOT / "announcements").glob("*.md")):
        def die(msg):
            sys.exit(f"announcements: {path.name}: {msg}")

        text = path.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not m:
            die("expected frontmatter: a --- block with title and date")
        try:
            meta = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            die("the frontmatter is not valid YAML")
        title = meta.get("title")
        if not isinstance(title, str) or not title.strip():
            die("frontmatter needs a title, a plain string")

        def stated(key):
            v = meta.get(key)
            if not isinstance(v, (datetime.date, datetime.datetime)):
                die(f"{key} is missing or quoted; write it unquoted, as "
                    f"{key}: 2026-11-24 or {key}: 2026-11-24T06:00:00-0500")
            if isinstance(v, datetime.datetime) and v.utcoffset() is None:
                die(f"a timestamp needs its UTC offset, as {key}: "
                    "2026-11-24T06:00:00-0500")
            return as_instant(v)

        when = stated("date")
        items.append({"title": title.strip(), "date": when,
                      "updated": stated("updated") if meta.get("updated") is not None else when,
                      "stem": path.stem, "body": text[m.end():]})
    items.sort(key=lambda it: (it["date"], it["stem"]), reverse=True)
    return items


def convert(text):
    def repl(m):
        kind = ALERTS.get(m.group(1), "note")
        body = m.group(2)
        lines = [(l[2:] if l.startswith("> ") else l[1:]) for l in body.splitlines()]
        indented = "\n".join(("    " + l) if l.strip() else l for l in lines)
        return f"!!! {kind}\n{indented}\n"

    return ALERT_RE.sub(repl, text)


def de_dead_links(text, page_rel, docs):
    """A link goes only to a page the tree publishes, or to a file that
    rides along (a picture); anything else keeps its words and loses the
    link, so a lesson still being written never breaks the build."""
    here = docs / page_rel

    def repl(m):
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        path = target.split("#", 1)[0]
        if not path:
            return m.group(0)
        resolved = (here.parent / path).resolve()
        try:
            resolved.relative_to(docs)
        except ValueError:
            return label
        return m.group(0) if resolved.exists() else label

    return LINK_RE.sub(repl, text)


def nav_entry(node):
    if node.rel is None:
        kids = [k for k in (nav_entry(c) for c in node.children) if k]
        return {node.menu: kids} if kids else None
    dest = "/".join(node.rel.parts)
    if node.children:
        kids = [k for k in (nav_entry(c) for c in node.children) if k]
        return {node.menu: [{node.menu: dest}] + kids}
    return {node.menu: dest}


def yaml_list(items, indent=0):
    out, pad = "", "  " * indent
    for item in items:
        if isinstance(item, dict):
            for k, v in item.items():
                if isinstance(v, list):
                    out += f"{pad}- {k}:\n" + yaml_list(v, indent + 1)
                else:
                    out += f"{pad}- {k}: {v}\n"
        else:
            out += f"{pad}- {item}\n"
    return out


def summary(rel):
    """A page's first plain sentence, whole, for the landing page's
    one-liners. Never cut: a landing page that trails off reads broken."""
    try:
        lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    if lines and lines[0].strip() == "---":
        # Frontmatter is not prose; the scan starts after it.
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    for line in lines:
        s = line.strip()
        if not s or s.startswith(("#", ">", "<", "!", "|", "-")) or s.startswith("[!"):
            continue
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
        s = re.sub(r"<[^>]+>", "", s)
        s = re.sub(r"[*_`]+", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            m = re.match(r"(.+?[.!?])(?:\s|$)", s)
            return m.group(1) if m else s
    return ""


def leaf_pages(node):
    for child in node.children:
        if child.rel is None:
            yield from leaf_pages(child)
        else:
            yield child


def landing(roots, notices):
    """The site's front page, from the tree: what the guide covers, a line
    per tutorial, and the reference pages, with the recent notices on
    top. Everything links to the page it names, and the build regenerates
    it, so the list never goes stale."""
    hub = roots[0]
    guide, subsections, reference = [], [], []
    for child in hub.children:
        if child.rel is None:
            # A section of nothing but reference pages lists under
            # Reference; anything else is a section in its own right.
            leaves = list(leaf_pages(child))
            if leaves and all(leaf.rel.parts[0] == "reference" for leaf in leaves):
                reference.extend(leaves)
            else:
                subsections.append(child)
            continue
        if child.children:
            subsections.append(child)
        elif child.rel.parts[0] == "reference":
            reference.append(child)
        else:
            guide.append(child)
    out = ["# Kitsune documentation", "",
           "Documentation for Kitsune, the Stony Brook Supercomputing Center's",
           "computing system. The guide sections are outlines; they fill in as",
           "Kitsune is deployed.", "",
           '<dl class="sbsc-specs">',
           "  <dt>Compute nodes</dt><dd>162</dd>",
           "  <dt>Processors</dt><dd>2x AMD EPYC 9965 per node</dd>",
           "  <dt>Cores</dt><dd>60,000+</dd>",
           "  <dt>Peak performance</dt><dd>6.7 PFLOPS, double precision</dd>",
           "  <dt>Storage</dt><dd>6 PB usable GPFS</dd>",
           "  <dt>Coming online</dt><dd>Q1 2027</dd>",
           "</dl>",
           "",
           "Funded by the National Science Foundation under award OAC-2505376.",
           ""]
    if notices:
        out += ["## Announcements", ""]
        for it in notices[:5]:
            rel = pathlib.PurePosixPath(f"announcements/{it['stem']}.md")
            out.append(f"- [{it['title']}]({'/'.join(rel.parts)}): {summary(rel)}")
        out += ["", "[All announcements](announcements/index.md)", ""]
    if guide:
        out += ["## System guide", ""]
        out += [f"- [{p.menu}]({'/'.join(p.rel.parts)}): {summary(p.rel)}" for p in guide]
        out.append("")
    for section in subsections:
        out += [f"## {section.menu}", ""]
        for leaf in leaf_pages(section):
            out.append(f"- [{leaf.menu}]({'/'.join(leaf.rel.parts)}): {summary(leaf.rel)}")
        out.append("")
    if reference:
        out += ["## Reference", ""]
        out += [f"- [{p.menu}]({'/'.join(p.rel.parts)}): {summary(p.rel)}" for p in reference]
        out.append("")
    return "\n".join(out)


def announcements_section(notices):
    """The navigation's Announcements branch: the index first, then the
    ten newest notices. The rest stay reachable from the index."""
    kids = [Node(it["title"], it["title"],
                 pathlib.PurePosixPath(f"announcements/{it['stem']}.md"), [])
            for it in notices[:10]]
    return nav_entry(Node("Announcements", "Announcements",
                          pathlib.PurePosixPath("announcements/index.md"), kids))


def announcements_index(notices):
    """The section's own page, generated like the landing: every notice,
    newest first, because the navigation and the front page carry only
    the recent ones."""
    out = ["# Announcements", "",
           "Scheduled maintenance, changes to queues or storage, and known",
           "problems land here, newest first. If the cluster behaves",
           "differently than these pages describe, check here before",
           "anything else.", ""]
    for it in notices:
        rel = pathlib.PurePosixPath(f"announcements/{it['stem']}.md")
        when = f"{it['date']:%B} {it['date'].day}, {it['date'].year}"
        out.append(f"- [{it['title']}]({it['stem']}.md) ({when}): {summary(rel)}")
    return "\n".join(out) + "\n"


def announcements_feed(notices, site_url, docs):
    """The notices' own channel. The plugin emits exactly two feeds, both
    page activity; announcements are authored content with a stated
    publish date, so this channel is the generator's to write."""
    base = site_url.rstrip("/")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
           "<channel>",
           "  <title>Kitsune announcements</title>",
           f"  <link>{escape(base + '/')}</link>",
           "  <description>Maintenance windows, software updates, and "
           "service notices for Kitsune.</description>",
           f'  <atom:link href="{escape(base)}/feed_rss_announcements.xml" '
           'rel="self" type="application/rss+xml"/>',
           "  <language>en</language>",
           f"  <lastBuildDate>{format_datetime(notices[0]['date'])}</lastBuildDate>"]
    for it in notices[:20]:
        link = f"{base}/announcements/{it['stem']}/"
        blurb = summary(pathlib.PurePosixPath(f"announcements/{it['stem']}.md"))
        out += ["  <item>",
                f"    <title>{escape(it['title'])}</title>",
                f"    <link>{escape(link)}</link>",
                f'    <guid isPermaLink="true">{escape(link)}</guid>',
                f"    <pubDate>{format_datetime(it['date'])}</pubDate>",
                f"    <description>{escape(blurb)}</description>",
                "  </item>"]
    out += ["</channel>", "</rss>", ""]
    (docs / "feed_rss_announcements.xml").write_text("\n".join(out), encoding="utf-8")
    print(f"feed_rss_announcements.xml: {min(len(notices), 20)} entries")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", help="the address the site is served from; feeds need it absolute")
    args = ap.parse_args()
    site, roots = read_tree()
    site_url = args.site_url or site.get("site", "")
    # Notices are read before the previous output is removed, so a
    # malformed one never costs the last good tree.
    notices = parse_announcements()

    if OUT.exists():
        shutil.rmtree(OUT)
    docs = OUT / "docs"
    docs.mkdir(parents=True)
    assets = docs / "assets"
    shutil.copytree(ROOT / "assets", assets, dirs_exist_ok=True)
    # The SBSC theme's stylesheet and our accessibility additions ride
    # along like the assets: tracked files, copied beside the pages.
    shutil.copytree(ROOT / "stylesheets", docs / "stylesheets",
                    dirs_exist_ok=True)

    # Two passes. First every page lands in the tree unchanged, so a link
    # from an early page (the front page lists them all) finds its target
    # file no matter what order the tree lists them in. Then each page is
    # converted in place.
    pages = list(all_pages(roots)) + [
        Node(it["title"], it["title"],
             pathlib.PurePosixPath(f"announcements/{it['stem']}.md"), [])
        for it in notices]
    for page in pages:
        target = docs / pathlib.PurePosixPath(*page.rel.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / page.rel, target)
    dates = git_dates()
    by_rel = {f"announcements/{it['stem']}.md": it for it in notices}
    for page in pages:
        target = docs / pathlib.PurePosixPath(*page.rel.parts)
        text = de_dead_links(convert(target.read_text(encoding="utf-8")), page.rel, docs)
        blurb = summary(page.rel)
        notice = by_rel.get(str(page.rel))
        if notice:
            # A notice's frontmatter is replaced, not stamped: the
            # author's dates are the truth, and the plugin must never
            # fall back to the build minute for a missing updated.
            body = re.sub(r"\A---\n.*?\n---\n\n?", "", text, flags=re.S)
            desc = (f"description: {as_yaml_scalar(blurb)}\n"
                    if blurb else "")
            text = (f"---\ndate: {notice['date']:%Y-%m-%dT%H:%M:%S%z}\n"
                    f"updated: {notice['updated']:%Y-%m-%dT%H:%M:%S%z}\n"
                    f"{desc}---\n\n{body}")
        else:
            text = with_dates(text, dates.get(str(page.rel)), blurb)
        target.write_text(text, encoding="utf-8")

    # The landing page rides along in the feed, dated by the newest source.
    latest = max((d[0] for d in dates.values()), default=None)
    (docs / "index.md").write_text(
        with_dates(landing(roots, notices), None if latest is None else [latest, latest]),
        encoding="utf-8")

    # The section's index rides along too, dated by the newest notice.
    if notices:
        newest = notices[0]["date"].strftime("%Y-%m-%dT%H:%M:%S%z")
        (docs / "announcements").mkdir(exist_ok=True)
        (docs / "announcements" / "index.md").write_text(
            with_dates(announcements_index(notices), [newest, newest],
                       "Maintenance windows, software updates, and service "
                       "notices for Kitsune, newest first."),
            encoding="utf-8")

    nav = [{HOME_LABEL: "https://sbsc.stonybrook.edu"}]
    hub = roots[0]
    # The front page is the site's home: its link, then its sections beside
    # it, not under a second copy of its own name.
    nav.append({hub.menu: "index.md"})
    if notices:
        nav.append(announcements_section(notices))
    for child in hub.children:
        sub = nav_entry(child)
        if sub:
            nav.append(sub)
    for root in roots[1:]:
        entry = nav_entry(root)
        if entry:
            nav.append(entry)

    # The site's address arrives with the deployment (--site_url), never
    # hard-coded. The RSS feed needs an absolute address, so the plugin is
    # wired only when one is known. The dates themselves arrive through
    # each page's frontmatter (date, updated), stamped above from the
    # sources' git history; use_git cannot see the generated copies. A
    # date without a time of its own reads as midnight Eastern, the same
    # clock the notices' own channel uses. The channel image is the
    # shield, the theme's own mark, its address derived the same way.
    url_line = f"site_url: {site_url}" if site_url else ""
    rss_block = ('  - rss:\n      use_git: false\n      date_from_meta:\n'
                 '        as_creation: date\n        as_update: updated\n'
                 '        datetime_format: "%Y-%m-%dT%H:%M:%S%z"\n'
                 '        default_time: 00:00\n'
                 '        default_timezone: America/New_York\n'
                 f'      image: {site_url.rstrip("/")}/assets/sbsc-shield.svg\n'
                 '      pretty_print: true\n'
                 '      length: 40') if site_url else ""
    (OUT / "mkdocs.yml").write_text(f"""\
# Built by tools/build_docs.py from site.yaml: edit the tree there, not here.
site_name: SBSC Documentation
site_description: Documentation for Kitsune at the Stony Brook Supercomputing Center.
{url_line}
use_directory_urls: true
strict: true
copyright: Stony Brook Supercomputing Center, Stony Brook University
nav:
{yaml_list(nav).rstrip()}
plugins:
  - search
{rss_block}
theme:
  name: material
  custom_dir: overrides
  language: en
  font: false
  logo: assets/sbsc-shield.svg
  favicon: assets/sbsc-shield.svg
  palette:
    - scheme: default
      primary: custom
      accent: custom
      toggle: {{ icon: material/weather-night, name: Switch to dark mode }}
    - scheme: slate
      primary: custom
      accent: custom
      toggle: {{ icon: material/weather-sunny, name: Switch to light mode }}
  features:
    - content.code.copy
    - navigation.footer
    - navigation.path
    - navigation.sections
    - navigation.tabs
    - navigation.top
    - navigation.tracking
extra_css:
  - stylesheets/sbsc.css
  - stylesheets/sbsc-docs.css
extra:
  homepage: https://sbsc.stonybrook.edu/
markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
""", encoding="utf-8")

    # Material's own logo partial hardcodes alt="logo", a name that helps
    # no one using a screen reader; the override directory carries ours,
    # with the center's name instead. The rest of the partial is the
    # theme's, so an icon-only configuration keeps working.
    override = OUT / "overrides" / "partials" / "logo.html"
    override.parent.mkdir(parents=True, exist_ok=True)
    override.write_text("""\
{% if config.theme.logo %}
  <img src="{{ config.theme.logo | url }}" alt="Stony Brook Supercomputing Center">
{% else %}
  {% set icon = config.theme.icon.logo or "material/library" %}
  {% include ".icons/" ~ icon ~ ".svg" %}
{% endif %}
""", encoding="utf-8")

    # The brand stylesheet is no longer written here: the SBSC theme ships
    # as tracked files under stylesheets/ (the theme itself, plus our
    # accessibility additions in sbsc-docs.css), copied into the tree
    # above. The interim generated look survives in git history under the
    # tag pre-sbsc-theme.

    # The feeds' human-readable view, written beside them at the site
    # root; its relative addresses work at any deployment path. Browsers
    # apply it through the stylesheet processing instruction that
    # tools/style_feeds.py adds to the built feeds after mkdocs runs.
    # The notices' channel carries each item's line as well, so it gets
    # the variant view; tokens carry the differences, because the XSL's
    # own braces rule out an f-string.
    if site_url and notices:
        announcements_feed(notices, site_url, docs)
    if site_url:
        xsl = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:atom="http://www.w3.org/2005/Atom">
<xsl:output method="html" encoding="UTF-8" doctype-system="about:legacy-compat"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title><xsl:value-of select="rss/channel/title"/></title>
<style>
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        Helvetica, Arial, sans-serif;
  color: #17283e;
  background: #ffffff;
}
/* The docs header's twin: white ground, navy top rule, shield and name. */
header {
  background: #ffffff;
  border-top: 4px solid #112d50;
  border-bottom: 1px solid #dbe4ee;
}
header .home {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin: 8px 16px;
  color: #112d50;
  font-weight: 700;
  text-decoration: none;
}
header img { display: block; height: 1.9rem; width: auto; }
main { max-width: 44rem; margin: 0 auto; padding: 1.5rem 16px 4rem; }
h1 { font-size: 1.5rem; margin: 0 0 0.5rem; color: #112d50; }
.what { margin: 0 0 1.5rem; }
.what code { font-size: 0.9em; overflow-wrap: anywhere; }
ol { list-style: none; margin: 0; padding: 0; }
li { border-top: 1px solid #dbe4ee; }
li a {
  display: flex;
  align-items: center;
  min-height: 24px;
  padding: 0.5rem 0 0.25rem;
  color: #155cbb;
  text-decoration: underline;
}
.when { margin: 0 0 0.6rem; color: #52657b; font-size: 0.875rem; }@@BLURB_CSS@@
a:focus-visible {
  outline: 3px solid #2a8fd6;
  outline-offset: 2px;
}
</style>
</head>
<body>
<header>
  <a class="home" href="{rss/channel/link}">
    <img src="assets/sbsc-shield.svg" alt="Stony Brook Supercomputing Center"/>
    <span>SBSC Documentation</span>
  </a>
</header>
<main>
<h1><xsl:value-of select="rss/channel/title"/></h1>
<p class="what">@@WHAT@@ Subscribe by copying its address,
<code><xsl:value-of select="rss/channel/atom:link/@href"/></code>, into a
feed reader.</p>
<ol>
<xsl:for-each select="rss/channel/item">
  <li>
    <a href="{link}"><xsl:value-of select="title"/></a>
    <p class="when"><xsl:value-of select="pubDate"/></p>@@BLURB@@
  </li>
</xsl:for-each>
</ol>
</main>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
        (docs / "feed.xsl").write_text(
            xsl.replace("@@WHAT@@", "This page is a feed: the documentation's "
                               "new and updated pages, newest first.")
               .replace("@@BLURB_CSS@@", "")
               .replace("@@BLURB@@", ""), encoding="utf-8")
        (docs / "announcements.xsl").write_text(
            xsl.replace("@@WHAT@@", "This page is a feed: announcements for "
                               "Kitsune, newest first: maintenance windows, "
                               "software updates, and service notices.")
               .replace("@@BLURB_CSS@@", "\n.blurb { margin: 0 0 0.6rem; }")
               .replace("@@BLURB@@", "\n    <p class=\"blurb\">"
                                     "<xsl:value-of select=\"description\"/></p>"),
            encoding="utf-8")

    # Local scan URLs: mkdocs serve keeps the address's path prefix, so the
    # urls carry it too (the a11y scan and any link check use this list).
    prefix = "/" + site_url.rstrip("/").split("/", 3)[-1] if site_url.count("/") >= 3 else ""
    (OUT / "urls-local.txt").write_text(
        f"http://127.0.0.1:8000{prefix}/\n"
        + (f"http://127.0.0.1:8000{prefix}/announcements/\n" if notices else "")
        + "".join(f"http://127.0.0.1:8000{prefix}{page_url(p)}\n" for p in pages),
        encoding="utf-8")
    print(f"docs-site: {len(pages)} pages, nav {len(nav)} top-level entries"
          + (f", {len(notices)} announcements" if notices else ""))


if __name__ == "__main__":
    main()
