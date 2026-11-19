#!/usr/bin/env python3
"""Port the SeaWulf and NVwulf documentation from RCI's site.

Research Computing and Informatics keeps the guides for SeaWulf and
NVwulf at rci.stonybrook.edu. This script copies the pages named in
MANIFEST into this repository as Markdown, so the SBSC site carries
them beside Kitsune's, each one crediting its source:

    pip install -r requirements-port.txt
    python tools/port_rci.py [--cache DIR] [--nav FILE]

Each run fetches every page again and rewrites its copy, so running it
after RCI updates a page brings the change over. --cache keeps the
fetched HTML in DIR and reads it from there on later runs. --nav writes
the SeaWulf and NVwulf branches for site.yaml to FILE, built from the
manifest and the pages' own titles and "Applies to" lists.

Only the page's own content comes over. The site's menus, sidebars,
search box and footer stay behind, and so does the footer's Google
Form, which is RCI's accessibility report, not an account form. A link
to a page that is ported becomes a link to our copy; a link to any
other RCI page goes to rci.stonybrook.edu. Pictures are saved under
assets/rci/. A picture with no alt attribute stops the run, since the
site's accessibility check would fail it; one with an empty alt is
decoration (the app icons) and is dropped.
"""
from __future__ import annotations

import argparse
import html
import pathlib
import posixpath
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml
from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter

ROOT = pathlib.Path(__file__).resolve().parent.parent
RCI = "https://rci.stonybrook.edu"
AGENT = "Mozilla/5.0 (compatible; sbsc-docs-port)"
PAUSE = 0.5  # seconds between requests, to go easy on RCI's server

