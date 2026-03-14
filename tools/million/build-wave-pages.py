#!/usr/bin/env python3
"""Build HTML pages from wave-selection.csv — handles quoted CSV properly."""

import csv
import os
from pathlib import Path

ROOT = Path("/workspaces/sideguy-solutions")
os.chdir(ROOT)

SELECTION = Path("docs/million-page/selected/wave-selection.csv")
if not SELECTION.exists():
    print("No wave-selection.csv found. Run select-wave-pages.sh first.")
    raise SystemExit(1)

public = Path("public")
public.mkdir(exist_ok=True)

built = 0

with open(SELECTION, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        url        = row.get("url", "").strip().strip('"')
        title      = row.get("title", "").strip().strip('"')
        h1         = row.get("h1", "").strip().strip('"')
        theme      = row.get("theme", "").strip().strip('"')
        audience   = row.get("audience", "").strip().strip('"')
        use_case   = row.get("use_case", "").strip().strip('"')
        industry   = row.get("industry", "").strip().strip('"')
        city       = row.get("city", "").strip().strip('"')
        state      = row.get("state", "").strip().strip('"')
        modifier   = row.get("modifier", "").strip().strip('"')
        page_type  = row.get("page_type", "").strip().strip('"')
        intent     = row.get("intent", "").strip().strip('"')
        score      = row.get("score", "").strip().strip('"')

        if not url or not h1:
            continue

        file_path = public / url.lstrip("/")
        file_path.parent.mkdir(parents=True, exist_ok=True)

        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <meta name="description" content="{h1}. Human-first clarity from SideGuy Solutions.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com{url}">
  <meta name="robots" content="index,follow">
</head>
<body>
  <main style="max-width:940px;margin:0 auto;padding:40px 20px;font-family:-apple-system,system-ui,sans-serif;line-height:1.65;">
    <p><a href="/index.html">&larr; Back to Home</a></p>
    <h1>{h1}</h1>
    <p>SideGuy is where Google discovers the problem, AI explains it, and a real human resolves it.</p>

    <h2>What this page covers</h2>
    <p>This page focuses on <strong>{theme}</strong> for <strong>{industry}</strong> in <strong>{city}, {state}</strong>, with emphasis on <strong>{page_type}</strong> and <strong>{use_case}</strong>.</p>

    <h2>Why people search this</h2>
    <p>Usually they want clarity on whether the technology is useful, what it costs, how implementation works, what risks matter, and whether it fits their business or workflow.</p>

    <h2>Audience</h2>
    <p>{audience}</p>

    <h2>Use case</h2>
    <p>{use_case}</p>

    <h2>Industry angle</h2>
    <p>{industry} teams often need practical explanations instead of hype. SideGuy keeps the tone calm, direct, and implementation-aware.</p>

    <h2>Local angle</h2>
    <p>Businesses in {city}, {state} often need help evaluating new systems without getting lost in vendor noise.</p>

    <h2>Search modifier</h2>
    <p>{modifier}</p>

    <h2>FAQ</h2>
    <p><strong>What is this really about?</strong><br>This page helps explain the real-world use of {theme}.</p>
    <p><strong>Who is this for?</strong><br>{audience}</p>
    <p><strong>What does SideGuy do?</strong><br>Clarity before cost. Calm explanation first, then human help if needed.</p>

    <h2>Related Pages</h2>
    <ul>
      <li><a href="/ai-agents-answer-engine-traffic.html">AI Agents &amp; Answer Engine Traffic</a></li>
      <li><a href="/machine-to-machine-payments.html">Machine-to-Machine Payments</a></li>
      <li><a href="/solana-payments.html">Solana Payments</a></li>
      <li><a href="/usdc-merchant-payments.html">USDC Merchant Payments</a></li>
    </ul>

    <div style="margin-top:48px;padding:22px;border:1px solid #ddd;border-radius:20px;">
      <strong>Text PJ</strong>
      <p>Need a real human to help you sort through the noise?</p>
      <p><a href="sms:+17735441231">Text PJ: 773-544-1231</a></p>
    </div>
  </main>
</body>
</html>
"""
        file_path.write_text(html)
        built += 1

print(f"Built {built} wave pages.")
