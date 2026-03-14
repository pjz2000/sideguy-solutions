#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 2:
    print("Usage: build_from_slug.py <slug>")
    sys.exit(1)

slug = sys.argv[1]
title = slug.replace("-", " ").title()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title} | SideGuy Solutions</title>
  <meta name="description" content="Guide explaining {title.lower()} for businesses and operators. Human-first clarity from SideGuy Solutions.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/{slug}.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:-apple-system,system-ui,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>{title}</h1>
    <p>SideGuy explains {title.lower()} so businesses can understand costs, tools, and options before making decisions.</p>

    <h2>How It Works</h2>
    <p>Understanding {title.lower()} helps businesses evaluate solutions without wasting time or money.</p>

    <h2>Examples</h2>
    <ul>
      <li>Real-world use cases</li>
      <li>Automation opportunities</li>
      <li>Future infrastructure implications</li>
    </ul>

    <div style="margin-top:48px;padding:20px;border:1px solid #ddd;border-radius:18px;">
      <strong>Need help? Text PJ directly.</strong>
      <p>Real human guidance — no sales pitch.</p>
      <p><a href="sms:+17735441231">Text PJ: 773-544-1231</a></p>
    </div>
  </main>
</body>
</html>
"""

os.makedirs("public", exist_ok=True)
path = f"public/{slug}.html"

with open(path, "w") as f:
    f.write(html)

print("Created:", path)
