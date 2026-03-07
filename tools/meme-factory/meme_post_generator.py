import datetime

title = input("Meme title: ")
text = input("Meme caption: ")

slug = title.lower().replace(" ", "-").replace("'", "").replace("?", "")
now = datetime.datetime.now().strftime("%B %d, %Y")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · SideGuy Meme</title>
<meta name="description" content="Funny tech meme about {title} — SideGuy Solutions">
<style>
  :root {{
    --bg0:#eefcff;
    --ink:#073044;
    --mint:#21d3a1;
    --mint2:#00c7ff;
    --card:#fff;
    --r:14px;
  }}
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{
    font-family:-apple-system,system-ui,"Segoe UI",Roboto,Inter,sans-serif;
    background:radial-gradient(ellipse at 20% 40%,#b8f4f0 0%,#d6f5ff 35%,#eefcff 70%,#fff8f0 100%);
    color:var(--ink);min-height:100vh;
  }}
  header{{
    display:flex;align-items:center;justify-content:space-between;
    padding:14px 24px;background:rgba(255,255,255,.7);
    backdrop-filter:blur(8px);border-bottom:1px solid rgba(33,211,161,.25);
  }}
  .brand{{font-weight:800;font-size:1.15rem;color:var(--ink);text-decoration:none}}
  .pill{{
    background:var(--mint);color:#fff;font-size:.8rem;font-weight:700;
    padding:6px 16px;border-radius:99px;text-decoration:none;
  }}
  main{{max-width:700px;margin:0 auto;padding:40px 20px 80px}}
  .meme-card{{
    background:#fff;border-radius:20px;
    box-shadow:0 8px 32px rgba(7,48,68,.10);
    overflow:hidden;margin-bottom:32px;
  }}
  .meme-banner{{
    background:linear-gradient(135deg,var(--mint),var(--mint2));
    padding:48px 32px;text-align:center;
  }}
  .meme-banner h1{{
    font-size:clamp(1.4rem,4vw,2rem);color:#fff;font-weight:900;
    line-height:1.25;text-shadow:0 2px 8px rgba(0,0,0,.15);
  }}
  .meme-body{{padding:28px 32px}}
  .caption{{
    font-size:1.15rem;line-height:1.65;color:var(--ink);
    margin-bottom:20px;background:#f5fffe;border-left:4px solid var(--mint);
    padding:16px 20px;border-radius:0 var(--r) var(--r) 0;
  }}
  .tagline{{color:#567;font-size:.9rem;margin-top:16px;font-style:italic}}
  .meta{{font-size:.8rem;color:#89a;margin-top:8px}}
  .floating{{
    position:fixed;bottom:24px;right:24px;z-index:999;
    background:var(--mint);color:#fff;font-weight:800;font-size:.85rem;
    padding:14px 20px;border-radius:99px;text-decoration:none;
    box-shadow:0 4px 20px rgba(33,211,161,.45);
    animation:pulse 2.5s ease-in-out infinite;
  }}
  @keyframes pulse{{0%,100%{{box-shadow:0 4px 20px rgba(33,211,161,.45)}}50%{{box-shadow:0 4px 32px rgba(33,211,161,.75)}}}}
  footer{{text-align:center;padding:24px;color:#89a;font-size:.8rem}}
</style>
</head>
<body>
<header>
  <a class="brand" href="/">SideGuy Solutions</a>
  <a class="pill" href="sms:+17735441231">Text PJ</a>
</header>
<main>
  <div class="meme-card">
    <div class="meme-banner">
      <h1>{title}</h1>
    </div>
    <div class="meme-body">
      <p class="caption">{text}</p>
      <p class="tagline">Technology is confusing. Humor helps. SideGuy — clarity before cost.</p>
      <p class="meta">Posted {now}</p>
    </div>
  </div>
</main>
<a class="floating" href="sms:+17735441231">Text PJ · 773-544-1231</a>
<footer>&copy; 2026 SideGuy Solutions &middot; San Diego</footer>
</body>
</html>
"""

filename = f"memes/{slug}.html"
with open(filename, "w") as f:
    f.write(html)

print("Meme page created:", filename)
