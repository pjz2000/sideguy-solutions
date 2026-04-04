#!/bin/bash

echo "😂 Injecting Meme Intelligence Strip"

find . -maxdepth 1 -name "*.html" | while read FILE; do
  if ! grep -q "meme-intelligence-strip" "$FILE"; then
    perl -0pi -e 's#</body>#<section id="meme-intelligence-strip" style="max-width:980px;margin:40px auto 20px;padding:24px;border-radius:18px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);backdrop-filter:blur(8px);"><div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;opacity:.65;margin-bottom:8px;">SideGuy Meme Intelligence</div><h3 style="margin:0 0 10px;">"I'\''m in business development. I develop the business. What don'\''t you understand?"</h3><p style="margin:0;opacity:.85;">The humor is the point: behind every meme is real architecture — search signals routed to the right pages, human trust blocks, conversion pathways, and real-world problem resolution.</p></section></body>#s' "$FILE"
      echo "😂 memed $FILE"
  fi
done

cat > docs/memes/meme-intelligence-doctrine.md <<DOC
# Meme Intelligence Doctrine

Purpose:
- make SideGuy feel human
- improve memorability + shares
- differentiate from sterile AI sites
- explain architecture through humor
- keep the site alive and current
DOC

echo "✅ Meme strip injected"
