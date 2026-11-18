#!/usr/bin/env python3
"""
a11y_scan.py — WCAG 2.2 AA scanner producing remediation-ready findings.

Every finding answers four questions:

  WHERE ON THE SITE  page URL, page region, nearest visible heading above it,
                     surrounding text, CSS selector, pixel position, and a
                     screenshot with the element outlined in red
  WHAT IS WRONG      the criterion, the failure, and who it affects
  WHAT TO CHANGE     current markup and corrected markup, side by side
  WHERE TO FIX       the page Markdown, the build in tools/, or the theme

It also emits a coverage manifest stating which of the 55 WCAG 2.2 A/AA criteria
it could and could not test, so the output cannot be mistaken for a full audit.

Usage
-----
    python a11y_scan.py --site https://sbsc.stonybrook.edu --axe axe.min.js
    python a11y_scan.py --urls urls.txt --out results/2026-08-21
    python a11y_scan.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import html as htmlmod
import json
import pathlib
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_AXE = ROOT / "tools" / "axe.min.js"

try:
    from playwright.sync_api import sync_playwright, Error as PWError
except ImportError:
    sys.exit("Playwright missing. Run:  pip install playwright && playwright install chromium")


# ═══════════════════════════════════════════════════════════════════════════
#  1 · WCAG 2.2 A/AA COVERAGE MANIFEST
# ═══════════════════════════════════════════════════════════════════════════

AUTO, HEUR, MANUAL = "AUTO", "HEURISTIC", "MANUAL"

COVERAGE: dict[str, tuple[str, str, str, str]] = {
    "1.1.1":  ("A",  "Non-text Content", AUTO, "Detects missing/empty/generic/filename alt and unlabelled image links. Cannot judge whether alt text is ACCURATE."),
    "1.2.1":  ("A",  "Audio-only and Video-only (Prerecorded)", MANUAL, "Someone must watch or listen and decide if an alternative exists."),
    "1.2.2":  ("A",  "Captions (Prerecorded)", HEUR, "Detects a missing <track kind=captions>. Cannot verify caption quality or sync."),
    "1.2.3":  ("A",  "Audio Description or Media Alternative", MANUAL, "Requires viewing the media."),
    "1.2.4":  ("AA", "Captions (Live)", MANUAL, "Live media only."),
    "1.2.5":  ("AA", "Audio Description (Prerecorded)", MANUAL, "Requires viewing the media."),
    "1.3.1":  ("A",  "Info and Relationships", HEUR, "Detects heading skips, bold-as-heading, tables without headers, unlabelled inputs. Semantic intent still needs review."),
    "1.3.2":  ("A",  "Meaningful Sequence", HEUR, "Compares DOM order against visual order approximately."),
    "1.3.3":  ("A",  "Sensory Characteristics", MANUAL, "Detecting 'click the round button on the right' needs reading comprehension."),
    "1.3.4":  ("AA", "Orientation", AUTO, "Checks for orientation-locking CSS."),
    "1.3.5":  ("AA", "Identify Input Purpose", AUTO, "Checks autocomplete tokens on fields collecting user information."),
    "1.4.1":  ("A",  "Use of Color", MANUAL, "Requires judging whether colour is the ONLY means of conveying something."),
    "1.4.2":  ("A",  "Audio Control", AUTO, "Detects autoplaying audio/video without controls."),
    "1.4.3":  ("AA", "Contrast (Minimum)", AUTO, "Via axe-core. Text over images or video cannot be measured reliably and is flagged separately."),
    "1.4.4":  ("AA", "Resize Text", AUTO, "Tests a 200%-zoom-equivalent viewport for clipping and horizontal scroll."),
    "1.4.5":  ("AA", "Images of Text", HEUR, "Flags candidate images. Confirming pixels-as-text needs OCR and judgement."),
    "1.4.10": ("AA", "Reflow", AUTO, "Tests at 320 CSS px and names the elements causing overflow."),
    "1.4.11": ("AA", "Non-text Contrast", HEUR, "axe covers some UI components. Focus rings and icon contrast need a human."),
    "1.4.12": ("AA", "Text Spacing", AUTO, "Applies the WCAG override CSS and detects clipped content."),
    "1.4.13": ("AA", "Content on Hover or Focus", MANUAL, "Tooltips and popovers must be tested by hovering."),
    "2.1.1":  ("A",  "Keyboard", HEUR, "Detects click handlers on non-focusable elements. Full operability needs a manual pass."),
    "2.1.2":  ("A",  "No Keyboard Trap", HEUR, "Tab-walk detects short focus cycles. Confirm modals by hand."),
    "2.1.4":  ("A",  "Character Key Shortcuts", MANUAL, "Requires exercising the application."),
    "2.2.1":  ("A",  "Timing Adjustable", MANUAL, "Session and timeout behaviour is not statically visible."),
    "2.2.2":  ("A",  "Pause, Stop, Hide", HEUR, "Detects autoplay media and unprompted motion, then looks for a pause control."),
    "2.3.1":  ("A",  "Three Flashes or Below Threshold", MANUAL, "Requires frame-by-frame luminance analysis."),
    "2.4.1":  ("A",  "Bypass Blocks", AUTO, "Checks skip link presence and that its target exists."),
    "2.4.2":  ("A",  "Page Titled", AUTO, "Checks presence, non-emptiness and cross-page uniqueness."),
    "2.4.3":  ("A",  "Focus Order", HEUR, "Tab-walk flags focus landing off-screen or on hidden elements."),
    "2.4.4":  ("A",  "Link Purpose (In Context)", HEUR, "Detects empty, generic and ambiguous-duplicate link text."),
    "2.4.5":  ("AA", "Multiple Ways", AUTO, "Checks for search plus navigation, or a sitemap."),
    "2.4.6":  ("AA", "Headings and Labels", HEUR, "Detects empty and duplicate headings. Descriptiveness is a judgement call."),
    "2.4.7":  ("AA", "Focus Visible", HEUR, "Tab-walk diffs computed styles focused vs unfocused."),
    "2.4.11": ("AA", "Focus Not Obscured (Minimum)", AUTO, "Tab-walk uses elementFromPoint to catch sticky overlays covering focus."),
    "2.5.1":  ("A",  "Pointer Gestures", MANUAL, "Multipoint and path gestures require interaction."),
    "2.5.2":  ("A",  "Pointer Cancellation", MANUAL, "Requires interaction."),
    "2.5.3":  ("A",  "Label in Name", AUTO, "Checks the visible label is contained in the accessible name."),
    "2.5.4":  ("A",  "Motion Actuation", MANUAL, "Device-motion features require a device."),
    "2.5.7":  ("AA", "Dragging Movements", MANUAL, "Requires identifying drag interactions and testing alternatives."),
    "2.5.8":  ("AA", "Target Size (Minimum)", AUTO, "Measures interactive elements against 24x24 CSS px."),
    "3.1.1":  ("A",  "Language of Page", AUTO, "Checks html[lang] presence and validity."),
    "3.1.2":  ("AA", "Language of Parts", MANUAL, "Requires detecting foreign-language passages in prose."),
    "3.2.1":  ("A",  "On Focus", HEUR, "Tab-walk detects context change triggered by focus alone."),
    "3.2.2":  ("A",  "On Input", MANUAL, "Requires changing form values and observing."),
    "3.2.3":  ("AA", "Consistent Navigation", AUTO, "Compares navigation link order across scanned pages."),
    "3.2.4":  ("AA", "Consistent Identification", HEUR, "Compares accessible names of repeated components across pages."),
    "3.2.6":  ("A",  "Consistent Help", AUTO, "Checks help/contact links appear consistently."),
    "3.3.1":  ("A",  "Error Identification", MANUAL, "Requires submitting forms with bad input."),
    "3.3.2":  ("A",  "Labels or Instructions", AUTO, "Checks every input for a programmatic label."),
    "3.3.3":  ("AA", "Error Suggestion", MANUAL, "Requires triggering validation errors."),
    "3.3.4":  ("AA", "Error Prevention (Legal, Financial, Data)", MANUAL, "Requires walking a transactional flow."),
    "3.3.7":  ("A",  "Redundant Entry", MANUAL, "Requires a multi-step process."),
    "3.3.8":  ("AA", "Accessible Authentication (Minimum)", HEUR, "Detects CAPTCHA and paste-blocking. Full flow needs manual testing."),
    "4.1.2":  ("A",  "Name, Role, Value", AUTO, "Checks accessible names on links, buttons and inputs, and aria-expanded on toggles."),
    "4.1.3":  ("AA", "Status Messages", MANUAL, "Requires triggering dynamic updates and observing live regions."),
}
# 4.1.1 Parsing was REMOVED in WCAG 2.2. Deliberately absent.


# ═══════════════════════════════════════════════════════════════════════════
#  1b · WCAG STRUCTURE — principle > guideline > criterion, and what each
#       criterion actually REQUIRES. Findings cite this so a reader can see
#       which rule was broken without looking anything up.
#       Requirement text is paraphrased, not quoted from the W3C spec.
# ═══════════════════════════════════════════════════════════════════════════

PRINCIPLE = {"1": "Perceivable", "2": "Operable", "3": "Understandable", "4": "Robust"}

GUIDELINE = {
    "1.1": "Text Alternatives", "1.2": "Time-based Media", "1.3": "Adaptable",
    "1.4": "Distinguishable", "2.1": "Keyboard Accessible", "2.2": "Enough Time",
    "2.3": "Seizures and Physical Reactions", "2.4": "Navigable",
    "2.5": "Input Modalities", "3.1": "Readable", "3.2": "Predictable",
    "3.3": "Input Assistance", "4.1": "Compatible",
}

# sc -> (version that introduced it, what it requires)
REQUIREMENT = {
 "1.1.1": ("2.0", "All non-text content has a text alternative serving an equivalent purpose. Purely decorative images are marked so assistive technology ignores them."),
 "1.2.1": ("2.0", "Prerecorded audio-only and video-only content has an alternative presenting equivalent information."),
 "1.2.2": ("2.0", "Prerecorded video with audio has captions."),
 "1.2.3": ("2.0", "Prerecorded video has an audio description or a full text alternative."),
 "1.2.4": ("2.0", "Live video with audio has captions."),
 "1.2.5": ("2.0", "Prerecorded video has an audio description."),
 "1.3.1": ("2.0", "Structure and relationships conveyed visually — headings, lists, tables, labels — are also available programmatically."),
 "1.3.2": ("2.0", "When sequence affects meaning, a correct reading order can be determined programmatically."),
 "1.3.3": ("2.0", "Instructions do not rely solely on shape, size, visual location, orientation or sound."),
 "1.3.4": ("2.1", "Content does not restrict its view to a single display orientation unless that orientation is essential."),
 "1.3.5": ("2.1", "Fields collecting information about the user expose their purpose programmatically, so browsers and assistive tech can autofill."),
 "1.4.1": ("2.0", "Colour is not the only visual means of conveying information, indicating an action, or distinguishing an element."),
 "1.4.2": ("2.0", "Audio that plays automatically for more than three seconds can be paused, stopped, or its volume controlled independently."),
 "1.4.3": ("2.0", "Text has a contrast ratio of at least 4.5:1, or 3:1 for large text (18pt, or 14pt bold)."),
 "1.4.4": ("2.0", "Text can be resized to 200% without assistive technology and without loss of content or function."),
 "1.4.5": ("2.0", "Information is conveyed by real text rather than images of text, wherever the same presentation is achievable with markup."),
 "1.4.10": ("2.1", "Content reflows to 320 CSS px wide without requiring scrolling in two dimensions."),
 "1.4.11": ("2.1", "User interface components and meaningful graphics have at least 3:1 contrast against adjacent colours."),
 "1.4.12": ("2.1", "No loss of content or function when line height, letter, word and paragraph spacing are increased to set minimums."),
 "1.4.13": ("2.1", "Content shown on hover or focus can be dismissed, hovered over, and stays visible until dismissed."),
 "2.1.1": ("2.0", "All functionality is operable through a keyboard, without requiring specific timings for keystrokes."),
 "2.1.2": ("2.0", "Keyboard focus can be moved away from any component using only the keyboard."),
 "2.1.4": ("2.1", "Single-character key shortcuts can be turned off, remapped, or are active only on focus."),
 "2.2.1": ("2.0", "Time limits can be turned off, adjusted, or extended by the user."),
 "2.2.2": ("2.0", "Content that moves, blinks or scrolls automatically for more than five seconds can be paused, stopped or hidden."),
 "2.3.1": ("2.0", "Nothing flashes more than three times per second, or flashes stay below the general and red flash thresholds."),
 "2.4.1": ("2.0", "A mechanism is available to bypass blocks of content repeated on multiple pages."),
 "2.4.2": ("2.0", "Pages have titles that describe their topic or purpose."),
 "2.4.3": ("2.0", "Focusable components receive focus in an order that preserves meaning and operability."),
 "2.4.4": ("2.0", "The purpose of each link can be determined from its text alone, or from its text plus programmatically determined context."),
 "2.4.5": ("2.0", "More than one way is available to locate a page within the site."),
 "2.4.6": ("2.0", "Headings and labels describe the topic or purpose."),
 "2.4.7": ("2.0", "Any keyboard-operable interface has a visible indicator of where focus currently is."),
 "2.4.11": ("2.2", "When a component receives focus, it is not entirely hidden by author-created content such as a sticky header."),
 "2.5.1": ("2.1", "Multipoint or path-based gestures have a single-pointer alternative."),
 "2.5.2": ("2.1", "Functions triggered by a single pointer can be aborted or undone before completion."),
 "2.5.3": ("2.1", "For components with visible text labels, the accessible name contains that visible text."),
 "2.5.4": ("2.1", "Functionality operated by device or user motion can also be operated by conventional controls, and motion actuation can be disabled."),
 "2.5.7": ("2.2", "Functionality using a dragging movement has a single-pointer alternative that does not require dragging."),
 "2.5.8": ("2.2", "Targets are at least 24 by 24 CSS pixels, unless spacing, equivalence, inline position or an essential presentation applies."),
 "3.1.1": ("2.0", "The default human language of the page is set programmatically."),
 "3.1.2": ("2.0", "The language of each passage differing from the page language is set programmatically."),
 "3.2.1": ("2.0", "Moving focus to a component does not by itself cause a change of context."),
 "3.2.2": ("2.0", "Changing a form control's setting does not automatically cause a change of context unless the user was warned."),
 "3.2.3": ("2.0", "Navigation repeated across pages appears in the same relative order each time."),
 "3.2.4": ("2.0", "Components with the same function are identified consistently across the site."),
 "3.2.6": ("2.2", "Help mechanisms repeated across pages appear in the same relative order, unless the user changes it."),
 "3.3.1": ("2.0", "Input errors are automatically detected, identified, and described to the user in text."),
 "3.3.2": ("2.0", "Labels or instructions are provided when content requires user input."),
 "3.3.3": ("2.0", "When an input error is detected and a correction is known, it is suggested to the user."),
 "3.3.4": ("2.0", "Submissions with legal, financial or data consequences are reversible, checked, or confirmable."),
 "3.3.7": ("2.2", "Information previously entered by the user is auto-populated or available to select, rather than re-entered."),
 "3.3.8": ("2.2", "Authentication does not require a cognitive function test unless an alternative or a mechanism to assist is available."),
 "4.1.2": ("2.0", "For all user interface components, the name, role, state and value can be determined programmatically."),
 "4.1.3": ("2.1", "Status messages can be determined programmatically through role or properties, without receiving focus."),
}

# criteria that are NOT WCAG — used by checks that report real defects outside the standard
NON_WCAG = {
 "__QA__":       ("Quality defect", "Not a WCAG criterion. Blocks or degrades access in practice."),
 "__ASSET__":    ("Asset governance", "Not a WCAG criterion. A reliability risk that can become one."),
 "__GOV__":      ("Content governance", "Not a WCAG criterion. Creates conditions for future failures."),
 "__ADVISORY__": ("Advisory", "Not a WCAG requirement at AA. Widely recommended practice."),
 "__REMOVED__":  ("Withdrawn criterion", "4.1.1 Parsing was REMOVED in WCAG 2.2 and is no longer a conformance failure."),
 "__AXE__":      ("Reported by axe-core", "Mapped to no single criterion by this tool."),
 "__OTHER__":    ("Uncategorised", ""),
}


def wcag_context(sc: str) -> dict:
    """Full citation for a criterion: principle, guideline, requirement, version."""
    if sc in NON_WCAG:
        label, note = NON_WCAG[sc]
        return dict(is_wcag=False, citation=label, principle="", guideline="",
                    requirement=note, version="", level="", name=label)
    lvl, name, _, _ = COVERAGE.get(sc, ("", sc, "", ""))
    parts = sc.split(".")
    gkey = ".".join(parts[:2]) if len(parts) >= 2 else ""
    ver, req = REQUIREMENT.get(sc, ("", ""))
    return dict(
        is_wcag=True, level=lvl, name=name, version=ver, requirement=req,
        principle=f"{parts[0]} {PRINCIPLE.get(parts[0], '')}".strip(),
        guideline=f"{gkey} {GUIDELINE.get(gkey, '')}".strip(),
        citation=f"WCAG {ver} Success Criterion {sc} {name} (Level {lvl})" if ver
                 else f"WCAG Success Criterion {sc} {name} (Level {lvl})",
    )


# ═══════════════════════════════════════════════════════════════════════════
#  2 · CHECK REGISTRY — impact and fix guidance for every check
# ═══════════════════════════════════════════════════════════════════════════

C, T, G, M = "content", "theme", "config", "module"

CHECKS: dict[str, dict] = {

"img-no-alt": dict(sc="1.1.1", sev="high", owner=C, mins=2,
    title="Image has no alt attribute",
    impact="Screen readers fall back to announcing the filename, or skip the image entirely. "
           "A user hears 'S B U C C dot P N G' or nothing at all.",
    fix="Add an alt attribute. If the image carries information, describe that information. "
        "If it is purely decorative, use alt=\"\" so assistive tech skips it.",
    after='<img src="{src}" alt="DESCRIBE THE INFORMATION THIS IMAGE CARRIES">',
    ),

"img-alt-empty-in-link": dict(sc="1.1.1", sev="high", owner=T, mins=10,
    title="Image with empty alt is the only content of a link",
    impact="The link has no accessible name at all. Screen readers announce 'link' with no indication "
           "of where it goes. This is the most common template-level failure on the web.",
    fix="Give the image meaningful alt text, or keep alt=\"\" and add visually-hidden text in the link.",
    after='<a href="{href}">\n  <img src="{src}" alt="{sitename} home">\n</a>\n\n'
          '<!-- or, keeping the image decorative: -->\n'
          '<a href="{href}">\n  <img src="{src}" alt="">\n'
          '  <span class="visually-hidden">{sitename} home</span>\n</a>',
    ),

"img-alt-generic": dict(sc="1.1.1", sev="high", owner=C, mins=15,
    title="Alt text is generic",
    impact="The alt text names the image but conveys none of its content. For a chart or diagram the "
           "whole point is the information it depicts, so a screen reader user gets nothing.",
    fix="Replace with text serving the same purpose as the image. For complex images put the full "
        "information in adjacent text and keep alt short.",
    after='<img src="{src}" alt="Organisational chart. Full structure listed below.">\n'
          '<ul>\n  <li>Director — [Name]\n    <ul><li>[Role] — [Name]</li></ul>\n  </li>\n</ul>',
    ),

"img-alt-filename": dict(sc="1.1.1", sev="high", owner=C, mins=2,
    title="Alt text is a filename",
    impact="A screen reader reads the filename character by character. It carries no meaning.",
    fix="Replace the filename with a description of what the image shows.",
    after='<img src="{src}" alt="DESCRIBE THE IMAGE">',
    ),

"img-alt-long": dict(sc="1.1.1", sev="low", owner=C, mins=10,
    title="Alt text is very long",
    impact="Long alt text cannot be paused, re-read or navigated. Users must hear it in one burst.",
    fix="Shorten alt to a brief identification and move the detail into visible text beside the image.",
    after='<img src="{src}" alt="SHORT IDENTIFICATION">\n<p>Full description in body text here.</p>',
    ),

"img-complex": dict(sc="1.4.5", sev="medium", owner=C, mins=45,
    title="Complex image may render text as pixels",
    impact="Text baked into an image cannot be resized, restyled, translated or read by assistive "
           "technology, and blurs on high-DPI screens.",
    fix="Rebuild the chart or diagram as real HTML — a nested list or a table with proper headers. "
        "If it must stay an image, provide the same information in adjacent text.",
    after='<table>\n  <caption>Organisational structure</caption>\n'
          '  <tr><th scope="col">Role</th><th scope="col">Name</th></tr>\n'
          '  <tr><td>Director</td><td>[Name]</td></tr>\n</table>',
    ),

"img-offsite": dict(sc="__ASSET__", sev="low", owner=C, mins=5,
    title="Image served from a different host",
    impact="Not a WCAG failure, but a live breakage risk: if the other host changes, blocks hotlinking "
           "or goes away, the image disappears with no warning.",
    fix="Download the image, upload it to this site's own media library, then update the reference.",
    after='<img src="/sites/default/files/images/{basename}" alt="...">',
    ),

"h1-missing": dict(sc="1.3.1", sev="medium", owner=T, mins=10,
    title="Page has no h1",
    impact="Screen reader users jumping to the first heading to learn what the page is find nothing.",
    fix="Ensure exactly one h1 that identifies the page.",
    after='<h1>{pagetitle}</h1>',
    ),

"h1-multiple": dict(sc="1.3.1", sev="medium", owner=C, mins=10,
    title="Page has more than one h1",
    impact="A page should have one h1 identifying what it is. Multiple h1s misrepresent the structure — "
           "a user jumping to the first heading may land on a carousel slide rather than the subject.",
    fix="Keep one h1 (the page title). Demote the others to h2, or drop heading markup entirely if "
        "they are decorative hero text.",
    after='<h1>{pagetitle}</h1>\n<!-- the other h1s become: -->\n<h2>{text}</h2>',
    ),

"heading-skip": dict(sc="1.3.1", sev="medium", owner=C, mins=5,
    title="Heading level skipped",
    impact="Heading levels convey document structure. A jump from h1 to h3 implies a missing section "
           "and disorients users navigating by heading level.",
    fix="Use the next level down. Never pick a heading level for its visual size — style with CSS.",
    after='<h{expected}>{text}</h{expected}>',
    ),

"heading-empty": dict(sc="2.4.6", sev="medium", owner=C, mins=2,
    title="Empty heading element",
    impact="Screen readers announce an empty heading, adding noise to the heading list and implying "
           "a section that is not there.",
    fix="Delete the empty heading, or give it text.",
    after="<!-- delete the empty heading entirely -->",
    ),

"heading-duplicate": dict(sc="2.4.6", sev="low", owner=C, mins=5,
    title="Duplicate heading text",
    impact="Identical headings are indistinguishable in a screen reader's heading list, so users "
           "cannot tell which section they are jumping to.",
    fix="Make each heading uniquely descriptive, or remove the redundant one.",
    after='<h2>Distinct, descriptive heading</h2>',
    ),

"bold-as-heading": dict(sc="1.3.1", sev="medium", owner=C, mins=3,
    title="Bold text used instead of a heading",
    impact="Screen reader users navigate long pages by pulling up a heading list and jumping. Bolded "
           "text does not appear in that list, so the structure is invisible to them and the content "
           "reads as one undifferentiated block.",
    fix="Change the element from a bold paragraph to a real heading at the appropriate level.",
    after='<h{suggested}>{text}</h{suggested}>',
    ),

"empty-paragraphs": dict(sc="1.3.1", sev="low", owner=C, mins=5,
    title="Empty paragraphs used as spacing",
    impact="Some screen readers announce these as 'blank', adding noise between real content.",
    fix="Delete them and control spacing with CSS.",
    after="<!-- delete the empty <p>&nbsp;</p> elements -->",
    ),

"style-in-content": dict(sc="__GOV__", sev="low", owner=C, mins=10,
    title="Raw <style> block pasted into page content",
    impact="Not a failure by itself, but it means editors have a text format permitting raw CSS. That "
           "is how inline colour and font overrides get introduced, and those DO break contrast and "
           "text-spacing conformance.",
    fix="Remove the style block. If the rule is needed, move it to the theme stylesheet.",
    after="<!-- remove the <style> block; put the CSS in the theme -->",
    ),

"no-main": dict(sc="1.3.1", sev="medium", owner=T, mins=10,
    title="No main landmark",
    impact="Screen reader users jump straight to the main landmark to bypass navigation. Without it "
           "they must tab through the header on every page.",
    fix="Wrap the primary content region in <main>.",
    after='<main id="main-content" role="main">\n  ...page content...\n</main>',
    ),

"nav-unlabelled": dict(sc="1.3.1", sev="low", owner=T, mins=10,
    title="Multiple navigation landmarks share no label",
    impact="A screen reader announces several identical 'navigation' regions with no way to tell "
           "primary navigation from footer links.",
    fix="Give each nav a distinguishing accessible name.",
    after='<nav aria-label="Primary">…</nav>\n<nav aria-label="Footer">…</nav>',
    ),

"table-no-th": dict(sc="1.3.1", sev="medium", owner=C, mins=5,
    title="Data table has no header cells",
    impact="Without <th> a screen reader cannot associate a data cell with its column or row. Users "
           "hear a stream of values with no idea what each one means.",
    fix="Mark the header row cells as <th> with a scope.",
    after='<table>\n  <caption>What this table shows</caption>\n'
          '  <tr><th scope="col">Column</th><th scope="col">Column</th></tr>\n'
          '  <tr><td>Value</td><td>Value</td></tr>\n</table>',
    ),

"table-no-scope": dict(sc="1.3.1", sev="low", owner=C, mins=3,
    title="Table headers have no scope",
    impact="Ambiguous header-to-cell association in tables with both row and column headers.",
    fix="Add scope=\"col\" or scope=\"row\" to each th.",
    after='<th scope="col">Column heading</th>',
    ),

"iframe-no-title": dict(sc="4.1.2", sev="medium", owner=C, mins=2,
    title="iframe has no title",
    impact="Screen readers announce the frame with no indication of what it contains.",
    fix="Add a title attribute describing the embedded content.",
    after='<iframe src="{src}" title="DESCRIBE THE EMBEDDED CONTENT"></iframe>',
    ),

"link-no-name": dict(sc="4.1.2", sev="high", owner=T, mins=10,
    title="Link has no accessible name",
    impact="Screen readers announce 'link' and nothing else. Voice control users cannot activate it "
           "because there is no name to speak.",
    fix="Add text, an aria-label, or visually-hidden text inside the link.",
    after='<a href="{href}">\n  <span aria-hidden="true">{icon}</span>\n'
          '  <span class="visually-hidden">DESCRIBE THE DESTINATION</span>\n</a>',
    ),

"link-vague": dict(sc="2.4.4", sev="medium", owner=C, mins=3,
    title="Link text does not describe its destination",
    impact="Screen reader users often navigate by pulling up a list of links, which strips surrounding "
           "context. A list of 'Read more, Read more, Click here' is unusable.",
    fix="Rewrite the link text so it makes sense read entirely on its own.",
    after='<a href="{href}">READ [THE SPECIFIC THING]</a>',
    ),

"link-ambiguous-dupe": dict(sc="2.4.4", sev="medium", owner=C, mins=5,
    title="Same link text, different destinations",
    impact="In a screen reader's link list these are indistinguishable, so the user cannot tell which "
           "one goes where.",
    fix="Make each link text unique, moving any distinguishing qualifier INSIDE the link.",
    after='<a href="{href}">Ookami FAQ</a>\n<a href="...">SeaWulf FAQ</a>',
    ),

"link-href-hash": dict(sc="4.1.2", sev="medium", owner=T, mins=15,
    title="Link used as a button",
    impact="A link announces as 'link' and implies navigation. If it opens a menu or dialog it should "
           "be a button, and it must expose its expanded/collapsed state.",
    fix="Change the element to a button and add aria-expanded, toggled in JS.",
    after='<button type="button" aria-expanded="false" aria-controls="{controls}">\n'
          '  <span class="visually-hidden">Open menu</span>\n'
          '  <svg aria-hidden="true" focusable="false">…</svg>\n</button>',
    ),

"link-zero-size": dict(sc="2.4.3", sev="medium", owner=T, mins=10,
    title="Link occupies zero pixels but is still focusable",
    impact="Keyboard users hit an invisible tab stop with nothing visible to show where they are.",
    fix="Give the control a visible box, or remove it from the tab order if it is not needed.",
    after='<!-- give it size, or if unused: -->\n<a href="..." tabindex="-1" aria-hidden="true">',
    ),

"link-newtab": dict(sc="__ADVISORY__", sev="low", owner=C, mins=2,
    title="Link opens in a new tab without warning",
    impact="An unexpected new tab disorients screen reader users and breaks the Back button for "
           "people who rely on it.",
    fix="Warn in the link text, or remove target=\"_blank\".",
    after='<a href="{href}" target="_blank">{text} '
          '<span class="visually-hidden">(opens in a new tab)</span></a>',
    ),

"button-no-name": dict(sc="4.1.2", sev="high", owner=T, mins=10,
    title="Button has no accessible name",
    impact="Announced as 'button' with no purpose. Unusable by screen reader and voice control users.",
    fix="Add visually-hidden text or an aria-label.",
    after='<button type="button">\n  <span class="visually-hidden">DESCRIBE THE ACTION</span>\n'
          '  <svg aria-hidden="true" focusable="false">…</svg>\n</button>',
    ),

"button-symbol-name": dict(sc="4.1.2", sev="high", owner=T, mins=10,
    title="Button's only name is a symbol",
    impact="Screen readers announce the glyph literally — often as 'times' or 'multiplication sign' — "
           "or skip it entirely.",
    fix="Hide the glyph from assistive tech and add real text.",
    after='<button type="button" class="search-close">\n'
          '  <span class="visually-hidden">Close search</span>\n'
          '  <span aria-hidden="true">&times;</span>\n</button>',
    ),

"toggle-no-expanded": dict(sc="4.1.2", sev="medium", owner=T, mins=15,
    title="Toggle does not expose aria-expanded",
    impact="Screen reader users cannot tell whether the menu or panel is currently open or closed.",
    fix="Add aria-expanded and keep it in sync in JavaScript.",
    after='<button aria-expanded="false" aria-controls="{controls}">…</button>\n\n'
          '// in the theme JS:\nbtn.setAttribute("aria-expanded", String(isOpen));',
    ),

"label-in-name": dict(sc="2.5.3", sev="medium", owner=T, mins=5,
    title="Visible label not contained in the accessible name",
    impact="Voice control users say what they see. If the visible text is not part of the accessible "
           "name, saying it does not activate the control.",
    fix="Ensure the aria-label starts with, or contains, the visible text.",
    after='<button aria-label="{visible} — additional context">{visible}</button>',
    ),

"input-no-label": dict(sc="3.3.2", sev="high", owner=T, mins=10,
    title="Form field has no programmatic label",
    impact="Screen readers announce the field type with no indication of what to type. Placeholder "
           "text does not count — it disappears on typing and is usually too low contrast.",
    fix="Associate a <label> using for/id, or add aria-label.",
    after='<label for="{id}">Field name</label>\n<input type="{type}" id="{id}" name="{name}">',
    ),

"input-no-autocomplete": dict(sc="1.3.5", sev="medium", owner=T, mins=10,
    title="Field collecting user information has no autocomplete",
    impact="Users with motor or cognitive disabilities rely on browser autofill. Without the attribute "
           "the browser cannot identify the field's purpose and everyone retypes information manually.",
    fix="Add the correct autocomplete token from the HTML specification.",
    after='<input type="{type}" name="{name}" autocomplete="{token}">',
    ),

"password-nopaste": dict(sc="3.3.8", sev="high", owner=T, mins=5,
    title="Password field blocks paste",
    impact="Defeats password managers, forcing users to memorise and retype credentials. WCAG 2.2 "
           "added this criterion specifically to stop the practice.",
    fix="Remove the paste-blocking handler.",
    after='<input type="password" name="{name}" autocomplete="current-password">',
    ),

"captcha": dict(sc="3.3.8", sev="medium", owner=M, mins=20,
    title="CAPTCHA present",
    impact="Image and audio CAPTCHAs are a cognitive-function test and a hard barrier for users with "
           "visual, cognitive or motor disabilities.",
    fix="Replace with a honeypot, which is invisible to users and to assistive technology.",
    after=""
          "# then configure at /admin/config/content/honeypot",
    ),

"media-autoplay-no-controls": dict(sc="2.2.2", sev="high", owner=T, mins=45,
    title="Media autoplays with no pause control",
    impact="Moving content lasting more than five seconds must be pausable. Auto-playing "
           "background video is a documented trigger for vestibular disorders and a major "
           "distraction for users with attention-related disabilities.",
    fix="Add a visible, keyboard-reachable pause control. Note that boolean attributes are "
        "already fine as-is: autoplay=\"autoplay\" and autoplay are identical, so leave existing "
        "markup alone. Add aria-hidden and an id, then style the button so it is actually "
        "findable. A prefers-reduced-motion query alone does NOT satisfy this criterion.",
    after='<!-- 1. MARKUP: keep your existing boolean attributes, add aria-hidden + id -->\n'
          '<div class="hero">\n'
          '  <video playsinline autoplay muted loop preload="metadata"\n'
          '         aria-hidden="true" id="hero-video">\n'
          '    <source src="YOUR-EXISTING-VIDEO.mp4" type="video/mp4">\n'
          '  </video>\n'
          '  <button type="button" id="hero-pause" class="hero-pause">\n'
          '    <span class="visually-hidden">Pause background video</span>\n'
          '    <svg class="hero-pause__icon" aria-hidden="true" focusable="false" viewBox="0 0 16 16">\n'
          '      <rect x="3" y="2" width="4" height="12"/><rect x="9" y="2" width="4" height="12"/>\n'
          '    </svg>\n'
          '  </button>\n'
          '</div>\n\n'
          '/* 2. CSS: without this the button is an unstyled dot. The scrim is what makes\n'
          '   icon contrast frame-independent — white on rgba(0,0,0,.65) is 7:1 even over\n'
          '   a pure white video frame, so 1.4.11 passes whatever is playing. */\n'
          '.hero {{ position: relative; }}\n'
          '#hero-video {{ position: absolute; inset: 0; width: 100%; height: 100%;\n'
          '  object-fit: cover; }}\n'
          '.hero-pause {{\n'
          '  position: absolute; right: 1rem; bottom: 1rem; z-index: 2;\n'
          '  display: inline-flex; align-items: center; justify-content: center;\n'
          '  width: 44px; height: 44px;          /* 2.5.8 needs 24; 44 is comfortable */\n'
          '  padding: 0; cursor: pointer;\n'
          '  border: 1px solid rgba(255,255,255,.75);\n'
          '  border-radius: 50%;\n'
          '  background: rgba(0,0,0,.65);\n'
          '  color: #fff;\n'
          '  transition: background-color .15s ease;\n'
          '}}\n'
          '.hero-pause:hover {{ background: rgba(0,0,0,.85); }}\n'
          '.hero-pause:focus-visible {{ outline: 3px solid #fff; outline-offset: 3px; }}\n'
          '.hero-pause__icon {{ width: 14px; height: 14px; fill: currentColor; }}\n\n'
          '/* 3. JS: the button is decoration without this. Handling reduced-motion here\n'
          '   rather than with display:none avoids leaving a hole in the hero. */\n'
          'const v = document.getElementById("hero-video");\n'
          'const b = document.getElementById("hero-pause");\n'
          'const label = b.querySelector(".visually-hidden");\n'
          'const icon = b.querySelector(".hero-pause__icon");\n'
          'const PAUSE = \'<rect x="3" y="2" width="4" height="12"/>\'\n'
          '            + \'<rect x="9" y="2" width="4" height="12"/>\';\n'
          'const PLAY  = \'<path d="M4 2l10 6-10 6z"/>\';\n'
          'function sync() {{\n'
          '  const paused = v.paused;\n'
          '  label.textContent = paused ? "Play background video" : "Pause background video";\n'
          '  icon.innerHTML = paused ? PLAY : PAUSE;\n'
          '}}\n'
          'b.addEventListener("click", () => {{ v.paused ? v.play() : v.pause(); }});\n'
          'v.addEventListener("play", sync);\n'
          'v.addEventListener("pause", sync);\n'
          'if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {{\n'
          '  v.removeAttribute("autoplay");\n'
          '  v.pause();\n'
          '}}\n'
          'sync();',
    ),

"media-autoplay-unmuted": dict(sc="1.4.2", sev="high", owner=T, mins=10,
    title="Media autoplays with sound",
    impact="Audio playing automatically for more than three seconds interferes with screen reader "
           "output, which the user then cannot hear.",
    fix="Add the muted attribute, or provide a control to stop the audio.",
    after='<video autoplay muted playsinline …>',
    ),

"video-no-captions": dict(sc="1.2.2", sev="medium", owner=C, mins=60,
    title="Video has no captions track",
    impact="Deaf and hard-of-hearing users get no access to spoken content.",
    fix="If the video conveys information, add a captions track. If it is decorative with no audio, "
        "mark it aria-hidden so assistive tech ignores it.",
    after='<video …>\n  <track kind="captions" src="captions.vtt" srclang="en" label="English" default>\n'
          '</video>\n\n<!-- or, if decorative: -->\n<video aria-hidden="true" …>',
    ),

"lang-missing": dict(sc="3.1.1", sev="high", owner=T, mins=2,
    title="html element has no lang attribute",
    impact="Screen readers choose a voice and pronunciation rules from the page language. Without it, "
           "English may be read with the wrong phonetics.",
    fix="Add a valid language tag to the html element.",
    after='<html lang="en" dir="ltr">',
    ),

"lang-invalid": dict(sc="3.1.1", sev="medium", owner=T, mins=2,
    title="html lang attribute is not a valid language tag",
    impact="An unrecognised tag is ignored, so assistive tech falls back to a default voice.",
    fix="Use a valid BCP 47 tag such as en or en-US.",
    after='<html lang="en">',
    ),

"title-missing": dict(sc="2.4.2", sev="high", owner=T, mins=5,
    title="Page has no title",
    impact="The title is the first thing a screen reader announces and the label users see in tabs, "
           "bookmarks and history.",
    fix="Give the page a unique, descriptive title.",
    after='<title>Page name | Site name</title>',
    ),

"title-duplicate": dict(sc="2.4.2", sev="medium", owner=C, mins=10,
    title="Multiple pages share the same title",
    impact="Users with many tabs open, or reviewing browser history, cannot tell the pages apart.",
    fix="Give each page a distinct title.",
    after='<title>Distinct page name | Site name</title>',
    ),

"skip-missing": dict(sc="2.4.1", sev="medium", owner=T, mins=15,
    title="No skip link",
    impact="Keyboard users must tab through the entire header on every page before reaching content.",
    fix="Add a skip link as the first focusable element, made visible on focus.",
    after='<a href="#main-content" class="visually-hidden focusable">Skip to main content</a>',
    ),

"skip-broken": dict(sc="2.4.1", sev="high", owner=T, mins=5,
    title="Skip link points to a target that does not exist",
    impact="The link appears to work but focus goes nowhere, so the bypass mechanism silently fails.",
    fix="Ensure the target id exists on the element wrapping main content.",
    after='<a href="#main-content" class="visually-hidden focusable">Skip to main content</a>\n…\n'
          '<main id="main-content" tabindex="-1">',
    ),

"click-not-focusable": dict(sc="2.1.1", sev="high", owner=T, mins=15,
    title="Click handler on a non-focusable element",
    impact="The control works with a mouse but not a keyboard, so keyboard-only users cannot use it.",
    fix="Use a real <button>, or add tabindex=\"0\", a role and a keydown handler.",
    after='<button type="button" onclick="…">Label</button>',
    ),

"orientation-lock": dict(sc="1.3.4", sev="medium", owner=T, mins=10,
    title="CSS may lock display orientation",
    impact="Users with a device mounted in a fixed position, for example on a wheelchair, cannot rotate it.",
    fix="Remove the orientation lock and let content reflow in both orientations.",
    after="/* delete the orientation-locking media query */",
    ),

"target-too-small": dict(sc="2.5.8", sev="medium", owner=T, mins=10,
    title="Target smaller than 24x24 CSS px",
    impact="Users with tremor, limited dexterity or touch input cannot reliably hit it. New in WCAG 2.2.",
    fix="Increase the clickable area to at least 24x24 using padding rather than font size. Check "
        "whether the spacing exception applies before treating it as a failure.",
    after='.{cls} {{\n  min-width: 24px;\n  min-height: 24px;\n  display: inline-flex;\n'
          '  align-items: center;\n  justify-content: center;\n}}',
    ),

"focus-offscreen": dict(sc="2.4.3", sev="high", owner=T, mins=30,
    title="Focus lands on a hidden or off-screen element",
    impact="Keyboard users tab into content they cannot see, with no visible indication of where focus "
           "went. Classic symptom of carousel slides or menus left in the tab order.",
    fix="Remove non-visible content from the tab order.",
    after='<!-- inactive slide -->\n<div class="slide" aria-hidden="true" inert>…</div>\n\n'
          '/* or */\n.slide:not(.is-active) {{ display: none; }}',
    ),

"focus-obscured": dict(sc="2.4.11", sev="high", owner=T, mins=15,
    title="Focused element hidden behind a sticky element",
    impact="Keyboard users tab to a control that scrolls under the sticky header and cannot see what "
           "is focused. New in WCAG 2.2, and the most common 2.2 failure.",
    fix="Add scroll-margin-top equal to the sticky header's height on focusable elements.",
    after=':is(a, button, input, select, textarea, [tabindex]):focus {{\n'
          '  scroll-margin-top: {height}px; /* height of the sticky header */\n}}',
    ),

"focus-invisible": dict(sc="2.4.7", sev="high", owner=T, mins=10,
    title="No visible focus indicator",
    impact="Keyboard users cannot see where they are on the page. Usually caused by outline:none in a "
           "CSS reset with no replacement.",
    fix="Provide a clearly visible indicator. Never remove the outline without replacing it.",
    after=':is(a, button, input, select, textarea, [tabindex]):focus-visible {{\n'
          '  outline: 3px solid #990000;\n  outline-offset: 2px;\n}}',
    ),

"focus-trap": dict(sc="2.1.2", sev="high", owner=T, mins=30,
    title="Possible keyboard trap",
    impact="A keyboard user who tabs in cannot tab out and must reload the page. Total blocker.",
    fix="Ensure Escape closes the component and focus returns to the trigger. Intentional focus "
        "containment inside an OPEN modal is correct, but it must be escapable.",
    after='dialog.addEventListener("keydown", e => {{\n'
          '  if (e.key === "Escape") {{ close(); trigger.focus(); }}\n}});',
    ),

"focus-navigates": dict(sc="3.2.1", sev="high", owner=T, mins=20,
    title="Focus alone triggers navigation",
    impact="Keyboard users tabbing through the page are moved off it involuntarily and cannot reach "
           "later content.",
    fix="Trigger navigation on activation (click/Enter), never on focus.",
    after='el.addEventListener("click", go);  // not "focus"',
    ),

"reflow-320": dict(sc="1.4.10", sev="high", owner=T, mins=45,
    title="Horizontal scrolling required at 320 CSS px",
    impact="Users who zoom to 400% or use a small screen must scroll in two directions to read every "
           "line, which makes reading extremely laborious.",
    fix="Make fixed-width elements fluid. Offenders on this page: {offenders}",
    after='.{cls} {{\n  max-width: 100%;\n  width: auto;\n}}\n'
          'table {{ display: block; overflow-x: auto; }}  /* tables may scroll */\n'
          'img, video {{ max-width: 100%; height: auto; }}',
    ),

"resize-200": dict(sc="1.4.4", sev="medium", owner=T, mins=30,
    title="Content breaks at 200% zoom",
    impact="Low-vision users routinely browse at 200%. Content must stay readable without loss of "
           "functionality.",
    fix="Use relative units (rem/em/%) rather than fixed pixel widths for text containers.",
    after='.container {{ max-width: 100%; }}\nhtml {{ font-size: 100%; }}',
    ),

"text-spacing-clip": dict(sc="1.4.12", sev="medium", owner=T, mins=30,
    title="Content clips when text spacing is increased",
    impact="Users with dyslexia and low vision override line height and letter spacing. Content must "
           "not be cut off when they do.",
    fix="Avoid fixed heights on text containers; use min-height and let content grow.",
    after='.{cls} {{\n  min-height: 2rem;   /* not height */\n  overflow: visible;\n}}',
    ),

"motion-css-animation": dict(sc="2.2.2", sev="high", owner=T, mins=20,
    title="CSS animation runs automatically with no pause control",
    impact="Looping CSS animation lasting more than five seconds must be pausable. It is a "
           "barrier for users with vestibular and attention-related disabilities, and unlike "
           "video it has no built-in controls at all.",
    fix="Stop the animation after a few iterations, or add a control that pauses it. "
        "Respecting prefers-reduced-motion is good practice but does not by itself satisfy 2.2.2.",
    after='/* bound the loop so it stops within 5s */\n'
          '.ticker {{ animation: scroll 4s linear 1; }}\n\n'
          '/* or make it pausable, and honour motion preferences */\n'
          '.ticker.is-paused {{ animation-play-state: paused; }}\n'
          '@media (prefers-reduced-motion: reduce) {{\n'
          '  .ticker {{ animation: none; }}\n}}',
    ),

"motion-unidentified": dict(sc="2.2.2", sev="medium", owner=T, mins=20,
    title="Page changes on its own, source not identified",
    impact="Something on the page moves or updates without user input. If it runs for more than "
           "five seconds it needs a pause control. The scanner could not determine what is "
           "moving, so this needs a human to look.",
    fix="Open the page and watch it for ten seconds. Identify what changes — a slideshow, an "
        "animation, an auto-refreshing region, an embedded third-party widget — then apply the "
        "matching remedy. If the movement stops within five seconds, this is not a failure.",
    after="<!-- identify the moving element first; no generic fix applies -->",
    ),

"motion-no-pause": dict(sc="2.2.2", sev="high", owner=T, mins=30,
    title="Carousel rotates automatically with no pause control",
    impact="Content moving for more than five seconds without a pause control is a barrier for users "
           "with attention, vestibular and cognitive disabilities.",
    fix="Disable autoplay, or add a visible keyboard-reachable pause control.",
    after='<button type="button" class="carousel-pause" aria-pressed="false">\n'
          '  <span class="visually-hidden">Pause carousel</span>\n</button>',
    ),

"motion-has-pause": dict(sc="2.2.2", sev="low", owner=T, mins=10,
    title="Automatic motion detected, pause control appears present",
    impact="Likely conforming, but the control must actually work and be keyboard reachable.",
    fix="Confirm the control is reachable by Tab, has an accessible name, and genuinely stops the "
        "motion rather than only the current slide.",
    after="<!-- verify manually -->",
    ),

"nav-inconsistent": dict(sc="3.2.3", sev="medium", owner=G, mins=15,
    title="Navigation order differs between pages",
    impact="Users who learn the navigation order — especially screen reader and switch users — have "
           "to relearn it on each page.",
    fix="Present the same navigation in the same relative order on every page.",
    after="<!-- same menu, same order, every page -->",
    ),

"help-inconsistent": dict(sc="3.2.6", sev="low", owner=G, mins=10,
    title="Help/contact link not present on all pages",
    impact="WCAG 2.2 requires help mechanisms to appear in a consistent relative order wherever they "
           "are repeated.",
    fix="Place the contact link in the same position on every page.",
    after="<!-- footer contact link on every page -->",
    ),

"aria-dangling-id": dict(sc="1.3.1", sev="high", owner=T, mins=15,
    title="aria-labelledby / aria-describedby points at a missing ID",
    impact="The accessible name resolves to nothing, so the control is announced as unlabelled. "
           "Worse than no ARIA at all, because it overrides any name the element would otherwise have. "
           "Usually caused by a duplicated block or a template emitting an ID that no longer exists.",
    fix="Make the referenced ID exist and be unique, or remove the ARIA reference and use a real "
        "<label> or visible text instead.",
    after='<span id="search-label">Search this site</span>\n'
          '<input type="search" aria-labelledby="search-label">',
    ),

"duplicate-id": dict(sc="__REMOVED__", sev="low", owner=T, mins=10,
    title="Duplicate id attribute",
    impact="NOT a WCAG 2.2 failure — 4.1.1 Parsing was removed. But duplicate IDs break "
           "aria-labelledby, label[for], and skip-link targets, so fix any that ARIA depends on.",
    fix="Make IDs unique. Deprioritise unless an ARIA reference or a label depends on the ID.",
    after='<div id="block-search-1">…</div>\n<div id="block-search-2">…</div>',
    ),

"contrast-over-media": dict(sc="1.4.3", sev="high", owner=T, mins=45,
    title="Text over an image, video or gradient without sufficient contrast",
    impact="Contrast against moving or photographic backgrounds varies frame by frame, so some "
           "frames always fail. Low-vision users lose the text unpredictably.",
    fix="Put a solid or heavily-tinted scrim behind the text, move the text out of the media, or "
        "replace the background with a flat colour. Do not rely on a text-shadow.",
    after='.hero__text {{\n  background: rgba(0,0,0,.62);   /* solid scrim, not a shadow */\n'
          '  padding: 1rem 1.25rem;\n  color: #fff;\n}}',
    ),

"contrast-ui": dict(sc="1.4.11", sev="medium", owner=T, mins=20,
    title="UI component contrast below 3:1",
    impact="Form field borders, focus rings, icons and control boundaries must reach 3:1 against "
           "what is adjacent. Below that, low-vision users cannot tell where a field begins or "
           "whether a control is focused.",
    fix="Raise the border and focus-ring colours to at least 3:1 against their background. Grey "
        "hairline borders (#ccc on white is 1.6:1) are the usual culprit.",
    after='input, select, textarea {{\n  border: 1px solid #6b6b6b;   /* 3.4:1 on white */\n}}\n'
          ':focus-visible {{\n  outline: 3px solid #990000;  /* 7.9:1 on white */\n'
          '  outline-offset: 2px;\n}}',
    ),

"broken-link": dict(sc="__QA__", sev="medium", owner=C, mins=5,
    title="Broken link (404 or unreachable)",
    impact="Not a WCAG failure on its own, but it denies access to content and wastes the time of "
           "users who navigate link-by-link, for whom backtracking is expensive.",
    fix="Correct or remove the link.",
    after='<a href="/correct/path">Descriptive link text</a>',
    ),

"missing-image": dict(sc="__QA__", sev="high", owner=C, mins=5,
    title="Image fails to load",
    impact="A broken image shows alt text at best and nothing at all at worst, so any information "
           "the image carried is simply gone for every user.",
    fix="Re-upload the image to this site's media library and update the reference.",
    after='<img src="/sites/default/files/images/FILE.png" alt="…">',
    ),

"js-error": dict(sc="__QA__", sev="medium", owner=T, mins=30,
    title="JavaScript error on page load",
    impact="Script errors can leave menus, carousels and overlays half-initialised. That commonly "
           "produces exactly the accessibility failures elsewhere in this report: toggles with no "
           "aria-expanded, focus trapped in a half-open menu, carousels that never pause.",
    fix="Open DevTools → Console, reproduce, and fix the throwing script. Do this BEFORE debugging "
        "any interactive-widget accessibility issue.",
    after="// check the console on every page before remediating widgets",
    ),

"multiple-ways": dict(sc="2.4.5", sev="medium", owner=M, mins=20,
    title="Only one way to locate pages",
    impact="Users navigate differently — some browse menus, others search. At least two ways must "
           "be available.",
    fix="Provide a site search, a sitemap, or both, alongside navigation.",
    after="",
    ),
}


def check_meta(cid: str) -> dict:
    if cid in CHECKS:
        return CHECKS[cid]
    if cid.startswith("axe-"):
        return dict(sc="__AXE__", sev="medium", owner=T, mins=15,
                    title=f"axe-core: {cid[4:]}", impact="Reported by axe-core.",
                    fix="See the axe rule reference for remediation guidance.", after="",
                    )
    return dict(sc="__OTHER__", sev="low", owner=T, mins=10, title=cid, impact="",
                fix="", after="", )


# ═══════════════════════════════════════════════════════════════════════════
#  3 · IN-PAGE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════

DOM_JS = r"""
() => {
  const F = [];
  let seq = 0;

  const cssPath = el => {
    const parts = []; let n = el;
    while (n && n.nodeType === 1 && parts.length < 6) {
      let s = n.nodeName.toLowerCase();
      if (n.id) { parts.unshift(s + '#' + n.id); break; }
      const c = (n.className || '').toString().trim().split(/\s+/).filter(Boolean)[0];
      if (c) s += '.' + c;
      const sib = n.parentElement
        ? Array.from(n.parentElement.children).filter(x => x.nodeName === n.nodeName) : [];
      if (sib.length > 1) s += ':nth-of-type(' + (sib.indexOf(n) + 1) + ')';
      parts.unshift(s); n = n.parentElement;
    }
    return parts.join(' > ');
  };

  const visible = el => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0') return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const rendered = el => {
    const s = getComputedStyle(el);
    return s.display !== 'none' && s.visibility !== 'hidden';
  };

  function accName(el, d) {
    d = d || 0;
    if (!el || d > 3 || !el.getAttribute) return '';
    const lb = el.getAttribute('aria-labelledby');
    if (lb) {
      const t = lb.split(/\s+/).map(i => document.getElementById(i)).filter(Boolean)
                 .map(n => n.textContent.trim()).join(' ');
      if (t) return t;
    }
    const al = el.getAttribute('aria-label');
    if (al && al.trim()) return al.trim();
    if (/^(INPUT|SELECT|TEXTAREA)$/.test(el.tagName)) {
      if (el.id) {
        const l = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
        if (l && l.textContent.trim()) return l.textContent.trim();
      }
      const w = el.closest('label');
      if (w && w.textContent.trim()) return w.textContent.trim();
      return (el.getAttribute('title') || '').trim();
    }
    let t = '';
    for (const n of el.childNodes) {
      if (n.nodeType === 3) t += n.textContent;
      else if (n.nodeType === 1) {
        if (n.getAttribute && n.getAttribute('aria-hidden') === 'true') continue;
        if (n.tagName === 'IMG') t += ' ' + (n.getAttribute('alt') || '');
        else if (n.tagName === 'svg') {
          const ti = n.querySelector('title'); t += ' ' + (ti ? ti.textContent : '');
        } else t += ' ' + accName(n, d + 1);
      }
    }
    t = t.replace(/\s+/g, ' ').trim();
    return t || (el.getAttribute('title') || '').trim();
  }

  // ── page-level facts ──────────────────────────────────────────────────
  const bodyCls = document.body.className || '';
  const slEl = document.querySelector('link[rel=shortlink]');
  const shortlink = slEl ? (slEl.getAttribute('href') || '') : '';
  const nodeId = (shortlink.match(/node\/(\d+)/) || bodyCls.match(/page-node-(\d+)/) || [])[1] || null;
  const nodeType = (bodyCls.match(/node--type-([a-z0-9_-]+)/) ||
                    bodyCls.match(/page-node-type-([a-z0-9_-]+)/) || [])[1] || null;
  const fb = document.querySelector('[id^="block-"]');
  const themeName = fb ? (fb.id.match(/^block-([a-z0-9]+)-/) || [])[1] : null;
  const snEl = document.querySelector('.site-branding__name, .site-name, [class*=site-name]');
  const siteName = (snEl && snEl.textContent.trim()) || document.title.split('|').pop().trim();

  const allHeads = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'));
  function headAbove(el) {
    let best = null;
    for (const h of allHeads) {
      if (h.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING) best = h; else break;
    }
    return best ? (best.tagName + ' "' + best.textContent.trim().slice(0, 60) + '"') : null;
  }

  // ── WHERE is this on the page ─────────────────────────────────────────
  function locate(el) {
    if (!el || !el.getBoundingClientRect) return {
      selector: '(page)', region: 'whole page', nearest_heading: null, nearby_text: '',
      doc_x: 0, doc_y: 0, width: 0, height: 0, fold: '-', html: '',
      origin: 'theme'
    };
    const r = el.getBoundingClientRect();
    const lm = el.closest('header,[role=banner],nav,[role=navigation],main,[role=main],' +
                          'footer,[role=contentinfo],aside,[role=complementary]');
    let region = lm ? lm.tagName.toLowerCase() : null;
    if (lm && lm.getAttribute('role')) region = lm.getAttribute('role');
    const rc = el.closest('[class*="region-"]');
    const regionName = rc ? (rc.className.toString().match(/region-([a-z0-9-]+)/) || [])[1] : null;

    const blockEl = el.closest('[id^="block-"]');
    const viewEl = el.closest('[class*="view-id-"]');
    const viewId = viewEl ? (viewEl.className.toString().match(/view-id-([a-z0-9_]+)/) || [])[1] : null;
    const fieldEl = el.closest('[class*="field--name-"]');
    const fieldName = fieldEl
      ? (fieldEl.className.toString().match(/field--name-([a-z0-9_]+)/) || [])[1] : null;
    const mediaEl = el.closest('[data-entity-type="media"],[class*="media--type-"]');
    const mediaUuid = el.getAttribute('data-entity-uuid') ||
                      (mediaEl ? mediaEl.getAttribute('data-entity-uuid') : null);
    const paraEl = el.closest('[class*="paragraph--type-"]');
    const paraType = paraEl
      ? (paraEl.className.toString().match(/paragraph--type-([a-z0-9-]+)/) || [])[1] : null;
    const inMain = !!el.closest('main,[role=main],#main-content,.region-content');
    const inBody = fieldName === 'body' || !!el.closest('.field--name-body,.text-formatted');

    const own = (el.textContent || '').replace(/\s+/g, ' ').trim();
    let ctx = own.slice(0, 130);
    if (!ctx) {
      // No text of its own (image, icon, input). Anchor it between its neighbours
      // so a human can find it on the page by eye.
      let before = '', after = '';
      let n = el.previousElementSibling, hops = 0;
      while (n && !before && hops++ < 4) {
        before = (n.textContent || '').replace(/\s+/g, ' ').trim(); n = n.previousElementSibling;
      }
      n = el.nextElementSibling; hops = 0;
      while (n && !after && hops++ < 4) {
        after = (n.textContent || '').replace(/\s+/g, ' ').trim(); n = n.nextElementSibling;
      }
      const b = before ? '…' + before.slice(-55) : '';
      const a = after ? after.slice(0, 55) + '…' : '';
      ctx = (b + '  [THIS ELEMENT]  ' + a).trim();
      if (ctx === '[THIS ELEMENT]') ctx = '';
    }
    const same = Array.from(document.getElementsByTagName(el.tagName));

    return {
      selector: cssPath(el),
      region: regionName || region || 'unknown',
      nearest_heading: headAbove(el),
      nearby_text: ctx.slice(0, 130),
      nth_of_type: same.indexOf(el) + 1,
      total_of_type: same.length,
      doc_x: Math.round(r.left + window.scrollX),
      doc_y: Math.round(r.top + window.scrollY),
      width: Math.round(r.width), height: Math.round(r.height),
      fold: (r.top + window.scrollY) < 800
            ? 'above the fold' : 'below the fold (scroll ~' + Math.round(r.top + window.scrollY) + 'px)',
      html: (el.outerHTML || '').replace(/ data-a11y-id="[^"]*"/g, '')
              .replace(/\s+/g, ' ').slice(0, 400),
      origin: 'page'
    };
  }

  const add = (cid, msg, el, vars) => {
    const id = 'F' + String(++seq).padStart(3, '0');
    if (el && el.setAttribute) el.setAttribute('data-a11y-id', id);
    F.push(Object.assign({id: id, check: cid, message: msg, vars: vars || {}}, locate(el)));
  };

  // ═══ PAGE LEVEL ═══
  const lang = document.documentElement.getAttribute('lang');
  if (!lang) add('lang-missing', 'The <html> element has no lang attribute.', document.documentElement, {});
  else if (!/^[a-z]{2,3}(-[A-Za-z0-9]+)*$/.test(lang))
    add('lang-invalid', 'html[lang="' + lang + '"] is not a valid BCP 47 language tag.',
        document.documentElement, {lang: lang});
  if (!document.title || !document.title.trim())
    add('title-missing', 'Page has no <title> element.', null, {});

  for (const sh of Array.from(document.styleSheets)) {
    let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    for (const r of Array.from(rules || [])) {
      if (r.conditionText && /orientation\s*:\s*(portrait|landscape)/.test(r.conditionText)
          && /transform|rotate/.test(r.cssText))
        add('orientation-lock', 'A media query may lock display orientation.', null, {});
    }
  }

  // ═══ IMAGES ═══
  const GEN = /^(image|photo|picture|graphic|icon|logo|img|chart|org ?chart|banner|spacer|graph|screenshot|thumbnail)\.?$/i;
  document.querySelectorAll('img').forEach(img => {
    const alt = img.getAttribute('alt');
    const src = img.getAttribute('src') || '';
    const base = src.split('/').pop().split('?')[0];
    if (alt === null) add('img-no-alt', 'Image has no alt attribute at all.', img, {src: src, basename: base});
    else if (alt.trim() === '') {
      const link = img.closest('a, button');
      if (link && !accName(link).trim())
        add('img-alt-empty-in-link',
            'An image with empty alt is the only content of this link, so the link has no accessible name.',
            link, {src: src, href: link.getAttribute('href') || '#', sitename: siteName, basename: base});
    } else {
      if (GEN.test(alt.trim()))
        add('img-alt-generic',
            'Alt text "' + alt + '" names the image but conveys none of the information it contains.',
            img, {src: src, alt: alt, basename: base});
      if (/\.(png|jpe?g|gif|svg|webp)$/i.test(alt.trim()))
        add('img-alt-filename', 'Alt text is a filename: "' + alt + '".', img,
            {src: src, alt: alt, basename: base});
      if (alt.length > 150)
        add('img-alt-long', 'Alt text is ' + alt.length + ' characters long.', img,
            {src: src, alt: alt, basename: base});
      if (/\b(chart|diagram|graph|map|infographic|org|structure)\b/i.test(alt))
        add('img-complex',
            'This looks like a complex image. Check whether it renders text as pixels and needs a long description.',
            img, {src: src, alt: alt, basename: base});
    }
    try {
      const u = new URL(src, location.href);
      if (u.hostname && u.hostname !== location.hostname)
        add('img-offsite', 'Image is served from ' + u.hostname + ', a different host from this site.',
            img, {src: src, host: u.hostname, basename: base});
    } catch (e) {}
  });

  // ═══ HEADINGS ═══
  const heads = allHeads.filter(visible);
  const h1s = heads.filter(h => h.tagName === 'H1');
  if (!h1s.length)
    add('h1-missing', 'Page has no <h1>.', null, {pagetitle: document.title.split('|')[0].trim()});
  if (h1s.length > 1)
    h1s.slice(1).forEach(h => add('h1-multiple',
      'Page has ' + h1s.length + ' <h1> elements. This one reads "' + h.textContent.trim().slice(0,50) +
      '"; the others are ' + h1s.filter(x => x !== h)
        .map(x => '"' + x.textContent.trim().slice(0,35) + '"').join(', ') + '.',
      h, {pagetitle: h1s[0].textContent.trim(), text: h.textContent.trim()}));

  // Empty headings collapse to zero height, so they never pass visible().
  // Test them against rendered() in their own pass or they can never be found.
  allHeads.filter(rendered).forEach(h => {
    if (!h.textContent.trim() && !accName(h))
      add('heading-empty', 'Empty <' + h.tagName.toLowerCase() + '> with no text or accessible name.', h, {});
  });

  let prev = 0;
  heads.forEach(h => {
    const lvl = +h.tagName[1];
    if (prev && lvl > prev + 1)
      add('heading-skip',
          'Heading level jumps from h' + prev + ' to h' + lvl + ', skipping h' + (prev + 1) + '.',
          h, {expected: prev + 1, text: h.textContent.trim().slice(0, 60)});
    prev = lvl;
  });
  const hs = {};
  heads.forEach(h => {
    const t = h.textContent.trim().toLowerCase();
    if (!t) return;
    if (hs[t]) add('heading-duplicate',
      'Heading text "' + h.textContent.trim().slice(0,50) + '" appears more than once on this page.', h, {});
    hs[t] = 1;
  });

  document.querySelectorAll('p').forEach(p => {
    const kids = Array.from(p.childNodes).filter(n => n.nodeType !== 3 || n.textContent.trim());
    if (kids.length !== 1) return;
    const k = kids[0];
    if (k.nodeType !== 1 || ['STRONG','B'].indexOf(k.tagName) < 0) return;
    const t = p.textContent.trim();
    if (!t || t.length > 90 || /[.!?]$/.test(t)) return;
    const nx = p.nextElementSibling;
    if (nx && /^(P|UL|OL|DIV|TABLE|DL)$/.test(nx.tagName)) {
      const ab = headAbove(p);
      const lvl = ab ? Math.min(6, (+ab.match(/H(\d)/)[1]) + 1) : 2;
      add('bold-as-heading',
          '"' + t.slice(0,60) + '" is styled as a heading but marked up as <' +
          k.tagName.toLowerCase() + '>, so it will not appear in a screen reader\'s heading list.',
          p, {text: t, suggested: lvl});
    }
  });

  let emp = 0, firstEmp = null;
  document.querySelectorAll('p').forEach(p => {
    if (!p.textContent.replace(/[\s\u00a0]/g,'') && !p.querySelector('img,svg,input,iframe')) {
      emp++; if (!firstEmp) firstEmp = p;
    }
  });
  if (emp) add('empty-paragraphs',
    emp + ' empty paragraph(s) used as vertical spacing on this page.', firstEmp, {count: emp});

  const mn = document.querySelector('main,[role=main],#main-content,#content');
  if (mn && mn.querySelector('style'))
    add('style-in-content', 'A <style> block is embedded inside the page content.',
        mn.querySelector('style'), {});

  // ═══ LINKS ═══
  const VAGUE = /^(click here|here|read more|more|learn more|read the story|read story|details|link|this|continue|go|see more|#|>|»|→|\.\.\.)$/i;
  const byText = {};
  document.querySelectorAll('a').forEach(a => {
    if (!rendered(a)) return;
    const href = a.getAttribute('href');
    const name = accName(a).trim();
    const r = a.getBoundingClientRect();
    if (href !== null && r.width === 0 && r.height === 0)
      add('link-zero-size', 'Link occupies zero pixels but is still in the tab order.', a, {href: href});
    if (!name)
      add('link-no-name', 'Link has no accessible name — screen readers announce only "link".',
          a, {href: href || '#', icon: (a.innerHTML || '').replace(/\s+/g,' ').slice(0,60)});
    else if (VAGUE.test(name))
      add('link-vague',
          'Link text "' + name + '" does not describe its destination when read out of context.',
          a, {href: href || '#', text: name});
    if (href === '#' || href === '' || /^javascript:\s*void/i.test(href || ''))
      add('link-href-hash',
          '<a href="' + href + '"> does not navigate anywhere, so it is doing a button\'s job.',
          a, {href: href, controls: a.getAttribute('aria-controls') || 'TARGET_ID'});
    if (a.getAttribute('target') === '_blank' &&
        !/new (window|tab)/i.test(name + (a.getAttribute('title') || '')))
      add('link-newtab', 'Link "' + name.slice(0,40) + '" opens in a new tab with no warning.',
          a, {href: href, text: name});
    if (name && href) {
      const k = name.toLowerCase();
      (byText[k] = byText[k] || []).push({href: a.href, el: a});
    }
  });
  Object.keys(byText).forEach(txt => {
    const list = byText[txt];
    const t = {}; list.forEach(x => t[x.href] = 1);
    const n = Object.keys(t).length;
    if (list.length > 1 && n > 1)
      list.forEach(x => add('link-ambiguous-dupe',
        list.length + ' links on this page read "' + txt + '" but lead to ' + n +
        ' different destinations (' + Object.keys(t).map(u => {
          try { return new URL(u).pathname; } catch (e) { return u; }
        }).slice(0,3).join(', ') + '). In a screen reader\'s link list they are indistinguishable.',
        x.el, {href: x.href, text: txt}));
  });

  // ═══ BUTTONS ═══
  document.querySelectorAll('button,[role=button],input[type=submit],input[type=button]').forEach(b => {
    if (!rendered(b)) return;
    const n = (b.value || accName(b)).trim();
    if (!n) add('button-no-name', 'Button has no accessible name.', b, {});
    else if (/^[×✕✖x✗+\-<>«»‹›]$/.test(n))
      add('button-symbol-name',
          'The button\'s only accessible name is the symbol "' + n + '", which screen readers ' +
          'announce literally (often as "times") or skip.', b, {name: n});
    const ctrl = b.getAttribute('aria-controls') || b.getAttribute('data-target') ||
                 b.getAttribute('data-toggle');
    if (ctrl && !b.hasAttribute('aria-expanded'))
      add('toggle-no-expanded', 'This toggle does not expose aria-expanded state.', b, {controls: ctrl});
  });

  // ═══ FORMS ═══
  const AC = {username:'username', fname:'given-name', lname:'family-name', name:'name',
              email:'email', mail:'email', tel:'tel', phone:'tel', zip:'postal-code',
              postal:'postal-code', address:'street-address', city:'address-level2',
              org:'organization', company:'organization', country:'country-name', bday:'bday'};
  document.querySelectorAll('input,select,textarea').forEach(f => {
    const type = (f.getAttribute('type') || 'text').toLowerCase();
    if (['hidden','submit','button','reset','image'].indexOf(type) >= 0) return;
    if (!rendered(f)) return;
    const nm = accName(f);
    if (!nm) add('input-no-label', 'This form field has no programmatic label.',
                 f, {id: f.id || 'field-id', name: f.name || 'field_name', type: type});
    const key = ((f.name||'') + ' ' + (f.id||'') + ' ' + nm).toLowerCase();
    let want = null;
    Object.keys(AC).forEach(k => {
      if (!want && new RegExp('(^|[^a-z])' + k, 'i').test(key)) want = [k, AC[k]];
    });
    if (want && !f.getAttribute('autocomplete'))
      add('input-no-autocomplete',
          'Field "' + (nm || f.name) + '" collects user information but has no autocomplete attribute.',
          f, {token: want[1], name: f.name || '', type: type, id: f.id || ''});
    if (type === 'password' &&
        (f.getAttribute('onpaste') === 'return false' || f.hasAttribute('data-nopaste')))
      add('password-nopaste', 'This password field blocks paste.', f, {name: f.name || ''});
  });
  const cap = document.querySelector('[class*=captcha i],[id*=captcha i],iframe[src*=recaptcha]');
  if (cap) add('captcha', 'A CAPTCHA is present on this page.', cap, {});

  document.querySelectorAll('a,button,[role=button]').forEach(el => {
    if (!visible(el)) return;
    const al = el.getAttribute('aria-label');
    if (!al) return;
    const vis = Array.from(el.childNodes).filter(n => n.nodeType === 3)
      .map(n => n.textContent).join(' ').replace(/\s+/g,' ').trim();
    if (vis && al.toLowerCase().indexOf(vis.toLowerCase()) < 0)
      add('label-in-name',
          'Visible text "' + vis + '" is not contained in the accessible name "' + al + '".',
          el, {visible: vis, label: al});
  });

  // ═══ MEDIA ═══
  document.querySelectorAll('video,audio').forEach(m => {
    const auto = m.hasAttribute('autoplay') || m.autoplay;
    const ctl = m.hasAttribute('controls');
    const mut = m.hasAttribute('muted') || m.muted;
    const s1 = m.querySelector('source');
    const src = m.getAttribute('src') || (s1 ? s1.getAttribute('src') : '') || '';
    if (auto && !ctl)
      add('media-autoplay-no-controls',
          '<' + m.tagName.toLowerCase() + '> autoplays with no controls attribute and no pause control found.',
          m, {src: src});
    if (auto && !mut)
      add('media-autoplay-unmuted',
          '<' + m.tagName.toLowerCase() + '> autoplays without the muted attribute.', m, {src: src});
    if (m.tagName === 'VIDEO' && !m.querySelector('track[kind=captions]') &&
        m.getAttribute('aria-hidden') !== 'true')
      add('video-no-captions', 'Video has no captions track and is not marked decorative.', m, {src: src});
  });

  // ═══ LANDMARKS ═══
  if (!document.querySelector('main,[role=main]')) add('no-main', 'Page has no <main> landmark.', null, {});
  const skip = Array.from(document.querySelectorAll('a[href^="#"]')).slice(0,4)
    .filter(a => /skip|jump/i.test(a.textContent))[0];
  if (!skip) add('skip-missing', 'No skip link found near the start of the page.', null, {});
  else {
    const id = skip.getAttribute('href').slice(1);
    if (id && !document.getElementById(id) && !document.getElementsByName(id).length)
      add('skip-broken', 'Skip link points to #' + id + ', which does not exist on this page.',
          skip, {target: id});
  }
  const navs = Array.from(document.querySelectorAll('nav,[role=navigation]')).filter(visible);
  const unl = navs.filter(n => !n.getAttribute('aria-label') && !n.getAttribute('aria-labelledby'));
  if (unl.length > 1)
    add('nav-unlabelled', unl.length + ' navigation landmarks have no distinguishing label.', unl[1], {});

  // ═══ TABLES / FRAMES / HANDLERS ═══
  document.querySelectorAll('table').forEach(t => {
    if (t.getAttribute('role') === 'presentation') return;
    if (!t.querySelector('th')) add('table-no-th', 'This table has no <th> header cells.', t, {});
    else if (t.querySelectorAll('th').length > 1 && !t.querySelector('th[scope]'))
      add('table-no-scope', 'Table header cells have no scope attribute.', t, {});
  });
  document.querySelectorAll('iframe').forEach(f => {
    if (!visible(f)) return;
    if (!f.getAttribute('title') && !f.getAttribute('aria-label'))
      add('iframe-no-title', 'iframe has no title attribute.', f, {src: f.getAttribute('src') || ''});
  });
  document.querySelectorAll('[onclick]').forEach(el => {
    if (/^(A|BUTTON|INPUT|SELECT|TEXTAREA|SUMMARY)$/.test(el.tagName)) return;
    if (el.hasAttribute('tabindex')) return;
    add('click-not-focusable',
        '<' + el.tagName.toLowerCase() + '> has a click handler but cannot receive keyboard focus.', el, {});
  });

  // ═══ TARGET SIZE ═══
  const TSEL = 'a[href],button,input:not([type=hidden]),select,textarea,[role=button],[role=link],' +
               '[role=tab],[role=checkbox],[role=menuitem],summary,[tabindex]:not([tabindex="-1"])';
  document.querySelectorAll(TSEL).forEach(el => {
    if (!visible(el)) return;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    const inline = el.tagName === 'A' && s.display.indexOf('inline') === 0 && el.parentElement &&
                   /^(P|LI|TD|SPAN|H[1-6]|DD|DT)$/.test(el.parentElement.tagName);
    if (inline) return;
    if (r.width < 24 || r.height < 24)
      add('target-too-small',
          'Interactive target is ' + Math.round(r.width) + 'x' + Math.round(r.height) +
          ' CSS px; the WCAG 2.2 minimum is 24x24.', el,
          {w: Math.round(r.width), h: Math.round(r.height),
           cls: (el.className||'').toString().split(/\s+/).filter(Boolean)[0] || 'control'});
  });

  const hdr = document.querySelector('header,[role=banner],.region-header');
  let stickyH = 0;
  if (hdr) {
    const p = getComputedStyle(hdr).position;
    if (p === 'fixed' || p === 'sticky') stickyH = Math.round(hdr.getBoundingClientRect().height);
  }

  return {
    findings: F, title: document.title, lang: lang, site_name: siteName, sticky_header_px: stickyH,
    origin: 'page',
    navLinks: navs.length
      ? Array.from(navs[0].querySelectorAll('a')).map(a => accName(a).trim()).filter(Boolean) : [],
    helpLinks: Array.from(document.querySelectorAll('a')).map(a => accName(a).trim().toLowerCase())
                 .filter(n => /^(contact|help|support|contact us|get help)$/.test(n)),
    hasSearch: !!document.querySelector(
      'input[type=search],[role=search],form[action*=search],input[name*=search i]'),
    headingOutline: heads.map(h => ({level: +h.tagName[1], text: h.textContent.trim().slice(0,70)})),
    counts: {images: document.querySelectorAll('img').length,
             links: document.querySelectorAll('a').length,
             inputs: document.querySelectorAll('input,select,textarea').length,
             media: document.querySelectorAll('video,audio').length,
             headings: heads.length}
  };
}
"""

TEXT_SPACING_CSS = ("* { line-height: 1.5 !important; letter-spacing: 0.12em !important; "
                    "word-spacing: 0.16em !important; } p { margin-bottom: 2em !important; }")

CLIP_PROBE = r"""
() => {
  const out = [];
  document.querySelectorAll('p,li,td,th,h1,h2,h3,h4,h5,h6,a,button,span,div').forEach(el => {
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return;
    const oY = el.scrollHeight > el.clientHeight + 2, oX = el.scrollWidth > el.clientWidth + 2;
    const hid = s.overflow === 'hidden' || s.overflowY === 'hidden' || s.overflowX === 'hidden';
    if ((oY || oX) && hid && el.clientHeight > 0)
      out.push({tag: el.tagName.toLowerCase(), text: (el.textContent||'').trim().slice(0,60),
                cls: (el.className||'').toString().split(/\s+/).filter(Boolean)[0] || ''});
  });
  return out.slice(0, 15);
}
"""


# ═══════════════════════════════════════════════════════════════════════════
#  4 · BROWSER-ONLY CHECKS
# ═══════════════════════════════════════════════════════════════════════════

AXE_TO_SC = {
    "color-contrast": "1.4.3", "image-alt": "1.1.1", "input-image-alt": "1.1.1", "area-alt": "1.1.1",
    "link-name": "4.1.2", "button-name": "4.1.2", "label": "3.3.2", "html-has-lang": "3.1.1",
    "html-lang-valid": "3.1.1", "valid-lang": "3.1.2", "document-title": "2.4.2",
    "frame-title": "4.1.2", "heading-order": "1.3.1", "list": "1.3.1", "listitem": "1.3.1",
    "th-has-data-cells": "1.3.1", "td-headers-attr": "1.3.1", "landmark-one-main": "1.3.1",
    "region": "1.3.1", "bypass": "2.4.1", "tabindex": "2.4.3", "autocomplete-valid": "1.3.5",
    "target-size": "2.5.8", "meta-viewport": "1.4.4", "no-autoplay-audio": "1.4.2",
    "video-caption": "1.2.2", "scrollable-region-focusable": "2.1.1", "aria-required-attr": "4.1.2",
    "aria-valid-attr-value": "4.1.2", "aria-allowed-attr": "4.1.2", "aria-hidden-focus": "4.1.2",
    "nested-interactive": "4.1.2",
}


def run_axe(page, axe_src):
    try:
        if axe_src:
            page.evaluate(axe_src)
        else:
            page.add_script_tag(url="https://cdn.jsdelivr.net/npm/axe-core@4.10.2/axe.min.js")
            page.wait_for_function("() => window.axe !== undefined", timeout=15000)
        return page.evaluate("""
            async () => {
              const r = await axe.run(document, {
                runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']},
                resultTypes:['violations']});
              return r.violations.map(v => ({
                id:v.id, impact:v.impact, help:v.help, helpUrl:v.helpUrl, count:v.nodes.length,
                nodes:v.nodes.slice(0,6).map(n => ({target:n.target, html:(n.html||'').slice(0,300),
                  summary:(n.failureSummary||'').slice(0,400)}))}));
            }"""), None
    except Exception as e:
        return [], f"{type(e).__name__}: {str(e)[:160]}"


def _loc(**kw):
    d = dict(selector="(page)", region="whole page", nearest_heading=None, nearby_text="",
             doc_x=0, doc_y=0, width=0, height=0, fold="-", html="",
              vars={})
    d.update(kw)
    return d


def focus_walk(page, sticky_px, max_tabs=70):
    out = []
    try:
        page.evaluate("() => { window.scrollTo(0,0); document.body.focus(); }")
        page.keyboard.press("Tab")
    except PWError:
        return out
    sigs = []
    for i in range(max_tabs):
        try:
            info = page.evaluate(r"""
            () => {
              const el = document.activeElement;
              if (!el || el === document.body) return null;
              const r = el.getBoundingClientRect(), s = getComputedStyle(el);
              const nm = (el.getAttribute('aria-label')||el.textContent||el.value||'')
                          .replace(/\s+/g,' ').trim().slice(0,50);
              let obsc = null;
              if (r.width>0 && r.height>0) {
                const cx = Math.min(Math.max(r.left+r.width/2,1), innerWidth-1);
                const cy = Math.min(Math.max(r.top+r.height/2,1), innerHeight-1);
                const top = document.elementFromPoint(cx,cy);
                if (top && top!==el && !el.contains(top) && !top.contains(el)) {
                  const ts = getComputedStyle(top);
                  const anc = top.closest('header,.sticky,[class*=fixed]');
                  if (ts.position==='fixed'||ts.position==='sticky'||
                      (anc && ['fixed','sticky'].indexOf(getComputedStyle(anc).position)>=0))
                    obsc = (anc||top).tagName.toLowerCase()+'.'+
                           (((anc||top).className)||'').toString().split(/\s+/)[0];
                }
              }
              return {tag:el.tagName.toLowerCase(), name:nm,
                sel: el.id ? '#'+el.id
                     : el.tagName.toLowerCase()+'.'+(((el.className)||'').toString().split(/\s+/)[0]||''),
                sig: el.tagName+'|'+nm, x:Math.round(r.left+scrollX), y:Math.round(r.top+scrollY),
                w:Math.round(r.width), h:Math.round(r.height),
                off: r.width===0||r.height===0||r.bottom<0||r.right<0||r.left>innerWidth,
                hid: s.visibility==='hidden'||s.display==='none'||s.opacity==='0',
                outline: s.outlineStyle+' '+s.outlineWidth, shadow: s.boxShadow,
                obsc: obsc, url: location.href};
            }""")
        except PWError:
            break
        if info is None:
            break
        base = dict(selector=info["sel"], region="(keyboard focus order)", nearest_heading=None,
                    nearby_text=info["name"], doc_x=info["x"], doc_y=info["y"],
                    width=info["w"], height=info["h"],
                    fold="above the fold" if info["y"] < 800 else f"below the fold (scroll ~{info['y']}px)",
                    html="", )
        if info["url"] != page.url:
            out.append(dict(id=f"K{i:03d}", check="focus-navigates", vars={},
                            message=f"Tab stop {i+1} (<{info['tag']}> '{info['name']}') triggered "
                                    f"navigation on focus alone, before any activation.", **base))
            break
        if info["off"] or info["hid"]:
            out.append(dict(id=f"K{i:03d}", check="focus-offscreen", vars={},
                            message=f"Tab stop {i+1} lands on a hidden or off-screen element "
                                    f"(<{info['tag']}> '{info['name']}', {info['w']}x{info['h']}px).", **base))
        if info["obsc"]:
            out.append(dict(id=f"K{i:03d}o", check="focus-obscured", vars={"height": sticky_px or 80},
                            message=f"Tab stop {i+1} (<{info['tag']}> '{info['name']}') is covered by a "
                                    f"fixed/sticky element ({info['obsc']}).", **base))
        if (info["outline"].startswith("none") or " 0px" in info["outline"]) and info["shadow"] == "none":
            out.append(dict(id=f"K{i:03d}f", check="focus-invisible", vars={},
                            message=f"Tab stop {i+1} (<{info['tag']}> '{info['name']}') shows neither an "
                                    f"outline nor a box-shadow when focused.", **base))
        sigs.append(info["sig"])
        if len(sigs) >= 12 and len(set(sigs[-12:])) <= 3:
            out.append(dict(id=f"K{i:03d}t", check="focus-trap", vars={},
                            message=f"The last 12 tab stops cycled among {len(set(sigs[-12:]))} "
                                    f"element(s) — possible keyboard trap. Confirm by hand; this may "
                                    f"be an open modal.", **base))
            break
        try:
            page.keyboard.press("Tab")
        except PWError:
            break
    seen, ded = set(), []
    for f in out:
        k = (f["check"], f["message"][:50])
        if k not in seen:
            seen.add(k)
            ded.append(f)
    return ded[:20]


def motion_check(page, already_flagged=None):
    """2.2.2 — detect movement with no user input, then IDENTIFY THE SOURCE.

    Reporting 'something moved' with generic carousel advice is worse than
    useless: on a page whose only motion is an autoplaying video, the video
    check has already reported the same failure with the correct fix. This
    classifies the source and suppresses the duplicate.
    """
    already_flagged = already_flagged or set()
    vp = page.viewport_size or {"width": 1280, "height": 900}
    clip = {"x": 0, "y": 0,
            "width": min(1200, vp["width"]), "height": min(700, vp["height"])}
    # Sample four times, not twice. A carousel whose period divides evenly into
    # the sampling window lands on the same slide at both ends and reads as
    # static — comparing several frames makes that aliasing very unlikely.
    try:
        frames = [page.screenshot(clip=clip)]
        for _ in range(3):
            page.wait_for_timeout(2400)
            frames.append(page.screenshot(clip=clip))
    except Exception as ex:
        print(f"    motion check skipped ({type(ex).__name__})")
        return []
    if len(set(frames)) == 1:
        return []

    src = page.evaluate(r"""() => {
      const vis = el => {
        const s = getComputedStyle(el), r = el.getBoundingClientRect();
        return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0;
      };
      const desc = el => el.tagName.toLowerCase() +
        (el.id ? '#'+el.id : '') +
        ((el.className||'').toString().trim() ? '.'+(el.className||'').toString().trim().split(/\s+/)[0] : '');

      // 1. media actually playing right now
      const video = [];
      document.querySelectorAll('video,audio').forEach(m => {
        if (!m.paused && !m.ended && vis(m)) video.push(desc(m));
      });

      // 2. known carousel/slider containers that hold more than one slide
      const CAR = '[class*=slick],[class*=splide],[class*=swiper],[class*=glide],' +
                  '[class*=owl],[class*=carousel],[class*=slideshow],[class*=flickity],' +
                  '[class*=views-slideshow],[data-slider],[class*=cycle]';
      const carousel = [];
      document.querySelectorAll(CAR).forEach(el => {
        if (vis(el) && el.children.length > 1) carousel.push(desc(el));
      });

      // 3. CSS animations currently running for longer than 5s (or infinite)
      const animated = [];
      document.querySelectorAll('*').forEach(el => {
        if (animated.length > 5) return;
        const s = getComputedStyle(el);
        if (s.animationName === 'none' || s.animationPlayState !== 'running') return;
        const dur = parseFloat(s.animationDuration) || 0;
        const inf = s.animationIterationCount === 'infinite';
        if ((inf || dur > 5) && vis(el)) animated.push(desc(el));
      });

      const marquee = !!document.querySelector('marquee');
      const pause = Array.from(document.querySelectorAll('button,[role=button],a'))
        .some(x => /paus|stop|play|freeze/i.test((x.getAttribute('aria-label')||'')+' '+x.textContent));
      return {video, carousel, animated, marquee, pause};
    }""")

    loc = lambda sel: _loc(selector=sel, region="whole page")

    # Video already reported by media-autoplay-no-controls -> do not report twice.
    only_video = src["video"] and not src["carousel"] and not src["animated"] and not src["marquee"]
    if only_video:
        if "media-autoplay-no-controls" in already_flagged or "media-autoplay-unmuted" in already_flagged:
            return []      # same failure, already reported with the right fix
        return [dict(id="M001", check="media-autoplay-no-controls",
                     message=f"The page changes continuously with no user input. The source is "
                             f"playing media ({', '.join(src['video'][:2])}) with no pause control.",
                     **loc(src["video"][0]))]

    if src["carousel"]:
        note = ("A pause control appears to exist elsewhere on the page; confirm it is keyboard "
                "reachable and actually stops the rotation." if src["pause"] else
                "No pause, stop or hide control was found.")
        return [dict(id="M001", check="motion-has-pause" if src["pause"] else "motion-no-pause",
                     message=f"A rotating component ({', '.join(src['carousel'][:2])}) advances "
                             f"without user input. {note}",
                     **loc(src["carousel"][0]))]

    if src["animated"] or src["marquee"]:
        what = src["animated"][:2] or ["<marquee>"]
        return [dict(id="M001", check="motion-css-animation",
                     message=f"A looping or long-running CSS animation is playing "
                             f"({', '.join(what)}) with no way to pause it.",
                     **loc(what[0]))]

    return [dict(id="M001", check="motion-unidentified",
                 message="The rendered page changed over 7 seconds with no user input, but no "
                         "playing media, carousel or CSS animation could be identified. It may be "
                         "a third-party embed, an auto-refreshing region, or a transient load "
                         "effect that settles within five seconds.",
                 **loc("(page)"))]


def viewport_checks(page):
    out = []
    orig = page.viewport_size or {"width": 1280, "height": 900}

    page.set_viewport_size({"width": 320, "height": 800})
    page.wait_for_timeout(600)
    if page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"):
        bad = page.evaluate(r"""() => {
          const w = document.documentElement.clientWidth, out = [];
          document.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width>0 && r.right>w+2 && out.length<6 && getComputedStyle(el).position!=='fixed')
              out.push({sel: el.tagName.toLowerCase()+'.'+(((el.className)||'').toString().split(/\s+/)[0]||''),
                        w: Math.round(r.width)});
          }); return out; }""")
        names = ", ".join(f"{b['sel']} ({b['w']}px wide)" for b in bad) or "unidentified"
        out.append(dict(id="V001", check="reflow-320",
                        message=f"Horizontal scrolling is required at a 320 CSS px viewport. "
                                f"Elements overflowing: {names}.",
                        **_loc(selector=bad[0]["sel"] if bad else "(page)",
                               vars={"offenders": names,
                                     "cls": (bad[0]["sel"].split(".")[-1] if bad else "container")})))

    page.set_viewport_size({"width": 640, "height": 512})
    page.wait_for_timeout(400)
    if page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2"):
        out.append(dict(id="V002", check="resize-200",
                        message="Content requires horizontal scrolling at the 200%-zoom equivalent "
                                "(640px viewport).", **_loc()))

    page.set_viewport_size(orig)
    page.wait_for_timeout(300)
    page.add_style_tag(content=TEXT_SPACING_CSS)
    page.wait_for_timeout(500)
    clip = page.evaluate(CLIP_PROBE)
    if clip:
        sel = f"{clip[0]['tag']}.{clip[0]['cls']}" if clip[0]["cls"] else clip[0]["tag"]
        samples = "; ".join(f"<{c['tag']}> \"{c['text'][:35]}\"" for c in clip[:4])
        out.append(dict(id="V003", check="text-spacing-clip",
                        message=f"{len(clip)} element(s) clip their content when the WCAG text-spacing "
                                f"overrides are applied. Examples: {samples}",
                        **_loc(selector=sel, nearby_text=clip[0]["text"],
                               vars={"cls": clip[0]["cls"] or "text"})))
    page.reload(wait_until="networkidle")
    return out


def capture_shots(page, findings, shotdir, limit=45):
    """Screenshot each high/medium finding with the element outlined in red.

    Queries by dom_id (the per-page attribute Chromium set) but writes the file
    under the globally unique id, so pages cannot overwrite each other's shots.
    """
    shotdir.mkdir(parents=True, exist_ok=True)
    done = 0
    for f in findings:
        if done >= limit or f.get("severity") == "low":
            continue
        fid = f.get("dom_id") or f["id"]
        if not fid.startswith("F"):
            continue
        try:
            el = page.query_selector(f'[data-a11y-id="{fid}"]')
            if not el:
                continue
            el.scroll_into_view_if_needed(timeout=3000)
            page.wait_for_timeout(120)
            box = el.bounding_box()
            if not box or box["width"] < 1:
                continue
            page.evaluate("""(id) => {
                const el = document.querySelector('[data-a11y-id="'+id+'"]');
                if (!el) return;
                const r = el.getBoundingClientRect();
                const d = document.createElement('div');
                d.id = '__a11y_hl';
                Object.assign(d.style, {position:'fixed', left:(r.left-3)+'px', top:(r.top-3)+'px',
                  width:(r.width+6)+'px', height:(r.height+6)+'px', border:'3px solid #e11',
                  boxShadow:'0 0 0 3px rgba(238,17,17,.22)', pointerEvents:'none',
                  zIndex:2147483647, borderRadius:'2px'});
                document.body.appendChild(d);
            }""", fid)
            vw, vh = page.viewport_size["width"], page.viewport_size["height"]
            pad = 70
            x = max(0, box["x"] - pad)
            y = max(0, box["y"] - pad)
            clip = {"x": x, "y": y,
                    "width": max(30, min(vw - x, box["width"] + pad * 2)),
                    "height": max(30, min(vh - y, box["height"] + pad * 2))}
            page.screenshot(path=str(shotdir / f"{f['id']}.png"), clip=clip)
            f["screenshot"] = f"screenshots/{f['id']}.png"
            done += 1
        except Exception:
            pass
        finally:
            try:
                page.evaluate("() => { const d=document.getElementById('__a11y_hl'); if(d) d.remove(); }")
            except Exception:
                pass
    return done


# ═══════════════════════════════════════════════════════════════════════════
#  5 · ENRICHMENT
# ═══════════════════════════════════════════════════════════════════════════

SEV_RANK = {"high": 0, "medium": 1, "low": 2}
OWNER_LABEL = {C: "Content editor", T: "Developer (theme)", G: "Site administrator", M: "Module install"}


def fix_steps(f, ctx):
    d = f.get("origin_note") or {}
    meta = check_meta(f["check"])
    origin = d.get("origin", "theme template")
    node = d.get("node_id") or ctx.get("node_id")
    theme = d.get("theme") or ctx.get("theme") or "YOURTHEME"
    out = []

    if origin == "body field (WYSIWYG)":
        out.append("**Content** — this is inside a rich-text body field, so a content editor can fix it.")
        out.append(f"Edit at `/node/{node}/edit` → Body field" if node
                   else "Find the page under `/admin/content` and edit its Body field")
        if d.get("field_name") and d["field_name"] != "body":
            out.append(f"Field: `field_{d['field_name']}`")
    elif origin == "view":
        out.append(f"**View** — `/admin/structure/views/view/{d.get('view_id')}`")
        out.append("Check this view's field settings, row style and format settings.")
    elif origin == "paragraph":
        out.append(f"**Paragraph type** `{d.get('paragraph_type')}` — `/admin/structure/paragraphs_type`")
        if node:
            out.append(f"Content instance: `/node/{node}/edit`")
    elif origin == "block":
        bid = d.get("block_id") or ""
        out.append(f"**Block** — `/admin/structure/block/manage/{bid}`")
        tmpl = bid.replace(f"block-{theme}-", "") if theme else bid.replace("block-", "")
        out.append(f"Template override: `themes/custom/{theme}/templates/block/block--{tmpl}.html.twig`")
    elif origin == "node content":
        out.append("**Node display** — check the field's display settings.")
        if node:
            out.append(f"Content: `/node/{node}/edit`")
        if d.get("node_type"):
            out.append(f"Field config: `/admin/structure/types/manage/{d['node_type']}/fields`")
    else:
        out.append(f"**Theme** — `themes/custom/{theme}/templates/` or the theme's CSS/JS.")

    if d.get("media_uuid"):
        out.append(f"Media item UUID `{d['media_uuid']}` — manage at `/admin/content/media`")
    if d.get("block_id") and origin != "block":
        out.append(f"Containing block: `/admin/structure/block/manage/{d['block_id']}`")

    return out


def enrich(f, ctx):
    meta = check_meta(f["check"])
    lvl, name, _, _ = COVERAGE.get(meta["sc"], ("", meta["sc"], "", ""))
    f["sc"] = meta["sc"]
    f["severity"] = meta["sev"]
    f["title"] = meta["title"]
    f["impact"] = meta["impact"]
    f["criterion"] = name
    f["level"] = lvl
    f["owner"] = OWNER_LABEL.get(meta["owner"], meta["owner"])
    f["effort_min"] = meta["mins"]
    f["wcag"] = wcag_context(meta["sc"])
    v = dict(f.get("vars") or {})
    v.setdefault("src", ""); v.setdefault("href", "#")
    v.setdefault("sitename", ctx.get("site_name") or "Site")
    v.setdefault("text", ""); v.setdefault("pagetitle", "Page title")
    try:
        f["fix_what"] = meta["fix"].format(**v)
    except Exception:
        f["fix_what"] = meta["fix"]
    try:
        f["fix_after"] = meta["after"].format(**v)
    except Exception:
        f["fix_after"] = meta["after"]
    f["fix_before"] = f.get("html", "")
    f["fix_steps"] = fix_steps(f, ctx)
    return f


# ═══════════════════════════════════════════════════════════════════════════
#  5b · CONSOLIDATION — one defect, one finding; one source, one card
#
#  Three distinct kinds of duplication have to be handled separately:
#    1. A more specific check whose fix already covers a broader one
#       (a link that should be a button needs a name as part of that change).
#    2. Two checks landing on the same element under the same criterion.
#    3. axe-core reporting a defect this scanner already found NATIVELY on the
#       SAME element. Matching by criterion alone is too blunt — axe:list and
#       our heading checks are both 1.3.1 but are entirely different defects —
#       so elements are matched by identity, not by selector string.
#  Nothing is deleted silently: whatever is folded in is recorded on the
#  surviving finding and shown in the report.
# ═══════════════════════════════════════════════════════════════════════════

SUBSUMES = {
    # winner                       : checks whose fix it already contains
    "link-href-hash":              {"link-no-name"},
    "img-alt-empty-in-link":       {"link-no-name"},
    "link-ambiguous-dupe":         {"link-vague"},
    "button-symbol-name":          {"button-no-name"},
    "skip-broken":                 {"skip-missing"},
    "media-autoplay-no-controls":  {"motion-no-pause", "motion-unidentified"},
    "img-alt-filename":            {"img-alt-generic"},
}


def resolve_axe_targets(page, axe_nodes):
    """Map each axe node to the data-a11y-id of the element it points at, so an
    axe result can be matched to a native finding by element identity."""
    sels = [str(n["target"][0]) for n in axe_nodes if n.get("target")]
    if not sels:
        return {}
    try:
        return page.evaluate("""(sels) => {
          const out = {};
          for (const s of sels) {
            try {
              const el = document.querySelector(s);
              if (el) out[s] = el.getAttribute('data-a11y-id') || null;
            } catch (e) { /* axe selectors are not always valid querySelector input */ }
          }
          return out;
        }""", sels)
    except Exception:
        return {}


def consolidate(findings):
    """Collapse duplicates and group everything sharing a source."""
    for f in findings:
        f["source_key"] = f.get("selector") or "(page)"
        f.setdefault("also", [])

    by_src = defaultdict(list)
    for f in findings:
        by_src[f["source_key"]].append(f)

    dropped = set()

    # ── 1. subsumption: a specific fix that already covers a broader one ──
    for src, group in by_src.items():
        present = {f["check"]: f for f in group if id(f) not in dropped}
        for winner, losers in SUBSUMES.items():
            if winner not in present:
                continue
            for f in group:
                if f["check"] in losers and id(f) not in dropped:
                    dropped.add(id(f))
                    present[winner]["also"].append(
                        f"Also flagged as \u201c{f.get('title', f['check'])}\u201d "
                        f"({f['sc']}); the change above resolves it.")

    # ── 2. axe duplicating a native finding on the SAME element ──
    #    This MUST run before the generic same-criterion collapse below, or the
    #    axe result gets swept up there and loses its attribution — it would be
    #    folded in as an anonymous duplicate instead of credited as independent
    #    confirmation, which is the more useful fact for the reader.
    native_by_el = defaultdict(set)
    for f in findings:
        if id(f) in dropped or f["check"].startswith("axe-"):
            continue
        if f.get("dom_id"):
            native_by_el[f["dom_id"]].add(f["sc"])
    for f in findings:
        if id(f) in dropped or not f["check"].startswith("axe-"):
            continue
        el = f.get("axe_dom_id")
        if el and f["sc"] in native_by_el.get(el, ()):
            for g in findings:
                if (g.get("dom_id") == el and g["sc"] == f["sc"]
                        and id(g) not in dropped and not g["check"].startswith("axe-")):
                    dropped.add(id(f))
                    g["also"].append("Independently confirmed by axe-core "
                                     f"({f['check'][4:]}).")
                    break

    # ── 3. same element, same criterion ──
    for src, group in by_src.items():
        live = [f for f in group if id(f) not in dropped]
        per_sc = defaultdict(list)
        for f in live:
            per_sc[f["sc"]].append(f)
        for sc, same in per_sc.items():
            if len(same) < 2:
                continue
            same.sort(key=lambda f: (SEV_RANK.get(f["severity"], 3),
                                     f["check"].startswith("axe-")))
            keep = same[0]
            for f in same[1:]:
                dropped.add(id(f))
                if f["check"].startswith("axe-"):
                    keep["also"].append("Independently confirmed by axe-core "
                                        f"({f['check'][4:]}).")
                else:
                    keep["also"].append(
                        f"Same element also matched \u201c{f.get('title', f['check'])}\u201d "
                        f"under the same criterion.")

    kept = [f for f in findings if id(f) not in dropped]

    # ── 4. cross-reference everything left that shares a source ──
    live_by_src = defaultdict(list)
    for f in kept:
        live_by_src[f["source_key"]].append(f)
    for src, group in live_by_src.items():
        if len(group) < 2 or src == "(page)":
            continue
        for f in group:
            f["related"] = [(g["id"], g.get("title", g["check"]), g["sc"])
                            for g in group if g is not f]
            f["group_size"] = len(group)

    # cluster same-source findings together, worst source first
    order = {src: min(SEV_RANK.get(f["severity"], 3) for f in g)
             for src, g in live_by_src.items()}
    kept.sort(key=lambda f: (order.get(f["source_key"], 3), f["source_key"],
                             SEV_RANK.get(f["severity"], 3), f["sc"]))
    return kept, len(dropped)


# ═══════════════════════════════════════════════════════════════════════════
#  6 · SCAN ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════════

def scan_page(page, url, axe_src, deep, shotdir, page_no=1, native=True):
    res = {"url": url, "findings": [], "screenshots": 0}
    try:
        page.goto(url, wait_until="networkidle", timeout=45000)
    except Exception as e:
        res["findings"] = [enrich(dict(id="E001", check="__load__",
                                       message=f"Could not load page: {type(e).__name__}", **_loc()), {})]
        return res
    page.wait_for_timeout(800)

    if native:
        dom = page.evaluate(DOM_JS)
        ctx = dict(site_name=dom.get("site_name", ""))
        res.update({k: v for k, v in dom.items() if k != "findings"})
        findings = list(dom["findings"])
    else:
        dom, ctx, findings = {}, {}, []
    for f in findings:                      # make ids unique across pages
        f["dom_id"] = f["id"]
        f["id"] = f"P{page_no}-{f['id']}"

    viol, axe_err = run_axe(page, axe_src)
    res["axe_error"] = axe_err
    axe_map = resolve_axe_targets(page, [n for v in viol for n in v["nodes"]])
    axe_extra = []
    for v in viol:
        sc = AXE_TO_SC.get(v["id"], "__AXE__")
        sev = {"critical": "high", "serious": "high", "moderate": "medium"}.get(v.get("impact"), "low")
        for j, n in enumerate(v["nodes"][:4]):
            summary = (n.get("summary") or "").splitlines()
            axe_extra.append(dict(
                id=f"A{v['id'][:12]}-{j}", check=f"axe-{v['id']}",
                message=f"{v['help']} ({v['count']} instance(s) on this page). "
                        f"{summary[0] if summary else ''}".strip(),
                _sc=sc, _sev=sev, _url=v.get("helpUrl", ""),
                **_loc(selector=str(n["target"][0]) if n.get("target") else "",
                       region="(reported by axe-core)", html=n.get("html", ""))))

    for f in findings:
        enrich(f, ctx)
    for f in axe_extra:
        enrich(f, ctx)
        f["sc"] = f.pop("_sc")
        f["severity"] = f.pop("_sev")
        lvl, nm, _, _ = COVERAGE.get(f["sc"], ("", f["sc"], "", ""))
        f["criterion"], f["level"] = nm, lvl
        f["fix_what"] = f"Consult the axe rule reference: {f.pop('_url', '')}"
    findings += axe_extra

    if shotdir:
        res["screenshots"] = capture_shots(page, findings, shotdir, limit=45 if deep else 20)

    if deep:
        seen_checks = {f["check"] for f in findings}
        deep_f = (focus_walk(page, dom.get("sticky_header_px", 0))
                  + motion_check(page, seen_checks) + viewport_checks(page))
        for f in deep_f:                        # these need page-prefixing too
            f["dom_id"] = f["id"]
            f["id"] = f"P{page_no}-{f['id']}"
            findings.append(enrich(f, ctx))

    findings, merged = consolidate(findings)
    res["merged_duplicates"] = merged
    res["findings"] = findings
    return res


def cross_page(pages):
    out = []
    titles = defaultdict(list)
    for p in pages:
        if p.get("title"):
            titles[p["title"].strip()].append(p["url"])
    for t, urls in titles.items():
        if len(urls) > 1:
            out.append(enrich(dict(id="X001", check="title-duplicate",
                message=f'{len(urls)} pages share the title "{t[:60]}": {", ".join(urls)}',
                **_loc(selector="<title>", region="document head", nearby_text=t,
                       html=f"<title>{t}</title>", )), {}))
    navs = [(p["url"], tuple(p.get("navLinks") or [])) for p in pages if p.get("navLinks")]
    if len(navs) > 1:
        for u, n in navs[1:]:
            if n and n != navs[0][1]:
                out.append(enrich(dict(id="X002", check="nav-inconsistent",
                    message=f"Navigation link order on {u} differs from {navs[0][0]}.",
                    **_loc(selector="nav", region="header", )), {}))
                break
    helps = [(p["url"], p.get("helpLinks") or []) for p in pages]
    missing = [u for u, h in helps if not h]
    if missing and len(missing) < len(helps):
        out.append(enrich(dict(id="X003", check="help-inconsistent",
            message=f"A contact/help link is present on some pages but missing on {len(missing)}: "
                    f"{', '.join(missing[:4])}",
            **_loc(selector="footer a", region="footer", )), {}))
    if pages and not any(p.get("hasSearch") for p in pages) and not any(p.get("navLinks") for p in pages):
        out.append(enrich(dict(id="X004", check="multiple-ways",
            message="No site search and no navigation menu were found on any scanned page.",
            **_loc(selector="(site)", region="site-wide")), {}))
    return out


# ═══════════════════════════════════════════════════════════════════════════
#  7 · REPORTS
# ═══════════════════════════════════════════════════════════════════════════

def finding_card(f, url):
    w = f.get("wcag") or wcag_context(f["sc"])
    L = [f"#### `{f['id']}` · {f.get('title','')}", "",
         f"**{f['severity'].upper()}** · {f.get('owner','')} · ~{f.get('effort_min','')} min", "",
         "**Guideline being addressed**", "", "| | |", "|---|---|"]
    if w["is_wcag"]:
        L += [f"| Criterion | **{w['citation']}** |",
              f"| Principle | {w['principle']} |",
              f"| Guideline | {w['guideline']} |",
              f"| Introduced in | WCAG {w['version']} |",
              f"| What it requires | {w['requirement']} |"]
    else:
        L += [f"| Classification | **{w['citation']}** |",
              f"| Note | {w['requirement']} |"]
    L += ["", "**Where on the site**", "", "| | |", "|---|---|",
          f"| Page | {url} |", f"| Region | {f.get('region','—')} |"]
    if f.get("nearest_heading"):
        L.append(f"| Under heading | {f['nearest_heading']} |")
    if f.get("nearby_text"):
        L.append(f"| Nearby text | \"{f['nearby_text'][:110]}\" |")
    if f.get("nth_of_type"):
        L.append(f"| Instance | element {f['nth_of_type']} of {f.get('total_of_type','?')} of its type |")
    if f.get("doc_y"):
        L.append(f"| Position | x={f['doc_x']} y={f['doc_y']} · {f.get('fold','')} |")
    L += [f"| Selector | `{f.get('selector','')}` |", ""]
    if f.get("screenshot"):
        L += [f"![Location of {f['id']} on the page, element outlined in red]({f['screenshot']})", ""]
    L += ["**How it fails**", "",
          f"*{f.get('title','')}* — {f.get('message', '')}"]
    if f.get("impact"):
        L += ["", f"**Effect on users.** {f['impact']}"]
    L += ["", "**What to change**", "", f.get("fix_what", "")]
    if f.get("fix_before"):
        L += ["", "Current markup:", "", "```html", f["fix_before"][:400], "```"]
    if f.get("fix_after"):
        L += ["", "Change to:", "", "```html", f["fix_after"], "```"]
    L += ["", "**Where to fix**", ""]
    L += [f"- {s}" for s in f.get("fix_steps", [])]
    if f.get("also"):
        L += ["", "**Folded into this finding**", ""]
        L += [f"- {a}" for a in f["also"]]
    if f.get("related"):
        L += ["", f"**Same element, {f['group_size']} findings in total** — fix them "
                  f"together in one edit:", ""]
        L += [f"- `{rid}` · {sc} · {t}" for rid, t, sc in f["related"]]
    L += ["", "---", ""]
    return L


def write_reports(pages, xpage, outdir, meta):
    outdir.mkdir(parents=True, exist_ok=True)
    allf = [(p["url"], f) for p in pages for f in p["findings"]] + [("(all pages)", f) for f in xpage]

    (outdir / "report.json").write_text(json.dumps(
        {"meta": meta, "pages": pages, "cross_page": xpage,
         "coverage": {k: dict(zip(("level", "name", "status", "note"), v)) for k, v in COVERAGE.items()}},
        indent=2, default=str), encoding="utf-8")

    with open(outdir / "findings.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ID", "Severity", "SC", "Criterion", "Level", "WCAG version",
                    "Principle", "Guideline", "What the criterion requires",
                    "How it fails", "Title", "Page", "Region",
                    "Under heading", "Nearby text", "Selector", "Position Y", "Screenshot",
                    "Source element", "Findings on this element", "Related finding IDs",
                    "Owner", "Effort (min)", "What is wrong", "What to change", "Replacement markup",
                    "Where to fix", "Status", "Assigned to", "Date fixed"])
        for url, f in allf:
            wc = f.get("wcag") or wcag_context(f["sc"])
            w.writerow([f["id"], f["severity"], f["sc"], f.get("criterion", ""), f.get("level", ""),
                        wc.get("version", ""), wc.get("principle", ""), wc.get("guideline", ""),
                        wc.get("requirement", ""), f.get("message", "")[:400],
                        f.get("title", ""), url, f.get("region", ""), f.get("nearest_heading", "") or "",
                        (f.get("nearby_text", "") or "")[:90], f.get("selector", ""), f.get("doc_y", ""),
                        f.get("screenshot", ""), f.get("source_key", ""),
                        f.get("group_size", 1),
                        " ".join(r for r, _, _ in f.get("related", [])),
                        f.get("owner", ""), f.get("effort_min", ""),
                        f.get("message", "")[:400], f.get("fix_what", "")[:400],
                        f.get("fix_after", "")[:400],
                        " | ".join(f.get("fix_steps", []))[:500], "Open", "", ""])

    # coverage.md
    cl = ["# WCAG 2.2 A/AA — test coverage manifest", "",
          f"Generated {meta['generated']} · {meta['pages_scanned']} page(s)", "",
          "This manifest exists so the scan cannot be mistaken for a full audit.", ""]
    b = defaultdict(list)
    for sc, (lvl, nm, st, nt) in sorted(COVERAGE.items(), key=lambda x: [int(n) for n in x[0].split(".")]):
        b[st].append((sc, lvl, nm, nt))
    hd = {AUTO: ("Tested automatically", "Machine-decided. A clean result here is meaningful."),
          HEUR: ("Flagged for human confirmation", "Signals detected; each hit needs review."),
          MANUAL: ("NOT TESTED — requires a human", "The scanner is silent. **Silence is not a pass.**")}
    for st in (AUTO, HEUR, MANUAL):
        t, blurb = hd[st]
        cl += [f"## {t} ({len(b[st])} of {len(COVERAGE)})", "", blurb, "",
               "| SC | Level | Criterion | Notes |", "|---|---|---|---|"]
        cl += [f"| {sc} | {lvl} | {nm} | {nt} |" for sc, lvl, nm, nt in b[st]]
        cl.append("")
    cl += ["---", "", "**4.1.1 Parsing** was removed in WCAG 2.2 and is deliberately not tested.", ""]
    (outdir / "coverage.md").write_text("\n".join(cl), encoding="utf-8")

    counts = defaultdict(int)
    for _, f in allf:
        counts[f["severity"]] += 1
    by_owner = defaultdict(lambda: [0, 0])
    for _, f in allf:
        by_owner[f.get("owner", "?")][0] += 1
        by_owner[f.get("owner", "?")][1] += f.get("effort_min", 0)

    r = [f"# Accessibility findings — {meta['site']}", "",
         f"**Generated:** {meta['generated']}  ",
         f"**Standard:** WCAG 2.2 Level AA  ",
         f"**Pages scanned:** {meta['pages_scanned']}  ",
         f"**Deep checks:** {'yes' if meta['deep'] else 'no (--fast)'}  ",
         f"**axe-core:** {meta['axe_status']}", "",
         "Every finding states where it is on the site, what is wrong, the markup to change, and "
         "where to fix it. See `coverage.md` for what was **not** tested.", "",
         f"Duplicates merged: **{meta.get('merged', 0)}**. Findings sharing an element are "
         "grouped and cross-referenced so one element is one job.", "",
         "## Totals", "", "| Severity | Count |", "|---|---|",
         f"| High | {counts['high']} |", f"| Medium | {counts['medium']} |",
         f"| Low | {counts['low']} |", f"| **Total** | **{sum(counts.values())}** |", "",
         "## Work split by owner", "", "| Owner | Findings | Estimated effort |", "|---|---|---|"]
    for o, (n, m) in sorted(by_owner.items(), key=lambda x: -x[1][0]):
        r.append(f"| {o} | {n} | {m // 60}h {m % 60}m |")
    r += ["", "## Fix these first", "",
          "High severity, ordered by how little time each takes.", "",
          "| ID | Finding | SC | Page | Owner | Min |", "|---|---|---|---|---|---|"]
    for u, f in sorted([(u, f) for u, f in allf if f["severity"] == "high"],
                       key=lambda x: x[1].get("effort_min", 99))[:12]:
        r.append(f"| `{f['id']}` | {f.get('title','')} | {f['sc']} | "
                 f"{urlparse(u).path or u} | {f.get('owner','')} | {f.get('effort_min','')} |")
    r.append("")

    if xpage:
        r += ["## Site-wide findings", ""]
        for f in xpage:
            r += finding_card(f, "(all pages)")

    r += ["## Findings by page", ""]
    for p in pages:
        r += [f"### {p['url']}", ""]
        c = p.get("counts", {})
        if c:
            r += [f"*{c.get('headings',0)} headings · {c.get('images',0)} images · {c.get('links',0)} links "
                  f"· {c.get('inputs',0)} form fields · {c.get('media',0)} media elements*", ""]
        if p.get("headingOutline"):
            r += ["<details><summary>Heading outline for this page</summary>", ""]
            r += [f"{'  ' * (h['level'] - 1)}- h{h['level']}: {h['text']}" for h in p["headingOutline"][:40]]
            r += ["", "</details>", ""]
        if not p["findings"]:
            r += ["No automated findings. This does **not** mean the page conforms — see "
                  "the manual criteria in `coverage.md`.", ""]
            continue
        for f in p["findings"]:
            r += finding_card(f, p["url"])

    saw = {f["check"] for _, f in allf}
    r += ["## Manual testing still required", "",
          "Twenty-two criteria cannot be automated. Based on what this scan found, prioritise these:", ""]
    todo = []
    if any(c.startswith(("media-", "motion-")) or c == "video-no-captions" for c in saw):
        todo.append("**Watch the video/carousel** with the sound off, then with the screen off. Decide "
                    "whether it conveys information (needs captions and a text alternative — 1.2.1–1.2.3) "
                    "or is decorative (mark it aria-hidden).")
    todo += ["**Keyboard only.** Unplug the mouse. Tab every page: can you reach everything, always see "
             "where you are, and escape every menu and modal?",
             "**Screen reader.** VoiceOver (Cmd+F5). Pull up the heading list with VO+U — does it "
             "describe the page?",
             "**Zoom to 400%** and read a full content page.",
             "**Check colour is never the only signal** — 1.4.1 cannot be automated at all."]
    if any(c.startswith("input-") or c == "captcha" for c in saw):
        todo.append("**Submit every form** empty and with invalid values. Are errors announced, tied to "
                    "their field, and do they suggest a correction (3.3.1, 3.3.3)?")
    if "focus-trap" in saw or "link-href-hash" in saw:
        todo.append("**Open and close the search overlay and mobile menu by keyboard.** Does Escape close "
                    "them? Does focus return to the trigger (2.1.2)?")
    r += [f"{i}. {t}" for i, t in enumerate(todo, 1)] + [""]
    (outdir / "report.md").write_text("\n".join(r), encoding="utf-8")

    write_html(allf, outdir, meta, counts, by_owner)


def write_html(allf, outdir, meta, counts, by_owner):
    e = htmlmod.escape

    def md(t: str) -> str:
        """Escape, then render the small markdown subset used in guidance strings
        (**bold** and `code`) so it doesn't leak as literal asterisks/backticks."""
        t = e(t or "")
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        return t
    SEVC = {"high": "#b3261e", "medium": "#8a4708", "low": "#4a5560"}
    cards = []
    for url, f in allf:
        shot = (f'<img src="{f["screenshot"]}" alt="Screenshot of the page area containing {e(f["id"])}, '
                f'with the affected element outlined in red">') if f.get("screenshot") else ""
        rows = [("Page", f'<a href="{e(url)}">{e(url)}</a>'), ("Region", e(f.get("region", "-")))]
        if f.get("nearest_heading"):
            rows.append(("Under heading", e(f["nearest_heading"])))
        if f.get("nearby_text"):
            rows.append(("Nearby text", f'"{e(f["nearby_text"][:110])}"'))
        if f.get("nth_of_type"):
            rows.append(("Instance", f'element {f["nth_of_type"]} of {f.get("total_of_type","?")}'))
        if f.get("doc_y"):
            rows.append(("Position", f'x={f["doc_x"]} y={f["doc_y"]} — {e(f.get("fold",""))}'))
        rows.append(("Selector", f'<code>{e(f.get("selector",""))}</code>'))
        loc = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
        before = (f'<p class="lbl">Current markup</p><pre>{e(f["fix_before"][:400])}</pre>'
                  if f.get("fix_before") else "")
        after = (f'<p class="lbl">Change to</p><pre class="fix">{e(f["fix_after"])}</pre>'
                 if f.get("fix_after") else "")
        steps = "".join(f"<li>{md(x)}</li>" for x in f.get("fix_steps", []))
        also = ("<h4>Folded into this finding</h4><ul class=\"dr\">"
                + "".join(f"<li>{e(a)}</li>" for a in f["also"]) + "</ul>") if f.get("also") else ""
        rel = ("<div class=\"related\"><strong>Same element — "
               f"{f.get('group_size',0)} findings, fix together:</strong><ul>"
               + "".join(f'<li><a href="#{e(r)}"><code>{e(r)}</code></a> · {e(sc)} · {e(t)}</li>'
                         for r, t, sc in f["related"]) + "</ul></div>") if f.get("related") else ""
        imp = (f'<p class="impact"><strong>Effect on users.</strong> {e(f.get("impact",""))}</p>'
               if f.get("impact") else "")
        w = f.get("wcag") or wcag_context(f["sc"])
        if w["is_wcag"]:
            cite = (f'<p class="cite"><strong>{e(w["citation"])}</strong></p>'
                    f'<table class="loc">'
                    f'<tr><th>Principle</th><td>{e(w["principle"])}</td></tr>'
                    f'<tr><th>Guideline</th><td>{e(w["guideline"])}</td></tr>'
                    f'<tr><th>Introduced</th><td>WCAG {e(w["version"])}</td></tr>'
                    f'<tr><th>Requires</th><td>{e(w["requirement"])}</td></tr></table>')
        else:
            cite = (f'<p class="cite cite--nonwcag"><strong>{e(w["citation"])}</strong></p>'
                    f'<p class="notewcag">{e(w["requirement"])}</p>')
        cards.append(f"""
<article class="card" id="{e(f['id'])}" data-sev="{f['severity']}" data-owner="{e(f.get('owner',''))}">
 <header>
  <span class="badge" style="background:{SEVC.get(f['severity'],'#555')}">{f['severity'].upper()}</span>
  <span class="fid">{e(f['id'])}</span>
  <h3>{e(f.get('title',''))}</h3>
  <p class="sc">{e(f.get('owner',''))} · ~{f.get('effort_min','')} min</p>
 </header>
 <div class="grid">
  <div><h4>Guideline being addressed</h4>{cite}
   <h4>Where on the site</h4><table class="loc">{loc}</table>{shot}</div>
  <div><h4>How it fails</h4><p><em>{e(f.get('title',''))}</em> — {e(f.get('message',''))}</p>{imp}
   <h4>What to change</h4><p>{md(f.get('fix_what',''))}</p>{before}{after}
   <h4>Where to fix</h4><ul class="fix">{steps}</ul>{also}{rel}</div>
 </div>
</article>""")

    orows = "".join(f"<tr><td>{e(o)}</td><td>{n}</td><td>{m//60}h {m%60}m</td></tr>"
                    for o, (n, m) in sorted(by_owner.items(), key=lambda x: -x[1][0]))
    doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Accessibility findings — {e(meta['site'])}</title><style>
