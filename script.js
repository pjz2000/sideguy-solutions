document.addEventListener('DOMContentLoaded', () => {
    let walletConnected = false;
    let publicKey = null;

    // Your Original calcYield - Enhanced
    const calcYield = () => {
        const principalEl = document.getElementById('principal');
        const daysEl = document.getElementById('days');
        const apyEl = document.getElementById('apy');
        const resultEl = document.getElementById('result');

        const p = parseFloat(principalEl.value);
        const d = parseFloat(daysEl.value);
        const r = parseFloat(apyEl.value) / 100;

        if (isNaN(p) || p <= 0) {
            resultEl.innerHTML = '<em>Enter a positive principal—start small, stack big!</em>';
            return;
        }
        if (isNaN(d) || d <= 0) {
            resultEl.innerHTML = '<em>Days must be positive—yields compound over time.</em>';
            return;
        }
        if (isNaN(r) || r < 0 || r > 1) {
            resultEl.innerHTML = '<em>APY 0-100%—5-12% is NCSD sweet spot.</em>';
            return;
        }

        const yieldAmt = p * (Math.pow(1 + r / 365, d) - 1);
        const total = p + yieldAmt;
        resultEl.innerHTML = `Est. Yield: $${yieldAmt.toFixed(2)} (Total: $${total.toFixed(2)}) | <em>Yields vary—consult for live rates & setups.</em>`;
    };

    // Phantom Connect
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
                loadBalance();
            } catch (err) {
                console.error('Phantom connect failed:', err);
                alert('Connect canceled—manual mode still rocks!');
            }
        } else {
            alert('Phantom not detected—install from phantom.app & refresh.');
        }
    };

    // Disconnect
    const disconnectWallet = async () => {
        if (window.solana) await window.solana.disconnect();
        walletConnected = false;
        publicKey = null;
        const statusEl = document.getElementById('status');
        if (statusEl) statusEl.textContent = '';
        document.getElementById('connectWallet').style.display = 'inline-block';
        document.getElementById('disconnectWallet').style.display = 'none';
        document.getElementById('balance').textContent = '';
        // Reset principal to default
        document.getElementById('principal').value = '1000';
    };

    // Load Balance & Auto-Fill
    const loadBalance = async () => {
        if (!publicKey) return;
        try {
            const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'));
            const balance = await connection.getBalance(new solanaWeb3.PublicKey(publicKey));
            const solBalance = balance / solanaWeb3.LAMPORTS_PER_SOL;
            const balanceEl = document.getElementById('balance');
            if (balanceEl) {
                const usdEst = Math.round(solBalance * 150); // Rough SOL price
                balanceEl.innerHTML = `${solBalance.toFixed(4)} SOL (~$${usdEst} USD) <br><small>Bridge to USDC for yields?</small>`;
                document.getElementById('principal').value = usdEst;
            }
            calcYield(); // Auto-recalc on balance load
        } catch (err) {
            console.error('Balance fetch failed:', err);
            document.getElementById('balance').textContent = 'Fetch error—check net.';
        }
    };

    // Event Listeners
    document.getElementById('connectWallet').addEventListener('click', connectWallet);
    document.getElementById('disconnectWallet').addEventListener('click', disconnectWallet);
    // Calc button (your original)
    document.querySelector('button[onclick="calcYield()"]').addEventListener('click', calcYield);
    // Live update on input change
    ['principal', 'days', 'apy'].forEach(id => {
        document.getElementById(id).addEventListener('input', calcYield);
    });

    // Auto-detect Phantom on load
    if (window.solana && window.solana.isPhantom) {
        // Optional seamless reconnect: window.solana.connect({ onlyIfTrusted: true });
    }
});