# What comes over, in RCI's own order: (our path, RCI's path, group).
# The folder says where a page belongs. shared/ holds what RCI marks as
# applying to all clusters, or to SeaWulf and NVwulf both; seawulf/ and
# nvwulf/ hold the rest; software/ is the module catalog. The group is
# the heading the page sits under in RCI's documentation index.
MANIFEST = [
    ("seawulf/README.md", "/hpc/clusters/seawulf", "overview"),
    ("nvwulf/README.md", "/hpc/clusters/nvwulf", "overview"),
    ("shared/requesting-accounts-project-numbers.md", "/docs/requesting-accounts-project-numbers", "connect"),
    ("shared/duo-authentication.md", "/docs/duo-authentication", "connect"),
    ("shared/connecting-cluster.md", "/docs/connecting-cluster", "connect"),
    ("shared/passwordless-ssh.md", "/docs/passwordless-ssh", "connect"),
    ("seawulf/x11-forwarding.md", "/docs/x11-forwarding", "connect"),
    ("nvwulf/getting-access-nvwulf.md", "/docs/getting-access-nvwulf", "connect"),
    ("nvwulf/getting-started-nvwulf.md", "/docs/getting-started-nvwulf", "connect"),
    ("seawulf/quick-start-guide.md", "/docs/quick-start-guide", "jobs"),
    ("shared/slurm-overview-commands.md", "/docs/slurm-overview-commands", "jobs"),
    ("shared/writing-job-scripts.md", "/docs/writing-job-scripts", "jobs"),
    ("shared/interactive-jobs.md", "/docs/interactive-jobs", "jobs"),
    ("seawulf/example-jobs.md", "/docs/example-jobs", "jobs"),
    ("shared/managing-jobs.md", "/docs/managing-jobs", "jobs"),
    ("seawulf/queue-selection-guide.md", "/docs/queue-selection-guide", "jobs"),
    ("seawulf/shared-nodes.md", "/docs/shared-nodes", "jobs"),
    ("seawulf/guide-embarrassingly-parallel-workflows.md", "/docs/guide-embarrassingly-parallel-workflows", "jobs"),
    ("seawulf/guide-using-openmp-and-mpi.md", "/docs/guide-using-openmp-and-mpi", "jobs"),
    ("shared/choosing-time-limits.md", "/docs/choosing-time-limits", "jobs"),
    ("nvwulf/gpu-interactive-sessions.md", "/docs/gpu-interactive-sessions", "jobs"),
    ("nvwulf/nvwulf-queues.md", "/docs/nvwulf-queues", "jobs"),
    ("shared/job-failures.md", "/docs/job-failures", "jobs"),
    ("seawulf/storage-layout-policies.md", "/docs/storage-layout-policies", "storage"),
    ("seawulf/checking-storage-quotas.md", "/docs/checking-storage-quotas", "storage"),
    ("shared/file-transfer-cli.md", "/docs/file-transfer-cli", "storage"),
    ("seawulf/globus-file-transfer.md", "/docs/globus-file-transfer", "storage"),
    ("seawulf/backing-rclone.md", "/docs/backing-rclone", "storage"),
    ("seawulf/cifs-sshfs-access.md", "/docs/cifs-sshfs-access", "storage"),
    ("seawulf/accessing-project-space-cifs.md", "/docs/accessing-project-space-cifs", "storage"),
    ("shared/using-modules.md", "/docs/using-modules", "software-env"),
    ("shared/conda-environments.md", "/docs/conda-environments", "software-env"),
    ("shared/python-package-management.md", "/docs/python-package-management", "software-env"),
    ("shared/managing-custom-software.md", "/docs/managing-custom-software", "software-env"),
    ("seawulf/installing-source.md", "/docs/installing-source", "software-env"),
    ("shared/ondemand-overview.md", "/docs/ondemand-overview", "ondemand"),
    ("shared/jupyter-notebooks.md", "/docs/jupyter-notebooks", "ondemand"),
    ("shared/rstudio.md", "/docs/rstudio", "ondemand"),
    ("seawulf/matlab-open-ondemand.md", "/docs/matlab-open-ondemand", "ondemand"),
    ("shared/code-server.md", "/docs/code-server", "ondemand"),
    ("shared/seawulf-desktop.md", "/docs/seawulf-desktop", "ondemand"),
    ("seawulf/job-composer.md", "/docs/job-composer", "ondemand"),
    ("seawulf/seawulf-ondemand-apps.md", "/docs/seawulf-ondemand-apps", "ondemand"),
    ("nvwulf/nvwulf-ondemand-apps.md", "/docs/nvwulf-ondemand-apps", "ondemand"),
    ("nvwulf/ondemand-3d-ct-scan.md", "/docs/ondemand-3d-ct-scan", "ondemand-apps"),
    ("nvwulf/ondemand-cellprofiler.md", "/docs/ondemand-cellprofiler", "ondemand-apps"),
    ("seawulf/ondemand-coot.md", "/docs/ondemand-coot", "ondemand-apps"),
    ("nvwulf/ondemand-cryosparc.md", "/docs/ondemand-cryosparc", "ondemand-apps"),
    ("nvwulf/ondemand-cylinter.md", "/docs/ondemand-cylinter", "ondemand-apps"),
    ("seawulf/ondemand-galaxy.md", "/docs/ondemand-galaxy", "ondemand-apps"),
    ("seawulf/ondemand-gaussview.md", "/docs/ondemand-gaussview", "ondemand-apps"),
    ("seawulf/ondemand-octave.md", "/docs/ondemand-octave", "ondemand-apps"),
    ("seawulf/ondemand-igv.md", "/docs/ondemand-igv", "ondemand-apps"),
    ("seawulf/ondemand-jupyterlab.md", "/docs/ondemand-jupyterlab", "ondemand-apps"),
    ("nvwulf/ondemand-llm-chat.md", "/docs/ondemand-llm-chat", "ondemand-apps"),
    ("seawulf/ondemand-mathematica.md", "/docs/ondemand-mathematica", "ondemand-apps"),
    ("nvwulf/ondemand-minerva-author.md", "/docs/ondemand-minerva-author", "ondemand-apps"),
    ("shared/ondemand-moe.md", "/docs/ondemand-moe", "ondemand-apps"),
    ("nvwulf/ondemand-napari.md", "/docs/ondemand-napari", "ondemand-apps"),
    ("nvwulf/ondemand-ollama.md", "/docs/ondemand-ollama", "ondemand-apps"),
    ("shared/ondemand-paraview.md", "/docs/ondemand-paraview", "ondemand-apps"),
    ("seawulf/ondemand-phenix.md", "/docs/ondemand-phenix", "ondemand-apps"),
    ("nvwulf/ondemand-protein-prediction.md", "/docs/ondemand-protein-prediction", "ondemand-apps"),
    ("seawulf/ondemand-pymol.md", "/docs/ondemand-pymol", "ondemand-apps"),
    ("nvwulf/ondemand-qupath.md", "/docs/ondemand-qupath", "ondemand-apps"),
    ("nvwulf/ondemand-relion.md", "/docs/ondemand-relion", "ondemand-apps"),
    ("seawulf/ondemand-tensorboard.md", "/docs/ondemand-tensorboard", "ondemand-apps"),
    ("seawulf/ondemand-chimerax.md", "/docs/ondemand-chimerax", "ondemand-apps"),
    ("nvwulf/ondemand-vllm.md", "/docs/ondemand-vllm", "ondemand-apps"),
    ("shared/login-node-etiquette.md", "/docs/login-node-etiquette", "policies"),
    ("shared/node-utilization.md", "/docs/node-utilization", "policies"),
    ("shared/fairshare-job-priority.md", "/docs/fairshare-job-priority", "policies"),
    ("shared/when-ask-help.md", "/docs/when-ask-help", "policies"),
    ("shared/hpc-cheat-sheet.md", "/docs/hpc-cheat-sheet", "policies"),
    ("shared/hpc-good-conduct.md", "/docs/hpc-good-conduct", "policies"),
    ("software/README.md", "/hpc/software", "catalog"),
    ("software/gcc.md", "/hpc/software/gcc", "software"),
    ("software/intel-oneapi.md", "/hpc/software/intel-oneapi", "software"),
    ("software/aocc.md", "/hpc/software/aocc", "software"),
    ("software/nvhpc.md", "/hpc/software/nvhpc", "software"),
    ("software/llvm.md", "/hpc/software/llvm", "software"),
    ("software/intel-mpi.md", "/hpc/software/intel-mpi", "software"),
    ("software/mvapich.md", "/hpc/software/mvapich", "software"),
    ("software/openmpi.md", "/hpc/software/openmpi", "software"),
    ("software/mpi4py.md", "/hpc/software/mpi4py", "software"),
    ("software/bowtie2.md", "/hpc/software/bowtie2", "software"),
    ("software/hts.md", "/hpc/software/hts", "software"),
    ("software/genomeassembly.md", "/hpc/software/genomeassembly", "software"),
    ("software/genomeannotation.md", "/hpc/software/genomeannotation", "software"),
    ("software/metagenomics.md", "/hpc/software/metagenomics", "software"),
    ("software/diffexp.md", "/hpc/software/diffexp", "software"),
    ("software/singlecell.md", "/hpc/software/singlecell", "software"),
    ("software/popgen.md", "/hpc/software/popgen", "software"),
    ("software/gwas.md", "/hpc/software/gwas", "software"),
    ("software/phylo.md", "/hpc/software/phylo", "software"),
    ("software/structural-variant.md", "/hpc/software/structural-variant", "software"),
    ("software/bioconvert.md", "/hpc/software/bioconvert", "software"),
    ("software/qiime.md", "/hpc/software/qiime", "software"),
    ("software/freesurfer.md", "/hpc/software/freesurfer", "software"),
    ("software/fsl.md", "/hpc/software/fsl", "software"),
    ("software/gromacs.md", "/hpc/software/gromacs", "software"),
    ("software/namd.md", "/hpc/software/namd", "software"),
    ("software/lammps.md", "/hpc/software/lammps", "software"),
    ("software/ambermd.md", "/hpc/software/ambermd", "software"),
    ("software/vasp.md", "/hpc/software/vasp", "software"),
    ("software/aocl.md", "/hpc/software/aocl", "software"),
    ("software/intel-mkl.md", "/hpc/software/intel-mkl", "software"),
    ("software/openblas.md", "/hpc/software/openblas", "software"),
    ("software/fftw3.md", "/hpc/software/fftw3", "software"),
    ("software/petsc.md", "/hpc/software/petsc", "software"),
    ("software/mpfr.md", "/hpc/software/mpfr", "software"),
    ("software/mathematica.md", "/hpc/software/mathematica", "software"),
    ("software/matlab.md", "/hpc/software/matlab", "software"),
    ("software/pytorch.md", "/hpc/software/pytorch", "software"),
    ("software/tensorflow.md", "/hpc/software/tensorflow", "software"),
    ("software/scikit-learn.md", "/hpc/software/scikit-learn", "software"),
    ("software/ollama.md", "/hpc/software/ollama", "software"),
    ("software/paraview.md", "/hpc/software/paraview", "software"),
    ("software/vmd.md", "/hpc/software/vmd", "software"),
    ("software/matplotlib.md", "/hpc/software/matplotlib", "software"),
    ("software/hdf5.md", "/hpc/software/hdf5", "software"),
    ("software/netcdf.md", "/hpc/software/netcdf", "software"),
    ("software/gnu-parallel.md", "/hpc/software/gnu-parallel", "software"),
    ("software/cmake.md", "/hpc/software/cmake", "software"),
    ("software/git.md", "/hpc/software/git", "software"),
    ("software/singularity.md", "/hpc/software/singularity", "software"),
    ("software/jupyter.md", "/hpc/software/jupyter", "software"),
    ("software/htop.md", "/hpc/software/htop", "software"),
    ("software/valgrind.md", "/hpc/software/valgrind", "software"),
    ("software/linaro-forge.md", "/hpc/software/linaro-forge", "software"),
    ("software/python.md", "/hpc/software/python", "software"),
    ("software/r.md", "/hpc/software/r", "software"),
    ("software/anaconda.md", "/hpc/software/anaconda", "software"),
]

