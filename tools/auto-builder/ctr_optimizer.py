"""
ctr_optimizer.py — Retrofit all problem pages with sharp, click-worthy titles,
unique meta descriptions, and H1s derived from slug intent patterns.
"""
import os, re

PAGES_DIR = "public/problem-pages"
LOG = "docs/internal-links/ctr-optimizer-log.txt"

# Intent pattern → (title template, meta template)
# {T} = topic phrase (slug words, title-cased)
# {TL} = topic phrase (lower-case)
PATTERNS = [
    # why-is-X-so-expensive
    (r"why[-_]is[-_](.+?)[-_]so[-_]expensive",
     "Why Is {T} So Expensive? — Honest Breakdown · SideGuy San Diego",
     "Real reasons {TL} costs so much in San Diego — what operators need to know before signing anything.",
     "Why Is {T} So Expensive?"),

    # how-to-lower-X or how-to-reduce-X
    (r"how[-_]to[-_](lower|reduce)[-_](.+)",
     "How to Lower {T} — Real Options for San Diego Operators · SideGuy",
     "Practical ways to cut {TL} costs without switching providers or guessing. Plain-language guidance from SideGuy.",
     "How to Lower {T}"),

    # what-is-X
    (r"what[-_]is[-_](.+)",
     "What Is {T}? — Plain-Language Answer · SideGuy San Diego",
     "Clear, honest explanation of {TL} — no jargon, no vendor spin. Know what you're dealing with before you spend.",
     "What Is {T}?"),

    # who-helps-with-X or who-do-i-call-for-X
    (r"who[-_](helps[-_]with|do[-_]i[-_]call[-_]for)[-_](.+)",
     "Who Helps With {T} in San Diego? · SideGuy",
     "Not sure who to call for {TL}? SideGuy maps the right person for your situation — before you pay for the wrong one.",
     "Who Helps With {T} in San Diego?"),

    # is-X-worth-it
    (r"is[-_](.+?)[-_]worth[-_]it",
     "Is {T} Worth It? — Honest Answer for San Diego Operators · SideGuy",
     "Straight answer on whether {TL} is worth the cost for a small business. No upsell. No fluff.",
     "Is {T} Worth It?"),

    # X-vs-Y
    (r"(.+?)[-_]vs[-_](.+)",
     "{T} — Which Is Right for Your San Diego Business? · SideGuy",
     "Side-by-side breakdown of {TL} — what actually matters for local operators, not what vendors tell you.",
     "{T} — Which Is Right for You?"),

    # X-stopped-working or X-not-working
    (r"(.+?)[-_](stopped[-_]working|not[-_]working)",
     "{T} Stopped Working — What to Check First · SideGuy San Diego",
     "{TL} down? Here's what to check before you call anyone or pay for a service call.",
     "{T} Stopped Working — What to Check First"),

    # X-near-me
    (r"(.+?)[-_]near[-_]me",
     "{T} Near San Diego — What to Ask Before You Hire · SideGuy",
     "Looking for {TL} near San Diego? Know what fair pricing looks like and what questions to ask first.",
     "{T} Near San Diego — What to Ask First"),

    # X-cost or X-pricing
    (r"(.+?)[-_](cost|pricing)(?:[-_]san[-_]diego)?$",
     "How Much Does {T} Cost in San Diego? — Real Price Breakdown · SideGuy",
     "Real price ranges for {TL} in San Diego. No estimates pulled from thin air — just honest operator context.",
     "How Much Does {T} Cost in San Diego?"),

    # X-for-small-business
    (r"(.+?)[-_]for[-_]small[-_]business",
     "{T} for Small Business — What Actually Works · SideGuy San Diego",
     "What San Diego small businesses actually need to know about {TL} — without the enterprise sales pitch.",
     "{T} for Small Business"),

    # X-roi
    (r"(.+?)[-_]roi",
     "{T} ROI — Is It Worth the Investment? · SideGuy San Diego",
     "Honest look at {TL} ROI for San Diego operators. What to measure, what to ignore, what to ask vendors.",
     "{T} — Is the ROI Real?"),

    # X-san-diego (generic local)
    (r"(.+?)[-_]san[-_]diego$",
     "{T} in San Diego — What Operators Need to Know · SideGuy",
     "Plain-language guide to {TL} for San Diego businesses. Clarity before cost — that's the SideGuy promise.",
     "{T} in San Diego — What to Know"),
]

