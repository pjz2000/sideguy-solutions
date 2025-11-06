# Quick Deployment Guide

## 🚀 Deploy Changes to GitHub Pages

### Standard Workflow (3 Steps)

```bash
# 1. Stage all changes
git add .

# 2. Commit with a message
git commit -m "Your descriptive message here"

# 3. Push to main branch
git push origin main
```

**That's it!** Your changes will be live in 1-2 minutes at `www.sideguysolutions.com`

---

## 📝 Common Commands

### Check Status
```bash
git status
```

### See What Changed
```bash
git diff
```

### Add Specific Files
```bash
git add index.html styles.css script.js
```

### One-Liner Deploy
```bash
git add . && git commit -m "Update website" && git push origin main
```

---

## ⚠️ Important Notes

- ✅ Always push to `main` branch (GitHub Pages uses this)
- ✅ Don't delete the `CNAME` file (breaks custom domain)
- ✅ Test locally before pushing
- ✅ Wait 1-2 minutes after pushing for deployment

---

## 🔍 Verify Deployment

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Check **Deployments** section for latest build status
4. Visit `www.sideguysolutions.com` to see changes

---

## 🐛 If Deployment Fails

1. Check GitHub Actions tab for errors
2. Verify all files are committed
3. Ensure you're on `main` branch: `git branch`
4. Try pushing again: `git push origin main`

---

For detailed documentation, see [README.md](./README.md)

