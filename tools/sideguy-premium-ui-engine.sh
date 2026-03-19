#!/usr/bin/env bash

# ==========================================================
# SIDEGUY PREMIUM UI ENGINE
# WARNING: This script modifies ALL HTML files in public/.
#
# CONFLICTS WITH EXISTING DESIGN SYSTEM:
# - Existing pages use a light ocean theme (inline CSS :root)
# - This injects a dark body background that overrides it
# - Adds an external Google Fonts CDN link (against project policy)
# - Injects a fixed command bar into every page
#
# DO NOT run this on production without reviewing the visual
# result on at least 10 representative pages first.
#
# Usage: bash tools/sideguy-premium-ui-engine.sh --confirm
# ==========================================================

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

if [ "${1:-}" != "--confirm" ]; then
  echo ""
  echo "SAFETY STOP"
  echo "========================================================="
  echo "This script injects CSS and a fixed command bar into"
  echo "ALL HTML files under public/ (~1,725+ pages)."
  echo ""
  echo "KNOWN CONFLICTS:"
  echo "  - Overrides existing light ocean inline body styles"
  echo "  - Adds external Google Fonts CDN (project uses none)"
  echo "  - Fixed command bar may cover existing page headers"
  echo ""
  echo "Review the impact on a sample page first."
  echo "Then run with --confirm to proceed:"
  echo ""
  echo "  bash tools/sideguy-premium-ui-engine.sh --confirm"
  echo "========================================================="
  echo ""
  exit 0
fi

mkdir -p tools/ui
mkdir -p logs

echo ""
echo "======================================"
echo "SIDEGUY PREMIUM UI ENGINE"
echo "Calm Futuristic Command Center Mode"
echo "======================================"
echo ""

########################################
# GLOBAL STYLE BLOCK
########################################

cat > tools/ui/ui-style.html <<'EOF'

<!-- SIDEGUY UI UPGRADE -->

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

<style>

body {
  font-family: 'Inter', sans-serif;
  background: linear-gradient(180deg,#061018,#0b1f33);
  color: #e6f0ff;
}

/* HERO GLOW */
.hero-glow {
  background: radial-gradient(circle at center, rgba(0,255,200,0.15), transparent 60%);
  padding: 60px 20px;
  text-align: center;
}

/* GLASS CARDS */
.glass {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 20px;
  margin: 20px 0;
  border: 1px solid rgba(255,255,255,0.1);
  transition: all 0.3s ease;
}

.glass:hover {
  transform: translateY(-5px);
  box-shadow: 0 0 30px rgba(0,255,200,0.2);
}

/* COMMAND BAR */
.command-bar {
  position: fixed;
  top: 0;
  width: 100%;
  background: rgba(0,0,0,0.8);
  padding: 10px;
  font-size: 12px;
  text-align: center;
  z-index: 9999;
  border-bottom: 1px solid rgba(0,255,200,0.3);
}

/* TEXT PJ ORB */
.textpj {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg,#00ffaa,#00cfff);
  padding: 16px 20px;
  border-radius: 50px;
  font-weight: bold;
  box-shadow: 0 0 25px rgba(0,255,200,0.6);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(0,255,200,0.7); }
  70% { box-shadow: 0 0 0 20px rgba(0,255,200,0); }
}

</style>

<div class="command-bar">
SIDEGUY COMMAND CENTER — STATUS: ONLINE — AI: READY — PJ: AVAILABLE
</div>

EOF

########################################
# SAFE INJECT FUNCTION
########################################

inject_ui () {

  FILE=$1

  if grep -q "SIDEGUY UI UPGRADE" "$FILE"; then
    return
  fi

  TMP=$(mktemp)

  awk '
  /<head>/ {
    print;
    system("cat tools/ui/ui-style.html");
    next;
  }
  {print}
  ' "$FILE" > "$TMP"

  mv "$TMP" "$FILE"

  echo "[✓] UI upgraded → $FILE"
}

########################################
# APPLY TO ALL HTML
########################################

echo ""
echo "Upgrading UI across site..."

while IFS= read -r file; do
  inject_ui "$file"
done < <(find public -name "*.html")

echo ""
echo "======================================"
echo "UI UPGRADE COMPLETE"
echo "======================================"
echo ""
