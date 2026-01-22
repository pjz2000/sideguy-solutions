#!/usr/bin/env bash
# =========================================
# SIDEGUY — MAINTENANCE SCRIPT
# Quick access to all maintenance commands
# =========================================

set -e

show_help() {
  cat << EOF
SideGuy Solutions — Maintenance Commands

Usage: bash maintain.sh [command]

Commands:
  health       Run repository health check
  audit        Run metadata SEO audit
  sitemap      Regenerate XML sitemap
  html-map     Generate HTML sitemap (human-readable)
  clean        Clean any backup/temp files (if any)
  full         Run all checks and regenerate everything

Examples:
  bash maintain.sh health
  bash maintain.sh audit
  bash maintain.sh full

EOF
}

health_check() {
  echo "🔍 Running repository health check..."
  python3 health-check.py
}

metadata_audit() {
  echo "📊 Running metadata SEO audit..."
  python3 metadata-audit.py
}

generate_sitemap() {
  echo "🗺️  Regenerating XML sitemap..."
  python3 generate-xml-sitemap.py
}

generate_html_sitemap() {
  echo "📄 Generating HTML sitemap..."
  bash generate-sitemap-failsafe.sh
}

clean_repo() {
  echo "🧹 Cleaning repository..."
  find . -maxdepth 1 -name "*.backup.*" -delete 2>/dev/null || true
  find . -maxdepth 1 -name "*.tmp" -delete 2>/dev/null || true
  echo "✅ Cleanup complete"
}

run_full() {
  echo "🚀 Running full maintenance..."
  echo ""
  clean_repo
  echo ""
  generate_sitemap
  echo ""
  generate_html_sitemap
  echo ""
  health_check
  echo ""
  metadata_audit
  echo ""
  echo "✅ Full maintenance complete!"
}

# Main logic
case "${1:-help}" in
  health)
    health_check
    ;;
  audit)
    metadata_audit
    ;;
  sitemap)
    generate_sitemap
    ;;
  html-map)
    generate_html_sitemap
    ;;
  clean)
    clean_repo
    ;;
  full)
    run_full
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    echo "❌ Unknown command: $1"
    echo ""
    show_help
    exit 1
    ;;
esac
