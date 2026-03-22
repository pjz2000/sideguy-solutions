#!/usr/bin/env bash

########################################
# SIDEGUY PREMIUM UI ENGINE
#
# !! DESIGN CONFLICT WARNING !!
#
# This script injects a dark body theme (background: linear-gradient
# #061018 → #0b1f33) via sed -i into ALL production HTML files.
#
# SideGuy's existing design uses a LIGHT ocean theme defined via
# CSS custom properties (--bg0, --bg1, --bg2, --ink) with inline
# styles. Injecting dark body styles WILL conflict with those
# variables and may break page layouts across 1,700+ pages.
#
# BEFORE RUNNING:
#   1. Test on ONE page manually first
#   2. Commit / backup your current state (git commit -am "backup")
#   3. Verify the injection doesn't fight existing inline styles
#   4. Pass --confirm to allow execution
#
# USAGE:
#   bash tools/ui/upgrade-ui.sh --confirm
########################################

if [ "$1" != "--confirm" ]; then
  echo ""
  echo "!! SAFETY GATE !!"
  echo ""
  echo "This script modifies ALL production HTML pages with a dark"
  echo "body theme that conflicts with SideGuy's existing light CSS."
  echo ""
  echo "Read the warning at the top of this file before proceeding."
  echo ""
  echo "To run: bash tools/ui/upgrade-ui.sh --confirm"
  echo ""
  exit 1
fi

cd /workspaces/sideguy-solutions || exit 1

echo ""
echo "Applying premium UI (confirmed)..."
echo ""

COUNT=0
SKIPPED=0

while IFS= read -r file; do

  if grep -q "SIDEGUY UI" "$file"; then
    SKIPPED=$((SKIPPED+1))
    continue
  fi

  # NOTE: sed -i multiline append after <head> — Linux GNU sed only
  sed -i '/<head>/a <style>body{font-family:Inter,sans-serif;background:linear-gradient(#061018,#0b1f33);color:#e6f0ff;}.command-bar{position:fixed;top:0;width:100%;background:rgba(0,0,0,0.9);padding:10px;text-align:center;font-size:12px;border-bottom:1px solid #00ffaa;z-index:9999;}.glass{background:rgba(255,255,255,0.05);backdrop-filter:blur(10px);padding:20px;border-radius:14px;border:1px solid rgba(255,255,255,0.1);}.textpj{position:fixed;bottom:20px;right:20px;background:linear-gradient(135deg,#00ffaa,#00ccff);padding:16px;border-radius:40px;box-shadow:0 0 20px rgba(0,255,200,0.6);animation:pulse 2s infinite;}@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(0,255,200,0.7);}70%{box-shadow:0 0 0 20px rgba(0,255,200,0);}}<\/style><!-- SIDEGUY UI -->' "$file"

  COUNT=$((COUNT+1))

done < <(find public -name "*.html")

echo "UI upgraded: $COUNT files"
echo "Skipped (already done): $SKIPPED files"