DEST = {path.lower(): dest for dest, path, _ in MANIFEST}

# The navigation each system gets, for --nav. "Getting started" leads
# with RCI's "New here? Start with these" steps for that system; the
# other groups follow RCI's documentation index.
SYSTEMS = [
    ("SeaWulf", "seawulf", ["shared/requesting-accounts-project-numbers.md",
                            "shared/connecting-cluster.md",
                            "seawulf/quick-start-guide.md",
                            "shared/ondemand-overview.md"]),
    ("NVwulf", "nvwulf", ["nvwulf/getting-access-nvwulf.md",
                          "nvwulf/getting-started-nvwulf.md",
                          "shared/connecting-cluster.md",
                          "shared/ondemand-overview.md"]),
]
GROUPS = [
    ("connect", "Connecting and accounts"),
    ("jobs", "Jobs and SLURM"),
    ("storage", "Storage and transfer"),
    ("software-env", "Software environment"),
    ("ondemand", "Open OnDemand"),
    ("policies", "Policies and fair use"),
]
# Where a page lives when both systems list it: its breadcrumb and tab.
HOME_SYSTEM = {"shared": "seawulf", "software": "seawulf",
               "seawulf": "seawulf", "nvwulf": "nvwulf"}

# Pieces of RCI's pages that are the site's furniture, not the guide.
DROP = ["style", "script", "noscript", "svg", "input", "button", "form",
        "iframe", "aside", ".applies-note", ".visually-hidden", ".hidden",
        ".svc-tools", "#catChips", ".chips", "#swCount", "[aria-hidden=true]"]

