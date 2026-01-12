const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const axe = require('axe-core');

const files = [
  'what-changed-in-last-12-months.html',
  'payments-savings/what-changed-payments-last-12-months.html',
  'longtail/how-to-switch-payment-providers-without-downtime.html',
  'longtail/how-to-audit-your-processor-in-30-minutes.html',
  'longtail/understanding-interchange-fees-for-small-business.html',
  'longtail/when-to-use-on-chain-settlements-for-payments.html',
  'longtail/payment-retry-strategies-for-subscriptions.html',
  'longtail/how-to-handle-chargebacks-efficiently.html',
  'longtail/payment-processing-for-marketplaces.html',
  'longtail/how-to-implement-instant-payouts.html',
  'longtail/ai-for-local-marketing-small-business.html',
  'longtail/ai-cost-estimation-for-small-businesses.html',

  // NEW — North County pilot pages
  'longtail/encinitas-who-to-call-under-sink-leak.html',
  'longtail/solana-beach-how-to-apply-for-sdgande-rebates.html',
  'longtail/cardiff-how-to-lower-electric-bill-small-business.html',
  'longtail/leucadia-ai-for-local-marketing.html',
  'longtail/san-diego-how-to-switch-payment-providers-without-downtime.html',
  'longtail/encinitas-what-to-do-if-your-processor-raises-fees.html',
  'longtail/solana-beach-ac-freezing-up.html',
  'longtail/cardiff-how-to-prepare-for-a-payment-audit.html',
  'longtail/leucadia-how-to-find-a-local-licensed-contractor.html',

  // Batch 1 (priorities 11-20)
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

  // New pilot page
  'longtail/san-diego-payment-processing-for-marketplaces.html',

  // Batch 2 (priorities 21-30)
  'longtail/solana-beach-how-to-implement-subscription-billing.html',
  'longtail/cardiff-how-to-estimate-ai-project-costs.html',
  'longtail/encinitas-optimize-local-seo.html',
  'longtail/leucadia-when-to-use-on-chain-settlements.html',
  'longtail/san-diego-how-to-handle-chargebacks-for-subscriptions.html',
  'longtail/solana-beach-choose-local-hvac-service.html',
  'longtail/cardiff-audit-online-ordering-flow.html',
  'longtail/encinitas-when-to-replace-your-roof.html',
  'longtail/leucadia-how-to-use-utm-tracking.html',
  'longtail/san-diego-key-questions-before-signing-payment-contract.html'
];

(async function(){
  let summary = [];
  for(const f of files){
    const p = path.resolve(f);
    if(!fs.existsSync(p)){
      console.warn('MISSING:', f);
      continue;
    }
    const html = fs.readFileSync(p,'utf8');
    const dom = new JSDOM(html, { url: 'http://localhost/' });
    try{
      // Provide global window/document for axe when using jsdom
      // Provide a broad set of globals for axe to work with jsdom
      global.window = dom.window;
      global.document = dom.window.document;
      global.Node = dom.window.Node;
      global.Element = dom.window.Element;
      global.HTMLElement = dom.window.HTMLElement;
      global.HTMLDocument = dom.window.HTMLDocument || dom.window.Document;
      global.navigator = dom.window.navigator;
      global.getComputedStyle = dom.window.getComputedStyle;
      global.requestAnimationFrame = dom.window.requestAnimationFrame;

      const results = await new Promise((resolve, reject) => {
        axe.run(global.document, { runOnly: {type:'tag', values:['wcag2a','wcag2aa']} }, (err, res) => err ? reject(err) : resolve(res));
      });

      // Cleanup globals we set
      delete global.window;
      delete global.document;
      delete global.Node;
      delete global.Element;
      delete global.HTMLElement;
      delete global.HTMLDocument;
      delete global.navigator;
      delete global.getComputedStyle;
      delete global.requestAnimationFrame;
      const violations = results.violations || [];
      summary.push({file:f, count:violations.length, violations});
      console.log('\n==', f, '— violations:', violations.length);
      for(const v of violations){
        console.log('-', v.id, `(${v.impact})`, '-', v.help);
        // print a sample node
        if(v.nodes && v.nodes[0]){
          console.log('  sample target:', v.nodes[0].target.join(', '));
          console.log('  message:', v.nodes[0].failureSummary.replace(/\n/g,' '));
        }
      }
    }catch(e){
      console.error('ERROR scanning', f, e && e.message);
    }
  }

  const total = summary.reduce((a,b)=>a+b.count,0);
  console.log('\nSUMMARY: scanned', summary.length, 'pages — total violations:', total);
  process.exit(0);
})();