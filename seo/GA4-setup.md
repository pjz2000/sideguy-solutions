GA4 Setup for SideGuy Solutions

Goal: Add GA4 Measurement ID (G-XXXX) into the site template. We leave page_view disabled so teams can control when to send views.

Snippet to insert (replace G-MEASUREMENT_ID with your ID):

<script async src="https://www.googletagmanager.com/gtag/js?id=G-MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);} 
  gtag('js', new Date());
  gtag('config', 'G-MEASUREMENT_ID', { 'send_page_view': false });
</script>

Where to put it:
- Insert the snippet before the closing </body> in `template-v304.html` if you want site-wide analytics.
- If you prefer to only add analytics to long-tail pages, paste into `longtail/template.html` instead.

Notes:
- We attempted an automated insertion earlier but exact text matching failed in the template (whitespace/formatting mismatch). Manual paste is safe and quick.
- If you want, I can re-run the automated edit after you confirm where you'd like it (site-wide vs only long-tail) and provide the Measurement ID; or I can open a draft PR with the snippet placeholder commented out for you to replace the ID.
