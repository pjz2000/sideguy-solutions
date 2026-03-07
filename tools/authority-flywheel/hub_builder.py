"""
Authority Hub Page Builder
==========================
Generates SideGuy-style hub pages from data/authority/hubs.json.

Architecture mirrors _template.html:
  - Inline CSS with :root CSS variables (no external stylesheets)
  - Radial gradient ocean background
  - topbar homePill -> back to home
  - brandRow with animated brandOrb
  - Two-column layout: main content (left) + rightRail (sticky, desktop)
  - cards grid -> noteCard -> bigCta
  - Floating "Text PJ" orb (fixed, bottom-right)
  - Live timestamp + weather (Open-Meteo, no key)

Text PJ: sms:+17735441231 / 773-544-1231
"""

import json

HUB_META = {
    "ai-automation": {
        "desc": "Common AI automation problems for San Diego small businesses — what tools cost, how long setup takes, and when automation actually makes sense.",
        "problems": [
            ("What does AI automation actually cost?", [
                "Basic tools (Zapier, Make): free–$50/mo",
                "Managed setup: $500–2,000 one-time",
                "Ongoing workflows: $50–200/month",
                "Define the problem first, then find the tool",
            ]),
            ("How long does setup take?", [
                "Simple reminders / review requests: 1–3 days",
                "CRM integrations: 2–6 weeks",
                "Fast claims = corners being cut",
                "Ask for a milestone timeline in writing",
            ]),
            ("Will it replace my staff?", [
                "Repetitive well-defined tasks: reduces hours",
                "Relationship or judgment work: no",
                "Most real installs augment, not replace",
                "Honest vendors tell you which tasks aren't automatable",
            ]),
        ],
        "note": "Start with one workflow. Measure it for 30 days. Then expand.",
    },
    "payments": {
        "desc": "Payment processor fees, POS system traps, and how San Diego operators reduce costs without switching everything overnight.",
        "problems": [
            ("Why are my fees so high?", [
                "Interchange + processor markup + POS markup stack",
                "Card-present vs card-not-present rates differ",
                "Surcharging rules vary by state",
                "Most operators never negotiated their rate",
            ]),
            ("Should I switch processors?", [
                "Check your effective rate (total fees ÷ volume)",
                "Industry average: 1.5–2.5% for retail",
                "Switching has contract exit costs",
                "Get 3 quotes before deciding",
            ]),
            ("POS system locked in?", [
                "Proprietary hardware ties you to one processor",
                "Open systems (Square, Clover) have more flexibility",
                "Lease vs buy: leasing is almost always worse",
                "Ask about data portability before signing",
            ]),
        ],
        "note": "The cheapest processor isn't always the right one. Match the tool to your ticket size and volume.",
    },
    "lead-generation": {
        "desc": "SEO, Google Ads, and website traffic problems for contractors and local businesses in San Diego — what actually works and what wastes money.",
        "problems": [
            ("Why isn't my website getting traffic?", [
                "No local SEO signals (GMB, citations, reviews)",
                "Pages don't match what customers search",
                "Site loads slowly on mobile",
                "Zero backlinks from relevant local sources",
            ]),
            ("Is Google Ads worth it for me?", [
                "CPCs in home services: $10–80 per click",
                "Conversion rate matters more than clicks",
                "Bad landing pages waste ad spend",
                "Start with $500/mo minimum to get real data",
            ]),
            ("My leads dropped — what happened?", [
                "Algorithm update hit your rankings",
                "Competitor launched or improved their site",
                "Seasonal drop (check year-over-year)",
                "GMB listing got suspended or flagged",
            ]),
        ],
        "note": "SEO takes 3–6 months to show results. Ads can be turned on immediately. Use both — not either/or.",
    },
    "business-operations": {
        "desc": "CRM systems, employee scheduling, inventory software — how San Diego operators pick tools without over-complicating their business.",
        "problems": [
            ("Which CRM is right for my size?", [
                "Under 10 staff: a spreadsheet or Notion may work",
                "10–50 staff: HubSpot Free or Zoho CRM",
                "Over 50: Salesforce or industry-specific tool",
                "Wrong CRM = data you never trust",
            ]),
            ("Scheduling software chaos", [
                "Paper and texting breaks at 8+ employees",
                "Homebase and Deputy work for hourly staff",
                "Integrations with payroll matter most",
                "Trial period before you commit",
            ]),
            ("Inventory software: where to start", [
                "Google Sheets until it breaks — then upgrade",
                "Lightspeed, Cin7, or Shopify POS for retail",
                "Match to your number of SKUs and locations",
                "Don't buy more software than you'll use",
            ]),
        ],
        "note": "Pick boring tools that your team will actually use. The best software is the one nobody complains about.",
    },
    "technology-decisions": {
        "desc": "How to evaluate AI tools, compare CRMs, and make technology decisions without getting sold something you don't need.",
        "problems": [
            ("Best AI tools for small business?", [
                "ChatGPT / Claude: writing, drafting, research",
                "Zapier / Make: connecting apps without code",
                "Notion AI: notes, SOPs, internal docs",
                "Start with one tool for one task",
            ]),
            ("CRM comparison: what matters", [
                "Contact limit on free tier",
                "Pipeline / deal tracking",
                "Email integration (Gmail / Outlook)",
                "Export your data before you're locked in",
            ]),
            ("How to evaluate any software vendor", [
                "Ask for a real customer reference — not a testimonial",
                "Understand the cancellation clause before signing",
                "Check if data export is included or extra",
                "Pilot with real data for 30 days",
            ]),
        ],
        "note": "Technology is a tool. Match it to a specific problem. Never buy 'the best' — buy what fits.",
    },
}

