#!/usr/bin/env python3
"""Build the documentation site.

site.yaml decides what publishes and in what order; this script turns it
into an MkDocs (Material) site under docs-site/:

    python tools/build_docs.py [--site-url https://...]

GitHub alerts ("> [!NOTE]") become Material admonitions, and a link whose
target never publishes keeps its words and loses the link, so the strict
build never fails on a page still being written. The feeds come from git
history (mkdocs-rss-plugin), so build from a checkout, not an export.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs-site"
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
    parts = page.rel.parts
    return "/" + "/".join(parts[:-1] + (parts[-1][:-3],)) + "/"


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


def landing(roots):
    """The site's front page, from the tree: what the guide covers, a line
    per tutorial, and the reference pages. Everything links to the page it
    names, and the build regenerates it, so the list never goes stale."""
    hub = roots[0]
    guide, subsections, reference = [], [], []
    for child in hub.children:
        if child.rel is None:
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
           "Kitsune is deployed.", ""]
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", help="the address the site is served from; feeds need it absolute")
    args = ap.parse_args()
    site, roots = read_tree()
    site_url = args.site_url or site.get("site", "")

    if OUT.exists():
        shutil.rmtree(OUT)
    docs = OUT / "docs"
    docs.mkdir(parents=True)
    assets = docs / "assets"
    shutil.copytree(ROOT / "assets", assets, dirs_exist_ok=True)

    # Two passes. First every page lands in the tree unchanged, so a link
    # from an early page (the front page lists them all) finds its target
    # file no matter what order the tree lists them in. Then each page is
    # converted in place.
    pages = list(all_pages(roots))
    for page in pages:
        target = docs / pathlib.PurePosixPath(*page.rel.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / page.rel, target)
    for page in pages:
        target = docs / pathlib.PurePosixPath(*page.rel.parts)
        text = de_dead_links(convert(target.read_text(encoding="utf-8")), page.rel, docs)
        target.write_text(text, encoding="utf-8")

    (docs / "index.md").write_text(landing(roots), encoding="utf-8")

    nav = [{HOME_LABEL: "https://sbsc.stonybrook.edu"}]
    hub = roots[0]
    # The front page is the site's home: its link, then its sections beside
    # it, not under a second copy of its own name.
    nav.append({hub.menu: "index.md"})
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
    # wired only when one is known.
    url_line = f"site_url: {site_url}" if site_url else ""
    rss_block = ("  - rss:\n      use_git: " + ("true" if (ROOT / ".git").exists() else "false")
                 + "\n      length: 20") if site_url else ""
    (OUT / "mkdocs.yml").write_text(f"""\
# Built by tools/build_docs.py from site.yaml: edit the tree there, not here.
site_name: SBSC Documentation
{url_line}
use_directory_urls: true
strict: true
nav:
{yaml_list(nav).rstrip()}
plugins:
  - search
{rss_block}
theme:
  name: material
  language: en
  font: false
  logo: assets/sbsc-brand.svg
  favicon: assets/kitsune-emblem-sb.svg
  palette:
    - scheme: default
      primary: red
      accent: indigo
  features:
    - content.code.copy
    - navigation.top
    - navigation.tracking
extra_css:
  - assets/sbsc.css
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

    (assets / "sbsc.css").write_text("""\
/* The center's tokens, the Kitsune placeholder mark, Material's theme
   colors in the house palette, the lockup on its white plate, and the fox
   watermark. The palette setting takes only Material's own color names,
   and its runtime sets data-md-color-primary on the body, so the overrides
   use the same selectors from this later stylesheet and win the cascade. */
[data-md-color-primary="red"] {
  --md-primary-fg-color: #990000;
  --md-primary-fg-color--light: #6B000D;
  --md-primary-fg-color--dark: #6B000D;
  --md-primary-bg-color: #ffffff;
  --md-primary-bg-color--light: #ffffff;
}
[data-md-color-accent="indigo"] {
  --md-accent-fg-color: #002244;
}
/* The wordmark's colors are set for a light ground, so it rides a white
   plate wherever Material places it: the header bar, and the navigation
   drawer's logo row once the window narrows. */
.md-header .md-header__button.md-logo,
.md-header .md-logo,
.md-nav__button.md-logo {
  background: #ffffff;
  border-radius: 3px;
  padding: 3px 10px;
  margin-right: 2px;
}
.md-header .md-logo img { max-height: 1.6rem; width: auto; }

/* The left navigation is the navigation; a page's own sections stay in the
   page, so the right-hand contents column is off. Written twice to outrank
   the theme's own rule for it. */
.md-sidebar--secondary.md-sidebar--secondary { display: none; }

mark {
  background: #F8F2C5;
  color: #4B4B4B;
  border-bottom: 2px dashed #4B4B4B;
  padding: 0 2px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
body::after {
  content: "";
  position: fixed;
  right: 0;
  bottom: 0;
  width: 260px;
  max-width: 30vw;
  aspect-ratio: 1;
  background: url("kitsune-emblem-sb.svg") bottom right / contain no-repeat;
  opacity: 0.05;
  pointer-events: none;
  z-index: 0;
}
@media print, (forced-colors: active) {
  body::after { display: none; }
}

/* Findings from the axe scan, 2026-11-13. The theme ships its inline text
   links distinguished by color alone (1.4.1), navigation links 18px tall
   where the AA floor is 24px (2.5.8), and the footer credit at 45% white
   on the dark footer (1.4.3). The underline covers lists and table cells
   too. The theme's code-comment and variable tokens sit at 4.47:1 on the
   code background (1.4.3), one step under the line. */
.md-content p a,
.md-content li a,
.md-content td a { text-decoration: underline; }
.md-sidebar--primary .md-nav__link {
  display: flex;
  align-items: center;
  min-height: 24px;
}
.md-copyright, .md-copyright a { color: rgba(255, 255, 255, 0.75); }
.md-typeset .c1, .md-typeset .nv { color: #666666; }
""", encoding="utf-8")

    # Local scan URLs: mkdocs serve keeps the address's path prefix, so the
    # urls carry it too (the a11y scan and any link check use this list).
    prefix = "/" + site_url.rstrip("/").split("/", 3)[-1] if site_url.count("/") >= 3 else ""
    (OUT / "urls-local.txt").write_text(
        f"http://127.0.0.1:8000{prefix}/\n"
        + "".join(f"http://127.0.0.1:8000{prefix}{page_url(p)}\n" for p in pages),
        encoding="utf-8")
    print(f"docs-site: {len(list(all_pages(roots)))} pages, nav {len(nav)} top-level entries")


if __name__ == "__main__":
    main()
