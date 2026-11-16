# Kitsune documentation

The documentation for Kitsune, built with MkDocs. The Markdown files are
the pages; `site.yaml` says what publishes and in what order, and
`tools/build_docs.py` builds the site under `docs-site/`.

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
`tools/check.sh` builds the site and reports anything broken. For the
accessibility scan, build once, then:

    pip install -r requirements-a11y.txt
    playwright install chromium
    python tools/a11y_scan.py

The scan checks every built page against WCAG 2.2 AA and writes its
reports under `docs-site/a11y/` (`report.html` is the one to open; it
carries a findings card per issue, with screenshots, plus `coverage.md`
saying what automation cannot test). It serves the built site itself, so
no server needs to be running. `--axe-core` runs the automated gate only
and exits nonzero on any axe-core violation at Level A/AA; that is the
mode CI runs on every push and pull request. The axe-core script ships
vendored as `tools/axe.min.js`, so only the browser driver is a
dependency. Deploying to GitHub Pages stays off until the repository
variable `DOCS_DEPLOY` is set to "true"; see `.github/workflows/docs.yml`.
