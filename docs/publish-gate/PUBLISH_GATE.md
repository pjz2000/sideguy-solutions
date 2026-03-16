# SideGuy Publish Gate

Purpose:

Prevent weak pages from entering the live index.

This script checks pages for:

title tag
H1 tag
word count
internal links
canonical tag
FAQ schema

Pages must pass quality thresholds before:

being linked internally
being added to sitemaps
being promoted from reserve to live

Command:

bash tools/intelligence/publish-gate.sh .

Output:

logs/publish-gate/publish-gate-report.txt

Workflow:

run publish gate

fix failing pages

promote passing pages to sitemap

repeat