ALERT_WORDS = {"tip": "TIP", "warning": "WARNING", "important": "IMPORTANT",
               "caution": "CAUTION", "note": "NOTE"}


class Converter(MarkdownConverter):
    """markdownify, fitted to Python-Markdown and to this site's build."""

    def convert_li(self, el, text, parent_tags):
        # Python-Markdown reads a list item's later lines only when they
        # sit four spaces in, whatever the width of the bullet.
        text = (text or "").strip()
        if not text:
            return "\n"
        parent = el.parent
        if parent is not None and parent.name == "ol":
            start = parent.get("start")
            start = int(start) if start and str(start).isnumeric() else 1
            bullet = f"{start + len(el.find_previous_siblings('li'))}."
        else:
            bullet = "-"
        lines = text.split("\n")
        rest = "".join("\n" + ("    " + line if line.strip() else "")
                       for line in lines[1:])
        return f"{bullet} {lines[0]}{rest}\n"

    def convert_pre(self, el, text, parent_tags):
        code = el.get_text().strip("\n")
        if not code.strip():
            return ""
        fence = "```"
        while fence in code:
            fence += "`"
        return f"\n\n{fence}\n{code}\n{fence}\n\n"

    def convert_br(self, el, text, parent_tags):
        if "_inline" in parent_tags and ({"td", "th"} & parent_tags):
            return "<br>" + text
        return super().convert_br(el, text, parent_tags)

    def convert_hN(self, n, el, text, parent_tags):
        out = super().convert_hN(n, el, text, parent_tags)
        if el.get("id") and "_inline" not in parent_tags:
            out = out.rstrip("\n") + " {#" + el["id"] + "}\n\n"
        return out

    def convert_div(self, el, text, parent_tags):
        classes = el.get("class") or []
        if ("callout" in classes or "hx-alert" in classes) \
                and "_inline" not in parent_tags and "li" not in parent_tags:
            body = text.strip()
            if not body:
                return ""
            label = el.find("strong")
            word = label.get_text(strip=True).rstrip(":").lower() if label else ""
            kind = ALERT_WORDS.get(word, "NOTE")
            if word in ALERT_WORDS:
                # The box carries the word as its title already.
                body = re.sub(r"\A\*\*[^*\n]+\*\*:?\s*", "", body)
                body = body[:1].upper() + body[1:]
            quoted = "\n".join(("> " + line) if line.strip() else ">"
                               for line in body.split("\n"))
            return f"\n\n> [!{kind}]\n{quoted}\n\n"
        return super().convert_div(el, text, parent_tags)

    def convert_details(self, el, text, parent_tags):
        summary = html.escape(el.get("data-summary", "Details"), quote=False)
        anchor = f' id="{el["id"]}"' if el.get("id") else ""
        return (f'\n\n<details markdown="1"{anchor}>\n<summary>{summary}</summary>\n\n'
                f"{text.strip()}\n\n</details>\n\n")

    def convert_figcaption(self, el, text, parent_tags):
        return f"\n\n*{text.strip()}*\n\n" if text.strip() else ""


