import os
import re
import json
import glob
import math
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from collections import defaultdict, Counter

ROOT = "."
OUT_DIR = "docs/intelligence"
DATA_DIR = "data/signals"
BRIEF_MD = os.path.join(OUT_DIR, "daily-upgrade-brief.md")
BRIEF_JSON = os.path.join(OUT_DIR, "daily-upgrade-brief.json")
SIGNALS_JSON = os.path.join(DATA_DIR, "latest-signals.json")

FEEDS = [
    ("OpenAI Blog", "https://openai.com/news/rss.xml"),
    ("Anthropic News", "https://www.anthropic.com/news/rss.xml"),
    ("Google Blog", "https://blog.google/rss/"),
    ("Google Search Central", "https://developers.google.com/search/blog/rss.xml"),
    ("Hacker News Front Page", "https://hnrss.org/frontpage"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge AI", "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml")
]

STOPWORDS = {
    "the","and","for","with","that","this","from","into","your","you","are","how","why","what",
    "when","where","can","will","just","more","than","about","after","before","over","under",
    "they","them","their","have","has","had","was","were","its","it","our","out","new","now",
    "not","but","who","all","use","using","used","via","get","gets","make","makes","made",
    "best","top","day","days","week","weeks","today","latest","update","launch","announces",
    "announced","release","releases","released","news","guide","blog","post","posts","report",
    "says","saying","say","next","future","tools","tool","app","apps","software","company",
    "companies","business","businesses","internet","web","online","site","sites","page","pages",
    "system","systems","service","services","help","helps","helping","explained","explain",
    "small","local","real","human","better","improve","improves","improving","upgrade","upgrades",
    "san","diego"
}

KEYWORD_GROUPS = {
    "ai_agents": [
        "agent","agents","agentic","computer use","computer-use","browser use","operator",
        "workflow","autonomous","automation"
    ],
    "ai_search": [
        "search","seo","ranking","rankings","google search","search console","indexing",
        "crawl","crawling","discover"
    ],
    "payments": [
        "payments","payment","merchant","checkout","settlement","stablecoin","solana",
        "chargeback","processor","processing","fees"
    ],
    "dev_tools": [
        "copilot","github","cursor","claude","openai api","api","sdk","developer",
        "coding agent","coding","repo","terminal"
    ],
    "small_business_ops": [
        "small business","smb","operator","ops","workflow","crm","scheduling","lead",
        "customer support","automation"
    ],
    "energy": [
        "solar","battery","ev charging","energy","grid","utility","clean tech","hvac"
    ],
    "betting_markets": [
        "kalshi","prediction market","polymarket","sports betting","dfs","underdog","odds"
    ]
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 SideGuyTrendRadar/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()

def clean_html(text):
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.S|re.I)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.S|re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def parse_rss(xml_bytes):
    text = xml_bytes.decode("utf-8", errors="ignore")
    root = ET.fromstring(text)
    items = []
    for item in root.findall(".//item"):
        title = clean_html("".join(item.findtext("title", default="")))
        link = clean_html("".join(item.findtext("link", default="")))
        desc = clean_html("".join(item.findtext("description", default="")))
        pub = clean_html("".join(item.findtext("pubDate", default="")))
        if title:
            items.append({"title": title, "link": link, "summary": desc, "published": pub})
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns):
        title = clean_html("".join(entry.findtext("atom:title", default="", namespaces=ns)))
        summary = clean_html("".join(entry.findtext("atom:summary", default="", namespaces=ns)))
        if not summary:
            summary = clean_html("".join(entry.findtext("atom:content", default="", namespaces=ns)))
        link = ""
        for l in entry.findall("atom:link", ns):
            href = l.attrib.get("href", "")
            if href:
                link = href
                break
        published = (
            entry.findtext("atom:published", default="", namespaces=ns)
            or entry.findtext("atom:updated", default="", namespaces=ns)
        )
        if title:
            items.append({"title": title, "link": link, "summary": summary, "published": clean_html(published)})
    return items