with open("data/authority/hubs.json") as f:
    hubs = json.load(f)

for hub in hubs:
    filename = f"{hub}.html"
    title_str = hub.replace("-", " ").title()
    meta = HUB_META.get(hub, {
        "desc": f"SideGuy guide to {hub.replace('-',' ')} for San Diego small businesses.",
        "problems": [("Common Questions", ["Understanding tools", "Reducing costs", "Implementation challenges"])],
        "note": "Need help? Text PJ.",
    })

    problems_html = ""
    for card_title, bullets in meta["problems"]:
        lis = "\n              ".join(f"<li>{b}</li>" for b in bullets)
        problems_html += f"""
          <article class="card">
            <p class="cardTitle">{card_title}</p>
            <ul class="bullets">
              {lis}
            </ul>
          </article>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <title>{title_str} \xb7 SideGuy Solutions (San Diego)</title>
  <meta name="description" content="{meta['desc']}" />
  <link rel="canonical" href="https://sideguysolutions.com/{filename}" />
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="SideGuy Solutions" />
  <meta property="og:title" content="{title_str} \xb7 SideGuy Solutions (San Diego)" />
  <meta property="og:description" content="{meta['desc']}" />
  <meta property="og:url" content="https://sideguysolutions.com/{filename}" />
  <meta name="twitter:card" content="summary" />

  <style>
    :root{{
      --bg0:#eefcff; --bg1:#d7f5ff; --bg2:#bfeeff;
      --ink:#073044; --muted:#3f6173; --muted2:#5e7d8e;
      --card:#ffffffcc; --stroke:rgba(7,48,68,.10); --stroke2:rgba(7,48,68,.07);
      --mint:#21d3a1; --mint2:#00c7ff; --blue:#4aa9ff; --blue2:#1f7cff;
      --r:22px; --pill:999px;
    }}
    *{{box-sizing:border-box}}
    html,body{{height:100%}}
    body{{
      margin:0;
      font-family:-apple-system,system-ui,Segoe UI,Roboto,Inter,Arial,sans-serif;
      color:var(--ink);
      background:radial-gradient(1200px 900px at 22% 10%,#fff 0%,var(--bg0) 25%,var(--bg1) 60%,var(--bg2) 100%);
      -webkit-font-smoothing:antialiased;
      overflow-x:hidden;
    }}
    body:before{{
      content:""; position:fixed; inset:-20%;
      background:
        radial-gradient(closest-side at 18% 20%,rgba(33,211,161,.18),transparent 55%),
        radial-gradient(closest-side at 78% 28%,rgba(74,169,255,.16),transparent 52%),
        radial-gradient(closest-side at 62% 82%,rgba(0,199,255,.12),transparent 55%),
        radial-gradient(closest-side at 25% 85%,rgba(33,211,161,.10),transparent 58%);
      filter:blur(18px); pointer-events:none; z-index:-2;
    }}
    .topbar{{position:sticky;top:0;z-index:50;padding:14px 14px 10px;display:flex;justify-content:center;pointer-events:none;}}
    .homePill{{pointer-events:auto;text-decoration:none;display:inline-flex;align-items:center;gap:10px;padding:10px 16px;border-radius:var(--pill);background:linear-gradient(180deg,rgba(255,255,255,.84),rgba(255,255,255,.62));border:1px solid var(--stroke2);box-shadow:0 10px 28px rgba(7,48,68,.08);color:var(--ink);font-weight:700;font-size:12px;letter-spacing:.02em;backdrop-filter:blur(14px);}}
    .homeDot{{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 0 0 3px rgba(255,255,255,.95),0 10px 18px rgba(33,211,161,.18);}}
    .wrap{{max-width:1120px;margin:0 auto;padding:26px 22px 92px;}}
    .layout{{display:grid;grid-template-columns:1.15fr .85fr;gap:22px;align-items:start;min-height:calc(100vh - 120px);}}
    @media(max-width:980px){{.layout{{grid-template-columns:1fr;gap:16px;}}}}
    .brandRow{{display:flex;align-items:flex-start;gap:14px;margin-bottom:14px;}}
    .brandOrb{{width:38px;height:38px;border-radius:50%;background:radial-gradient(circle at 30% 20%,#fff 0%,rgba(255,255,255,.65) 18%,rgba(33,211,161,.85) 55%,rgba(0,199,255,.85) 100%);box-shadow:0 0 0 4px rgba(255,255,255,.92),0 18px 40px rgba(33,211,161,.22),0 14px 26px rgba(0,199,255,.14);position:relative;flex:0 0 auto;}}
    .brandOrb:after{{content:"";position:absolute;inset:-18px;border-radius:50%;background:radial-gradient(circle,rgba(33,211,161,.22),transparent 65%);filter:blur(6px);z-index:-1;animation:pulse 2.4s ease-in-out infinite;}}
    @keyframes pulse{{0%,100%{{transform:scale(.96);opacity:.70}}50%{{transform:scale(1.05);opacity:1}}}}
    .brandMeta{{line-height:1.1;padding-top:2px;}}
    .brandName{{font-weight:800;letter-spacing:.06em;text-transform:uppercase;font-size:12px;color:rgba(7,48,68,.78);}}
    .brandSub{{margin-top:6px;font-size:12px;color:rgba(7,48,68,.62);}}
    .liveLine{{margin-top:8px;font-size:12px;color:rgba(7,48,68,.62);display:flex;flex-wrap:wrap;gap:10px;align-items:center;}}
    .liveTag{{display:inline-flex;align-items:center;gap:8px;padding:7px 10px;border-radius:var(--pill);background:rgba(255,255,255,.68);border:1px solid var(--stroke2);backdrop-filter:blur(10px);}}
    .spark{{width:8px;height:8px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 0 0 3px rgba(255,255,255,.9);}}
    h1{{margin:10px 0 8px;font-size:44px;letter-spacing:-.03em;line-height:1.02;}}
    @media(max-width:520px){{h1{{font-size:34px}}}}
    .lede{{margin:0 0 14px;font-size:14px;line-height:1.6;color:var(--muted);max-width:720px;}}
    .cards{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:14px;}}
    @media(max-width:980px){{.cards{{grid-template-columns:repeat(2,minmax(0,1fr));}}}}
    @media(max-width:560px){{.cards{{grid-template-columns:1fr;}}}}
    .card{{background:linear-gradient(180deg,var(--card),rgba(255,255,255,.70));border:1px solid var(--stroke2);border-radius:18px;box-shadow:0 12px 34px rgba(7,48,68,.08);padding:14px 14px 12px;backdrop-filter:blur(14px);min-height:132px;}}
    .cardTitle{{font-weight:800;font-size:13px;margin:0 0 8px;color:rgba(7,48,68,.82);}}
    .bullets{{margin:0;padding-left:16px;font-size:12px;line-height:1.5;color:rgba(7,48,68,.64);}}
    .bullets li{{margin:0 0 6px}}
    .noteCard{{margin-top:12px;background:linear-gradient(180deg,rgba(255,255,255,.70),rgba(255,255,255,.55));border:1px dashed rgba(7,48,68,.12);border-radius:18px;padding:12px 14px;color:rgba(7,48,68,.62);font-size:12px;line-height:1.55;backdrop-filter:blur(14px);}}
    .bigCta{{margin-top:14px;background:linear-gradient(180deg,rgba(33,211,161,.15),rgba(0,199,255,.12));border:1px solid rgba(7,48,68,.10);border-radius:22px;padding:18px 16px;box-shadow:0 20px 60px rgba(7,48,68,.10);display:flex;align-items:center;justify-content:space-between;gap:14px;backdrop-filter:blur(14px);}}
    @media(max-width:560px){{.bigCta{{flex-direction:column;align-items:flex-start;}}}}
    .bigCta h2{{margin:0;font-size:14px;letter-spacing:.02em;}}
    .bigCta .small{{margin-top:6px;font-size:12px;color:rgba(7,48,68,.65);line-height:1.45;}}
    .btn{{text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:12px 14px;border-radius:var(--pill);border:1px solid rgba(255,255,255,.75);color:#fff;font-weight:800;font-size:12px;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 18px 40px rgba(0,199,255,.22);white-space:nowrap;}}
    .btn:active{{transform:translateY(1px);}}
    .rightRail{{position:sticky;top:78px;display:flex;justify-content:flex-end;}}
    @media(max-width:980px){{.rightRail{{position:relative;top:auto;justify-content:flex-start;}}}}
    .railStack{{display:flex;align-items:flex-start;gap:12px;}}
    .railOrbs{{display:flex;flex-direction:column;gap:12px;align-items:flex-end;}}
    .railOrb{{width:86px;height:86px;border-radius:999px;position:relative;border:1px solid rgba(255,255,255,.75);box-shadow:0 24px 55px rgba(7,48,68,.16);backdrop-filter:blur(14px);overflow:hidden;cursor:pointer;text-decoration:none;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;letter-spacing:.02em;font-size:12px;text-align:center;padding:10px;}}
    .railOrb:before{{content:"";position:absolute;inset:-20%;background:radial-gradient(circle at 30% 22%,rgba(255,255,255,.90),rgba(255,255,255,.35) 28%,transparent 56%),radial-gradient(circle at 65% 80%,rgba(0,0,0,.16),transparent 55%);opacity:.60;pointer-events:none;}}
    .railOrb:after{{content:"";position:absolute;inset:-18px;border-radius:999px;background:radial-gradient(circle,rgba(33,211,161,.22),transparent 62%);filter:blur(7px);opacity:.9;pointer-events:none;animation:pulse 2.4s ease-in-out infinite;}}
    .orbGreen{{background:radial-gradient(circle at 30% 15%,#fff,rgba(33,211,161,.95) 45%,rgba(0,199,255,.95) 100%);}}
    .orbBlue{{background:radial-gradient(circle at 30% 15%,#fff,rgba(74,169,255,.95) 45%,rgba(31,124,255,.98) 100%);}}
    .orbSoft{{background:radial-gradient(circle at 30% 15%,#fff,rgba(255,255,255,.82) 30%,rgba(255,255,255,.58) 100%);color:rgba(7,48,68,.82);border:1px solid rgba(7,48,68,.10);}}
    .orbSoft:after{{background:radial-gradient(circle,rgba(74,169,255,.18),transparent 65%);}}
    .railLabels{{display:flex;flex-direction:column;gap:14px;padding-top:2px;}}
    .railLabel{{width:190px;padding:11px 12px;border-radius:16px;background:rgba(255,255,255,.64);border:1px solid var(--stroke2);backdrop-filter:blur(14px);box-shadow:0 14px 34px rgba(7,48,68,.08);color:rgba(7,48,68,.76);font-size:12px;line-height:1.35;}}
    .railLabel b{{color:rgba(7,48,68,.88);}}
    .floating{{position:fixed;right:18px;bottom:16px;z-index:999;display:flex;align-items:center;gap:10px;}}
    .floatPill{{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:16px;background:rgba(255,255,255,.66);border:1px solid var(--stroke2);box-shadow:0 18px 55px rgba(7,48,68,.14);backdrop-filter:blur(14px);min-width:220px;}}
    .floatPill .t1{{font-weight:900;font-size:12px;color:rgba(7,48,68,.88);display:flex;align-items:center;gap:8px;}}
    .chatDot{{width:10px;height:10px;border-radius:50%;background:linear-gradient(135deg,var(--mint),var(--mint2));box-shadow:0 0 0 3px rgba(255,255,255,.9);}}
    .floatPill .t2{{font-size:11px;color:rgba(7,48,68,.62);}}
    .floatBtn{{width:54px;height:54px;border-radius:999px;background:radial-gradient(circle at 30% 20%,#fff,rgba(33,211,161,.95) 52%,rgba(0,199,255,.95) 100%);border:1px solid rgba(255,255,255,.8);box-shadow:0 0 0 4px rgba(255,255,255,.92),0 22px 60px rgba(0,199,255,.22),0 18px 42px rgba(33,211,161,.18);position:relative;text-decoration:none;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;letter-spacing:.02em;font-size:11px;text-align:center;}}
    .floatBtn:after{{content:"";position:absolute;inset:-16px;border-radius:999px;background:radial-gradient(circle,rgba(33,211,161,.28),transparent 62%);filter:blur(7px);animation:pulse 2.2s ease-in-out infinite;z-index:-1;}}
    .microFooter{{margin-top:18px;font-size:11px;color:rgba(7,48,68,.55);}}
    .microFooter a{{color:rgba(31,124,255,.85);text-decoration:none;font-weight:700;}}
  </style>
</head>

<body>

  <div class="topbar">
    <a class="homePill" href="index.html" aria-label="Back to home">
      <span class="homeDot"></span>
      Back to home
    </a>
  </div>

  <div class="wrap">
    <div class="layout">

      <main>
        <div class="brandRow">
          <div class="brandOrb" aria-hidden="true"></div>
          <div class="brandMeta">
            <div class="brandName">SideGuy Solutions</div>
            <div class="brandSub">San Diego \xb7 Human Guidance Layer</div>
            <div class="liveLine">
              <span class="liveTag"><span class="spark"></span> Updated live \xb7 <span id="localTime">\u2014</span></span>
              <span class="liveTag">Weather \xb7 <span id="wx">\u2014</span></span>
              <span class="liveTag">Hub \xb7 {title_str}</span>
            </div>
          </div>
        </div>

        <h1>{title_str}</h1>
        <p class="lede">{meta['desc']}</p>

        <section class="cards" aria-label="Common problems">
          {problems_html}
        </section>

        <div class="noteCard">
          <b>Real talk:</b> {meta['note']}
        </div>

        <section class="bigCta" aria-label="Talk to a real person">
          <div>
            <h2>Talk to a real person</h2>
            <div class="small">
              Text PJ directly. Describe what's going on.<br/>
              <b>773-544-1231</b> \xb7 San Diego
            </div>
          </div>
          <a class="btn" href="sms:+17735441231" rel="nofollow" aria-label="Text PJ for clarity">Text PJ \xb7 773-544-1231</a>
        </section>

        <div class="microFooter">
          SideGuy Solutions \xb7 <span id="dateStamp">\u2014</span> \xb7
          <a href="index.html">Homepage</a>
        </div>
      </main>

      <aside class="rightRail" aria-label="Quick actions">
        <div class="railStack">
          <div class="railOrbs">
            <a class="railOrb orbGreen" href="sms:+17735441231" rel="nofollow" aria-label="Text PJ">Text PJ</a>
            <a class="railOrb orbBlue" href="index.html" aria-label="Home">Home</a>
            <a class="railOrb orbSoft" href="index.html#start-simple" aria-label="Start Simple">Start<br/>Simple</a>
            <a class="railOrb orbSoft" href="index.html#no-pressure" aria-label="No pressure">No<br/>pressure</a>
          </div>
          <div class="railLabels">
            <div class="railLabel"><b>Text PJ</b><br/>Fast human response. No tickets. No weird portals.</div>
            <div class="railLabel"><b>Home</b><br/>See all SideGuy topics and guidance pages.</div>
            <div class="railLabel"><b>Start Simple</b><br/>Quick checklist \u2192 next best step. Avoid overreacting.</div>
            <div class="railLabel"><b>No pressure</b><br/>Clarity first. If we can't help, we'll say so.</div>
          </div>
        </div>
      </aside>

    </div>
  </div>

  <div class="floating" aria-label="Text PJ floating orb">
    <div class="floatPill">
      <div class="t1"><span class="chatDot"></span> Text PJ</div>
      <div class="t2">One text \xb7 calm answers \xb7 <b>773-544-1231</b></div>
    </div>
    <a class="floatBtn" href="sms:+17735441231" rel="nofollow" aria-label="Text PJ now">Text<br/>PJ</a>
  </div>

  <script>
    function fmtTime(d){{ return d.toLocaleTimeString([],{{hour:'numeric',minute:'2-digit'}}); }}
    function fmtDate(d){{ return d.toLocaleDateString([],{{year:'numeric',month:'short',day:'numeric'}}); }}
    function updateTime(){{
      const now = new Date();
      document.getElementById("localTime").textContent = fmtTime(now);
      document.getElementById("dateStamp").textContent = "Updated " + fmtDate(now);
    }}
    updateTime();
    setInterval(updateTime, 15000);
    const wxCodes = {{0:"Clear",1:"Mainly clear",2:"Partly cloudy",3:"Cloudy",45:"Fog",48:"Fog",51:"Light drizzle",53:"Drizzle",55:"Heavy drizzle",61:"Light rain",63:"Rain",65:"Heavy rain",71:"Light snow",73:"Snow",75:"Heavy snow",80:"Rain showers",81:"Rain showers",82:"Heavy showers",95:"Thunderstorm",96:"Thunderstorm",99:"Thunderstorm"}};
    async function loadWeather(){{
      try{{
        const r = await fetch("https://api.open-meteo.com/v1/forecast?latitude=32.7157&longitude=-117.1611&current=temperature_2m,weather_code&temperature_unit=fahrenheit&timezone=auto");
        const d = await r.json();
        document.getElementById("wx").textContent = Math.round(d.current.temperature_2m) + "\u00b0F \xb7 " + (wxCodes[d.current.weather_code]||"—");
      }} catch(e) {{ document.getElementById("wx").textContent = "San Diego"; }}
    }}
    loadWeather();
  </script>

</body>
</html>
"""
    with open(filename, "w") as f:
        f.write(html)
    print("Created hub page:", filename)