def to_markdown(node):
    return Converter(heading_style="ATX", bullets="-", strong_em_symbol="*",
                     escape_underscores=False, escape_asterisks=True).convert_soup(node)


def fetch(path, cache, binary=False):
    """One page (or picture) from RCI, through the cache when there is one."""
    url = path if path.startswith("http") else RCI + path
    name = None
    if cache:
        key = urllib.parse.urlsplit(url).path.strip("/").replace("/", "_") or "index"
        name = cache / (key if binary else key + ".html")
        if name.exists():
            return name.read_bytes() if binary else name.read_text(encoding="utf-8")
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    time.sleep(PAUSE)
    if name:
        name.write_bytes(data)
    return data if binary else data.decode("utf-8")


def slugify(text):
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def rewrite_link(href, dest):
    """Our copy's address for an RCI link, from the page at dest."""
    parts = urllib.parse.urlsplit(href)
    if parts.scheme not in ("", "http", "https"):
        return href
    if parts.netloc not in ("", "rci.stonybrook.edu", "www.rci.stonybrook.edu"):
        return href
    if not parts.path.startswith("/"):
        return href
    key = parts.path.rstrip("/").lower() or "/"
    frag = f"#{parts.fragment}" if parts.fragment else ""
    if key in DEST:
        return posixpath.relpath(DEST[key], posixpath.dirname(dest) or ".") + frag
    return RCI + parts.path + frag


