#!/bin/bash
#
# Universal meta description fixer
# Handles both attribute orders: name/content and content/name
#

echo "🔧 Universal Meta Description Fixer"
echo "============================================================"

fixed=0
checked=0

for file in *.html; do
    # Skip templates and backups
    [[ "$file" =~ (template|backup|test|aaa-|index-) ]] && continue
    
    # Check if has generic description (any format)
    if grep -iq "Something breaks. Something stops working" "$file"; then
        
        # Determine description based on filename
        if [[ "$file" =~ "hvac" || "$file" =~ "ac-" || "$file" =~ "heater" ]]; then
            desc="HVAC help in San Diego. Clear options before calling. Understand the problem first."
        elif [[ "$file" =~ "plumb" || "$file" =~ "leak" || "$file" =~ "drain" || "$file" =~ "pipe" ]]; then
            desc="Plumbing help in San Diego. What to check first, when to call, what it costs."
        elif [[ "$file" =~ "electric" || "$file" =~ "outlet" || "$file" =~ "breaker" || "$file" =~ "light" ]]; then
            desc="Electrical help in San Diego. Safety-first guidance before calling an electrician."
        elif [[ "$file" =~ "payment" || "$file" =~ "merchant" ]]; then
            desc="Lower fees, instant settlements, human support. Payment processing for San Diego businesses."
        elif [[ "$file" =~ "roof" ]]; then
            desc="Roofing help in San Diego. When to repair vs replace, cost guidance, who to call."
        elif [[ "$file" =~ "foundation" ]]; then
            desc="Foundation repair guidance in San Diego. What to look for, when it's urgent, costs."
        elif [[ "$file" =~ "ai" || "$file" =~ "automat" ]]; then
            desc="AI and automation help for San Diego businesses. Human-first implementation. No hype."
        elif [[ "$file" =~ "crypto" || "$file" =~ "solana" ]]; then
            desc="Crypto payment setup for San Diego businesses. Solana Pay integration, wallet setup."
        elif [[ "$file" =~ "tech" || "$file" =~ "computer" ]]; then
            desc="Patient tech support for San Diego. No judgment, clear explanations. Help for everyone."
        elif [[ "$file" =~ "who-do-i-call" ]]; then
            topic=$(echo "$file" | sed 's/who-do-i-call-for-//; s/.html//; s/-/ /g')
            desc="Get clear guidance on $topic in San Diego. Human help when needed."
        else
            topic=$(echo "$file" | sed 's/.html//; s/-/ /g')
            desc="Get help with $topic in San Diego. Clear guidance, human support when needed."
        fi
        
        # Try both possible attribute orders
        # Pattern 1: name="description" content="..."
        sed -i.bak2 -E 's/(<meta[^>]*name="description"[^>]*content=")[^"]*(")/\1'"$desc"'\2/g' "$file"
        
        # Pattern 2: content="..." name="description"  
        sed -i.bak3 -E 's/(<meta[^>]*content=")[^"]*("[^>]*name="description")/\1'"$desc"'\2/g' "$file"
        
        ((fixed++))
        
        if [[ $fixed -le 10 ]]; then
            echo "✅ $file"
            echo "   $desc"
            echo ""
        fi
    fi
    
    ((checked++))
    if [[ $((checked % 100)) -eq 0 ]]; then
        echo "   ... checked $checked files"
    fi
done

# Clean up backup files
rm -f *.bak2 *.bak3

echo "============================================================"
echo "✅ Fixed: $fixed pages"
echo "📊 Total checked: $checked pages"
echo ""
echo "🎉 Done! Next: python3 metadata-audit.py to verify"