FALLBACK_TITLE = "{T} — SideGuy San Diego Guide"
FALLBACK_META  = "SideGuy explains {TL} for San Diego operators. Clear answers before you spend money."
FALLBACK_H1    = "{T}"


INTENT_PREFIXES = re.compile(
    r"^(why-is-|how-to-lower-|how-to-reduce-|what-is-|who-helps-with-|"
    r"who-do-i-call-for-|is-|when-|where-|does-|can-|should-|will-|"
    r"how-much-does-|how-much-is-)", re.I
)
INTENT_SUFFIXES = re.compile(
    r"(-so-expensive|-worth-it|-stopped-working|-not-working|-san-diego"
    r"|-near-me-san-diego|-near-me|-cost-san-diego|-pricing-san-diego"
    r"|-cost|-pricing|-roi|-for-small-business|-san-marcos|-encinitas"
    r"|-carlsbad|-escondido|-coronado|-chula-vista|-vista|-el-cajon)$", re.I
)

def core_topic(slug):
    """Strip intent words to get the pure topic phrase."""
    t = slug.lower()
    t = INTENT_PREFIXES.sub("", t)
    t = INTENT_SUFFIXES.sub("", t)
    # strip trailing -vs-* for vs pattern
    t = re.sub(r"-vs-.+$", "", t)
    return t.replace("-", " ").strip()


def topic_from_slug(slug):
    """Remove trailing -san-diego for display, strip common suffixes."""
    t = slug.replace("-", " ")
    return t


def apply_pattern(slug):
    slug_lower = slug.lower()
    topic = core_topic(slug)          # clean core topic, no intent words
    T  = topic.title()
    TL = topic.lower()

    for pattern, title_tpl, meta_tpl, h1_tpl in PATTERNS:
        m = re.search(pattern, slug_lower)
        if m:
            title = title_tpl.replace("{T}", T).replace("{TL}", TL)
            meta  = meta_tpl.replace("{T}", T).replace("{TL}", TL)
            h1    = h1_tpl.replace("{T}", T).replace("{TL}", TL)
            meta = meta[:155]
            return title, meta, h1

    # Fallback — use core topic
    return (
        FALLBACK_TITLE.replace("{T}", T),
        FALLBACK_META.replace("{T}", T).replace("{TL}", TL)[:155],
        FALLBACK_H1.replace("{T}", T),
    )


def patch_page(path, slug):
    html = open(path).read()
    title, meta, h1 = apply_pattern(slug)

    # Replace <title>
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', html, count=1)

    # Replace first <meta name="description"> (two exist in template — replace both)
    html = re.sub(
        r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\'][^/]*/?>',
        f'<meta name="description" content="{meta}"/>',
        html
    )

    # Replace canonical href
    html = re.sub(
        r'href="https://sideguysolutions\.com/[^"]*"',
        f'href="https://sideguysolutions.com/{slug}.html"',
        html, count=1
    )

    # Replace H1
    html = re.sub(r'(<h1[^>]*>)[^<]*(</h1>)', rf'\g<1>{h1}\g<2>', html, count=1)

    with open(path, "w") as f:
        f.write(html)
    return title, meta


def run():
    files = [f for f in os.listdir(PAGES_DIR) if f.endswith(".html")]
    log_lines = ["# CTR Optimizer Log\n"]
    updated = 0

    for fname in sorted(files):
        slug = fname.replace(".html", "")
        path = os.path.join(PAGES_DIR, fname)
        title, meta = patch_page(path, slug)
        log_lines.append(f"- [{slug}]\n  title: {title}\n  meta: {meta}\n")
        updated += 1

    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "w") as f:
        f.write("\n".join(log_lines))

    print(f"CTR optimizer complete: {updated} pages updated")
    print(f"Log: {LOG}")

run()