def tidy(body, dest, cache, problems):
    """RCI's markup, cut down to the guide itself and fitted for Markdown."""
    for selector in DROP:
        for el in body.select(selector):
            el.decompose()

    # RCI's custom blocks: tiles become a list, labels become plain text.
    for glance in body.select(".hx-glance"):
        ul = BeautifulSoup("<ul></ul>", "html.parser").ul
        for tile in glance.select(".hx-tile"):
            num, label = tile.find("b"), tile.find("span")
            li = BeautifulSoup("<li></li>", "html.parser").li
            li.append(BeautifulSoup(f"<strong>{html.escape(num.get_text(strip=True))}</strong> ",
                                    "html.parser"))
            li.append(label.get_text(" ", strip=True) if label else "")
            ul.append(li)
        glance.replace_with(ul)
    for kicker in body.select(".hx-kicker"):
        kicker.name = "p"
        kicker.attrs = {}
        kicker.string = kicker.get_text(strip=True)
        kicker.string.wrap(BeautifulSoup("", "html.parser").new_tag("em"))
    for code in body.select(".hx-code"):
        pre = BeautifulSoup("", "html.parser").new_tag("pre")
        pre.string = code.get_text()
        code.replace_with(pre)
    # A row of links that RCI's stylesheet spaces out (related pages, app
    # icons, buttons) would run together as one line; it becomes a list.
    for row in body.find_all(["div", "p", "nav"]):
        kids = [k for k in row.children
                if getattr(k, "name", None) or str(k).strip()]
        if len(kids) >= 2 and all(getattr(k, "name", None) == "a" for k in kids):
            ul = BeautifulSoup("<ul></ul>", "html.parser").ul
            for a in kids:
                li = BeautifulSoup("<li></li>", "html.parser").li
                li.append(a.extract())
                ul.append(li)
            row.replace_with(ul)
    for step in body.select("ol.hx-steps > li"):
        label = step.find("strong", recursive=False)
        if label and label.next_sibling is not None:
            label.insert_after(NavigableString(": "))

    # A list item that holds only a label and a value, like a module
    # name, reads as "label: value".
    for li in body.select("ul.spec-list > li"):
        spans = li.find_all("span", recursive=False)
        if len(spans) == 2:
            spans[0].insert_after(NavigableString(": "))

    for details in body.find_all("details"):
        summary = details.find("summary")
        details["data-summary"] = summary.get_text(" ", strip=True) if summary else "Details"
        if summary:
            summary.decompose()

    # Links within the page point at a heading (or an open-and-close
    # panel), since only those keep an address once converted.
    headings = re.compile(r"^h[2-6]$")
    for a in body.select('a[href^="#"]'):
        target = body.find(id=a["href"][1:]) if len(a["href"]) > 1 else None
        if target is None:
            a.unwrap()
            continue
        if headings.match(target.name) or target.name == "details":
            continue
        heading = target.find_previous(headings)
        if heading is None or body not in heading.parents:
            a.unwrap()
            continue
        if not heading.get("id"):
            heading["id"] = slugify(heading.get_text(" ", strip=True))
        a["href"] = "#" + heading["id"]

    for a in body.find_all("a", href=True):
        href = a["href"]
        if "docs.google.com/forms" in href:
            a.unwrap()
            continue
        a["href"] = rewrite_link(href, dest)
        for attr in ("target", "rel", "class", "style"):
            a.attrs.pop(attr, None)

    slug = dest[:-3].replace("/", "-").replace("-README", "")
    for img in body.find_all("img"):
        alt = img.get("alt")
        src = img.get("src") or ""
        if alt is None:
            problems.append(f"{dest}: picture without alt text: {src}")
            img.decompose()
            continue
        if not alt.strip():
            img.decompose()
            continue
        url = urllib.parse.urljoin(RCI + "/", src)
        name = posixpath.basename(urllib.parse.urlsplit(url).path)
        local = pathlib.PurePosixPath("assets", "rci", slug, name)
        target = ROOT / local
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(fetch(url, cache, binary=True))
        img.attrs = {"src": posixpath.relpath(str(local), posixpath.dirname(dest) or "."),
                     "alt": alt.strip()}

    # The page's own title is its one H1; anything RCI marked H1 inside
    # the content moves down a level, and the rest with it.
    if body.find("h1"):
        for level in range(5, 0, -1):
            for h in body.find_all(f"h{level}"):
                h.name = f"h{level + 1}"


def applies(el):
    note = el.select_one(".applies-note") if el else None
    chips = [c.get_text(strip=True) for c in note.select(".meta-chip")] if note else []
    return list(dict.fromkeys(chips))


