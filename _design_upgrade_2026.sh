#!/usr/bin/env bash

########################################
# SIDEGUY DESIGN UPGRADE 2026
# Modern professional styling refresh
########################################

PROJECT_ROOT="/workspaces/sideguy-solutions"
DATE="$(date +"%Y-%m-%d-%H%M%S")"

cd "$PROJECT_ROOT" || exit 1

# Modern 2026 CSS template
MODERN_CSS='<style>
:root {
  /* Color System - Professional 2026 palette */
  --bg-base: #f8fafb;
  --bg-elevated: #ffffff;
  --bg-overlay: rgba(255, 255, 255, 0.92);
  
  --text-primary: #0a1828;
  --text-secondary: #475569;
  --text-tertiary: #64748b;
  
  --accent-primary: #0ea5e9;
  --accent-hover: #0284c7;
  --accent-light: #e0f2fe;
  
  --mint: #10b981;
  --mint-hover: #059669;
  --mint-light: #d1fae5;
  
  --border-subtle: rgba(148, 163, 184, 0.12);
  --border-medium: rgba(148, 163, 184, 0.24);
  
  /* Shadows - Elevated depth */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.06), 0 2px 4px -2px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.08);
  
  /* Spacing */
  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  
  /* Border radius */
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  
  /* Typography */
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, system-ui, sans-serif;
  --font-display: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, system-ui, sans-serif;
}

/* Base reset */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

body {
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.7;
  color: var(--text-primary);
  background: var(--bg-base);
  min-height: 100vh;
}

/* Modern gradient background */
body::before {
  content: "";
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 600px;
  background: 
    radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.08), transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(16, 185, 129, 0.08), transparent 50%),
    linear-gradient(to bottom, rgba(248, 250, 251, 0.8), rgba(248, 250, 251, 1));
  pointer-events: none;
  z-index: -1;
}

/* Container */
.container {
  max-width: 840px;
  margin: 0 auto;
  padding: var(--space-2xl) var(--space-lg);
}

@media (max-width: 768px) {
  .container {
    padding: var(--space-xl) var(--space-md);
  }
}

/* Typography */
h1 {
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 2.75rem);
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  margin-bottom: var(--space-lg);
}

h2 {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 3vw, 1.875rem);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--text-primary);
  margin-top: var(--space-2xl);
  margin-bottom: var(--space-md);
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.01em;
  color: var(--text-primary);
  margin-top: var(--space-xl);
  margin-bottom: var(--space-sm);
}

p {
  color: var(--text-secondary);
  margin-bottom: var(--space-md);
  max-width: 70ch;
}

strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* Lists */
ul, ol {
  margin: var(--space-lg) 0;
  padding-left: var(--space-xl);
  color: var(--text-secondary);
}

li {
  margin-bottom: var(--space-sm);
  line-height: 1.7;
}

li::marker {
  color: var(--accent-primary);
}

/* Links */
a {
  color: var(--accent-primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

a:hover {
  color: var(--accent-hover);
}

/* Cards & Sections */
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
}

/* Context boxes */
.context-box {
  background: var(--mint-light);
  border-left: 4px solid var(--mint);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  margin: var(--space-xl) 0;
}

.context-box p {
  color: var(--text-primary);
  margin: 0;
}

/* CTA Section - Hero style */
.cta-section {
  background: linear-gradient(135deg, var(--bg-elevated) 0%, var(--accent-light) 100%);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xl);
  padding: var(--space-2xl);
  margin: var(--space-2xl) 0;
  box-shadow: var(--shadow-lg);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.1), transparent 70%);
  pointer-events: none;
}

.cta-section h3 {
  margin-top: 0;
  font-size: 1.5rem;
}

.cta-section p {
  color: var(--text-secondary);
  margin-bottom: var(--space-lg);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  padding: var(--space-md) var(--space-xl);
  font-size: 1rem;
  font-weight: 600;
  line-height: 1;
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-family: var(--font-sans);
}

.btn-primary {
  background: var(--mint);
  color: white;
  box-shadow: var(--shadow-md);
}

.btn-primary:hover {
  background: var(--mint-hover);
  box-shadow: var(--shadow-lg);
  transform: translateY(-1px);
}

.btn-secondary {
  background: var(--bg-elevated);
  color: var(--text-primary);
  border: 1px solid var(--border-medium);
}

.btn-secondary:hover {
  background: var(--bg-base);
  border-color: var(--accent-primary);
}

/* Phone link specific */
.phone-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-md) var(--space-lg);
  background: var(--mint);
  color: white;
  font-size: 1.125rem;
  font-weight: 600;
  border-radius: var(--radius-md);
  text-decoration: none;
  box-shadow: var(--shadow-md);
  transition: all 0.2s ease;
}

.phone-link:hover {
  background: var(--mint-hover);
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
  color: white;
}

/* Back link */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-xs);
  color: var(--text-tertiary);
  font-size: 0.9rem;
  margin-top: var(--space-2xl);
  text-decoration: none;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: var(--accent-primary);
}

/* Divider */
hr {
  border: none;
  border-top: 1px solid var(--border-subtle);
  margin: var(--space-2xl) 0;
}

/* Grid layouts */
.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-lg);
  margin: var(--space-lg) 0;
}

.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: var(--space-md);
  margin: var(--space-lg) 0;
}

/* Feature boxes */
.feature-box {
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
  transition: all 0.3s ease;
}

.feature-box:hover {
  border-color: var(--accent-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.feature-box h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--space-xs);
}

.feature-box p {
  font-size: 0.9rem;
  color: var(--text-tertiary);
  margin: 0;
}

/* Meta info */
.meta {
  font-size: 0.875rem;
  color: var(--text-tertiary);
  margin-top: var(--space-xs);
}

/* Responsive utilities */
@media (max-width: 640px) {
  .grid-2,
  .grid-3 {
    grid-template-columns: 1fr;
  }
  
  .cta-section {
    padding: var(--space-xl);
  }
  
  .btn,
  .phone-link {
    width: 100%;
    justify-content: center;
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus states for accessibility */
*:focus-visible {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
</style>'

echo "$MODERN_CSS" > /tmp/modern_css_template.txt
echo "✅ Modern CSS template created"
echo "📋 Template saved to /tmp/modern_css_template.txt"
echo ""
echo "Next: Apply to specific pages or create new template pages"
