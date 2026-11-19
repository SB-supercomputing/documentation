# SBSC documentation

The documentation for the Stony Brook Supercomputing Center's systems,
Kitsune, SeaWulf, and NVwulf, built with MkDocs. The Markdown files are
the pages; `site.yaml` says what publishes and in what order, and
`tools/build_docs.py` builds the site under `docs-site/`.

In `site.yaml`, a page publishes from its `source:` entry, once. A
`link:` entry lists the same page in one more place in the navigation,
which is how the pages SeaWulf and NVwulf share appear under both. The
page keeps the breadcrumb, tab, and previous and next links of its
`source:` entry wherever a reader finds it.

To work on the pages, clone the repository, set up a Python 3.9-or-newer
environment of your choosing (venv, conda, or your system Python), and with
it active:

    pip install -r requirements-docs.txt
    python tools/build_docs.py
    mkdocs serve -f docs-site/mkdocs.yml

Then open the address the server prints (http://127.0.0.1:8000 unless that
port is taken; it reloads on every save). The server builds and watches the
generated tree under `docs-site/`, so after editing the Markdown sources,
re-run `python tools/build_docs.py` and the reload picks the change up.
`tools/check.sh` builds the site and reports anything broken, links
included; it checks the external ones too, so it needs the network.

The look comes from two stylesheets under `stylesheets/`. `sbsc.css` is
the SBSC theme, copied from the main site's theme package; change only
its token block at the top, and only to follow the main site.
`sbsc-docs.css` holds what this site adds: the accessibility fixes, the
placeholder highlight, the hidden contents column, and the sidebar,
which lists every section of the site as a collapsible group on wide
and narrow screens alike. The site has a
light and a dark scheme, and readers switch with the toggle in the header.

For the accessibility scan, build once, then:

    pip install -r requirements-a11y.txt
    playwright install chromium
    python tools/a11y_scan.py

The scan checks every built page against WCAG 2.2 AA and writes its
reports under `docs-site/a11y/` (`report.html` is the one to open; it
carries a findings card per issue, with screenshots, plus `coverage.md`
saying what automation cannot test). It serves the built site itself, so
no server needs to be running. `--axe-core` runs the automated gate only
and exits nonzero on any axe-core violation at Level A/AA; that is the
mode CI runs on every push and pull request. Add `--scheme slate` to scan
the dark scheme; its reports go under `docs-site/a11y/slate/`, and CI
runs that as well. The axe-core script ships
vendored as `tools/axe.min.js`, so only the browser driver is a
dependency.

The SeaWulf and NVwulf pages come from the guide Research Computing and
Informatics keeps at rci.stonybrook.edu, and each one says so at the
bottom. `tools/port_rci.py` copies them: the pages land under
`shared/` (what applies to both clusters), `seawulf/`, `nvwulf/`, and
`software/`, and their pictures under `assets/rci/`. Edit those pages at
the source rather than here, then bring the change over:

    pip install -r requirements-port.txt
    python tools/port_rci.py --nav port-nav.yaml

The run rewrites every ported page. `port-nav.yaml` holds the SeaWulf
and NVwulf branches of the navigation; paste it over the marked block
in `site.yaml` when RCI adds, removes, or renames a page.

Announcements (maintenance windows, software changes, service notices)
cover all three systems, and each names its system in its title. They
are one file each under `announcements/`, named `YYYY-MM-DD-slug.md`,
with the title and date in the frontmatter:

    ---
    title: Scheduled maintenance on the Kitsune login nodes
    date: 2026-11-24
    ---

Dates are written unquoted; a quoted date is a string, and the build
rejects it. A date alone publishes at midnight Eastern time, the
center's own clock; when the time matters, write the timestamp with
its offset, as `2026-11-24T06:00:00-0500`, and add `updated:` only
when editing a notice that is already out. The build gathers the files
into the Announcements section, the front page (five newest), the
navigation (ten), and `feed_rss_announcements.xml` (twenty); the
section's index lists them all, and each notice also flows through the
two page feeds, since a new notice is a change like any other.

Deploying to GitHub Pages stays off until the repository
variable `DOCS_DEPLOY` is set to "true"; see `.github/workflows/docs.yml`.