def port(dest, path, group, cache, problems):
    page = BeautifulSoup(fetch(path, cache), "html.parser")
    h1 = page.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else path.rsplit("/", 1)[-1]
    main = page.select_one("main")
    meta = {"title": title, "group": group, "applies": [], "category": None,
            "module": None}
    lead = []
    if group == "software":
        hidden = page.select_one("#block-rci-page-content article")
        inner = hidden.find("div") if hidden else None
        meta["applies"] = applies(hidden)
        if inner:
            kids = [d for d in inner.find_all("div", recursive=False)
                    if "applies-note" not in (d.get("class") or [])]
            texts = [d for d in kids if not d.find("div")]
            for d in kids:
                pair = d.find_all("div", recursive=False)
                if len(pair) == 2 and pair[0].get_text(strip=True) == "Module name":
                    meta["module"] = pair[1].get_text(strip=True)
            if texts:
                lead.append(texts[0].get_text(" ", strip=True))
            if len(texts) > 2:
                lead.append(texts[1].get_text(" ", strip=True))
                meta["category"] = texts[-1].get_text(" ", strip=True)
            elif len(texts) == 2:
                meta["category"] = texts[-1].get_text(" ", strip=True)
        body = main.select_one("div.container.layout > div.content")
    else:
        body = page.select_one("#block-rci-page-content article")
        meta["applies"] = applies(body)
    tidy(body, dest, cache, problems)
    text = to_markdown(body)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    out = [f"# {title}", ""]
    for para in lead:
        out += [para, ""]
    if meta["module"]:
        out += [f"**Module name:** `{meta['module']}`", ""]
    out += [text, ""]
    if meta["category"]:
        out += [f"**Category:** {meta['category']}", ""]
    if meta["applies"]:
        out += [f"**Applies to:** {', '.join(meta['applies'])}", ""]
    url = RCI + path
    out += [f"Ported from RCI's guide: <{url}> (maintained by Research "
            "Computing and Informatics).", ""]
    target = ROOT / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out), encoding="utf-8")
    return meta


def menu(title):
    return re.sub(r"\s*\(Open OnDemand\)$", "", title)


def nav(meta):
    """site.yaml's SeaWulf and NVwulf branches."""
    by_group = {}
    for dest, _, group in MANIFEST:
        by_group.setdefault(group, []).append(dest)

    def entry(dest, system):
        home = HOME_SYSTEM[dest.split("/")[0]]
        title, label = meta[dest]["title"], menu(meta[dest]["title"])
        if home == system:
            item = {"title": title, "source": dest}
            if label != title:
                item["menu"] = label
            return item
        return {"link": dest, "menu": label}

    def serves(dest, system):
        top = dest.split("/")[0]
        return top in ("shared", system)

    branches = []
    for name, system, start in SYSTEMS:
        pages = [{"group": "Getting started",
                  "pages": [entry(d, system) for d in start]}]
        for key, label in GROUPS:
            items = [entry(d, system) for d in by_group.get(key, [])
                     if serves(d, system) and d not in start]
            if key == "ondemand":
                apps = [entry(d, system) for d in by_group.get("ondemand-apps", [])
                        if serves(d, system)]
                if apps:
                    items.append({"group": "Apps", "pages": apps})
            if items:
                pages.append({"group": label, "pages": items})
        categories = {}
        for dest in by_group.get("software", []):
            if system == "seawulf" or name in meta[dest]["applies"]:
                categories.setdefault(meta[dest]["category"] or "Other", []).append(
                    entry(dest, system))
        groups = [{"group": cat, "pages": items} for cat, items in categories.items()]
        if system == HOME_SYSTEM["software"]:
            pages.append({"title": meta["software/README.md"]["title"],
                          "source": "software/README.md", "pages": groups})
        else:
            pages.append({"group": "Software catalog",
                          "pages": [{"link": "software/README.md",
                                     "menu": "All software"}] + groups})
        branches.append({"title": name, "source": f"{system}/README.md",
                         "menu": name, "pages": pages})
    return branches


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=pathlib.Path,
                    help="keep fetched pages here and reuse them on later runs")
    ap.add_argument("--nav", type=pathlib.Path,
                    help="write the SeaWulf and NVwulf branches for site.yaml here")
    args = ap.parse_args()
    if args.cache:
        args.cache.mkdir(parents=True, exist_ok=True)

    problems, meta = [], {}
    for dest, path, group in MANIFEST:
        meta[dest] = port(dest, path, group, args.cache, problems)
    print(f"port_rci: {len(MANIFEST)} pages from {RCI}")
    if args.nav:
        args.nav.write_text(
            "# Written by tools/port_rci.py --nav: the SeaWulf and NVwulf branches.\n"
            + yaml.safe_dump(nav(meta), sort_keys=False, allow_unicode=True, width=1000),
            encoding="utf-8")
        print(f"port_rci: navigation written to {args.nav}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
