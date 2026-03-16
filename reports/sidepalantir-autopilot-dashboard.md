# SidePalantir Autopilot Dashboard

## Main Commands

### Generate brief + cluster plan
./tools/intelligence/autopilot-router.sh "topic name"

### Generate brief only
./tools/intelligence/auto-brief.sh "topic name"

### Generate cluster plan only
./tools/intelligence/cluster-autoplan.sh "topic name"

### Add page to sitemap
./tools/intelligence/sitemap-helper.sh "page.html"

### Add page link to homepage
./tools/intelligence/index-link-helper.sh "page.html" "Page Label"

### Log signal
./tools/intelligence/log-signal.sh "topic" "action" "page.html"

## Recommended Workflow
1. run autopilot-router
2. give brief to Claude / CPU-GPT
3. publish page
4. add sitemap entry
5. add internal link
6. log the signal
