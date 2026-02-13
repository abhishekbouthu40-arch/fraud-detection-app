# Deploy Fraud Shield

## Prerequisites

1. **Install Git** (if needed): [git-scm.com/downloads](https://git-scm.com/downloads)

2. **Push your code to GitHub**
   - Create a new repo at [github.com/new](https://github.com/new)
   - Initialize git and push:

   ```powershell
   cd "c:\Users\abhis\OneDrive\Desktop\fraud_detection_app"
   git init
   git add .
   git commit -m "Initial commit - Fraud Shield app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

   Or use **GitHub Desktop** to add and push the folder.

2. **Sign up** (free) on [Render](https://render.com) or [Railway](https://railway.app)

---

## Option A: Deploy on Render

### Method 1: Blueprint (uses render.yaml)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. **New** → **Blueprint**
3. Connect your GitHub account and select the repo
4. Render reads `render.yaml` and configures the service
5. Click **Apply**
6. Wait for the build (dataset + training + deploy)
7. Your app URL: `https://fraud-detection-app.onrender.com` (or similar)

### Method 2: Manual Web Service

1. **New** → **Web Service**
2. Connect GitHub and select the repo
3. Configure:
   - **Name:** fraud-detection-app
   - **Region:** Oregon (or nearest)
   - **Build Command:**
     ```
     pip install -r requirements.txt && python data/generate_dataset.py && python train.py
     ```
   - **Start Command:**
     ```
     gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
     ```
4. Click **Create Web Service**

---

## Option B: Deploy on Railway

1. Go to [Railway](https://railway.app) and sign in with GitHub
2. **New Project** → **Deploy from GitHub repo**
3. Select your fraud_detection_app repo
4. Railway uses `nixpacks.toml` and `railway.json` for build/start
5. After deploy, click the service → **Settings** → **Generate Domain**
6. Your app URL: `https://your-app.up.railway.app`

---

## After Deployment

- Open your app URL in a browser
- Use the form to check transactions for fraud
- `/health` endpoint: `https://your-app-url/health`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails on scikit-learn | Ensure `requirements.txt` has `scikit-learn>=1.5.0` |
| Model not found | Build must run `python train.py` (included in build commands) |
| App sleeps (Render free tier) | First request may take 30–60 seconds to wake |
