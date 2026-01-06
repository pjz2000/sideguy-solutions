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
  'longtail/ai-cost-estimation-for-small-businesses.html'
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