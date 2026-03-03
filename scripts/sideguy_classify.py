#!/usr/bin/env python3
"""
SideGuy Shared Classification Helpers
Used by build-pages.py and build-authority.py.
Import as: from sideguy_classify import slugify, topic_to_filename, classify_topic
"""

import re

DOMAIN = "https://sideguysolutions.com"

# ── Slug helpers ─────────────────────────────────────────────────────────────

def slugify(text):
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    slug = re.sub(r'(-san-diego)+$', '', slug)
    return slug

def topic_to_filename(topic):
    return f"{slugify(topic)}-san-diego.html"

def topic_to_url(topic):
    return f"{DOMAIN}/{topic_to_filename(topic)}"

# ── Industry extraction ───────────────────────────────────────────────────────

# Patterns that introduce an industry: "for X", "for X in san diego", etc.
_FOR_PATTERN = re.compile(
    r'\bfor\s+(.+?)(?:\s+in\s+san\s+diego|\s+san\s+diego)?$', re.IGNORECASE
)

def extract_industry(topic):
    """
    Return the industry slug from topics like 'ai automation for plumbers'
    or 'how ai helps dentists'. Returns None if no industry found.
    """
    m = _FOR_PATTERN.search(topic)
    if m:
        raw = m.group(1).strip().lower()
        # Filter out non-industry phrases
        non_industries = {
            'small business', 'local business', 'local businesses',
            'entrepreneurs', 'operators', 'merchants', 'restaurants',
            'business', 'businesses', 'contractors', 'freelancers',
        }
        if raw not in non_industries and len(raw.split()) <= 4:
            return re.sub(r'[^a-z0-9]+', '-', raw).strip('-')
    return None

# ── Category classification ───────────────────────────────────────────────────

CATEGORIES = {
    'ai-automation': [
        'ai automation', 'ai tools', 'ai chatbot', 'ai scheduling',
        'ai customer service', 'ai follow', 'ai lead', 'ai workflow',
        'how ai', 'using ai', 'automate', 'automation', 'ai agent',
        'ai copilot', 'ai intake', 'ai receptionist', 'ai phone',
        'ai scoring', 'ai proposal', 'ai contract', 'ai hiring',
        'ai employee', 'ai billing', 'ai reads', 'ai drafts',
        'ai handles', 'ai manages', 'ai analyzes', 'ai predicts',
        'ai improves', 'ai reduces', 'agentic ai', 'deploy ai',
        'build an ai', 'no code ai', 'gpt for', 'claude for',
        'ai for ', 'future of ai',
    ],
    'payments': [
        'credit card', 'payment process', 'processing fee', 'stripe',
        'invoice', 'invoicing', 'billing', 'chargeback', 'payroll',
        'get paid', 'collect payment', 'payment friction', 'payment rail',
        'payment terminal', 'payment gateway', 'paid in crypto',
        'lower payment', 'reduce payment', 'reduce fee',
    ],
    'crypto-solana': [
        'crypto', 'solana', 'usdc', 'stablecoin', 'bitcoin',
        'blockchain', 'web3', 'phantom', 'coinbase commerce',
        'volatility risk', 'crypto tax', 'crypto accounting',
        'crypto bookkeeping', 'crypto payroll', 'crypto merchant',
    ],
    'san-diego': [
        'san diego', 'north county', 'chula vista', 'la mesa',
        'el cajon', 'escondido', 'oceanside', 'carlsbad', 'encinitas',
        'national city', 'santee', 'lemon grove', 'poway',
    ],
}

def classify_topic(topic):
    """
    Returns dict:
      {
        'categories': list[str],   # e.g. ['ai-automation', 'san-diego']
        'industry':   str|None,    # e.g. 'plumbers'
      }
    """
    t = topic.lower()
    cats = [cat for cat, kws in CATEGORIES.items() if any(kw in t for kw in kws)]
    if not cats:
        cats = ['ai-automation']   # safe default
    return {
        'categories': cats,
        'industry': extract_industry(topic),
    }

# ── Pillar mapping ────────────────────────────────────────────────────────────

PILLAR_MAP = {
    'ai-automation':  'pillars/ai-automation-master-guide.html',
    'payments':       'pillars/payments-master-guide.html',
    'crypto-solana':  'pillars/crypto-payments-master-guide.html',
    'san-diego':      'pillars/san-diego-operator-guide.html',
}

PILLAR_LABELS = {
    'ai-automation':  'AI Automation Master Guide',
    'payments':       'Payments Master Guide',
    'crypto-solana':  'Crypto Payments Master Guide',
    'san-diego':      'San Diego Operator Guide',
}

CATEGORY_HUB_PATH = {
    'ai-automation':  'hubs/category-ai-automation.html',
    'payments':       'hubs/category-payments.html',
    'crypto-solana':  'hubs/category-crypto-solana.html',
    'san-diego':      'hubs/category-san-diego.html',
}

CATEGORY_HUB_LABELS = {
    'ai-automation':  'AI Automation Hub',
    'payments':       'Payments Hub',
    'crypto-solana':  'Crypto & Solana Hub',
    'san-diego':      'San Diego Hub',
}

def industry_hub_path(industry_slug):
    return f"hubs/industry-{industry_slug}.html"

def industry_hub_label(industry_slug):
    return industry_slug.replace('-', ' ').title() + ' Hub'
