import os
import re
import csv
import glob
import html as htmlmod
import datetime
from collections import defaultdict

RADAR_ARCHIVE = "docs/problem-radar/archive"
RADAR_CURRENT = "docs/problem-radar/radar-signals.tsv"
TREND_REPORT = "docs/trends/trend-report.md"
TREND_INCLUDE = "public/includes/trending-problems.html"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


def load_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def topic_scores(rows):
    """Return {topic: max_score} — prefer score field over count."""
    scores = {}
    for r in rows:
        topic = (r.get("topic") or "").strip()
        if not topic:
            continue
        try:
            score = int(r.get("score") or 0)
        except ValueError:
            score = 1
        scores[topic] = max(scores.get(topic, 0), score)
    return scores


def bucket_counts(rows):
    counts = defaultdict(int)
    for r in rows:
        counts[r.get("bucket") or "general"] += 1
    return counts


def compute_trends(new_scores, old_scores):
    trends = []
    for topic, score in new_scores.items():
        old = old_scores.get(topic, 0)
        change = score - old
        trends.append((topic, change, score))
    trends.sort(key=lambda x: (-x[1], -x[2]))
    return trends


def build_report(topic_trends, bucket_trends, mode):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    lines = [
        "# SideGuy Trend Report", "",
        f"Generated: {now}", "",
        f"Mode: **{mode}**", "",
    ]

    if mode == "delta":
        lines += ["## Rising Problems (Score Delta)", ""]
        for topic, change, score in topic_trends[:30]:
            sign = f"+{change}" if change >= 0 else str(change)
            lines.append(f"- {topic} ({sign}) | score {score}")
        lines += ["", "## Rising Clusters", ""]
        for bucket, change, count in bucket_trends[:20]:
            sign = f"+{change}" if change >= 0 else str(change)
            lines.append(f"- {bucket} ({sign})")
    else:
        lines += ["## Top Scored Problems (single snapshot)", ""]
        for topic, _, score in topic_trends[:40]:
            lines.append(f"- {topic} | score {score}")
        lines += ["", "## Cluster Sizes", ""]
        for bucket, change, count in bucket_trends[:20]:
            lines.append(f"- {bucket}: {count} topics")

    os.makedirs(os.path.dirname(TREND_REPORT), exist_ok=True)
    with open(TREND_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_include(topic_trends, mode):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%B %d, %Y")
    label = "Rising Problems" if mode == "delta" else "Top Problems This Week"

    items = []
    for topic, change, score in topic_trends[:12]:
        slug = slugify(topic)
        esc = htmlmod.escape(topic)
        badge = f"+{change}" if mode == "delta" and change > 0 else f"score {score}"
        items.append(
            f'<li><a href="/auto/problem-pages/{slug}.html">{esc}</a> '
            f'<span class="sg-trend-badge">{badge}</span></li>'
        )

    block = f"""<!-- SideGuy Trending Problems Include -->
<section class="sg-trending">
  <p class="sg-trend-kicker">Live Problem Radar · {now}</p>
  <h2>{htmlmod.escape(label)}</h2>
  <p>Topics the SideGuy radar is seeing move.</p>
  <ul>
    {''.join(items)}
  </ul>
  <p><a href="/public/discovery/problem-discovery.html">See all tracked problems →</a></p>
</section>
<style>
.sg-trending{{background:#fff;border-radius:16px;padding:24px 28px;margin:24px 0;border:1px solid #d9e8f2;box-shadow:0 4px 20px rgba(7,48,68,.07)}}
.sg-trend-kicker{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.65;margin:0 0 6px}}
.sg-trending h2{{margin:0 0 8px;font-size:1.25rem}}
.sg-trending ul{{padding-left:20px;margin:12px 0}}
.sg-trending li{{margin:6px 0}}
.sg-trending a{{color:#0b5cad;text-decoration:none}}
.sg-trending a:hover{{text-decoration:underline}}
.sg-trend-badge{{font-size:.8rem;background:#e0f9f3;color:#073044;padding:2px 8px;border-radius:99px;margin-left:6px}}
</style>
"""
    os.makedirs(os.path.dirname(TREND_INCLUDE), exist_ok=True)
    with open(TREND_INCLUDE, "w", encoding="utf-8") as f:
        f.write(block)


def run():
    archive_files = sorted(glob.glob(f"{RADAR_ARCHIVE}/radar-signals-*.tsv"))

    if len(archive_files) >= 2:
        latest_path = archive_files[-1]
        previous_path = archive_files[-2]
        mode = "delta"
        print(f"Comparing: {os.path.basename(latest_path)} vs {os.path.basename(previous_path)}")
    elif len(archive_files) == 1 or os.path.exists(RADAR_CURRENT):
        # Single snapshot — rank by score, report as baseline
        latest_path = archive_files[-1] if archive_files else RADAR_CURRENT
        previous_path = None
        mode = "baseline"
        print(f"Single snapshot mode: {os.path.basename(latest_path)}")
    else:
        print("[skip] No radar snapshots found. Run radar_v2.py first.")
        return

    new_rows = load_tsv(latest_path)
    old_rows = load_tsv(previous_path) if previous_path else []

    new_scores = topic_scores(new_rows)
    old_scores = topic_scores(old_rows)
    new_buckets = bucket_counts(new_rows)
    old_buckets = bucket_counts(old_rows)

    topic_trends = compute_trends(new_scores, old_scores)
    bucket_trends = compute_trends(new_buckets, old_buckets)

    build_report(topic_trends, bucket_trends, mode)
    build_include(topic_trends, mode)

    print("Trend engine complete.")
    print(f"Mode:              {mode}")
    print(f"Topics tracked:    {len(new_scores)}")
    print(f"Trend report:      {TREND_REPORT}")
    print(f"Trending include:  {TREND_INCLUDE}")


run()
