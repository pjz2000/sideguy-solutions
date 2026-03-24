#!/usr/bin/env bash

########################################
# SIDEGUY CLAVDEN CLUSTER BUILDER v2
# Perfected for SideGuy architecture
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || exit 1

########################################
# PAGE GENERATOR
########################################

create_page() {
  SLUG="$1"
  TITLE="$2"
  H1="$3"
  DESC="$4"
  CONTENT="$5"

  FILE="$PROJECT_ROOT/$SLUG.html"

  if [ -f "$FILE" ]; then
    echo "⏭️  Skipping existing: $SLUG"
    return
  fi

  cat > "$FILE" <<'EOFPAGE'
<!DOCTYPE html>
<html lang="en">
<head>
<meta name="robots" content="index, follow, max-image-preview:large" />
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>TITLE_PLACEHOLDER · SideGuy</title>
<link rel="canonical" href="https://sideguy.solutions/SLUG_PLACEHOLDER.html"/>
<meta content="DESC_PLACEHOLDER" name="description"/>
<style>
    :root{
      --bg0:#eefcff;
      --bg1:#d7f5ff;
      --bg2:#bfeeff;
      --ink:#073044;
      --muted:#3f6173;
      --muted2:#5e7d8e;

      --card:#ffffffcc;
      --card2:#ffffffb8;
      --stroke:rgba(7,48,68,.10);
      --stroke2:rgba(7,48,68,.07);
      --shadow: 0 18px 50px rgba(7,48,68,.10);

      --mint:#21d3a1;
      --mint2:#00c7ff;
      --blue:#4aa9ff;
      --blue2:#1f7cff;

      --r:22px;
      --pill:999px;

      --phone:"+17735441231";
      --phonePretty:"773-544-1231";
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family:-apple-system, system-ui, Segoe UI, Roboto, Inter, Arial, sans-serif;
      color:var(--ink);
      background:radial-gradient(1200px 900px at 22% 10%, #ffffff 0%, var(--bg0) 25%, var(--bg1) 60%, var(--bg2) 100%);
      -webkit-font-smoothing:antialiased;
      overflow-x:hidden;
    }

    body:before{
      content:"";
      position:fixed;
      inset:-20%;
      background:
        radial-gradient(closest-side at 18% 20%, rgba(33,211,161,.18), transparent 55%),
        radial-gradient(closest-side at 78% 28%, rgba(74,169,255,.16), transparent 52%),
        radial-gradient(closest-side at 62% 82%, rgba(0,199,255,.12), transparent 55%),
        radial-gradient(closest-side at 25% 85%, rgba(33,211,161,.10), transparent 58%);
      filter: blur(18px);
      pointer-events:none;
      z-index:-2;
    }

    .wrap{
      max-width:1120px;
      margin:0 auto;
      padding: 26px 22px 92px;
    }

    .topbar{
      position:sticky;
      top:0;
      z-index:50;
      padding:14px 14px 10px;
      display:flex;
      justify-content:center;
      pointer-events:none;
    }
    .homePill{
      pointer-events:auto;
      text-decoration:none;
      display:inline-flex;
      align-items:center;
      gap:10px;
      padding:10px 16px;
      border-radius:var(--pill);
      background:linear-gradient(180deg, rgba(255,255,255,.84), rgba(255,255,255,.62));
      border:1px solid var(--stroke2);
      box-shadow: 0 10px 28px rgba(7,48,68,.08);
      color:var(--ink);
      font-weight:700;
      font-size:12px;
      letter-spacing:.02em;
      backdrop-filter: blur(14px);
    }
    .homeDot{
      width:10px;height:10px;border-radius:50%;
      background:linear-gradient(135deg, var(--mint), var(--mint2));
      box-shadow: 0 0 0 3px rgba(255,255,255,.95), 0 10px 18px rgba(33,211,161,.18);
    }
</style>
</head>
<body>

<div class="topbar">
  <a href="index.html" class="homePill">
    <span class="homeDot"></span>
    SideGuy
  </a>
</div>

<div class="wrap">
<main aria-label="Main content">

<section class="clarity-layer" style="max-width:900px;margin:0 auto;padding:32px 20px;line-height:1.6;">

  <div style="background:linear-gradient(135deg,#ecfeff,#f0fdf4);border:1px solid #bae6fd;border-radius:18px;padding:28px 22px;margin-bottom:28px;">
    <p style="margin:0 0 10px 0;font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#0891b2;">
      SideGuy Clarity Layer
    </p>
    <h1 style="margin:0 0 12px 0;font-size:36px;line-height:1.1;color:var(--ink,#0f172a);">
      H1_PLACEHOLDER
    </h1>
    
    <section style='background:var(--card,#ffffffcc);padding:20px 24px;border-radius:var(--r,12px);margin:24px 0;border:1px solid var(--stroke,rgba(7,48,68,.10));box-shadow:0 2px 12px rgba(7,48,68,.06);'>
      <div style='font-size:14px;font-weight:600;color:var(--mint,#21d3a1);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;'>Quick Answer</div>
      <div style='font-size:15px;line-height:1.6;color:var(--ink,#073044);'>
        <p>Need clarity on this? Most questions come down to understanding what's real, what's hype, and whether it matters for your situation. This page cuts through the noise.</p>
      </div>
      <div style='margin-top:16px;padding-top:16px;border-top:1px solid var(--stroke2,rgba(7,48,68,.07));'>
        <p style='margin:0;font-size:14px;color:var(--muted,#3f6173);'><strong style='color:var(--ink,#073044);'>Need a real answer?</strong> Text PJ → <a href='tel:+17735441231' style='color:var(--mint,#21d3a1);text-decoration:none;font-weight:600;'>773-544-1231</a></p>
      </div>
    </section>

    <p style="margin:0 0 14px 0;font-size:18px;color:#334155;">
      This page exists to explain this concept in plain English — no jargon, no hype, just clarity.
    </p>
    <a href="sms:+17735441231" style="display:inline-block;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:var(--mint,#10b981);color:#ffffff;box-shadow:0 10px 30px rgba(16,185,129,.25);">
      Text PJ
    </a>
  </div>

CONTENT_PLACEHOLDER

  <div style="background:linear-gradient(135deg,#0f172a,#1e293b);color:#ffffff;border-radius:18px;padding:24px;margin-top:40px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:#ffffff;">Clarity before cost</h2>
    <p style="font-size:17px;color:#cbd5e1;margin-bottom:14px;">
      If you're stuck between options or need a plain-English read on what actually matters, text PJ. A quick outside perspective can save you time, money, and a bad decision.
    </p>
    <a href="sms:+17735441231" style="display:inline-block;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:var(--mint,#10b981);color:#ffffff;">
      Text PJ
    </a>
  </div>

</section>

</main>
</div>

<script>
  const pretty = "773-544-1231";
  const sms = "sms:+17735441231";
  document.querySelectorAll('a[href*="773"]').forEach(n => {
    if(n.href.includes('tel:')) n.href = 'tel:+17735441231';
    if(n.href.includes('sms:')) n.href = sms;
  });
</script>

</body>
</html>
EOFPAGE

  # Replace placeholders
  sed -i "s|TITLE_PLACEHOLDER|$TITLE|g" "$FILE"
  sed -i "s|SLUG_PLACEHOLDER|$SLUG|g" "$FILE"
  sed -i "s|DESC_PLACEHOLDER|$DESC|g" "$FILE"
  sed -i "s|H1_PLACEHOLDER|$H1|g" "$FILE"
  sed -i "s|CONTENT_PLACEHOLDER|$CONTENT|g" "$FILE"

  echo "✅ Created: $SLUG"
}

########################################
# CONTENT BLOCKS
########################################

CONTENT_BASIC='
  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">What people are really trying to figure out</h2>
    <p style="font-size:17px;color:#334155;">
      Most people searching this topic are trying to avoid three things:
    </p>
    <ul style="padding-left:22px;color:#334155;font-size:17px;">
      <li>Getting confused by hype and buzzwords</li>
      <li>Making a decision based on incomplete or biased information</li>
      <li>Missing what actually matters while getting lost in technical details</li>
    </ul>
    <p style="font-size:17px;color:#334155;">
      That is where SideGuy helps. We translate complex topics into clear next moves.
    </p>
  </div>

  <div style="background:rgba(255,255,255,0.7);border:1px solid var(--stroke,#e2e8f0);border-radius:16px;padding:22px;margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Plain English explanation</h2>
    <p style="font-size:17px;color:#334155;">
      This topic gets thrown around in crypto, finance, and tech circles — often without clear definitions. The reality is usually simpler than the marketing suggests, but understanding the core concept matters if you are evaluating platforms, making trades, or trying to understand where the industry is headed.
    </p>
  </div>

  <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:16px;padding:22px;margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Why people text SideGuy first</h2>
    <p style="font-size:17px;color:#334155;">
      Most crypto/finance sites either drown you in jargon or push you toward a specific platform. SideGuy is built for clarity before commitment. You get a human-first read on what matters for your situation before making a bigger move.
    </p>
  </div>

  <div style="margin-bottom:28px;">
    <h2 style="font-size:28px;margin-bottom:12px;color:var(--ink,#0f172a);">Best next step</h2>
    <p style="font-size:17px;color:#334155;">
      If you are trying to understand whether this matters for you — or how to evaluate platforms using different systems — text PJ. I will walk you through what is real, what is marketing, and what you should actually pay attention to.
    </p>
    <a href="sms:+17735441231" style="display:inline-block;margin-top:10px;padding:14px 20px;border-radius:999px;text-decoration:none;font-weight:700;background:var(--ink,#0f172a);color:#ffffff;">
      Text PJ Now
    </a>
  </div>
'

########################################
# PAGE LIST
########################################

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SIDEGUY CLAVDEN CLUSTER BUILDER v2"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

create_page "what-is-clavden-crypto" \
  "What is Clavden Crypto" \
  "What is Clavden Crypto" \
  "Plain English explanation of Clavden crypto infrastructure, what it means, and whether it matters for your trading decisions." \
  "$CONTENT_BASIC"

create_page "what-is-no-order-book-trading" \
  "No Order Book Trading Explained" \
  "What is No Order Book Trading" \
  "Simple explanation of no order book trading systems — how they work, why they exist, and what changes for users." \
  "$CONTENT_BASIC"

create_page "how-do-order-books-work-crypto" \
  "How Order Books Work in Crypto" \
  "How Do Order Books Work in Crypto" \
  "Understanding crypto order book mechanics — the traditional matching system most exchanges use." \
  "$CONTENT_BASIC"

create_page "what-is-amm-crypto" \
  "AMM Crypto Explained" \
  "What is an AMM in Crypto" \
  "Automated market makers explained simply — how liquidity pools replaced order books in DeFi." \
  "$CONTENT_BASIC"

create_page "what-is-intent-based-trading-crypto" \
  "Intent Based Trading Crypto" \
  "What is Intent-Based Trading in Crypto" \
  "New crypto trading execution model explained — what intent-based systems promise and how they differ." \
  "$CONTENT_BASIC"

create_page "order-book-vs-amm-crypto" \
  "Order Book vs AMM Crypto" \
  "Order Book vs AMM Crypto — Key Differences" \
  "Direct comparison of crypto trading models — order books vs automated market makers, pros and cons." \
  "$CONTENT_BASIC"

create_page "centralized-vs-decentralized-trading-manipulation" \
  "Centralized vs Decentralized Trading Manipulation" \
  "Centralized vs Decentralized Trading Manipulation" \
  "How manipulation differs in crypto systems — centralized exchange risks vs decentralized protocol vulnerabilities." \
  "$CONTENT_BASIC"

create_page "amm-vs-order-book-pros-cons" \
  "AMM vs Order Book Pros and Cons" \
  "AMM vs Order Book: Pros and Cons for Traders" \
  "Comprehensive comparison of crypto trading models — when to use AMMs, when order books make more sense." \
  "$CONTENT_BASIC"

create_page "best-trading-model-crypto-explained" \
  "Best Crypto Trading Model Explained" \
  "Best Trading Model in Crypto — Which One to Use" \
  "Choosing the right crypto trading system — depends on your assets, trade size, and priorities." \
  "$CONTENT_BASIC"

create_page "is-crypto-order-book-manipulation-real" \
  "Is Crypto Order Book Manipulation Real" \
  "Is Crypto Order Book Manipulation Real" \
  "Exploring manipulation in crypto markets — wash trading, spoofing, and what you can actually do about it." \
  "$CONTENT_BASIC"

create_page "how-to-avoid-market-manipulation-crypto" \
  "Avoid Crypto Market Manipulation" \
  "How to Avoid Market Manipulation in Crypto" \
  "Practical ways to trade smarter in crypto — recognizing manipulation tactics and choosing better platforms." \
  "$CONTENT_BASIC"

create_page "why-crypto-prices-feel-fake" \
  "Why Crypto Prices Feel Fake" \
  "Why Crypto Prices Feel Fake — Understanding Price Movement" \
  "Explaining the confusion around crypto pricing — why prices seem manipulated and what is actually happening." \
  "$CONTENT_BASIC"

create_page "are-centralized-exchanges-manipulated" \
  "Are Centralized Exchanges Manipulated" \
  "Are Centralized Exchanges Manipulated" \
  "Honest look at centralized exchange concerns — what is documented, what is speculation, what to watch." \
  "$CONTENT_BASIC"

create_page "best-no-order-book-crypto-exchanges" \
  "Best No Order Book Crypto Exchanges" \
  "Best No Order Book Crypto Exchanges" \
  "Platforms using alternative trading models — AMMs, intent-based systems, and what makes them different." \
  "$CONTENT_BASIC"

create_page "how-to-trade-without-order-book" \
  "Trade Without Order Book" \
  "How to Trade Without an Order Book" \
  "Guide to new trading systems — using AMMs, aggregators, and intent-based platforms effectively." \
  "$CONTENT_BASIC"

create_page "decentralized-trading-alternatives-crypto" \
  "Decentralized Trading Alternatives" \
  "Decentralized Trading Alternatives in Crypto" \
  "Options beyond centralized exchanges — DEXs, AMMs, peer-to-peer systems, and hybrid models." \
  "$CONTENT_BASIC"

create_page "future-of-crypto-trading-infrastructure" \
  "Future of Crypto Trading Infrastructure" \
  "Future of Crypto Trading Infrastructure" \
  "Where trading systems are going — trends in execution, liquidity provision, and market structure." \
  "$CONTENT_BASIC"

create_page "next-generation-crypto-exchanges-explained" \
  "Next Generation Crypto Exchanges" \
  "Next Generation Crypto Exchanges Explained" \
  "Modern exchange evolution — what is changing, what is marketing, and what actually matters." \
  "$CONTENT_BASIC"

create_page "will-order-books-be-replaced" \
  "Will Order Books Be Replaced" \
  "Will Order Books Be Replaced in Crypto Trading" \
  "Future of trading systems — whether order books will disappear and what might replace them." \
  "$CONTENT_BASIC"

create_page "clavden-infrastructure-crypto-explained" \
  "Clavden Infrastructure Crypto" \
  "Clavden Infrastructure Crypto Explained" \
  "Understanding the Clavden narrative — what it is, who is building it, and whether it changes anything." \
  "$CONTENT_BASIC"

########################################
# FINISH
########################################

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ CLAVDEN CLUSTER BUILD COMPLETE"
echo "20 pages created in root directory"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  1. Run: ./generate-sitemap-failsafe.sh"
echo "  2. Review pages in browser"
echo "  3. Commit: git add . && git commit -m 'Add: Clavden crypto cluster ($DATE)'"
echo ""
