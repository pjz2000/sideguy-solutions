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
    } // Phantom Integration - Add to script.js
let walletConnected = false;
let publicKey = null;

// Wait for DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Existing calcYield here...
    
    const connectWallet = async () => {
        if (window.solana && window.solana.isPhantom) {
            try {
                const resp = await window.solana.connect();
                publicKey = resp.publicKey.toString();
                walletConnected = true;
                document.getElementById('status') ? document.getElementById('status').textContent = `Connected: ${publicKey.slice(0,4)}...${publicKey.slice(-4)}` : console.log('Connected!');
                document.getElementById('connectWallet').style.display = 'none';
                if (document.getElementById('disconnectWallet')) document.getElementById('disconnectWallet').style.display = 'inline-block';
                loadBalance();
            } catch (err) {
                console.error('Phantom connect failed:', err);
                alert('Connect canceled—yields still await manual mode!');
            }
        } else {
            alert('Phantom not found—grab it at phantom.app and refresh.');
        }
    };

    const disconnectWallet = async () => {
        if (window.solana) await window.solana.disconnect();
        walletConnected = false;
        publicKey = null;
        document.getElementById('status') ? document.getElementById('status').textContent = '' : console.log('Disconnected');
        document.getElementById('connectWallet').style.display = 'inline-block';
        if (document.getElementById('disconnectWallet')) document.getElementById('disconnectWallet').style.display = 'none';
        // Reset balance display
        const balanceEl = document.getElementById('balance');
        if (balanceEl) balanceEl.textContent = '';
    };

    const loadBalance = async () => {
        if (!publicKey) return;
        try {
            // Need @solana/web3.js - add <script src="https://unpkg.com/@solana/web3.js@latest/lib/index.iife.min.js"></script> to index.html <head>
            const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'));
            const balance = await connection.getBalance(new solanaWeb3.PublicKey(publicKey));
            const solBalance = balance / solanaWeb3.LAMPORTS_PER_SOL;
            const balanceEl = document.getElementById('balance');
            if (balanceEl) {
                balanceEl.textContent = `${solBalance.toFixed(4)} SOL (~$${Math.round(solBalance * 150)} USD)`;
                // Auto-fill calc principal with USD equiv
                const principalInput = document.getElementById('principal');
                if (principalInput) principalInput.value = Math.round(solBalance * 150);
            }
        } catch (err) {
            console.error('Balance fetch failed:', err);
        }
    };

    // Tie to existing calcYield - enhance it to use wallet if connected
    const originalCalcYield = calcYield; // Backup your func
    calcYield = () => {
        originalCalcYield(); // Run yours
        if (walletConnected) loadBalance(); // Refresh on calc for fun
    };

    // Event hooks (add these IDs to your HTML)
    const connectBtn = document.getElementById('connectWallet');
    if (connectBtn) connectBtn.addEventListener('click', connectWallet);
    const disconnectBtn = document.getElementById('disconnectWallet');
    if (disconnectBtn) disconnectBtn.addEventListener('click', disconnectWallet);

    // Auto-detect on load
    if (window.solana && window.solana.isPhantom) {
        // window.solana.connect({ onlyIfTrusted: true }); // Uncomment for seamless reconnect
    }
});}
