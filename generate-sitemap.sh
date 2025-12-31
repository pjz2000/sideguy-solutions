#!/usr/bin/env bash

# ==========================================
# SIDEGUY — FULL VISUAL SITEMAP + PAGE COUNTS
# CPU-GPT SAFE | NO FRAGILE TOOLS
# ==========================================

# Backup existing sitemap
[ -f sitemap.html ] && cp sitemap.html sitemap.backup.$(date +%Y%m%d-%H%M).html

find . -type f -name "*.html" \
  ! -name "*backup*" \
  ! -name "sitemap.html" \
  | sort \
  | awk '
  BEGIN {
    print "<!DOCTYPE html><html><head><meta charset=\"utf-8\">"
    print "<title>SideGuy Solutions — All Pages</title>"
    print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
    print "<style>"
    print "body{font-family:system-ui,-apple-system,Arial;background:#eefcff;padding:24px}"
    print "h1{margin-bottom:6px}"
    print ".meta{color:#555;font-size:12px;margin-bottom:16px}"
    print ".section{margin-top:26px}"
    print "ul{columns:2;max-width:1400px}"
    print "li{margin:6px 0;break-inside:avoid}"
    print "a{text-decoration:none;color:#0a5cff;font-weight:600}"
    print "@media(max-width:900px){ul{columns:1}}"
    print "</style></head><body>"
    print "<h1>SideGuy Solutions — All Pages</h1>"
    print "<div class=\"meta\">Generated: " strftime("%Y-%m-%d %H:%M") "</div>"
  }

  {
    gsub("^\\./","",$0)
    split($0, parts, "/")
    section = (length(parts) > 1) ? parts[1] : "root-pages"
    pages[section] = pages[section] "\n<li><a href=\"/" $0 "\">" $0 "</a></li>"
    counts[section]++
    total++
  }

  END {
    print "<div class=\"section\"><b>Total pages:</b> " total "</div>"

    print "<div class=\"section\"><b>Pages by section:</b><ul>"
    for (s in counts) {
      print "<li><b>" s "</b>: " counts[s] "</li>"
    }
    print "</ul></div>"

    for (s in pages) {
      print "<div class=\"section\">"
      print "<h2>" s " (" counts[s] ")</h2>"
      print "<ul>" pages[s] "</ul>"
      print "</div>"
    }

    print "</body></html>"
  }' > sitemap.html

echo "✅ Visual sitemap with page counts created → sitemap.html"
