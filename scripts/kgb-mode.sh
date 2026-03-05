#!/usr/bin/env bash
# SIDEGUY KGB MODE — PROBLEM INTEL + AUTHORITY GRAVITY + AUTO-WIRING (vNext)
# Goal: radar → gravity → authority → hot page builds → link wiring → intel brief → sitemap → GSC submit list
# Usage: bash scripts/kgb-mode.sh
# Knobs: KGB_DRY_RUN=1 KGB_TOP=120 KGB_GRAVITY_LIMIT=800 bash scripts/kgb-mode.sh

set -e

echo "=== SIDEGUY KGB MODE: INTEL + GRAVITY + AUTHORITY (vNext) ==="
date
echo "pwd: $(pwd)"

PHONE_SMS="sms:+17735441231"
PHONE_TEL="tel:+17735441231"
export PHONE_SMS
export PHONE_TEL

# ── Knobs ─────────────────────────────────────────────────────────────────────
export KGB_TOP="${KGB_TOP:-80}"
export KGB_BUILD_LIMIT="${KGB_BUILD_LIMIT:-120}"
export KGB_WIRE_PER_PAGE="${KGB_WIRE_PER_PAGE:-10}"
export KGB_GRAVITY_LIMIT="${KGB_GRAVITY_LIMIT:-500}"
export KGB_DRY_RUN="${KGB_DRY_RUN:-0}"
export INDUSTRIES="${INDUSTRIES:-16}"

echo ""
echo "Knobs:"
echo "  KGB_TOP=${KGB_TOP}"
echo "  KGB_BUILD_LIMIT=${KGB_BUILD_LIMIT}"
echo "  KGB_WIRE_PER_PAGE=${KGB_WIRE_PER_PAGE}"
echo "  KGB_GRAVITY_LIMIT=${KGB_GRAVITY_LIMIT}"
echo "  KGB_DRY_RUN=${KGB_DRY_RUN}"
echo ""

# ── 0) Phone enforcement ──────────────────────────────────────────────────────
echo "[0/9] Enforce Text PJ phone where supported"
if [ -f "scripts/enforce-phone.py" ]; then
  python3 scripts/enforce-phone.py
else
  echo "  scripts/enforce-phone.py not found (ok)."
fi

# ── 1) Sitemap refresh (crawl map) ────────────────────────────────────────────
echo ""
echo "[1/9] Sitemap refresh"
if [ -f "scripts/generate-sitemap.py" ]; then
  python3 scripts/generate-sitemap.py
elif [ -f "scripts/generate_sitemap.py" ]; then
  python3 scripts/generate_sitemap.py
else
  echo "  No sitemap generator found (ok)."
fi

# ── 2) Refresh problem radar (fresh signal) ───────────────────────────────────
echo ""
echo "[2/9] Refresh Problem Radar"
if [ -f "scripts/problem-radar.py" ]; then
  python3 scripts/problem-radar.py
else
  echo "  scripts/problem-radar.py not found."
fi

RADAR_CSV=""
for f in \
  "radar/problem-radar-new.csv" \
  "radar/problem-radar.csv" \
  "problem-radar-new.csv" \
  "problem-radar.csv"
do
  if [ -f "$f" ]; then
    RADAR_CSV="$f"
    break
  fi
done
echo "  Radar file: ${RADAR_CSV:-NONE}"

# SG_FUTURE_RADAR_STEP
# ── 2b) Future Radar (SEO Time Travel) ───────────────────────────────────────
echo ""
echo "[2b] Future Radar (live signal fetch + score)"
if [ -f "scripts/future-radar.py" ]; then
  python3 scripts/future-radar.py
else
  echo "  scripts/future-radar.py not found (ok)."
fi
# SG_FUTURE_RADAR_STEP_END

# SG_FUTURE_AUTO_BUILDER_STEP
# ── 2c) Future Auto Builder ──────────────────────────────────────────────────
echo ""
echo "[2c] Future Auto Builder (build pages from radar topics)"
if [ -f "scripts/future-auto-builder.py" ]; then
  python3 scripts/future-auto-builder.py
else
  echo "  scripts/future-auto-builder.py not found (ok)."
fi
# SG_FUTURE_AUTO_BUILDER_STEP_END

# ── 3) Traffic Gravity scoring ────────────────────────────────────────────────
echo ""
echo "[3/9] Run Traffic Gravity (scoring)"
export LIMIT="${KGB_GRAVITY_LIMIT}"
export PER_PAGE="${KGB_WIRE_PER_PAGE}"
export DRY_RUN="${KGB_DRY_RUN}"

if [ -f "scripts/traffic-gravity.py" ]; then
  python3 scripts/traffic-gravity.py
else
  echo "  scripts/traffic-gravity.py not found (ok)."
fi

# ── 4) Authority engine refresh ───────────────────────────────────────────────
echo ""
echo "[4/9] Authority Engine refresh"
if [ -f "scripts/authority-engine.py" ]; then
  python3 scripts/authority-engine.py
else
  echo "  scripts/authority-engine.py not found (ok)."
fi

# ── 5) Build hot pages from radar (idempotent + limited) ─────────────────────
echo ""
echo "[5/9] Build Hot Pages (from radar) — idempotent + limited"
if [ "${KGB_DRY_RUN}" = "1" ]; then
  echo "  DRY RUN: skipping page generation."
