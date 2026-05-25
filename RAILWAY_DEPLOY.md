# 🚂 Railway Deployment Guide

## Prerequisites
- GitHub account with `quick-wiki` repository
- Railway account (sign up at railway.app)
- API keys ready:
  - `OPENROUTER_API_KEY`
  - `TAVILY_API_KEY`

## Deployment Steps

### 1. Deploy to Railway

1. **Go to Railway**: https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. **Select**: `sahil007-ai/quick-wiki`
4. **Add Environment Variables**:
   - Click "Variables" tab
   - Add:
     - `OPENROUTER_API_KEY` = `your_key_here`
     - `TAVILY_API_KEY` = `your_key_here`

### 2. Get Production URL

After deployment completes (2-5 minutes):
1. Go to **Settings** → **Networking**
2. Click **Generate Domain**
3. Copy your URL: `https://quick-wiki-production-XXXX.up.railway.app`

### 3. Test the API

```bash
# Health check
curl https://your-app.up.railway.app/api/health

# Test research endpoint
curl -X POST https://your-app.up.railway.app/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "How does machine learning work?",
    "max_analysts": 2
  }'
```

## Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key for LLM access | `sk-or-v1-...` |
| `TAVILY_API_KEY` | Tavily API key for web search | `tvly-...` |

## Monitoring

- **Logs**: Railway Dashboard → Deployments → View Logs
- **Metrics**: Railway Dashboard → Metrics tab
- **Health Check**: `GET /api/health`

## Troubleshooting

### Deployment Fails
- Check logs in Railway dashboard
- Verify all dependencies in `requirements.txt`
- Ensure Python 3.10+ is being used

### API Returns 500 Error
- Check environment variables are set correctly
- Verify API keys are valid
- Check Railway logs for detailed error messages

### CORS Errors from Frontend
- Verify frontend domain is in `main.py` CORS settings
- Check browser console for specific CORS error

## Production URL
Once deployed, update this with your actual URL:
```
Production API: https://quick-wiki-production-XXXX.up.railway.app
```
