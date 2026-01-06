import re
import sys
from pathlib import Path

files = [
  'longtail/encinitas-who-to-call-under-sink-leak.html',
  'longtail/solana-beach-how-to-apply-for-sdgande-rebates.html',
  'longtail/cardiff-how-to-lower-electric-bill-small-business.html',
  'longtail/leucadia-ai-for-local-marketing.html',
  'longtail/san-diego-how-to-switch-payment-providers-without-downtime.html',
  'longtail/encinitas-what-to-do-if-your-processor-raises-fees.html',
  'longtail/solana-beach-ac-freezing-up.html',
  'longtail/cardiff-how-to-prepare-for-a-payment-audit.html',
  'longtail/leucadia-how-to-find-a-local-licensed-contractor.html',

  # Batch 1 (11-20)
  'longtail/solana-beach-prepare-for-processor-fee-increase.html',
  'longtail/cardiff-ac-freezing-up.html',
  'longtail/encinitas-solar-rebates-financing.html',
  'longtail/leucadia-handle-chargebacks.html',
  'longtail/san-diego-instant-payouts-for-drivers.html',
  'longtail/solana-beach-pos-best-practices.html',
  'longtail/cardiff-same-day-plumber.html',
  'longtail/encinitas-audit-your-processor-in-30-minutes.html',
  'longtail/leucadia-ach-vs-card.html',
  'longtail/san-diego-prevent-fraud-small-merchants.html',

  # New pilot page
  'longtail/san-diego-payment-processing-for-marketplaces.html'
]

ok = True

print('Running quick QA checks on pilot pages...')
for f in files:
    p = Path(f)
    if not p.exists():
        print(f'  MISSING: {f}')
        ok = False
        continue
    s = p.read_text(encoding='utf-8')
    title = re.search(r'<title>(.*?)</title>', s, re.I|re.S)
    desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', s, re.I|re.S)
    canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', s, re.I|re.S)
    guard = 'Clarity before selling' in s or 'SideGuy:' in s
    jsonld = '<script type="application/ld+json">' in s
    h1 = re.search(r'<h1>(.*?)</h1>', s, re.I|re.S)
    lang = re.search(r'<html\s+lang=["\']en["\']', s, re.I|re.S)

    print(f'-- {f}')
    print('   title:', (title.group(1).strip() if title else 'MISSING'))
    if desc:
        ln = len(desc.group(1).strip())
        print(f'   meta desc: {ln} chars')
        if ln < 50 or ln > 160:
            print('     ⚠️ meta length out of recommended range (50-160)')
            ok = False
    else:
        print('   ⚠️ meta description: MISSING')
        ok = False
    print('   canonical:', 'OK' if canon else 'MISSING')
    if not canon:
        ok = False
    print('   guardrail:', 'OK' if guard else 'MISSING')
    if not guard:
        ok = False
    print('   JSON-LD FAQ:', 'OK' if jsonld else 'MISSING')
    if not jsonld:
        ok = False
    print('   H1:', 'OK' if h1 else 'MISSING')
    if not h1:
        ok = False
    print('   lang=en:', 'OK' if lang else 'MISSING')
    if not lang:
        ok = False

print('\nQA SUMMARY — all checks passed' if ok else '\nQA SUMMARY — issues found (see above)')
if not ok:
    sys.exit(2)
else:
    sys.exit(0)
