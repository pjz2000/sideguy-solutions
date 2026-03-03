#!/usr/bin/env python3
"""
ship013_metadata_repair.py — Public API for SHIP-013 dry-run and callers.

Adapts the internal _ship013_metadata_repair module to the argument signatures
expected by the SHIP-013A dry-run script:

    extract_service(txt)       → str   (full HTML text → clean service name)
    categorize(p, txt)         → str   (path + text → category constant)
    make_desc(service, cat)    → str   (2-arg; picks variant 0)
    make_title(service)        → str   (1-arg; builds a clean title)
    is_desc_broken(txt)        → bool  (full HTML text → checks meta description)

All heavy logic lives in _ship013_metadata_repair; this module is a thin
public adapter so scripts can `from ship013_metadata_repair import ...`
without caring about internal signatures.
"""

import re
from pathlib import Path

import _ship013_metadata_repair as _internal

# ── Re-export constants that callers may need ────────────────────────────────
SKIP_FILES         = _internal.SKIP_FILES
TEMPLATE_DESC_MARKERS = _internal.TEMPLATE_DESC_MARKERS
DESC_TEMPLATES     = _internal.DESC_TEMPLATES


# ── Adapted public functions ─────────────────────────────────────────────────

def extract_service(txt: str) -> str:
    """Extract clean service name from a full HTML document string.

    Parses <h1> and <title> from the text, then delegates to the
    internal extract_service(h1, title) implementation.
    """
    h1_m    = re.search(r'<h1[^>]*>([^<]+)</h1>', txt, re.IGNORECASE)
    title_m = re.search(r'<title>([^<]+)</title>', txt, re.IGNORECASE)
    h1    = h1_m.group(1).strip()    if h1_m    else ''
    title = title_m.group(1).strip() if title_m else ''
    return _internal.extract_service(h1, title)


def categorize(p, txt: str = '') -> str:
    """Categorise a page.

    Accepts:
      categorize(path_or_slug)           — original 1-arg form
      categorize(path_or_slug, txt)      — new 2-arg form from dry-run

    The second argument (full HTML text) is accepted for forward-
    compatibility but the category is determined from the slug/filename
    alone (same as the internal implementation).
    """
    slug = Path(p).name if not isinstance(p, str) else p
    return _internal.categorize(slug)


def make_desc(service: str, cat: str, variant: int = 0) -> str:
    """Build a meta description for (service, category).

    Signature matches both the internal 3-arg form and the dry-run's
    2-arg form; variant defaults to 0.
    """
    return _internal.make_desc(service, cat, variant)


def make_title(service: str, existing: str = '', cat: str = 'OTHER') -> str:
    """Build a page title from a service name.

    Returns a new title string. The 1-arg form used by the dry-run
    always generates a title (ignores existing-title length guard).
    """
    result = _internal.make_title(service, existing, cat)
    # make_title returns None when existing is already good; the dry-run
    # just wants to see what we *would* generate, so fall back to a default.
    if result is None:
        has_sd = 'san diego' in service.lower()
        result = f"{service} | SideGuy" if has_sd else f"{service} San Diego | SideGuy"
        if len(result) > 65:
            max_svc = 65 - len(' San Diego | SideGuy')
            result = f"{service[:max_svc].rstrip()} San Diego | SideGuy"
    return result


def is_desc_broken(txt: str) -> bool:
    """Return True if a page's meta description is missing or template-generated.

    Accepts a full HTML document string and extracts the <meta> description
    before delegating to the internal checker.
    """
    # Try both attribute orderings that appear in the wild
    desc_m = (
        re.search(r'<meta\s+name=["\']description["\']\s+content="([^"]*)"', txt, re.IGNORECASE) or
        re.search(r'<meta\s+content="([^"]*)"\s+name=["\']description["\']',  txt, re.IGNORECASE)
    )
    desc = desc_m.group(1).strip() if desc_m else ''
    return _internal.is_desc_broken(desc)