else
  if [ -n "${RADAR_CSV}" ] && [ -f "scripts/problem-multiplier-engine.sh" ]; then
    echo "  Using scripts/problem-multiplier-engine.sh LIMIT=${KGB_BUILD_LIMIT} TOPICS=${KGB_TOP}"
    LIMIT="${KGB_BUILD_LIMIT}" TOPICS="${KGB_TOP}" INDUSTRIES="${INDUSTRIES}" \
      bash scripts/problem-multiplier-engine.sh
  elif [ -n "${RADAR_CSV}" ] && [ -f "scripts/auto-build-problems.py" ]; then
    echo "  Using scripts/auto-build-problems.py"
    python3 scripts/auto-build-problems.py
  else
    echo "  No radar-aware builder found (ok)."
  fi
fi

# ── 6) Wire gravity links into high-leverage content ─────────────────────────
echo ""
echo "[6/9] Wire links into high-leverage content (no link-dump hubs)"
if [ "${KGB_DRY_RUN}" = "1" ]; then
  echo "  DRY RUN: skipping wiring."
else
  if [ -f "scripts/wire-traffic-gravity.py" ]; then
    PER_PAGE="${KGB_WIRE_PER_PAGE}" python3 scripts/wire-traffic-gravity.py
  else
    echo "  scripts/wire-traffic-gravity.py not found."
  fi
fi

# ── 7) Daily intel brief page ─────────────────────────────────────────────────
echo ""
echo "[7/9] Generate Daily Intel Brief page"
if [ "${KGB_DRY_RUN}" = "1" ]; then
  echo "  DRY RUN: skipping intel page generation."
else
  if [ -f "scripts/build-fresh-radar.py" ]; then
    python3 scripts/build-fresh-radar.py
  else
    echo "  scripts/build-fresh-radar.py not found (ok)."
  fi
fi

# ── 8) Sitemap refresh post-builds ───────────────────────────────────────────
echo ""
echo "[8/9] Sitemap refresh (post-build)"
if [ -f "scripts/generate-sitemap.py" ]; then
  python3 scripts/generate-sitemap.py
elif [ -f "scripts/generate_sitemap.py" ]; then
  python3 scripts/generate_sitemap.py
else
  echo "  No sitemap generator found (ok)."
fi

# ── 9) GSC priority submit list ───────────────────────────────────────────────
echo ""
echo "[9/9] Write GSC priority submit list"
mkdir -p reports

OUT="reports/gsc-priority.txt"
: > "$OUT"

BASE="https://sideguysolutions.com"

for p in \
  "knowledge-hub.html" \
  "authority-hub.html" \
  "fresh/radar.html" \
  "fresh/gravity.html" \
  "prediction-markets-hub.html" \
  "payments-infrastructure-hub.html" \
  "ai-automation-hub.html" \
  "operator-tools-hub.html" \
  "problems/index.html" \
  "concepts/index.html" \
  "decisions/index.html" \
  "katie/index.html"
do
  if [ -f "$p" ]; then
    echo "${BASE}/${p}" >> "$OUT"
  fi
done

for m in \
  "multiplier/problem-multiplier-built.csv" \
  "radar/problem-radar-new.csv" \
  "radar/problem-radar.csv"
do
  if [ -f "$m" ]; then
    echo "" >> "$OUT"
    echo "# source: $m" >> "$OUT"
    head -n "${KGB_TOP}" "$m" | \
      awk -F',' '
        BEGIN{IGNORECASE=1}
        NR==1{next}
        {
          for (i=1;i<=NF;i++){
            if ($i ~ /^https?:\/\//) { print $i; next }
          }
          if ($1 ~ /^[a-z0-9-]+$/) { print "'"${BASE}"'/problems/"$1".html"; next }
        }
      ' >> "$OUT"
  fi
done

# Dedup + cap to 300
python3 - <<'PY'
import os
path = "reports/gsc-priority.txt"
if not os.path.exists(path):
    raise SystemExit
seen, out = set(), []
for line in open(path, "r", encoding="utf-8", errors="ignore"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("#"):
        out.append(line)
        continue
    if line in seen:
        continue
    seen.add(line)
    out.append(line)
urls  = [x for x in out if not x.startswith("#")]
hdrs  = [x for x in out if x.startswith("#")]
final = hdrs + urls[:300]
open(path, "w", encoding="utf-8").write("\n".join(final) + "\n")
print(f"  Wrote {len(final)} lines to {path}")
PY

## SG_SELF_IMPROVE_STEP
# ── Self-Improving Pages ─────────────────────────────────────────────────────
echo ""
echo "[KGB] Self-Improving Pages (marker-based upgrades)..."
IMPROVE_LIMIT="${IMPROVE_LIMIT:-120}" python3 scripts/self-improve-pages.py
## SG_SELF_IMPROVE_STEP_END

echo ""
echo "=== KGB MODE COMPLETE ==="
echo "GSC submits list: ${OUT}"
echo ""
echo "Next run (report-only):"
echo "  KGB_DRY_RUN=1 KGB_TOP=120 KGB_GRAVITY_LIMIT=800 bash scripts/kgb-mode.sh"
echo ""
echo "Commit when ready:"
echo "  git add -A && git commit -m \"KGB Mode: radar + gravity + authority + intel brief (${PHONE_SMS})\""
