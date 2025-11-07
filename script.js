document.addEventListener('DOMContentLoaded', () => {
    // Calc Yield Button
    const calcBtn = document.getElementById('calcBtn');
    const resultDiv = document.getElementById('result');
    const principal = document.getElementById('principal');
    const days = document.getElementById('days');
    const apy = document.getElementById('apy');

    // Live preview on input change
    const inputs = [principal, days, apy];
    inputs.forEach(input => {
        if (input) {
            input.addEventListener('input', () => {
                if (resultDiv && resultDiv.style.display === 'block') {
                    calcBtn.click();
                }
            });
        }
    });

    if (calcBtn && resultDiv) {
        calcBtn.addEventListener('click', () => {
            resultDiv.innerHTML = '<span style="color: #fff;">Calculating...</span>';
            resultDiv.style.display = 'block';
            setTimeout(() => {
                const p = parseFloat(principal.value) || 0;
                const d = parseFloat(days.value) || 0;
                const a = parseFloat(apy.value) / 100 || 0;

                if (p <= 0 || d <= 0 || a <= 0) {
                    resultDiv.innerHTML = '<p style="color: #14F195;">Enter valid numbers for the drip, surfer.</p>';
                    return;
                }

                const dailyRate = a / 365;
                const yieldEst = p * (Math.pow(1 + dailyRate, d) - 1);
                const monthlyEst = p * (Math.pow(1 + dailyRate, 30) - 1);

                resultDiv.innerHTML = `
                    <p style="color: #000; font-size: 1.2em;">Est. Yield: $${yieldEst.toFixed(2)} (over ${d} days at ${apy.value}% APY)</p>
                    <p style="color: #fff; opacity: 0.9;">Monthly Drip: ~$${monthlyEst.toFixed(2)} — Upgrade to $99/mo for auto-stakes.</p>
                `;
            }, 300);
        });
    }

    // Email Form Submit
    const form = document.getElementById('dripSignup');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = form.querySelector('input[type="email"]').value;
            if (email) {
                alert(`Drip claimed for ${email}! Check inbox for Phantom setup + sim guide.`);
                console.log('Lead:', email);
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'lead_submit', { 'email': email });
                }
                form.reset();
            }
        });
    }

    // Phantom Wallet Connection
    const connectBtn = document.getElementById('connectWallet');
    const disconnectBtn = document.getElementById('disconnectWallet');
    const walletInputs = document.getElementById('walletInputs');
    const balance = document.getElementById('balance');
    const status = document.getElementById('status');

    // Check if real Phantom is available
    if (window.solana && window.solana.isPhantom) {
        // Real Phantom wallet integration
        let walletConnected = false;
        let publicKey = null;

        const connectWallet = async () => {
            try {
                const resp = await window.solana.connect();
                publicKey = resp.publicKey.toString();
                walletConnected = true;
                
                if (status) {
                    status.textContent = `Connected: ${publicKey.slice(0,4)}...${publicKey.slice(-4)}`;
                }
                
                if (connectBtn) connectBtn.style.display = 'none';
                if (disconnectBtn) disconnectBtn.style.display = 'inline-block';
                if (walletInputs) walletInputs.style.display = 'block';
                
                // Load balance
                if (typeof solanaWeb3 !== 'undefined') {
                    try {
                        const connection = new solanaWeb3.Connection(solanaWeb3.clusterApiUrl('mainnet-beta'), 'confirmed');
                        const balanceAmount = await connection.getBalance(new solanaWeb3.PublicKey(publicKey));
                        const solBalance = balanceAmount / solanaWeb3.LAMPORTS_PER_SOL;
                        const usdEst = Math.round(solBalance * 150);
                        
                        if (balance) {
                            balance.innerHTML = `${solBalance.toFixed(4)} SOL (~$${usdEst}) <br><small>Bridge to USDC? Yields await.</small>`;
                        }
                        if (principal) {
                            principal.value = usdEst || '1000';
                        }
                        if (calcBtn) calcBtn.click();
                    } catch (err) {
                        console.error('Balance error:', err);
                        if (balance) balance.textContent = 'Load failed—net check?';
                    }
                }
                
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'phantom_connect', { 'method': 'real' });
                }
            } catch (err) {
                console.error('Connect failed:', err);
                if (err.code === 4001) {
                    if (status) {
                        status.textContent = 'Connection canceled. Click to try again.';
                        status.style.color = '#ffc107';
                    }
                } else {
                    alert('Failed to connect wallet: ' + (err.message || 'Unknown error'));
                }
            }
        };

        const disconnectWallet = async () => {
            try {
                if (window.solana.isConnected) {
                    await window.solana.disconnect();
                }
            } catch (err) {
                console.error('Disconnect error:', err);
            }

            walletConnected = false;
            publicKey = null;

            if (status) status.textContent = '';
            if (connectBtn) {
                connectBtn.style.display = 'inline-block';
                connectBtn.disabled = false;
                connectBtn.textContent = 'Connect Phantom Wallet';
            }
            if (disconnectBtn) disconnectBtn.style.display = 'none';
            if (walletInputs) walletInputs.style.display = 'none';
            if (balance) balance.textContent = '';
            if (principal) {
                principal.value = '1000';
                if (calcBtn) calcBtn.click();
            }
        };

        if (connectBtn) {
            connectBtn.addEventListener('click', connectWallet);
        }
        if (disconnectBtn) {
            disconnectBtn.addEventListener('click', disconnectWallet);
        }

        // Handle wallet events
        window.solana.on('disconnect', () => {
            disconnectWallet();
        });

        window.solana.on('accountChanged', (publicKey) => {
            if (publicKey) {
                connectWallet();
            } else {
                disconnectWallet();
            }
        });

        // Check if already connected
        if (window.solana.isConnected && window.solana.publicKey) {
            connectWallet();
        }
    } else {
        // Phantom Stub (simulation mode)
        if (connectBtn) {
            connectBtn.addEventListener('click', () => {
                alert('Phantom connected (sim)—Balance loaded: $1,000 USDC. Tweak principal for your stack!');
                if (principal) principal.value = 1000;
                if (walletInputs) walletInputs.style.display = 'block';
                if (balance) balance.textContent = '$1,000 USDC';
                if (connectBtn) connectBtn.style.display = 'none';
                if (disconnectBtn) disconnectBtn.style.display = 'inline-block';
                if (status) status.textContent = 'Connected (simulation mode)';
                if (calcBtn) calcBtn.click();
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'phantom_connect', { 'method': 'sim' });
                }
            });
        }
        
        if (disconnectBtn) {
            disconnectBtn.addEventListener('click', () => {
                if (connectBtn) connectBtn.style.display = 'inline-block';
                if (disconnectBtn) disconnectBtn.style.display = 'none';
                if (walletInputs) walletInputs.style.display = 'none';
                if (balance) balance.textContent = '';
                if (principal) principal.value = '1000';
                if (status) status.textContent = '';
                if (calcBtn) calcBtn.click();
            });
        }
    }

    // Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
            });
        });
    }
});
