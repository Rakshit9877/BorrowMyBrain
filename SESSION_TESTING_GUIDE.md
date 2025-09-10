# 🚀 BorrowMyBrain Session Setup Guide - Complete AI Integration

## ✅ Current Status
Your session interface is now **FULLY FUNCTIONAL** with:
- Mock transcript pre-loaded ✅
- Working "Start Test Session" button ✅
- AI Summary generation (currently using mock data) ✅
- Session database storage ✅
- Video interface with Daily.co integration ✅

## 🎯 How to Test Right Now

1. **Go to your website**: http://127.0.0.1:8000
2. **Login**: Use username: `admin`, password: `admin123`
3. **Navigate to search page**: Click search or go to `/search/`
4. **Click "Start Test Session"** button (purple button at top)
5. **See the mock transcript** already loaded
6. **Click "Get AI Summary"** button to see AI-generated summary

## 🔧 Steps to Enable Real Gemini AI

### Step 1: Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (starts with `AIza...`)

### Step 2: Set Environment Variable
**Option A: Using .env file (Recommended)**
```bash
# Create .env file in your project root
cd /Users/rakshitjindal/Downloads/BorrowMyBrain
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Option B: Export in terminal**
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### Step 3: Update Django Settings
Add this to your `borrowmybrain/settings.py`:

```python
# Add at the top with other imports
from decouple import config

# Add at the bottom of settings.py
GEMINI_API_KEY = config('GEMINI_API_KEY', default=None)
```

### Step 4: Restart Server
```bash
python3 manage.py runserver
```

## 🧪 Testing Real AI Summary

1. After setting up Gemini API key and restarting
2. Go to session interface: `/session/start/`
3. Click "Get AI Summary" button
4. You should see a **real AI-generated summary** instead of mock data

## 🎥 Setting Up Real Video Calling (Optional)

### Daily.co API Setup
1. Go to [Daily.co](https://www.daily.co/) and create account
2. Get your API key from dashboard
3. Add to environment:
```bash
echo "DAILY_API_KEY=your_daily_api_key" >> .env
echo "DAILY_DOMAIN=your-domain.daily.co" >> .env
```

### Update settings.py:
```python
DAILY_API_KEY = config('DAILY_API_KEY', default=None)
DAILY_DOMAIN = config('DAILY_DOMAIN', default='test-domain.daily.co')
```

## 📁 Complete Environment Variables File (.env)
Create `/Users/rakshitjindal/Downloads/BorrowMyBrain/.env`:
```bash
# AI Services
GEMINI_API_KEY=your_gemini_api_key_here

# Video Calling (Optional)
DAILY_API_KEY=your_daily_api_key_here
DAILY_DOMAIN=your-domain.daily.co

# Database (Optional - for production)
DATABASE_URL=your_database_url

# Security (Optional - for production)
SECRET_KEY=your_secret_key_here
DEBUG=True
```

## 🔧 Troubleshooting

### If AI Summary Shows Mock Data:
1. ✅ Check if `.env` file exists and has `GEMINI_API_KEY`
2. ✅ Restart Django server after adding API key
3. ✅ Check browser console for any JavaScript errors
4. ✅ Verify API key is valid at Google AI Studio

### If "Start Test Session" Button Not Working:
1. ✅ Make sure you're logged in (admin/admin123)
2. ✅ Check browser console for errors
3. ✅ Verify server is running on http://127.0.0.1:8000

### If No Transcript Visible:
1. ✅ The mock transcript loads automatically
2. ✅ Check if JavaScript is enabled in browser
3. ✅ Look for any console errors

## 📊 Current Features Working

### ✅ Mock Mode (Current)
- Pre-loaded conversation transcript
- Mock AI summary generation
- Session interface with all buttons
- Database storage of sessions
- User notes functionality

### ✅ Production Mode (After API Setup)
- Real Gemini AI summary generation
- Intelligent content analysis
- Multiple language support (Hindi/English)
- Real Daily.co video calling
- Cloud recording capabilities

## 🎉 Quick Test Commands

```bash
# Test the session endpoint directly
curl -X GET http://127.0.0.1:8000/session/start/ -H "Cookie: sessionid=your_session_id"

# Test summary generation API
curl -X POST http://127.0.0.1:8000/api/generate-summary/ \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Test transcript", "session_id": 1}'
```

## 📝 Next Steps After Testing

1. **Test the basic functionality** ✅
2. **Set up Gemini API key** for real AI
3. **Optional**: Set up Daily.co for real video calls
4. **Optional**: Deploy to production server
5. **Optional**: Add more AI features (voice recognition, etc.)

## 🆘 Need Help?

If anything doesn't work:
1. Check the browser console (F12 → Console)
2. Check Django server logs in terminal
3. Verify all dependencies are installed
4. Make sure database migrations are applied

Your session interface is ready to test! 🎯
