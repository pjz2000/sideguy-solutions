document.addEventListener('DOMContentLoaded', () => {
    let walletConnected = false;
    let publicKey = null;

    // Wait for Solana Web3.js to load
    const waitForSolanaWeb3 = () => {
        return new Promise((resolve) => {
            if (typeof solanaWeb3 !== 'undefined') {
                resolve();
            } else {
                // Check every 100ms for the library
                const checkInterval = setInterval(() => {
                    if (typeof solanaWeb3 !== 'undefined') {
                        clearInterval(checkInterval);
                        resolve();
                    }
                }, 100);
                // Timeout after 5 seconds
                setTimeout(() => {
                    clearInterval(checkInterval);
                    console.warn('Solana Web3.js library not loaded');
                    resolve(); // Continue anyway
                }, 5000);
            }
        });
    };

    const calcYield = () => {
        const principalEl = document.getElementById('principal');
        const daysEl = document.getElementById('days');
        const apyEl = document.getElementById('apy');
        const resultEl = document.getElementById('result');

        if (!principalEl || !daysEl || !apyEl || !resultEl) return;

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
        // Check if Phantom is installed
        if (typeof window.solana === 'undefined') {
            alert('Phantom wallet not found. Please install Phantom from https://phantom.app/ and reload the page.');
            return;
        }

        if (!window.solana.isPhantom) {
            alert('Phantom wallet not detected. Please make sure Phantom extension is installed and enabled.');
            return;
        }

        try {
            // Disable button during connection
            const connectBtn = document.getElementById('connectWallet');
            if (connectBtn) {
                connectBtn.disabled = true;
                connectBtn.textContent = 'Connecting...';
            }

            const resp = await window.solana.connect();
            publicKey = resp.publicKey.toString();
            walletConnected = true;

            // Update UI
            const statusEl = document.getElementById('status');
            if (statusEl) {
                statusEl.textContent = `Connected: ${publicKey.slice(0,4)}...${publicKey.slice(-4)}`;
            }

            const connectWalletEl = document.getElementById('connectWallet');
            const disconnectWalletEl = document.getElementById('disconnectWallet');
            const walletInputsEl = document.getElementById('walletInputs');

            if (connectWalletEl) connectWalletEl.style.display = 'none';
            if (disconnectWalletEl) disconnectWalletEl.style.display = 'inline-block';
            if (walletInputsEl) walletInputsEl.style.display = 'block';

            // Load balance
            await loadBalance();
        } catch (err) {
            console.error('Connect failed:', err);
            
            // Re-enable button
            const connectBtn = document.getElementById('connectWallet');
            if (connectBtn) {
                connectBtn.disabled = false;
                connectBtn.textContent = 'Connect Phantom Wallet';
            }

            if (err.code === 4001) {
                // User rejected the request
                const statusEl = document.getElementById('status');
                if (statusEl) {
                    statusEl.textContent = 'Connection canceled. Click to try again.';
                    statusEl.style.color = '#ffc107';
                }
            } else {
                alert('Failed to connect wallet: ' + (err.message || 'Unknown error'));
            }
        }
    };

    const disconnectWallet = async () => {
        try {
            if (window.solana && window.solana.isConnected) {
                await window.solana.disconnect();
            }
        } catch (err) {
            console.error('Disconnect error:', err);
        }

        walletConnected = false;
        publicKey = null;

        const statusEl = document.getElementById('status');
        if (statusEl) {
            statusEl.textContent = '';
        }

        const connectWalletEl = document.getElementById('connectWallet');
        const disconnectWalletEl = document.getElementById('disconnectWallet');
        const walletInputsEl = document.getElementById('walletInputs');
        const balanceEl = document.getElementById('balance');
        const principalEl = document.getElementById('principal');

        if (connectWalletEl) {
            connectWalletEl.style.display = 'inline-block';
            connectWalletEl.disabled = false;
            connectWalletEl.textContent = 'Connect Phantom Wallet';
        }
        if (disconnectWalletEl) disconnectWalletEl.style.display = 'none';
        if (walletInputsEl) walletInputsEl.style.display = 'none';
        if (balanceEl) balanceEl.textContent = '';
        if (principalEl) {
            principalEl.value = '1000';
            calcYield();
        }
    };

    const loadBalance = async () => {
        if (!publicKey) return;

        // Wait for Solana Web3.js library
        await waitForSolanaWeb3();

        if (typeof solanaWeb3 === 'undefined') {
            const balanceEl = document.getElementById('balance');
            if (balanceEl) {
                balanceEl.innerHTML = '<em>Library loading... Please refresh if this persists.</em>';
            }
            return;
        }

        try {
            const connection = new solanaWeb3.Connection(
                solanaWeb3.clusterApiUrl('mainnet-beta'),
                'confirmed'
            );
            const balance = await connection.getBalance(new solanaWeb3.PublicKey(publicKey));
            const solBalance = balance / solanaWeb3.LAMPORTS_PER_SOL;
            
            const balanceEl = document.getElementById('balance');
            if (balanceEl) {
                const usdEst = Math.round(solBalance * 150);
                balanceEl.innerHTML = `${solBalance.toFixed(4)} SOL (~$${usdEst}) <br><small>Bridge to USDC? Yields await.</small>`;
                
                const principalEl = document.getElementById('principal');
                if (principalEl) {
                    principalEl.value = usdEst || '1000';
                }
            }
            calcYield();
        } catch (err) {
            console.error('Balance error:', err);
            const balanceEl = document.getElementById('balance');
            if (balanceEl) {
                balanceEl.innerHTML = '<em>Failed to load balance. Check your connection.</em>';
            }
        }
    };

    // Initialize event listeners
    const connectBtn = document.getElementById('connectWallet');
    if (connectBtn) {
        connectBtn.addEventListener('click', connectWallet);
    }

    const disconnectBtn = document.getElementById('disconnectWallet');
    if (disconnectBtn) {
        disconnectBtn.addEventListener('click', disconnectWallet);
    }

    const calcBtn = document.getElementById('calcBtn');
    if (calcBtn) {
        calcBtn.addEventListener('click', calcYield);
    }

    // Auto-calculate on input change
    ['principal', 'days', 'apy'].forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('input', calcYield);
        }
    });

    // Initialize calculator
    calcYield();

    // Listen for wallet connection events
    if (window.solana && window.solana.isPhantom) {
        // Handle wallet disconnect event
        window.solana.on('disconnect', () => {
            disconnectWallet();
        });

        // Handle account change
        window.solana.on('accountChanged', (publicKey) => {
            if (publicKey) {
                // User switched accounts
                connectWallet();
            } else {
                // User disconnected
                disconnectWallet();
            }
        });
        
        // Check if already connected on page load
        if (window.solana.isConnected && window.solana.publicKey) {
            publicKey = window.solana.publicKey.toString();
            walletConnected = true;
            
            const statusEl = document.getElementById('status');
            if (statusEl) {
                statusEl.textContent = `Connected: ${publicKey.slice(0,4)}...${publicKey.slice(-4)}`;
            }

            const connectWalletEl = document.getElementById('connectWallet');
            const disconnectWalletEl = document.getElementById('disconnectWallet');
            const walletInputsEl = document.getElementById('walletInputs');

            if (connectWalletEl) connectWalletEl.style.display = 'none';
            if (disconnectWalletEl) disconnectWalletEl.style.display = 'inline-block';
            if (walletInputsEl) walletInputsEl.style.display = 'block';
            
            loadBalance();
        }
    } else {
        // Show helpful message if Phantom not detected
        const statusEl = document.getElementById('status');
        if (statusEl) {
            statusEl.innerHTML = '<small style="color: #ffc107;">Install <a href="https://phantom.app/" target="_blank" style="color: #9945FF;">Phantom Wallet</a> to connect</small>';
        }
    }
});
