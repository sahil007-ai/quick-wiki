# 🧪 Testing Guide

## Local Testing

### 1. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create `.env` file:
```
OPENROUTER_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

### 3. Run FastAPI Server
```bash
uvicorn main:app --reload
```

Server starts at: **http://localhost:8000**

### 4. Test Endpoints

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

**Research Request:**
```bash
curl -X POST http://localhost:8000/api/research \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Impact of artificial intelligence on education",
    "max_analysts": 3
  }'
```

**Or use Thunder Client / Postman:**
- Method: POST
- URL: `http://localhost:8000/api/research`
- Body (JSON):
```json
{
  "topic": "Impact of AI on education",
  "max_analysts": 3
}
```

### 5. View API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Expected Response

```json
{
  "final_report": "# Title\n\n## Introduction\n\n...",
  "analysts": [
    {
      "name": "Dr. Sarah Chen",
      "role": "Education Technology Researcher", 
      "affiliation": "Stanford Graduate School of Education"
    }
  ],
  "status": "completed"
}
```

---

## Troubleshooting

**Error: "OpenRouter API key not configured"**
- Make sure `.env` file exists with `OPENROUTER_API_KEY`

**Error: "Module 'research_assistant' not found"**
- Make sure `research_assistant.py` is in the same directory as `main.py`

**Slow Response (1-3 minutes)**
- This is normal! Multi-agent research takes time
- Each analyst conducts interviews and gathers sources

---

## Next: Deploy to Railway

Once local testing works:
1. Push to GitHub: `git push origin main`
2. Deploy to Railway (I'll do this)
3. Test production URL
4. Integrate with frontend!
