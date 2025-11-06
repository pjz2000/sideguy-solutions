document.addEventListener('DOMContentLoaded', () => {
  // Calc Yield Button
  const calcBtn = document.getElementById('calcBtn');
  const resultDiv = document.getElementById('result');
  const principal = document.getElementById('principal');
  const days = document.getElementById('days');
  const apy = document.getElementById('apy');

  // Live preview on input change (relevant addition for stickiness)
  const inputs = [principal, days, apy];
  inputs.forEach(input => input.addEventListener('input', () => {
    if (resultDiv.style.display === 'block') calcBtn.click(); // Re-calc on tweak
  }));

  calcBtn.addEventListener('click', () => {
    // Quick flash "Calculating..." then compute
    resultDiv.innerHTML = '<span style="color: #fff;">Calculating...</span>';
    resultDiv.style.display = 'block';
    setTimeout(() => { // 300ms delay for feel
      const p = parseFloat(principal.value) || 0;
      const d = parseFloat(days.value) || 0;
      const a = parseFloat(apy.value) / 100 || 0;

      if (p <= 0 || d <= 0 || a <= 0) {
        resultDiv.innerHTML = '<p style="color: #14F195;">Enter valid numbers for the drip, surfer.</p>'; // Fixed: Visible teal on gradient
        return;
      }

      // Daily compound: P * (1 + r/365)^days
      const dailyRate = a / 365;
      const yieldEst = p * (Math.pow(1 + dailyRate, d) - 1);
      const monthlyEst = p * (Math.pow(1 + dailyRate, 30) - 1); // Bonus: Monthly teaser

      resultDiv.innerHTML = `
        <p style="color: #000; font-size: 1.2em;">Est. Yield: $${yieldEst.toFixed(2)} (over ${d} days at ${apy.value}% APY)</p>
        <p style="color: #fff; opacity: 0.9;">Monthly Drip: ~$${monthlyEst.toFixed(2)} — Upgrade to $99/mo for auto-stakes.</p>
      `;
    }, 300);
  });

  // Email Form Submit (Lead Capture Alert + GA Event)
  const form = document.getElementById('dripSignup');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = form.querySelector('input[type="email"]').value;
    if (email) {
      alert(`Drip claimed for ${email}! Check inbox for Phantom setup + sim guide. (Zapier hook next.)`);
      console.log('Lead:', email);
      gtag('event', 'lead_submit', { 'email': email }); // GA event track
      form.reset();
    }
  });

  // Phantom Stub (Connect Button - Alert for Now)
  const connectBtn = document.getElementById('connectWallet');
  connectBtn.addEventListener('click', () => {
    alert('Phantom connected (sim)—Balance loaded: $1,000 USDC. Tweak principal for your stack!');
    document.getElementById('principal').value = 1000;
    document.getElementById('walletInputs').style.display = 'block';
    document.getElementById('balance').textContent = '$1,000 USDC';
    gtag('event', 'phantom_connect', { 'method': 'sim' }); // GA track
  });
});
