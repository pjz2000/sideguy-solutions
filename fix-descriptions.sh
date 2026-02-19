#!/bin/bash
#
# Direct meta description replacer using sed
# Fixes pages with generic "Something breaks..." descriptions
#

echo "🔧 SideGuy Meta Description Fixer (sed-based)"
echo "============================================================"

count=0
fixed=0

for file in *.html; do
    # Skip templates and backups
    [[ "$file" =~ (template|backup|test|aaa-|index-) ]] && continue
    
    # Check if has generic description
    if grep -q "Something breaks. Something stops working" "$file" 2>/dev/null; then
        
        # Determine category and create appropriate description
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
        
        # Use sed to replace just the meta description content, preserving structure
        # This pattern matches the content value within the meta description tag
        sed -i.bak -E 's/(<meta name="description" content=")[^"]*(")/\1'"$desc"'\2/g' "$file"
        
        ((fixed++))
        
        # Show first 10
        if [[ $fixed -le 10 ]]; then
            echo "✅ $file"
            echo "   $desc"
            echo ""
        fi
    fi
    
    ((count++))
    
    # Progress indicator
    if [[ $((count % 100)) -eq 0 ]]; then
        echo "   ... processed $count files"
    fi
done

echo "============================================================"
echo "✅ Fixed: $fixed pages"
echo "📊 Total checked: $count pages"
echo ""
echo "🎉 Complete! Next: python3 generate-xml-sitemap.py"