:root{{--ink:#1c1c1c;--mut:#666;--line:#e4e0dc;--red:#990000}}
*{{box-sizing:border-box}}
body{{font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink);
max-width:1180px;margin:0 auto;padding:32px 24px;background:#fff}}
h1{{font-size:28px;margin:0 0 4px}}
h2{{font-size:20px;margin:38px 0 14px;padding-bottom:6px;border-bottom:2px solid var(--line)}}
h3{{font-size:16px;margin:6px 0}}
h4{{font-size:12px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut);margin:16px 0 6px}}
.sub{{color:var(--mut);margin:0 0 22px}}
table{{border-collapse:collapse;width:100%;font-size:13px;margin:8px 0 14px}}
th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
.loc th{{width:120px;color:var(--mut);font-weight:600;font-size:12px}}
.card{{border:1px solid var(--line);border-radius:8px;padding:18px 20px;margin:0 0 20px;
border-left:5px solid var(--line)}}
.card[data-sev=high]{{border-left-color:#b3261e}}
.card[data-sev=medium]{{border-left-color:#8a4708}}
.card[data-sev=low]{{border-left-color:#8a949e}}
.badge{{display:inline-block;color:#fff;font-size:10px;font-weight:700;letter-spacing:.06em;
padding:3px 7px;border-radius:3px;vertical-align:2px}}
.fid{{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--mut);margin-left:8px}}
.sc{{color:var(--mut);font-size:12.5px;margin:2px 0 0}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:26px}}
@media(max-width:860px){{.grid{{grid-template-columns:1fr}}}}
pre{{background:#f7f6f5;border:1px solid var(--line);border-radius:5px;padding:10px 12px;font-size:12px;
overflow-x:auto;white-space:pre-wrap;word-break:break-word;margin:4px 0 12px}}
pre.fix{{border-left:3px solid #1f7a3d;background:#f4faf6}}
.lbl{{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:10px 0 2px}}
.impact{{background:#fdf6f5;border-left:3px solid #b3261e;padding:8px 12px;font-size:13.5px;margin:8px 0}}
.dr li{{font-size:13.5px;margin-bottom:4px}}
.cite{{margin:0 0 8px;font-size:13.5px;padding:8px 12px;background:#f4f6f8;
 border-left:3px solid #2a5d8f;border-radius:0 4px 4px 0}}
.cite--nonwcag{{background:#faf7f2;border-left-color:#8a6d3b}}
.notewcag{{font-size:13px;color:#555;margin:0 0 12px}}
.related{{margin-top:14px;padding:10px 12px;background:#f2f6f2;border-left:3px solid #3d7a4e;
 border-radius:0 4px 4px 0;font-size:13px}}
.related ul{{margin:6px 0 0;padding-left:18px}} .related li{{margin-bottom:3px}}
img{{max-width:100%;border:1px solid var(--line);border-radius:5px;margin-top:10px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:12px;background:#f2f0ee;padding:1px 4px;
border-radius:3px;word-break:break-all}}
.filters{{margin:18px 0}}
.filters button{{font:inherit;font-size:13px;padding:5px 12px;margin:0 6px 6px 0;border:1px solid var(--line);
border-radius:20px;background:#fff;cursor:pointer}}
.filters button[aria-pressed=true]{{background:var(--red);color:#fff;border-color:var(--red)}}
.note{{background:#f7f6f5;border-left:3px solid var(--red);padding:12px 16px;margin:16px 0;font-size:14px}}
</style></head><body>
<h1>Accessibility findings</h1>
<p class="sub">{e(meta['site'])} · {e(meta['generated'])} · WCAG 2.2 Level AA ·
{meta['pages_scanned']} page(s) · axe-core: {e(meta['axe_status'])}</p>
<div class="note"><strong>Read <code>coverage.md</code> alongside this.</strong> Automated testing decides
roughly a third of WCAG 2.2 AA. Twenty-two criteria were not tested at all — silence is not a pass.</div>
<h2>Totals</h2><table><tr><th>Severity</th><th>Count</th></tr>
<tr><td>High</td><td>{counts['high']}</td></tr><tr><td>Medium</td><td>{counts['medium']}</td></tr>
<tr><td>Low</td><td>{counts['low']}</td></tr>
<tr><td><strong>Total</strong></td><td><strong>{sum(counts.values())}</strong></td></tr></table>
<h2>Work split by owner</h2>
<table><tr><th>Owner</th><th>Findings</th><th>Estimated effort</th></tr>{orows}</table>
<h2>Findings</h2>
<div class="filters">
<button aria-pressed="true" data-f="all">All</button>
<button aria-pressed="false" data-f="high">High only</button>
<button aria-pressed="false" data-f="Content editor">Content editor</button>
<button aria-pressed="false" data-f="Developer (theme)">Developer</button></div>
{''.join(cards)}
<script>
document.querySelectorAll('.filters button').forEach(function(b){{
 b.addEventListener('click',function(){{
  document.querySelectorAll('.filters button').forEach(function(x){{x.setAttribute('aria-pressed','false');}});
  b.setAttribute('aria-pressed','true');
  var f=b.dataset.f;
  document.querySelectorAll('.card').forEach(function(c){{
   c.hidden = !(f==='all' || c.dataset.sev===f || c.dataset.owner===f);
  }});
 }});
}});
</script></body></html>"""
    (outdir / "report.html").write_text(doc, encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════
#  9 · SELF TEST + CLI
# ═══════════════════════════════════════════════════════════════════════════

FIXTURE = """<!DOCTYPE html><html><head><title>Fixture</title>
<link rel="shortlink" href="/node/42"></head>
<body class="node--type-page page-node-42">
<header id="block-mytheme-branding" class="region-header"><a href="#"></a>
<a href="/"><img src="logo.png" alt=""></a><button>&times;</button></header>
<main id="main-content"><div class="field--name-body">
<h1>One</h1><h1>Two</h1><h3>Skipped</h3>
<img src="chart.png" alt="org chart">
<p><strong>Mission</strong></p><p>Body copy.</p><p>&nbsp;</p>
<a href="/a">Read more</a> <a href="/b">Read more</a>
<video autoplay src="x.mp4"></video>
<form><input type="text" name="your_email"><input type="text" id="nolabel"></form>
<table><tr><td>x</td></tr></table>
</div></main></body></html>"""


def selftest():
    tmp = pathlib.Path("/tmp/_a11y_fx.html")
    tmp.write_text(FIXTURE, encoding="utf-8")
    want = {"lang-missing", "img-alt-empty-in-link", "button-symbol-name", "h1-multiple",
            "heading-skip", "img-alt-generic", "bold-as-heading", "empty-paragraphs",
            "link-ambiguous-dupe", "media-autoplay-no-controls", "input-no-label",
            "input-no-autocomplete", "table-no-th", "skip-missing", "link-no-name"}
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1280, "height": 900})
        pg.goto(tmp.as_uri())
        dom = pg.evaluate(DOM_JS)
        b.close()
    got = {f["check"] for f in dom["findings"]}
    ctx = dict(site_name=dom.get("site_name", ""))
    print(f"self-test: {len(dom['findings'])} findings, {len(got)} distinct checks")
    body = [f for f in dom["findings"] if f["check"] == "img-alt-generic"]
    if body:
        s = enrich(dict(body[0]), ctx)
        print(f"sample: {s['id']} {s['sc']} '{s['title']}'")
        print(f"  region={s['region']}  under={s['nearest_heading']}")
        print(f"  owner={s['owner']}  fix steps={len(s['fix_steps'])}")
        print(f"  fix_after starts: {s['fix_after'][:60]!r}")
    miss = want - got
    if miss:
        print(f"\nFAIL — checks not fired: {sorted(miss)}")
        return 1
    print("\nPASS — Chromium, DOM checks, location capture and fix enrichment all working.")
    return 0


SKIP_EXT = re.compile(r"\.(pdf|jpe?g|png|gif|svg|webp|zip|gz|docx?|xlsx?|pptx?|"
                      r"mp4|mp3|wav|avi|mov|css|js|json|xml|rss|ics)$", re.I)


def _canon(url: str, root) -> str | None:
    """Same-host, extension-filtered, trailing-slash-normalised URL, or None."""
    try:
        p = urlparse(url)
    except ValueError:
        return None
    if p.scheme not in ("http", "https") or p.hostname != root.hostname:
        return None
    path = p.path or "/"
    if SKIP_EXT.search(path):
        return None
    c = f"{p.scheme}://{p.netloc}{path}"
    return c.rstrip("/") or f"{p.scheme}://{p.netloc}/"


def read_sitemap(page, site: str, root, depth: int = 0) -> list[str]:
    """Pull URLs from /sitemap.xml, following sitemap-index files one level.
    Catches orphan pages that link-crawling alone would miss."""
    if depth > 1:
        return []
    urls = []
    candidates = ([f"{site.rstrip('/')}/sitemap.xml"] if depth == 0 else [site])
    for sm in candidates:
        try:
            r = page.request.get(sm, timeout=15000)
            if not r.ok:
                continue
            body = r.text()
        except Exception:
            continue
        if "<sitemapindex" in body[:2000]:
            children = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)[:20]
            for child in children:
                urls += read_sitemap(page, child, root, depth + 1)
        else:
            for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body):
                c = _canon(loc, root)
                if c:
                    urls.append(c)
    return urls


def discover(page, site, limit, use_sitemap=True):
    """Breadth-first same-host crawl, seeded with the sitemap when one exists."""
    root = urlparse(site)
    seen, found = set(), []
    queue = [site.rstrip("/") or site]

    if use_sitemap:
        sm = read_sitemap(page, site, root)
        if sm:
            uniq = [u for u in dict.fromkeys(sm) if u not in queue]
            print(f"  sitemap.xml: {len(uniq)} URL(s)")
            queue += uniq
        else:
            print("  sitemap.xml: none found, crawling links only")

    while queue and len(found) < limit:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        try:
            page.goto(u, wait_until="domcontentloaded", timeout=25000)
        except Exception:
            continue
        # a redirect may land somewhere already queued
        landed = _canon(page.url, root) or u
        if landed in found:
            continue
        found.append(landed)
        seen.add(landed)
        try:
            hrefs = page.eval_on_selector_all("a[href]", "e => e.map(x => x.href)")
        except Exception:
            hrefs = []
        for h in hrefs:
            c = _canon(h, root)
            if c and c not in seen and c not in queue:
                queue.append(c)

    if queue:
        print(f"  note: stopped at --crawl {limit}; {len(queue)} more URL(s) were queued")
    return found


SET_SCHEME_JS = """(scheme) => {
  if (typeof __md_set !== "function") return false;
  const inputs = [...document.querySelectorAll('input[name="__palette"]')];
  const index = inputs.findIndex(x => x.getAttribute("data-md-color-scheme") === scheme);
  if (index < 0) return false;
  const x = inputs[index];
  __md_set("__palette", {index, color: {
    media: x.getAttribute("data-md-color-media") || "",
    scheme,
    primary: x.getAttribute("data-md-color-primary"),
    accent: x.getAttribute("data-md-color-accent")}});
  return true;
}"""


def main():
    ap = argparse.ArgumentParser(description="WCAG 2.2 AA scanner with remediation-ready findings.")
    ap.add_argument("--site")
    ap.add_argument("--urls")
    ap.add_argument("--crawl", type=int, default=100,
                    help="Max pages to discover when using --site (default 100)")
    ap.add_argument("--no-sitemap", action="store_true",
                    help="Skip sitemap.xml and crawl links only")
    ap.add_argument("--out", default=None,
                    help="report folder (default docs-site/a11y, or docs-site/a11y/<scheme> with --scheme)")
    ap.add_argument("--scheme", default=None,
                    help="scan in this Material color scheme, e.g. slate for dark mode "
                         "(default: the theme's first palette)")
    ap.add_argument("--axe", default=str(DEFAULT_AXE))
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--axe-core", action="store_true",
                    help="automated gate: fast scan, exit 1 when axe-core reports a non-minor violation")
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    if not a.site and not a.urls:
        # No arguments: serve the built site from docs-site/site and scan it.
        site_dir = ROOT / "docs-site" / "site"
        if not site_dir.is_dir():
            ap.error("nothing to scan: build first (tools/build_docs.py + mkdocs build), or pass --site/--urls")
        import http.server, threading, functools
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(site_dir))
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8123), handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        a.site = "http://127.0.0.1:8123"
        a._selfserved = site_dir

    axe_src, axe_status = None, "CDN (will attempt download)"
    if a.axe:
        p = pathlib.Path(a.axe)
        if not p.exists():
            print(f"axe file not found: {p}")
            return 1
        axe_src, axe_status = p.read_text(encoding="utf-8"), f"local ({p.name})"

    if a.out is None:
        a.out = str(ROOT / "docs-site" / "a11y" / (a.scheme or ""))
    outdir = pathlib.Path(a.out)
    shotdir = outdir / "screenshots"
    t0 = time.time()

    with sync_playwright() as pw:
        br = pw.chromium.launch(headless=not a.headed)
        ctx = br.new_context(viewport={"width": 1280, "height": 900},
                             user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                                        "(KHTML, like Gecko) Chrome/141.0 Safari/537.36 a11y_scan")
        page = ctx.new_page()
        if a.urls:
            urls = [u.strip() for u in pathlib.Path(a.urls).read_text().splitlines()
                    if u.strip() and not u.startswith("#")]
            site = a.site or urlparse(urls[0]).netloc
        elif getattr(a, "_selfserved", None):
            base = getattr(a, "_selfserved")
            urls = [a.site + "/"] + sorted(
                a.site + "/" + f.parent.relative_to(base).as_posix() + "/"
                for f in base.rglob("index.html") if f.parent != base)
            site = a.site
        else:
            print(f"Discovering pages under {a.site} …")
            urls = discover(page, a.site.rstrip("/"), a.crawl, use_sitemap=not a.no_sitemap)
            site = a.site
        print(f"{len(urls)} page(s) to scan\n")

        if a.scheme:
            # Material restores a reader's scheme from localStorage on every
            # page. Store the choice the way its own toggle does, through
            # the page's __md_set, so the key's scope and the toggle's index
            # are always the theme's own.
            page.goto(urls[0], wait_until="networkidle", timeout=45000)
            chosen = page.evaluate(SET_SCHEME_JS, a.scheme)
            if not chosen:
                print(f"no palette toggle for scheme {a.scheme!r} on {urls[0]}")
                return 1
            print(f"Color scheme: {a.scheme}\n")

        results = []
        for i, u in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] {u}")
            r = scan_page(page, u, axe_src, not a.fast and not a.axe_core, None if a.axe_core else shotdir, page_no=i, native=not a.axe_core)
            if a.scheme:
                shown = page.evaluate("document.body.getAttribute('data-md-color-scheme')")
                if shown != a.scheme:
                    print(f"    page shows scheme {shown!r}, not {a.scheme!r}; stopping")
                    return 1
            if i == 1:
                if r.get("axe_error"):
                    print(f"    axe unavailable ({r['axe_error'][:60]}) — contrast not tested")
                    axe_status = f"UNAVAILABLE — {r['axe_error'][:50]}"
                else:
                    axe_status = axe_status.replace("will attempt download", "loaded")
            hi = sum(1 for f in r["findings"] if f["severity"] == "high")
            print(f"    {len(r['findings'])} finding(s), {hi} high, {r.get('screenshots',0)} screenshot(s)")
            results.append(r)
        br.close()

    xp = cross_page(results) if not a.axe_core else []
    meta = dict(site=site, generated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
                pages_scanned=len(results), deep=not a.fast and not a.axe_core, axe_status=axe_status,
                merged=sum(p.get("merged_duplicates", 0) for p in results),
                duration_s=round(time.time() - t0, 1))
    write_reports(results, xp, outdir, meta)



    tot = sum(len(p["findings"]) for p in results) + len(xp)
    hi = sum(1 for p in results for f in p["findings"] if f["severity"] == "high")
    print(f"\n{'='*68}")
    print(f"  {tot} findings ({hi} high) across {len(results)} pages in {meta['duration_s']}s")
    print(f"  {outdir/'report.html'}    ← open this: full cards with screenshots")
    print(f"  {outdir/'report.md'}      same content in markdown")
    print(f"  {outdir/'findings.csv'}   tracker with Status / Assigned to / Date fixed")
    print(f"  {outdir/'coverage.md'}    what was NOT tested")
    print(f"  {outdir/'report.json'}    machine-readable")
    print(f"{'='*68}")
    if a.axe_core:
        gate = [f for p in results for f in p["findings"]
                if f["check"].startswith("axe-") and f["severity"] in ("high", "medium")]
        if gate:
            print(f"\nGATE: FAIL — {len(gate)} axe-core violation(s) at Level A/AA (see the report)")
            return 1
        print(f"\nGATE: PASS — no axe-core violations at Level A/AA")
    return 0


if __name__ == "__main__":
    sys.exit(main())
