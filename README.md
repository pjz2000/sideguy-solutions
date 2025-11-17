# SideGuy Solutions Website

A static website featuring Phantom wallet integration and a stablecoin yield calculator. Built with vanilla HTML, CSS, and JavaScript, hosted on GitHub Pages.

🌐 **Live Site**: [www.sideguysolutions.com](https://www.sideguysolutions.com)

## Features

- 🔗 **Phantom Wallet Integration**: Connect your Solana wallet to view balance and auto-fill calculator
- 💰 **Yield Calculator**: Calculate stablecoin yields with daily compounding
- 🎨 **Cosmic Purple Theme**: Modern, responsive design
- 📱 **Mobile Responsive**: Works seamlessly on all devices

## Project Structure

```
/
├── index.html          # Main HTML file
├── styles.css          # All CSS styles
├── script.js           # JavaScript functionality (wallet + calculator)
├── CNAME              # Custom domain configuration (www.sideguysolutions.com)
├── README.md          # This file
└── .cursorrules       # Cursor IDE rules
```

## Technologies Used

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **Vanilla JavaScript**: No frameworks
- **Solana Web3.js**: Phantom wallet integration
- **GitHub Pages**: Static site hosting

## Local Development

### Prerequisites

- A modern web browser (Chrome, Firefox, Safari, Edge)
- [Phantom Wallet Extension](https://phantom.app/) (for testing wallet features)
- Git (for version control)

### Running Locally

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd sideguy-solutions
   ```

2. **Open the website**:
   - Option 1: Simply open `index.html` in your browser
   - Option 2: Use a local server:
     ```bash
     # Using Python 3
     python3 -m http.server 8000
     
     # Using Node.js (if you have http-server installed)
     npx http-server -p 8000
     
     # Then visit http://localhost:8000
     ```

3. **Test Phantom Wallet**:
   - Install [Phantom Wallet Extension](https://phantom.app/)
   - Click "Connect Phantom Wallet" button
   - Approve the connection
   - Your balance should appear automatically

## Deployment to GitHub Pages

This website is automatically deployed to GitHub Pages when you push changes to the `main` branch.

### Initial Setup (One-time)

1. **Create a GitHub repository** (if you haven't already):
   - Go to GitHub and create a new repository
   - Name it `sideguy-solutions` (or your preferred name)

2. **Initialize Git and push** (if starting fresh):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/sideguy-solutions.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Click **Settings** → **Pages**
   - Under **Source**, select **Deploy from a branch**
   - Select **main** branch and **/ (root)** folder
   - Click **Save**
   - Your site will be available at `https://YOUR_USERNAME.github.io/sideguy-solutions/`

4. **Set up Custom Domain** (already configured):
   - The `CNAME` file is already in the repository
   - In GitHub Settings → Pages, add your custom domain: `www.sideguysolutions.com`
   - Update your DNS records to point to GitHub Pages (see DNS Configuration below)

### Deploying Changes

**Every time you make changes, follow these steps:**

1. **Make your changes** to `index.html`, `styles.css`, or `script.js`

2. **Test locally** (optional but recommended):
   - Open the site in your browser
   - Test wallet connection
   - Verify calculator works
   - Check mobile responsiveness

3. **Stage your changes**:
   ```bash
   git add .
   ```
   Or add specific files:
   ```bash
   git add index.html styles.css script.js
   ```

4. **Commit your changes**:
   ```bash
   git commit -m "Description of your changes"
   ```
   Examples:
   ```bash
   git commit -m "Update wallet connection UI"
   git commit -m "Fix calculator calculation bug"
   git commit -m "Improve mobile responsive design"
   ```

5. **Push to GitHub**:
   ```bash
   git push origin main
   ```

6. **Wait for deployment**:
   - GitHub Pages typically deploys within 1-2 minutes
   - You can check deployment status in: **Settings** → **Pages** → **Deployments**
   - Your changes will be live at `www.sideguysolutions.com`

### Quick Deploy Commands

```bash
# One-liner to add, commit, and push
git add . && git commit -m "Your commit message" && git push origin main
```

## DNS Configuration (Custom Domain)

If you need to set up or update the custom domain:

1. **In GitHub**:
   - Go to **Settings** → **Pages**
   - Under **Custom domain**, enter: `www.sideguysolutions.com`
   - Check **Enforce HTTPS** (recommended)

2. **In your DNS provider** (where you manage sideguysolutions.com):
   - Add a **CNAME record**:
     - **Name**: `www`
     - **Value**: `YOUR_USERNAME.github.io`
     - **TTL**: 3600 (or default)

   - Or add **A records** (if CNAME doesn't work):
     - Point to GitHub Pages IPs:
       - `185.199.108.153`
       - `185.199.109.153`
       - `185.199.110.153`
       - `185.199.111.153`

3. **Wait for DNS propagation** (can take up to 48 hours, usually much faster)

4. **Verify**: Visit `www.sideguysolutions.com` to confirm it's working

## Troubleshooting

### Website Not Updating After Push

- **Wait 1-2 minutes**: GitHub Pages needs time to build
- **Check deployment status**: Go to **Settings** → **Pages** → **Deployments**
- **Clear browser cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- **Check branch**: Ensure you pushed to `main` branch

### Phantom Wallet Not Connecting

- **Check extension**: Ensure Phantom wallet is installed and unlocked
- **Check browser console**: Open DevTools (F12) and look for errors
- **Verify Solana Web3.js**: Ensure the library is loading (check Network tab)
- **Try different browser**: Some browsers have better extension support

### Custom Domain Not Working

- **Check DNS records**: Verify CNAME or A records are correct
- **Wait for propagation**: DNS changes can take time
- **Check GitHub Settings**: Ensure custom domain is configured in Pages settings
- **Verify CNAME file**: Should contain `www.sideguysolutions.com`

### Calculator Not Working

- **Check browser console**: Look for JavaScript errors
- **Verify inputs**: Ensure all fields have valid numbers
- **Check wallet connection**: If using wallet balance, ensure wallet is connected

## File Descriptions

### `index.html`
Main HTML structure with:
- Header with wallet connection UI
- Yield calculator section
- Services section
- Footer

### `styles.css`
All styling including:
- Cosmic purple theme
- Responsive design
- Wallet button styles
- Calculator form styles

### `script.js`
JavaScript functionality:
- Phantom wallet connection/disconnection
- Balance loading from Solana network
- Yield calculation with daily compounding
- Auto-fill principal from wallet balance

### `CNAME`
Custom domain configuration file. **Do not delete this file!**

## Development Tips

1. **Test locally first**: Always test changes before pushing
2. **Use browser DevTools**: Check console for errors
3. **Test wallet features**: Requires Phantom extension
4. **Mobile testing**: Use browser DevTools device emulation
5. **Commit often**: Small, frequent commits are better than large ones

## Contributing

1. Make your changes
2. Test locally
3. Commit with descriptive messages
4. Push to main branch
5. Changes deploy automatically

## Support

For issues or questions:
- Check the troubleshooting section above
- Review browser console for errors
- Verify all files are committed and pushed

## License

© 2025 SideGuy Solutions. All rights reserved.

---

**Last Updated**: January 2025

f
