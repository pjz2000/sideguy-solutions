function calcYield() {
    const principal = parseFloat(document.getElementById('principal').value) || 0;
    const apy = parseFloat(document.getElementById('apy').value);
    const dailyRate = apy / 100 / 365;
    const dailyYield = principal * dailyRate;
    const resultEl = document.getElementById('result');
    if (principal > 0) {
        resultEl.innerHTML = `Est. Daily Yield: $${dailyYield.toFixed(2)} (at ${apy}% APY)`;
    } else {
        resultEl.innerHTML = 'Enter an amount to calculate.';
    }
}
