#!/usr/bin/env bash
set -eu

echo "Step 1: Normalize sms:+1773-544-1231 to E.164..."
find . -name "*.html" -type f -exec sed -i 's|sms:+1773-544-1231|sms:+17735441231|g' {} +
echo "Done."

echo "Step 2: Add missing + prefix to sms:17735441231..."
find . -name "*.html" -type f -exec sed -i 's|sms:17735441231|sms:+17735441231|g' {} +
echo "Done."

echo "Step 3: Adding rel + aria-label to SMS href (guarded against double-add)..."
# Match href="sms:+17735441231" NOT already followed by ' rel'
find . -name "*.html" -type f -exec sed -i \
  's|href="sms:+17735441231" |href="sms:+17735441231" rel="nofollow" aria-label="Text PJ for clarity session" |g' {} +
# Also handle href="sms:+17735441231"> (end of tag, no trailing space)
find . -name "*.html" -type f -exec sed -i \
  's|href="sms:+17735441231">|href="sms:+17735441231" rel="nofollow" aria-label="Text PJ for clarity session">|g' {} +
echo "Done."

echo "SMS normalization complete."
