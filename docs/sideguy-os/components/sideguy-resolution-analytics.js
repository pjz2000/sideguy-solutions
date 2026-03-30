(function () {
  function detectTopic(text) {
    const lower = (text || '').toLowerCase();
    if (/hvac|mini split|repair|replace|electrical|solar|battery|roof|plumbing/.test(lower)) return "home";
    if (/payment|payments|fees|subscription|pricing|processor|stripe|square|usdc|stablecoin/.test(lower)) return "money";
    if (/ai|automation|agent|workflow|gpt|claude|llm/.test(lower)) return "ai";
    if (/move|moving|relocation|san diego|rent|apartment|lifestyle/.test(lower)) return "life";
    if (/voice|robotics|future|prediction market|kalshi|signal/.test(lower)) return "future";
    return "general";
  }

  function trackBeefExposure() {
    const topic = detectTopic(document.body.innerText || '');
    const page = window.location.pathname;
    const record = {
      t: new Date().toISOString(),
      type: "exposure",
      topic,
      page
    };

    try {
      const existing = JSON.parse(localStorage.getItem("sg_resolution_analytics") || "[]");
      existing.push(record);
      localStorage.setItem("sg_resolution_analytics", JSON.stringify(existing));
    } catch(e) {}
  }

  function attachEscalationTracking() {
    const blocks = document.querySelectorAll(".sideguy-beef-block");
    blocks.forEach(block => {
      block.addEventListener("click", function () {
        const topic = detectTopic(document.body.innerText || '');
        const page = window.location.pathname;
        const record = {
          t: new Date().toISOString(),
          type: "escalation_click",
          topic,
          page
        };

        try {
          const existing = JSON.parse(localStorage.getItem("sg_resolution_analytics") || "[]");
          existing.push(record);
          localStorage.setItem("sg_resolution_analytics", JSON.stringify(existing));
        } catch(e) {}
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    trackBeefExposure();
    attachEscalationTracking();
  });
})();
