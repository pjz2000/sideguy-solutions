
#!/usr/bin/env bash

# ============================================================

# SIDEGUY CPU — BULK APPROVAL QUEUE (SAFE)

# SHIP-003

# ============================================================

#

# PURPOSE:

# - Promote explicitly approved sandbox pages to live

# - Never kill the shell

# - Always finish

#

# USAGE:

#   APPROVAL_LIST=approve.txt bash shipped/scripts/SHIP-003-bulk-approve-safe.sh

#

# ============================================================



set -u



LIVE_ROOT="site"

LOG_DIR="logs"

LOG_FILE="$LOG_DIR/approvals.log"

mkdir -p "$LOG_DIR"



APPROVAL_LIST="${APPROVAL_LIST:-}"



TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"

APPROVED_COUNT=0

SKIPPED_COUNT=0



echo "START BULK APPROVAL (SAFE)"



if [ -z "$APPROVAL_LIST" ]; then

  echo "WARN: APPROVAL_LIST not set. Nothing to do."

  exit 0

fi



if [ ! -f "$APPROVAL_LIST" ]; then

  echo "WARN: Approval list not found: $APPROVAL_LIST"

  exit 0

fi



while read -r SANDBOX_PAGE; do

  [ -z "$SANDBOX_PAGE" ] && continue



  if [[ "$SANDBOX_PAGE" != sandbox/* ]]; then

    echo "SKIP: Invalid path $SANDBOX_PAGE"

    SKIPPED_COUNT=$((SKIPPED_COUNT+1))

    continue

  fi



  if [ ! -f "$SANDBOX_PAGE" ]; then

    echo "SKIP: Missing file $SANDBOX_PAGE"

    SKIPPED_COUNT=$((SKIPPED_COUNT+1))

    continue

  fi



  REL_PATH="${SANDBOX_PAGE#sandbox/}"

  LIVE_PAGE="$LIVE_ROOT/$REL_PATH"

  LIVE_DIR="$(dirname "$LIVE_PAGE")"



  mkdir -p "$LIVE_DIR"

  cp "$SANDBOX_PAGE" "$LIVE_PAGE"



  echo "$TIMESTAMP | APPROVED | $SANDBOX_PAGE -> $LIVE_PAGE" >> "$LOG_FILE"

  echo "APPROVED: $LIVE_PAGE"



  APPROVED_COUNT=$((APPROVED_COUNT+1))



done < "$APPROVAL_LIST"



echo "DONE | approved=$APPROVED_COUNT skipped=$SKIPPED_COUNT"

exit 0

