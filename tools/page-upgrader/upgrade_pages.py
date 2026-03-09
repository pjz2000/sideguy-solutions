from pathlib import Path
import datetime

ROOT = Path("/workspaces/sideguy-solutions/public")

pages = list(ROOT.rglob("*.html"))

timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d")

count = 0

for page in pages:

    text = page.read_text()

    if '<link rel="canonical"' not in text:
        canonical = f'<link rel="canonical" href="https://www.sideguysolutions.com/{page.name}">'
        text = text.replace("</head>", canonical + "\n</head>")

    if "Updated:" not in text:
        text = text.replace("<body>", "<body>\n<p><em>Updated: " + timestamp + "</em></p>")

    if "Text PJ" not in text:
        cta = """
<div style="margin-top:40px;padding:20px;border:1px solid #ccc">
<strong>Need help implementing this?</strong><br>
Text PJ directly: <a href="sms:7735441231">773-544-1231</a>
</div>
"""
        text = text.replace("</body>", cta + "\n</body>")

    page.write_text(text)

    count += 1

print("Pages upgraded:", count)
