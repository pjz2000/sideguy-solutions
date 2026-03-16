# SidePalantir Autopilot Doctrine

## Goal
Convert good signals into clean, useful SideGuy architecture without creating spam.

## Autopilot Flow
1. detect topic
2. generate brief
3. generate cluster plan
4. operator approves or builds
5. add to sitemap
6. add internal links
7. log signal
8. compound authority

## Rules
- architecture first
- content second
- no blind bulk publishing
- every page needs a reason
- every page should fit a hub
- every page should help a real person
- use Text PJ as the human resolution layer
- calm tone beats hype tone

## Suggested Commands

### Create brief + cluster plan
./tools/intelligence/autopilot-router.sh "machine to machine payments"

### Add new page to sitemap
./tools/intelligence/sitemap-helper.sh "machine-to-machine-payments.html"

### Add homepage link
./tools/intelligence/index-link-helper.sh "machine-to-machine-payments.html" "Machine to Machine Payments"

### Log the move
./tools/intelligence/log-signal.sh "machine to machine payments" "Published page" "machine-to-machine-payments.html"
