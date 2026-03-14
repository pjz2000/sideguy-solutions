#!/usr/bin/env bash

PROJECT_ROOT="/workspaces/sideguy-solutions"
cd "$PROJECT_ROOT" || exit 1

mkdir -p public

cat > public/ai-native-development-platforms.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI-Native Development Platforms | SideGuy Solutions</title>
  <meta name="description" content="What AI-native development platforms and multiagent systems mean for businesses, builders, and operators.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/ai-native-development-platforms.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>AI-Native Development Platforms & Multiagent Systems</h1>
    <p>This is one of the biggest high-traffic technology themes in 2026. Businesses are moving from simple AI tools toward systems where multiple agents coordinate work, data, and decisions.</p>

    <h2>Why it matters</h2>
    <p>Search demand is moving beyond "what is AI" toward real implementation: orchestration, tools, workflows, deployment, security, oversight, and business use cases.</p>

    <h2>What SideGuy can cover at scale</h2>
    <ul>
      <li>what is a multiagent system</li>
      <li>ai-native development platform pricing</li>
      <li>multiagent workflows for small business</li>
      <li>best ai-native platforms for healthcare, legal, finance, and local services</li>
      <li>implementation guides by city, industry, and use case</li>
    </ul>

    <div style="margin-top:48px;padding:20px;border:1px solid #ddd;border-radius:18px;">
      <strong>Text PJ</strong>
      <p>Need calm help understanding whether this stuff is real, useful, or overkill?</p>
      <p><a href="sms:+17735441231">Text PJ: 773-544-1231</a></p>
    </div>
  </main>
</body>
</html>
HTML

cat > public/domain-specific-language-models.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Domain-Specific Language Models | SideGuy Solutions</title>
  <meta name="description" content="Industry-specific AI models explained for business owners and operators.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/domain-specific-language-models.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>Domain-Specific Language Models</h1>
    <p>The next search wave is not just general AI. It is AI tuned for specific industries, workflows, compliance needs, and operational contexts.</p>
    <p>This is perfect for SideGuy because it connects directly to vertical SEO clusters.</p>
  </main>
</body>
</html>
HTML

cat > public/physical-ai.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Physical AI | SideGuy Solutions</title>
  <meta name="description" content="Physical AI explained: robotics, hardware systems, automation, sensors, and real-world business applications.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/physical-ai.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>Physical AI</h1>
    <p>Physical AI combines AI with robots, sensors, equipment, vehicles, and hardware systems. It is a future infrastructure cluster, not a fad.</p>
  </main>
</body>
</html>
HTML

cat > public/preemptive-cybersecurity-ai-security-platforms.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Preemptive Cybersecurity & AI Security Platforms | SideGuy Solutions</title>
  <meta name="description" content="AI security and preemptive cybersecurity explained for business operators.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/preemptive-cybersecurity-ai-security-platforms.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>Preemptive Cybersecurity & AI Security Platforms</h1>
    <p>As AI systems expand, people search for prevention, monitoring, policy, and safety—not just cleanup after a breach.</p>
  </main>
</body>
</html>
HTML

cat > public/confidential-computing-data-provenance.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Confidential Computing & Data Provenance | SideGuy Solutions</title>
  <meta name="description" content="Privacy-first computing, attestation, and data provenance explained.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/confidential-computing-data-provenance.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>Confidential Computing & Data Provenance</h1>
    <p>Privacy, proof, attestation, trusted execution, and origin tracking are becoming major trust layers in AI and software infrastructure.</p>
  </main>
</body>
</html>
HTML

cat > public/ai-agents-answer-engine-traffic.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI Agents & Answer Engine Traffic | SideGuy Solutions</title>
  <meta name="description" content="How AI agents and answer engines are changing search traffic and SEO strategy.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://sideguysolutions.com/ai-agents-answer-engine-traffic.html">
</head>
<body>
  <main style="max-width:900px;margin:0 auto;padding:40px 20px;font-family:Inter,Arial,sans-serif;line-height:1.65;">
    <p><a href="/index.html">← Back to Home</a></p>
    <h1>AI Agents & Answer Engine Traffic</h1>
    <p>Search behavior is shifting. More queries are being mediated by agents and answer engines, which makes structured, specific, useful pages even more valuable.</p>
  </main>
</body>
</html>
HTML

echo "Hub pages built."
