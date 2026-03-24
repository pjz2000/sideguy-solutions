#!/usr/bin/env bash

########################################
# BATCH UPGRADE: AI PAGES TO 2026 DESIGN
# Applies modern CSS to 30 AI infrastructure pages
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

# List of 30 AI infrastructure pages
PAGES=(
  "who-builds-ai-data-centers.html"
  "ai-data-center-electrical-contractors.html"
  "data-center-power-infrastructure-cost.html"
  "how-to-build-ai-compute-facility.html"
  "data-center-electrical-upgrade-guide.html"
  "mission-critical-electrical-services-explained.html"
  "ai-data-center-construction-companies.html"
  "data-center-power-requirements-explained.html"
  "ai-infrastructure-contractors-near-me.html"
  "electrical-infrastructure-for-ai-facilities.html"
  "ai-data-center-infrastructure-explained.html"
  "electric-data-infrastructure-what-it-means.html"
  "future-of-ai-data-centers-energy-demand.html"
  "ai-data-center-power-consumption-explained.html"
  "ai-data-center-energy-usage-breakdown.html"
  "how-ai-is-impacting-the-power-grid.html"
  "data-center-electricity-demand-future.html"
  "why-ai-needs-more-energy-infrastructure.html"
  "how-ai-data-centers-are-built.html"
  "ai-infrastructure-companies-to-know.html"
  "what-powers-modern-data-centers.html"
  "cooling-systems-for-ai-data-centers.html"
  "ai-data-center-cost-breakdown.html"
  "how-businesses-can-prepare-for-ai-infrastructure.html"
  "investing-in-ai-energy-infrastructure.html"
  "ai-data-center-management-tools.html"
  "will-ai-break-the-power-grid.html"
  "next-generation-data-centers-explained.html"
  "ai-infrastructure-boom-what-to-expect.html"
  "electric-infrastructure-for-ai-future.html"
)

# Modern CSS - extracted from demo page
read -r -d '' MODERN_CSS << 'EOF'
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg-base: #f8fafb;
  --bg-elevated: #ffffff;
  --text-primary: #0a1828;
  --text-secondary: #475569;
  --text-tertiary: #64748b;
  --accent-primary: #0ea5e9;
  --accent-hover: #0284c7;
  --accent-light: #e0f2fe;
  --mint: #10b981;
  --mint-hover: #059669;
  --mint-light: #d1fae5;
  --border-subtle: rgba(148, 163, 184, 0.12);
  --border-medium: rgba(148, 163, 184, 0.24);
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, system-ui, sans-serif;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  scroll-behavior: smooth;
}

body {
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-primary);
  background: var(--bg-base);
  min-height: 100vh;
}

body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 600px;
  background: 
    radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.08), transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.08), transparent 50%),
    linear-gradient(to bottom, rgba(248, 250, 251, 0.8), rgba(248, 250, 251, 1));
  pointer-events: none;
  z-index: -1;
}

.container { max-width: 840px; margin: 0 auto; padding: var(--space-2xl) var(--space-lg); }

h1 {
  font-size: clamp(2rem, 5vw, 2.75rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: var(--space-lg);
}

h2 {
  font-size: clamp(1.5rem, 3vw, 1.875rem);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-top: var(--space-2xl);
  margin-bottom: var(--space-md);
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.01em;
  color: var(--text-primary);
  margin-top: var(--space-xl);
  margin-bottom: var(--space-sm);
}

p { color: var(--text-secondary); margin-bottom: var(--space-md); max-width: 70ch; }

strong { color: var(--text-primary); font-weight: 600; }

ul { margin: var(--space-lg) 0; padding-left: var(--space-xl); color: var(--text-secondary); }

li { margin-bottom: var(--space-sm); line-height: 1.7; }

li::marker { color: var(--accent-primary); }

a { color: var(--accent-primary); text-decoration: none; font-weight: 500; transition: color 0.2s ease; }

a:hover { color: var(--accent-hover); }

.context-box {
  background: var(--mint-light);
  border-left: 4px solid var(--mint);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin: var(--space-xl) 0;
}

.context-box p { color: var(--text-primary); margin: 0; }

.cta-box, .cta-section {
  background: linear-gradient(135deg, var(--bg-elevated) 0%, var(--accent-light) 100%);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  margin: var(--space-2xl) 0;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.1), transparent 70%);
  pointer-events: none;
}

.cta-box h3, .cta-section h3 { margin-top: 0; font-size: 1.5rem; }

.phone-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  background: var(--mint);
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  text-decoration: none;
  box-shadow: var(--shadow-md);
  transition: all 0.2s ease;
}

.phone-link:hover {
  background: var(--mint-hover);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
  color: white;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  color: var(--text-tertiary);
  font-size: 0.9rem;
  margin-top: var(--space-2xl);
  transition: color 0.2s ease;
}

.back-link:hover { color: var(--accent-primary); }

hr { border: none; border-top: 1px solid var(--border-subtle); margin: var(--space-2xl) 0; }

@media (max-width: 768px) {
  .container { padding: var(--space-xl) var(--space-md); }
  .cta-box, .cta-section { padding: var(--space-xl); }
  .phone-link { width: 100%; justify-content: center; }
}

*:focus-visible { outline: 2px solid var(--accent-primary); outline-offset: 2px; }
</style>
EOF

echo "🎨 Starting design upgrade for 30 AI pages..."
echo ""

upgrade_page() {
  local file="$1"
  
  if [ ! -f "$file" ]; then
    echo "⏭️  Skipped (not found): $file"
    return
  fi
  
  # Create backup
  cp "$file" "${file}.backup-$(date +%Y%m%d)"
  
  # Replace old <style> block with new modern CSS
  # Using awk to find and replace between <style> and </style>
  awk -v newcss="$MODERN_CSS" '
  BEGIN { in_style=0; style_replaced=0 }
  /<style>/ { 
    if (!style_replaced) {
      print newcss
      in_style=1
      style_replaced=1
      next
    }
  }
  /<\/style>/ {
    if (in_style) {
      in_style=0
      next
    }
  }
  !in_style { print }
  ' "$file" > "${file}.tmp"
  
  mv "${file}.tmp" "$file"
  echo "✅ Upgraded: $file"
}

COUNT=0
for page in "${PAGES[@]}"; do
  upgrade_page "$page"
  COUNT=$((COUNT+1))
done

echo ""
echo "✅ Design upgrade complete: $COUNT pages updated"
echo "📋 Backups created with .backup-$(date +%Y%m%d) extension"
echo ""
