#!/usr/bin/env python3
"""
SideGuy Solutions — Repository Health Check
Validates repo cleanliness and configuration
"""
import os
from pathlib import Path
import subprocess

def check_backup_files():
    """Verify no backup files in root"""
    root = Path('/workspaces/sideguy-solutions')
    backups = list(root.glob('*.backup.*'))
    if backups:
        print(f"⚠️  Found {len(backups)} backup files (should be 0)")
        return False
    print("✅ No backup files found")
    return True

def check_tmp_files():
    """Verify no temporary files"""
    root = Path('/workspaces/sideguy-solutions')
    tmp_files = list(root.glob('*.tmp'))
    if tmp_files:
        print(f"⚠️  Found {len(tmp_files)} .tmp files (should be 0)")
        return False
    print("✅ No .tmp files found")
    return True

def check_sitemap():
    """Verify sitemap exists and is valid"""
    root = Path('/workspaces/sideguy-solutions')
    sitemap = root / 'sitemap.xml'
    sitemap_index = root / 'sitemap-index.xml'
    
    if not sitemap.exists():
        print("⚠️  sitemap.xml missing")
        return False
    if not sitemap_index.exists():
        print("⚠️  sitemap-index.xml missing")
        return False
    
    # Check sitemap size
    size = sitemap.stat().st_size
    if size < 1000:
        print(f"⚠️  sitemap.xml too small ({size} bytes)")
        return False
    
    print(f"✅ Sitemaps valid (sitemap.xml: {size:,} bytes)")
    return True

def check_robots_txt():
    """Verify robots.txt configured correctly"""
    root = Path('/workspaces/sideguy-solutions')
    robots = root / 'robots.txt'
    
    if not robots.exists():
        print("⚠️  robots.txt missing")
        return False
    
    content = robots.read_text()
    if 'sitemap-index.xml' not in content.lower():
        print("⚠️  robots.txt doesn't reference sitemap-index.xml")
        return False
    
    print("✅ robots.txt configured correctly")
    return True

def check_gitignore():
    """Verify .gitignore exists"""
    root = Path('/workspaces/sideguy-solutions')
    gitignore = root / '.gitignore'
    
    if not gitignore.exists():
        print("⚠️  .gitignore missing")
        return False
    
    content = gitignore.read_text()
    if '*.backup.*' not in content:
        print("⚠️  .gitignore doesn't exclude backup files")
        return False
    
    print("✅ .gitignore configured correctly")
    return True

def count_html_pages():
    """Count HTML pages"""
    root = Path('/workspaces/sideguy-solutions')
    html_files = [f for f in root.glob('*.html') if not f.name.startswith('.')]
    print(f"📄 {len(html_files)} HTML pages in repository")
    return len(html_files)

def main():
    print("=" * 60)
    print("🔍 SIDEGUY REPOSITORY HEALTH CHECK")
    print("=" * 60 + "\n")
    
    checks = [
        check_backup_files(),
        check_tmp_files(),
        check_sitemap(),
        check_robots_txt(),
        check_gitignore()
    ]
    
    print()
    count_html_pages()
    
    print("\n" + "=" * 60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("🎉 Repository is clean and ready!")
    else:
        print(f"⚠️  {total - passed} checks failed ({passed}/{total} passed)")
    print("=" * 60)

if __name__ == '__main__':
    main()
