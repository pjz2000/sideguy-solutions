document.addEventListener('DOMContentLoaded', () => {
    let walletConnected = false;
    let publicKey = null;

    const calcYield = () => {
        const principalEl = document.getElementById('principal');
        const daysEl = document.getElementById('days');
        const apyEl = document.getElementById('apy');
        const resultEl = document.getElementById('result');

        const p = parseFloat(principalEl.value);
        const d = parseFloat(daysEl.value);
        const r = parseFloat(apyEl.value) / 100;

        if (isNaN(p) || p <= 0) {
            resultEl.innerHTML = '<em>Positive principal only—try $1000 for a Carlsbad coffee yield!</em>';
            return;
        }
        if (isNaN(d) || d <= 0) {
            resultEl.innerHTML = '<em>Days >0—compounds build over time, like Solana Beach waves.</em>';
            return;
        }
        if (isNaN(r) || r < 0 || r > 1) {
            resultEl.innerHTML = '<em>APY 0-100%—aim 5-12% for stablecoin stacks.</em>';
            return;
        }

        const yieldAmt = p * (Math.pow(1 + r / 365, d) - 1);
        const total = p + yieldAmt;
        resultEl.innerHTML = `Est. Yield: $${yieldAmt.toFixed(2)} (Total: $${total.toFixed(2)}) | <em>Yields fluctuate—book a consult for locked rates.</em>`;
    };

    const connectWallet = async () => {
        if (window.solana && window.solana.isPhantom) {
            try {
                const resp = await window.solana.connect();
                publicKey = resp.publicKey.toString();
                walletConnected = true;
                const statusEl = document.getElementById('status');
                if (statusEl) statusEl.textContent = `Connected: ${publicKey.slice(0,4)}...${publicKey.slice(-4)}`;
                document.getElementById('connectWallet').style.display = 'none';
                document.getElementById('disconnectWallet').style.display = 'inline-block';
                document.getElementById('walletInputs').style.display = 'block';
                loadBalance();
            } catch (err) {
                console.error('Connect failed:', err);
                alert('Canceled? No sweat—manual yields still slap.');
            }
        } else {
            alert('Phantom missing—snag it at phantom.app & reload.');
        }
    };

    const disconnectWallet = async () => {
        if (window.solana) await window.solana.disconnect();
        walletConnected = false;
        publicKey = null;
        const statusEl = document.getElementById('status');
        if (statusEl) statusEl.textContent = '';
        document.getElementById('connectWallet').style.display = 'inline-block';
        document.getElementById('disconnectWallet').style.display = 'none';
        document.getElementById('walletInputs').style.display = 'none';
        document.getElementById('balance').textContent = '';
        document.getElementById('principal').value = '1000';
        calcYield();
    };

    const loadBalance = async () => {
        if (!publicKey) return;
        try {
            const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'));
            const balance = await connection.getBalance(new solanaWeb3.PublicKey(publicKey));
            const solBalance = balance / solanaWeb3.LAMPORTS_PER_SOL;
            const balanceEl = document.getElementById('balance');
            if (balanceEl) {
                const usdEst = Math.round(solBalance * 150);
                balanceEl.innerHTML = `${solBalance.toFixed(4)} SOL (~$${usdEst}) <br><small>Bridge to USDC? Yields await.</small>`;
                document.getElementById('principal').value = usdEst || '1000';
            }
            calcYield();
        } catch (err) {
            console.error('Balance error:', err);
            document.getElementById('balance').textContent = 'Load failed—net check?';
        }
    };

    const connectBtn = document.getElementById('connectWallet');
    if (connectBtn) connectBtn.addEventListener('click', connectWallet);
    const disconnectBtn = document.getElementById('disconnectWallet');
    if (disconnectBtn) disconnectBtn.addEventListener('click', disconnectWallet);
    const calcBtn = document.getElementById('calcBtn');
    if (calcBtn) calcBtn.addEventListener('click', calcYield);

    ['principal', 'days', 'apy'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', calcYield);
    });

    // Listen for wallet connection events
    if (window.solana && window.solana.isPhantom) {
        // Handle wallet disconnect event
        window.solana.on('disconnect', () => {
            disconnectWallet();
        });
        
        // Check if already connected
        if (window.solana.isConnected && window.solana.publicKey) {
            publicKey = window.solana.publicKey.toString();
            walletConnected = true;
            const statusEl = document.getElementById('status');
            if (statusEl) statusEl.textContent = `Connected: ${publicKey.slice(0,4)}...${publicKey.slice(-4)}`;
            document.getElementById('connectWallet').style.display = 'none';
            document.getElementById('disconnectWallet').style.display = 'inline-block';
            document.getElementById('walletInputs').style.display = 'block';
            loadBalance();
        }
    }
});
