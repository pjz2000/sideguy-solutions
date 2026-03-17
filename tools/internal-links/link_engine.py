import re
from pathlib import Path


def _replace_in_text_only(html: str, keyword: str, link_tag: str) -> tuple[str, int]:
    """Replace keyword only in text nodes, skipping HTML tag attribute values."""
    parts = re.split(r'(<[^>]+>)', html)
    result = []
    replaced = False
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    for part in parts:
        if part.startswith('<'):
            result.append(part)          # inside a tag — never touch
        elif not replaced:
            new_part, n = pattern.subn(link_tag, part, count=1)
            if n:
                replaced = True
            result.append(new_part)
        else:
            result.append(part)
    return ''.join(result), 1 if replaced else 0

# Scan both public/ and root-level pages
ROOT_DIRS = [
    Path("/workspaces/sideguy-solutions/public"),
    Path("/workspaces/sideguy-solutions"),
]

# keyword → actual destination page on sideguy.solutions
# Ordered longest-match first to prevent partial overlaps
KEYWORD_LINKS = [
    ("ai scheduling automation",    "/hubs/category-ai-automation.html"),
    ("ai invoice automation",        "/hubs/category-ai-automation.html"),
    ("ai crm automation",            "/hubs/category-ai-automation.html"),
    ("ai lead qualification",        "/hubs/category-ai-automation.html"),
    ("ai email automation",          "/hubs/category-ai-automation.html"),
    ("ai intake form automation",    "/hubs/category-ai-automation.html"),
    ("ai customer support automation","/hubs/category-ai-automation.html"),
    ("ai chatbot",                   "/ai-automation-hub.html"),
    ("ai automation",                "/ai-automation-hub.html"),
    ("missed call",                  "/problems/missed-call-text-back.html"),
    ("no-show",                      "/problems/no-show-reduction-automation.html"),
    ("appointment reminder",         "/problems/calendar-booking-double-booked-fix.html"),
    ("double booking",               "/problems/calendar-booking-double-booked-fix.html"),
    ("webhook",                      "/problems/zapier-task-failed-webhook-timeout.html"),
    ("zapier",                       "/problems/zapier-task-failed-webhook-timeout.html"),
    ("payment processing",           "/hubs/category-payments.html"),
    ("chargeback",                   "/hubs/category-payments.html"),
    ("stripe",                       "/hubs/category-payments.html"),
    ("soc-2",                        "/hubs/category-compliance.html"),
    ("compliance",                   "/hubs/category-compliance.html"),
    ("knowledge hub",                "/knowledge-hub.html"),
]

# Marker to avoid re-linking the same keyword twice per page
MARKER = "data-sg-linked"

pages = []
for d in ROOT_DIRS:
    if d == Path("/workspaces/sideguy-solutions"):
        pages += list(d.glob("*.html"))   # root only, not recursive
    else:
        pages += list(d.rglob("*.html"))

updated = 0
skipped = 0

for page in pages:
    try:
        text = page.read_text(errors="ignore")
    except Exception:
        skipped += 1
        continue

    # Don't modify <head>, <style>, <script> blocks
    head_end = text.find("</head>")
    if head_end == -1:
        head_end = 0
    head = text[:head_end]
    body = text[head_end:]

    changed = False
    for keyword, dest in KEYWORD_LINKS:
        link_tag = f'<a href="{dest}" {MARKER}>{keyword}</a>'
        if MARKER + f'>{keyword}<' in body:
            continue  # already linked
        # Case-insensitive single replacement in body text nodes only
        # (never inside HTML attribute values — prevents nested-anchor corruption)
        new_body, n = _replace_in_text_only(body, keyword, link_tag)
        if n:
            body = new_body
            changed = True

    if changed:
        page.write_text(head + body)
        updated += 1

print(f"Internal links inserted : {updated} pages updated")
print(f"Skipped (unreadable)    : {skipped}")

