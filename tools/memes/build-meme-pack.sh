#!/bin/bash
mkdir -p meme-packs
for topic in ai-confusion payments local-business relocation future-tech
do
  cp seo-template.html "meme-packs/${topic}-meme-pack.html"
done
echo "[ok] meme packs generated"
