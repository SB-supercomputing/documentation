#!/usr/bin/env python3
"""Port the archived Ookami website into this repository, word for word.

Ookami reached end of life at the end of 2025. Its website was saved on
2026-11-05 into an archive folder (see that folder's README.md); this
script turns the saved pages into Markdown under ookami/, keeping every
word of each page as the site published it:

    pip install -r requirements-port.txt
    python tools/port_ookami.py [--archive DIR] [--links FILE] [--nav FILE]

The archive is read from disk; only the outbound links are checked over
the network, and --links keeps those answers in FILE so later runs
agree. --nav writes the Ookami branch for site.yaml.

What changes, and what does not:

- The words never change. Only the page's own content comes over: the
  university header, menus, sidebars, and footer stay behind.
- A link to another Ookami page goes to our copy of it. A linked file
  (PDF, slides, the project template) is copied to ookami/files/ and
  linked there. Pictures go to assets/ookami/.
- Videos are not uploaded: a link to one keeps its words and loses the
  link, and the page says so in its archive note. A link to a page that
  no longer answers, and has no saved copy, does the same.
- Each page opens with a note that it is archived and closes with the
  address it came from; both carry their own classes (archive,
  archive-credit), so they are never mistaken for the old site's words.
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import pathlib
import posixpath
import re
import shutil
import sys
import urllib.parse

from bs4 import BeautifulSoup, NavigableString

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from port_rci import Converter, slugify  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
HOST = "https://www.stonybrook.edu"
BASE = "/commcms/ookami/"
SAVED = "site/www.stonybrook.edu/commcms/ookami/"
WAYBACK_KEY = "support/faq/ookami-fujitsu-compilers"
WAYBACK_FILE = "wayback/20210928/commcms/ookami/support/faq/ookami-fujitsu-compilers.php.html"
RETRIEVED = "November 5, 2026"
MEDIA = (".mp4", ".mov", ".m4v", ".wmv", ".avi", ".webm", ".mp3", ".wav", ".m4a")

# Every page, in the order the navigation lists it: (page key, group).
# A key is the page's address under /commcms/ookami/, without .php.
FAQ = [
    "what_is_ookami", "ookami-account-request", "getting-a-project-on-ookami",
    "logging-into-ookami", "enroll-in-DUO-security", "getting-started-guide",
    "example-slurm-script", "core-thread-control-ookami",
    "core-thread-control-mpi-flags", "thread_binding",
    "submit-delete-check-slurm-jobs", "handling-job-output",
    "interactive_slurm_session", "understanding_login_nodes",
    "what_are_modules", "queues_on_ookami", "software_on_ookami",
    "open_ondemand", "ookami-arm-compilers", "ookami-cray-compilers",
    "ookami-gcc-compilers", "ookami-amd-compilers", "ookami-nvidia-compilers",
    "ookami-fujitsu-compilers", "ookami_storage_options",
    "project_space_permissions", "Vectorization_Flags", "Vectorization_Example",
    "profilers", "iacs_acknowledgement", "hipaa_concerns",
    "resetting_ookami_password", "passwordless_ssh",
    "transferring_data_to_ookami", "fixing_common_login_issues",
    "warning_modshare_library_path_duo", "remote_troubleshooting", "XDMoD",
    "power_usage",
    # On the site but not linked from its FAQ list.
    "available_math_libraries", "compiling",
    "conditional_compilation_by_architecture", "debugging_tools",
    "infiniband_topology", "NVIDIA Grace CPUs",
]
PAGES = (
    [("", "home")]
    + [("support", "support"), ("support/index_links_and_docs", "support"),
       ("support/faq", "faq")]
    + [(f"support/faq/{k}", "faq") for k in FAQ]
    + [(k, "about") for k in ("about", "people", "projects", "publications",
                              "announcements", "calendar", "system_status",
                              "ByteBoost")]
    + [("science_stories", "stories")]
    + [(f"science_stories/{k}", "stories") for k in
       (" Tumuklu", "Diehl", "Fernandez-Serra", "Gallagher", "Krysl", "Zhang", "Zhang2")]
    + [("user_meeting", "meetings"), ("user_meeting/UGM2023", "meetings")]
)
SECTIONS = {"support", "support/faq", "science_stories", "user_meeting"}
GROUPS = [("support", "Support"), ("about", "About Ookami"),
          ("stories", "Science stories"), ("meetings", "User meetings")]

# Alt text for screenshots the site published without any. Alt text is
# not the page's wording; a screen reader needs it to describe the
# picture. Keyed by (page key, picture number on the page, from 1).
ALT = {
    ("support/faq/logging-into-ookami", 1):
        "MobaXterm's start screen, with the Start local terminal button and a "
        "list of recent sessions including login.ookami.stonybrook.edu",
    ("support/faq/logging-into-ookami", 2):
        "MobaXterm's SSH session settings: remote host login.ookami.stonybrook.edu, "
        "Specify username checked with NETID, port 22",
    ("support/faq/logging-into-ookami", 3):
        "MobaXterm's Advanced SSH settings tab: X11-Forwarding checked and "
        "Execute command set to DUO_PASSCODE=push",
    ("support/faq/open_ondemand", 4):
        "Open OnDemand's Job Composer: the New Job menu open, offering From "
        "Default Template, From Specified Path, and From Selected Job",
}

# Ookami links the site itself got wrong, to pages the archive holds:
# the address each one meant. The link text is unchanged.
MEANT = {"faq/core-thread-control-ookami": "support/faq/core-thread-control-ookami"}
BROWSER = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CHROME = [".breadcrumb-wrapper", ".sidenav-desktop", ".sidenav-mobile",
          "script", "style", "noscript", "form", "iframe"]

NOTE = ("Ookami reached end of life at the end of 2025. This is a copy of its "
        "website, kept for reference; some original material is not included.")
NOTE_MEDIA = ("Past recordings, webinars, and seminar videos are not uploaded "
              "here; their titles appear below without links.")


def dest_of(key):
    if key == "":
        return "ookami/README.md"
    parts = [p.strip().lower().replace(" ", "-") for p in key.split("/")]
    if key in SECTIONS:
        return "ookami/" + "/".join(parts) + "/README.md"
    return "ookami/" + "/".join(parts) + ".md"


DEST = {key: dest_of(key) for key, _ in PAGES}


def source_file(archive, key):
    if key == WAYBACK_KEY:
        return archive / WAYBACK_FILE
    for name in ([key + ".php", key + "/index.php", key] if key else ["index.php"]):
        path = archive / SAVED / name
        if path.is_file():
            return path
    raise SystemExit(f"port_ookami: no saved page for '{key}'")


def page_url(key):
    if key == "":
        return HOST + BASE
    if key in SECTIONS or key in ("about", "people", "projects", "publications",
                                  "announcements", "calendar", "system_status"):
        return HOST + BASE + key + "/"
    if key.startswith("science_stories/"):
        return HOST + BASE + urllib.parse.quote(key)
    return HOST + BASE + urllib.parse.quote(key) + ".php"


def saved_files(archive):
    """Every saved file by the address it was fetched from."""
    by_url = {}
    with open(archive / "manifest.tsv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            for url in (row["url"], row["final"]):
                if url:
                    by_url.setdefault(normal(url), row["path"])
    return by_url


def normal(url):
    parts = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(parts.path)
    host = (parts.hostname or "").lower()
    if host == "stonybrook.edu":
        host = "www.stonybrook.edu"
    return f"{host}{path}" + (f"?{parts.query}" if parts.query else "")


def page_key(url):
    """The page key an address names, or None when it is not an Ookami page."""
    parts = urllib.parse.urlsplit(url)
    if (parts.hostname or "").lower() not in ("www.stonybrook.edu", "stonybrook.edu"):
        return None
    path = urllib.parse.unquote(parts.path)
    for prefix in ("/commcms/ookami", "/ookami"):
        if path == prefix or path.startswith(prefix + "/"):
            rel = path[len(prefix):].lstrip("/")
            break
    else:
        return None
    return re.sub(r"(/?index\.(php|html)|\.php)$", "", rel).rstrip("/")


def region(soup):
    """The page's own content: the university's furniture removed."""
    main = soup.select_one("#main-site-content")
    for selector in CHROME:
        for el in main.select(selector):
            el.decompose()
    return main


def words(text):
    return text.split()


def title_of(soup, main):
    """The page's title, and whether it is the first thing the page says
    (then it moves into the H1 in place) or comes from <title> (ours)."""
    heads = [h for h in main.find_all(re.compile(r"^h[1-6]$")) if h.get_text(strip=True)]
    lead = words(main.get_text(" "))
    if heads:
        head = heads[0]
        text = words(head.get_text(" "))
        if lead[:len(text)] == text:
            return head.get_text(" ", strip=True), head
    raw = soup.title.get_text(" ", strip=True) if soup.title else ""
    return re.sub(r"\s*\|\s*Ookami\s*$", "", raw) or "Ookami", None


class OokamiConverter(Converter):
    """markdownify as the RCI port uses it."""


def to_markdown(node):
    return OokamiConverter(heading_style="ATX", bullets="-", strong_em_symbol="*",
                           escape_underscores=False, escape_asterisks=True,
                           keep_inline_images_in=["td", "th", "a"]).convert_soup(node)


class Linker:
    """Where each link and picture goes, and what the run had to copy."""

    def __init__(self, archive, statuses):
        self.archive = archive
        self.by_url = saved_files(archive)
        self.statuses = statuses
        self.copied = {}
        self.unlinked = []

    def saved(self, url):
        path = self.by_url.get(normal(url))
        return self.archive / path if path else None

    def copy(self, src, rel):
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.stat().st_size != src.stat().st_size:
            shutil.copy2(src, target)
        self.copied[rel] = src
        return rel

    def file_rel(self, src):
        rel = str(src.relative_to(self.archive / "site"))
        rel = rel.split("commcms/ookami/", 1)[-1] if "commcms/ookami/" in rel else rel
        return "ookami/files/" + rel

    def picture_rel(self, src):
        rel = str(src.relative_to(self.archive / "site"))
        rel = rel.split("commcms/ookami/", 1)[-1] if "commcms/ookami/" in rel else rel
        return "assets/ookami/" + rel

    def alive(self, url):
        """Whether an outbound address still answers. A page that is gone
        (404, 410) or a host that never answers is dead; before saying
        so, ask again as a browser would, since some sites turn scripts
        away with the same codes."""
        if url not in self.statuses:
            from check_links import fetch
            status = fetch(url)
            if status is None or status in (404, 410) or status >= 500:
                status = browser_status(url)
            self.statuses[url] = status
        status = self.statuses[url]
        return not (status is None or status in (404, 410))


def browser_status(url):
    import urllib.error
    import urllib.request
    request = urllib.request.Request(url, headers={"User-Agent": BROWSER})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status
    except urllib.error.HTTPError as err:
        return err.code
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None


def relative(target, dest):
    rel = posixpath.relpath(target, posixpath.dirname(dest))
    return urllib.parse.quote(rel, safe="/#")


def tidy(main, key, dest, linker, notes):
    page = page_url(key)
    # Line breaks inside a code block are its lines.
    for br in main.select("pre br"):
        br.replace_with("\n")
    # Outside code, a line break in the saved HTML is a space as the
    # browser shows it; left in, it could start a Markdown list.
    for text in main.find_all(string=True):
        if not text.find_parent(["pre", "code"]) and re.search(r"\s", text):
            text.replace_with(re.sub(r"\s+", " ", str(text)))
    # Spaces the site wrapped in bold or italic markup sit outside it,
    # where Markdown keeps them; markup around nothing but a space is a
    # space; and bold split into pieces with nothing between joins up.
    inline = ["strong", "b", "em", "i", "span", "a", "u"]
    # A line break at the edge of bold or italic text breaks the line
    # outside it, where Markdown can keep it.
    for el in main.find_all(inline):
        while el.contents and getattr(el.contents[-1], "name", None) == "br":
            el.insert_after(el.contents[-1].extract())
        while el.contents and getattr(el.contents[0], "name", None) == "br":
            el.insert_before(el.contents[0].extract())
    for el in main.find_all(inline):
        if not el.get_text().strip() and not el.find("img"):
            el.replace_with(" " if el.get_text() else "")
    for el in main.find_all(inline):
        first, last = el.contents[:1], el.contents[-1:]
        if first and isinstance(first[0], NavigableString) and first[0][:1].isspace():
            stripped = first[0].lstrip()
            first[0].replace_with(stripped)
            el.insert_before(" ")
        if last and isinstance(el.contents[-1], NavigableString) and el.contents[-1][-1:].isspace():
            tail = el.contents[-1]
            tail.replace_with(tail.rstrip())
            el.insert_after(" ")
    for el in main.find_all(["strong", "b", "em", "i"]):
        nxt = el.next_sibling
        while nxt is not None and getattr(nxt, "name", None) == el.name:
            for child in list(nxt.contents):
                el.append(child.extract())
            nxt.decompose()
            nxt = el.next_sibling
    # A list item with no text of its own, holding only another list, is
    # the site's way of indenting: its items join the outer list.
    for li in main.find_all("li"):
        kids = [k for k in li.children if getattr(k, "name", None) or str(k).strip()]
        if len(kids) == 1 and getattr(kids[0], "name", None) in ("ul", "ol"):
            inner = kids[0]
            for item in inner.find_all("li", recursive=False):
                li.insert_before(item.extract())
            li.decompose()
    # Table cells the site left outside any table are plain blocks.
    for cell in main.find_all(["td", "th", "tr", "tbody", "thead"]):
        if not cell.find_parent("table"):
            cell.name = "div"
    # A one-column table that only stacks a picture over its caption is
    # layout: its cells become blocks, so the picture stays a picture.
    for table in main.find_all("table"):
        rows = table.find_all("tr")
        if rows and all(len(r.find_all(["td", "th"], recursive=False)) <= 1 for r in rows):
            for cell in table.find_all(["td", "th"]):
                cell.name = "div"
            for part in table.find_all(["tr", "tbody", "thead", "tfoot"]):
                part.unwrap()
            table.name = "div"
            table.attrs = {}
    for h in main.find_all(re.compile(r"^h[1-6]$")):
        if not h.get_text(strip=True):
            h.decompose()

    # Links within the page go to a heading, the only thing that keeps an
    # address once converted.
    headings = re.compile(r"^h[2-6]$")
    for a in main.select('a[href^="#"]'):
        target = main.find(id=a["href"][1:]) or main.find(attrs={"name": a["href"][1:]}) \
            if len(a["href"]) > 1 else None
        if target is None:
            a.unwrap()
            continue
        heading = target if headings.match(target.name) else target.find_previous(headings)
        if heading is None or main not in heading.parents:
            a.unwrap()
            continue
        if not heading.get("id"):
            heading["id"] = slugify(heading.get_text(" ", strip=True))
        a["href"] = "#" + heading["id"]

    for a in main.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("#"):
            continue
        if href.lower().startswith(("mailto:", "tel:")):
            continue
        url = urllib.parse.urljoin(page, href)
        parts = urllib.parse.urlsplit(url)
        frag = f"#{parts.fragment}" if parts.fragment else ""
        for attr in ("target", "rel", "class", "style", "title"):
            a.attrs.pop(attr, None)
        if parts.scheme not in ("http", "https"):
            a.unwrap()
            continue
        if parts.path.lower().endswith(MEDIA):
            notes.add("media")
            linker.unlinked.append((dest, "video", url))
            a.unwrap()
            continue
        key2 = page_key(url)
        key2 = MEANT.get(key2, key2)
        if key2 in DEST:
            a["href"] = relative(DEST[key2], dest) + frag
            continue
        src = linker.saved(url.split("#")[0])
        if key2 is not None and src is not None and not src.suffix.lower() in (".php", ".html", ""):
            a["href"] = relative(linker.copy(src, linker.file_rel(src)), dest)
            continue
        if src is not None and src.suffix.lower() in (".pdf", ".docx", ".tex", ".zip", ".eps",
                                                     ".pptx", ".png", ".jpg", ".jpeg"):
            a["href"] = relative(linker.copy(src, linker.file_rel(src)), dest)
            continue
        if key2 is not None:
            # An Ookami address the archive has no copy of: it was gone
            # before the site was saved.
            linker.unlinked.append((dest, "missing", url))
            a.unwrap()
            continue
        if linker.alive(url.split("#")[0]):
            a["href"] = url
        else:
            linker.unlinked.append((dest, "dead", url))
            a.unwrap()

    count = 0
    for img in main.find_all("img"):
        count += 1
        src = img.get("src") or ""
        alt = (img.get("alt") or "").strip() or ALT.get((key, count))
        if src.startswith("data:"):
            m = re.match(r"data:image/(\w+);base64,(.*)", src, re.S)
            ext = {"jpeg": "jpg"}.get(m.group(1), m.group(1))
            rel = f"assets/ookami/inline/{dest[7:-3].replace('/', '-')}-{count}.{ext}"
            target = ROOT / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(base64.b64decode(m.group(2)))
        else:
            saved = linker.saved(urllib.parse.urljoin(page, src))
            if saved is None:
                linker.unlinked.append((dest, "picture", src))
                img.decompose()
                continue
            rel = linker.copy(saved, linker.picture_rel(saved))
        if not alt:
            notes.add(f"needs alt: picture {count} ({rel})")
        img.attrs = {"src": relative(rel, dest), "alt": alt or ""}


def port(archive, key, linker):
    path = source_file(archive, key)
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    main = region(soup)
    title, head = title_of(soup, main)
    dest = DEST[key]
    notes = set()
    tidy(main, key, dest, linker, notes)

    levels = [int(h.name[1]) for h in main.find_all(re.compile(r"^h[1-6]$"))
              if h is not head]
    if head is not None:
        top = int(head.name[1])
        head.decompose()
        shift = top - 1
    else:
        shift = (min(levels) - 2) if levels else 0
    for h in main.find_all(re.compile(r"^h[1-6]$")):
        h.name = f"h{min(6, max(2, int(h.name[1]) - shift))}"

    body = to_markdown(main)
    body = re.sub(r"[ \t]+\n", "\n", body)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    note = [f"    {NOTE}"]
    if "media" in notes:
        note += ["", f"    {NOTE_MEDIA}"]
    # The original address is the record of where the page came from;
    # it is shown, not linked, since the old site is gone.
    source = (f"the Internet Archive's copy of `{page_url(key)}`, saved September 28, 2021"
              if key == WAYBACK_KEY else f"`{page_url(key)}`, retrieved {RETRIEVED}")
    out = [f"# {title}", "", '!!! note archive "Archived page"', *note, "",
           body, "", f"Archived from {source}.", "{: .archive-credit }", ""]
    target = ROOT / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out), encoding="utf-8")
    return {"title": title, "from_page": head is not None,
            "problems": sorted(n for n in notes if n.startswith("needs alt"))}


def nav(meta):
    def entry(key):
        return {"title": meta[key]["title"], "source": DEST[key]}

    by_group = {}
    for key, group in PAGES:
        by_group.setdefault(group, []).append(key)
    support = [entry(k) for k in by_group["support"]]
    support.append({"title": meta["support/faq"]["title"], "source": DEST["support/faq"],
                    "menu": "FAQ", "pages": [entry(k) for k in by_group["faq"]
                                             if k != "support/faq"]})
    pages = [{"group": "Support", "pages": support},
             # The old site's home page is the first About page. The tab
             # itself opens on systems/ookami.md.
             {"group": "About Ookami",
              "pages": [{"title": meta[""]["title"], "source": DEST[""],
                         "menu": "Archived home page"}]
              + [entry(k) for k in by_group["about"]]},
             {"title": meta["science_stories"]["title"], "source": DEST["science_stories"],
              "menu": "Science stories",
              "pages": [entry(k) for k in by_group["stories"] if k != "science_stories"]},
             {"title": meta["user_meeting"]["title"], "source": DEST["user_meeting"],
              "menu": "User meetings",
              "pages": [entry(k) for k in by_group["meetings"] if k != "user_meeting"]}]
    return [{"title": "Ookami", "source": "systems/ookami.md", "menu": "Ookami",
             "label": "System Information", "pages": pages}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", type=pathlib.Path, default=ROOT.parent / "ookami-archive")
    ap.add_argument("--links", type=pathlib.Path,
                    help="keep outbound link checks here and reuse them")
    ap.add_argument("--nav", type=pathlib.Path,
                    help="write the Ookami branch for site.yaml here")
    args = ap.parse_args()
    if not (args.archive / "manifest.tsv").is_file():
        sys.exit(f"port_ookami: no archive at {args.archive} (pass --archive)")

    statuses = {}
    if args.links and args.links.exists():
        statuses = json.loads(args.links.read_text(encoding="utf-8"))
    linker = Linker(args.archive, statuses)
    for old in ("ookami", "assets/ookami"):
        if (ROOT / old).exists():
            shutil.rmtree(ROOT / old)
    meta, problems = {}, []
    for key, _ in PAGES:
        meta[key] = port(args.archive, key, linker)
        problems += [f"{DEST[key]}: {p}" for p in meta[key]["problems"]]
    if args.links:
        args.links.write_text(json.dumps(linker.statuses, indent=1, sort_keys=True),
                              encoding="utf-8")
    print(f"port_ookami: {len(PAGES)} pages, {len(linker.copied)} files copied")
    for dest, why, url in linker.unlinked:
        print(f"port_ookami: unlinked ({why}) in {dest}: {url}")
    if args.nav:
        import yaml
        args.nav.write_text("# Written by tools/port_ookami.py --nav: the Ookami branch.\n"
                            + yaml.safe_dump(nav(meta), sort_keys=False,
                                             allow_unicode=True, width=1000),
                            encoding="utf-8")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