def normalize_token(token):
    token = token.lower().strip()
    token = re.sub(r"[^a-z0-9\-\+ ]", "", token)
    token = re.sub(r"\s+", " ", token)
    return token.strip()

def tokenize(text):
    text = text.lower().replace("/", " ").replace("-", " ")
    words = re.findall(r"[a-z0-9\+]{2,}", text)
    return [w for w in words if w not in STOPWORDS and len(w) >= 3]

def detect_groups(text):
    found = []
    hay = text.lower()
    for group, terms in KEYWORD_GROUPS.items():
        for t in terms:
            if t.lower() in hay:
                found.append(group)
                break
    return found

def title_to_topic(title, summary):
    combined = f"{title} {summary}"
    tokens = tokenize(combined)
    counts = Counter(tokens)
    top = [w for w, _ in counts.most_common(8)]
    groups = detect_groups(combined)
    pretty = list(groups[:2])
    for w in top:
        if w not in pretty:
            pretty.append(w)
    return pretty[:6]

def read_html(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def visible_text(html):
    t = re.sub(r"<script.*?</script>", " ", html, flags=re.S|re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S|re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def score_page(html, filename):
    text = visible_text(html).lower()
    links = len(re.findall(r'<a\s[^>]*href=', html, flags=re.I))
    words = len(text.split())
    score = 0
    if re.search(r"<h1[^>]*>.*?</h1>", html, flags=re.I|re.S):
        score += 8
    if words >= 700:
        score += 14
    elif words >= 400:
        score += 10
    elif words >= 250:
        score += 6
    if links >= 12:
        score += 12
    elif links >= 6:
        score += 8
    elif links >= 3:
        score += 4
    if re.search(r"faq|frequently asked", text): score += 10
    if re.search(r"last updated|updated|build version|timestamp", text): score += 6
    if re.search(r"text pj|773-544-1231", text): score += 12
    if re.search(r"clarity before cost|real human|human help|operator", text): score += 8
    if re.search(r"how it works|process|what happens next", text): score += 8
    fn = filename.lower()
    if "payment" in fn: bucket = "payments"
    elif "seo" in fn or "search" in fn: bucket = "seo"
    elif "ai" in fn or "automation" in fn or "agent" in fn: bucket = "ai"
    elif "hvac" in fn or "electric" in fn or "plumb" in fn or "roof" in fn: bucket = "services"
    elif "energy" in fn or "solar" in fn: bucket = "energy"
    elif "bet" in fn or "kalshi" in fn or "money" in fn: bucket = "money"
    else: bucket = "general"
    return score, bucket, words, links, text

def collect_pages():
    pages = []
    for path in glob.glob("*.html"):
        if os.path.basename(path).startswith("."): continue
        html = read_html(path)
        if not html.strip(): continue
        score, bucket, words, links, text = score_page(html, path)
        pages.append({"file": path, "score": score, "bucket": bucket, "words": words, "links": links, "text": text})
    return pages

def page_match_score(page, signal):
    score = 0
    combined = f"{signal['title']} {signal['summary']}".lower()
    for group in signal["groups"]:
        if group == "ai_agents":
            if page["bucket"] == "ai": score += 22
            if any(x in page["text"] for x in ["agent","automation","operator","workflow"]): score += 10
        elif group == "ai_search":
            if page["bucket"] == "seo": score += 22
            if any(x in page["text"] for x in ["seo","search","indexing","ranking","google"]): score += 10
        elif group == "payments":
            if page["bucket"] == "payments": score += 22
            if any(x in page["text"] for x in ["payments","settlement","chargeback","processor","solana"]): score += 10
        elif group == "dev_tools":
            if page["bucket"] == "ai": score += 12
            if any(x in page["text"] for x in ["claude","github","copilot","cursor","terminal","repo"]): score += 10
        elif group == "small_business_ops":
            if any(x in page["text"] for x in ["small business","operator","lead","automation","workflow"]): score += 12
        elif group == "energy":
            if page["bucket"] == "energy" or any(x in page["file"].lower() for x in ["solar","energy","ev","hvac"]): score += 18
        elif group == "betting_markets":
            if page["bucket"] == "money": score += 16
    topic_tokens = set(signal["topics"])
    page_tokens = set(tokenize(page["file"].replace(".html", "").replace("-", " ")))
    score += len(topic_tokens.intersection(page_tokens)) * 8
    score += max(0, 50 - page["score"]) * 0.35
    if page["words"] >= 250: score += 4
    return round(score, 2)

def suggest_actions(page, signal):
    text = page["text"]
    actions = []
    if not re.search(r"faq|frequently asked", text):
        actions.append(f"add FAQ about: {signal['short_question']}")
    if not re.search(r"how it works|process|what happens next", text):
        actions.append("add how-it-works / process block")
    if not re.search(r"last updated|updated|build version|timestamp", text):
        actions.append("add freshness timestamp / build version")
    if not re.search(r"text pj|773-544-1231", text):
        actions.append("add premium Text PJ orb / human CTA")
    if len(re.findall(r'<a\s[^>]*href=', read_html(page["file"]), flags=re.I)) < 6:
        actions.append("add 5-10 contextual internal links to hub + sibling pages")
    if "ai_agents" in signal["groups"]: actions.append("add section on agent workflows / computer-use AI")
    if "ai_search" in signal["groups"]: actions.append("add search impact note / indexing implications")
    if "payments" in signal["groups"]: actions.append("add payments angle: lower fees, settlement, stablecoin rails")
    if "dev_tools" in signal["groups"]: actions.append("add operator tooling section: Claude, Cursor, GitHub, terminal workflows")
    if "small_business_ops" in signal["groups"]: actions.append("add small-business use case examples")
    if "energy" in signal["groups"]: actions.append("add practical local energy / HVAC angle")
    if "betting_markets" in signal["groups"]: actions.append("add market structure / signal engine explanation")
    actions.append("add one concrete example / scenario block tied to the new signal")
    deduped = []
    for a in actions:
        if a not in deduped: deduped.append(a)
    return deduped[:6]

def make_question(signal):
    mapping = {
        "ai_agents": "what does this mean for AI agents and automation?",
        "ai_search": "what does this mean for SEO and search visibility?",
        "payments": "what does this mean for merchant payments and settlement?",
        "dev_tools": "what does this mean for coding tools and operator workflows?",
        "small_business_ops": "how can a small business actually use this?",
        "energy": "how does this affect energy, solar, or HVAC decisions?",
        "betting_markets": "how does this affect prediction markets or sports-betting tools?"
    }
    if signal["groups"]:
        return mapping.get(signal["groups"][0], "what does this mean in practice?")
    return "what does this mean in practice?"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    all_items = []
    fetch_errors = []
    for source_name, url in FEEDS:
        try:
            raw = fetch(url)
            items = parse_rss(raw)
            for item in items[:8]:
                title = item["title"].strip()
                summary = item["summary"].strip()
                topics = title_to_topic(title, summary)
                groups = detect_groups(f"{title} {summary}")
                signal = {
                    "source": source_name,
                    "title": title,
                    "link": item["link"],
                    "published": item["published"],
                    "summary": summary[:500],
                    "topics": topics,
                    "groups": groups,
                    "short_question": make_question({"groups": groups})
                }
                all_items.append(signal)
        except Exception as e:
            fetch_errors.append({"source": source_name, "url": url, "error": str(e)})
    deduped = []
    seen = set()
    for item in all_items:
        key = normalize_token(item["title"])
        if not key or key in seen: continue
        seen.add(key)
        deduped.append(item)
    for item in deduped:
        score = 0
        score += len(item["groups"]) * 15
        score += min(10, len(item["topics"]))
        hay = f"{item['title']} {item['summary']}".lower()
        if any(x in hay for x in ["ai","automation","agent","search","seo","payments","solana","merchant","small business","google","operator","cursor","claude","github"]):
            score += 15
        item["signal_score"] = score
    deduped.sort(key=lambda x: (-x["signal_score"], x["source"], x["title"]))
    top_signals = deduped[:15]
    pages = collect_pages()
    upgrade_packets = []
    create_ideas = []
    for signal in top_signals:
        scored = []
        for page in pages:
            m = page_match_score(page, signal)
            if m > 8: scored.append((m, page))
        scored.sort(key=lambda x: (-x[0], x[1]["file"]))
        best_matches = []
        for m, page in scored[:5]:
            best_matches.append({
                "file": page["file"],
                "bucket": page["bucket"],
                "page_score": page["score"],
                "match_score": m,
                "actions": suggest_actions(page, signal)
            })
        upgrade_packets.append({"signal": signal, "matches": best_matches})
        if len(best_matches) == 0 or (best_matches and best_matches[0]["match_score"] < 16):
            slug_seed = signal["topics"][:4]
            slug = "-".join([re.sub(r"[^a-z0-9]+", "-", x.lower()).strip("-") for x in slug_seed if x]).strip("-")
            if slug:
                create_ideas.append({"suggested_file": f"{slug}.html", "reason": "new signal with weak existing page match", "source_signal": signal["title"]})
    payload = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "signals_count": len(top_signals),
        "feed_errors": fetch_errors,
        "top_signals": top_signals,
        "upgrade_packets": upgrade_packets,
        "create_ideas": create_ideas[:10]
    }
    with open(SIGNALS_JSON, "w", encoding="utf-8") as f:
        json.dump(top_signals, f, indent=2)
    with open(BRIEF_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    lines = []
    lines.append("# SideGuy Daily Upgrade Brief")
    lines.append("")
    lines.append(f"Generated: {payload['generated_at']}")
    lines.append("")
    lines.append("## What this does")
    lines.append("- scans recent public feeds")
    lines.append("- detects SideGuy-relevant tech / search / payments / ops signals")
    lines.append("- matches them to existing root HTML pages")
    lines.append("- suggests upgrades before creating random new pages")
    lines.append("")
    if fetch_errors:
        lines.append("## Feed fetch notes")
        for e in fetch_errors:
            lines.append(f"- {e['source']}: {e['error']}")
        lines.append("")
    lines.append("## Top signals")
    for i, s in enumerate(top_signals[:10], 1):
        group_label = ", ".join(s["groups"]) if s["groups"] else "general"
        lines.append(f"### {i}. {s['title']}")
        lines.append(f"- Source: {s['source']}")
        lines.append(f"- Published: {s['published'] or 'n/a'}")
        lines.append(f"- Groups: {group_label}")
        lines.append(f"- Topics: {', '.join(s['topics'])}")
        if s["link"]: lines.append(f"- Link: {s['link']}")
        if s["summary"]: lines.append(f"- Why it matters: {s['summary'][:240]}...")
        lines.append("")
    lines.append("## Recommended page upgrades")
    for packet in upgrade_packets[:10]:
        s = packet["signal"]
        lines.append(f"### Signal: {s['title']}")
        lines.append(f"- Key question: {s['short_question']}")
        if packet["matches"]:
            for match in packet["matches"][:3]:
                lines.append(f"- Upgrade: `{match['file']}` (match {match['match_score']}, page score {match['page_score']})")
                for action in match["actions"]:
                    lines.append(f"  - {action}")
        else:
            lines.append("- No strong existing page match found")
        lines.append("")
    if create_ideas:
        lines.append("## New page ideas only where needed")
        for idea in create_ideas[:10]:
            lines.append(f"- `{idea['suggested_file']}` — {idea['reason']} — signal: {idea['source_signal']}")
        lines.append("")
    lines.append("## Operator note")
    lines.append("Inventory-first wins: upgrade the strongest relevant existing pages before creating net-new pages.")
    lines.append("")
    with open(BRIEF_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {BRIEF_MD}")
    print(f"Wrote {BRIEF_JSON}")
    print(f"Wrote {SIGNALS_JSON}")
    print(f"Signals analyzed: {len(top_signals)}")
    print(f"Pages scanned: {len(pages)}")

if __name__ == "__main__":
    main()
