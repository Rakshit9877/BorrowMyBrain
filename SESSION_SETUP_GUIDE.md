# BorrowMyBrain Session Integration Setup Guide

## Prerequisites

### 1. Daily.co Account Setup
1. Go to [Daily.co](https://www.daily.co/) and create an account
2. Navigate to the Developer section in your dashboard
3. Create a new domain (e.g., `yourdomain.daily.co`)
4. Get your API key from the Developer section
5. Enable cloud recording in your domain settings

### 2. Google Cloud Setup
1. Create a Google Cloud Project at [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the following APIs:
   - Speech-to-Text API
   - Cloud Storage API
   - (Optional) Vertex AI API for advanced Gemini features

3. Create a Service Account:
   - Go to IAM & Admin > Service Accounts
   - Create a new service account with these roles:
     - Storage Admin
     - Speech-to-Text Editor
   - Generate and download a JSON key file

4. Create a Google Cloud Storage bucket:
   - Go to Cloud Storage > Buckets
   - Create a new bucket (note the name for settings)

### 3. Gemini AI API Setup
1. Go to [Google AI for Developers](https://ai.google.dev/)
2. Get your Gemini API key
3. (Alternative) Use Vertex AI for production deployments

### 4. System Requirements
- Python 3.8+
- FFmpeg installed on your system:
  - **macOS**: `brew install ffmpeg`
  - **Ubuntu**: `sudo apt update && sudo apt install ffmpeg`
  - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Environment Configuration

Create a `.env` file in your project root with the following variables:

```env
# Daily.co Configuration
DAILY_API_KEY=your_daily_api_key_here
DAILY_DOMAIN=yourdomain.daily.co

# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json
GCS_BUCKET_NAME=your-gcs-bucket-name

# Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Django Configuration
SECRET_KEY=your_django_secret_key
DEBUG=True
```

## Installation Steps

### 1. Install Python Dependencies
```bash
pip install -r requirements_session.txt
```

### 2. Update Django Settings
Add the following to your `settings.py`:

```python
from decouple import config
import os

# Session and AI Configuration
DAILY_API_KEY = config('DAILY_API_KEY', default='')
DAILY_DOMAIN = config('DAILY_DOMAIN', default='')
GCS_BUCKET_NAME = config('GCS_BUCKET_NAME', default='')
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')

# Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config('GOOGLE_APPLICATION_CREDENTIALS', default='')

# Media files configuration (if not already set)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 3. Database Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Collect Static Files
```bash
python manage.py collectstatic
```

## Testing the Integration

### 1. Start the Development Server
```bash
python manage.py runserver
```

### 2. Test the Session Interface
1. Navigate to your search results page: `http://localhost:8000/search/`
2. Click on "Start Test Session" button
3. Allow camera and microphone permissions
4. The video call interface should load with Daily.co integration

### 3. Test AI Summary Generation
1. In an active session, speak for a few minutes
2. Click "Get AI Summary" button
3. The system should:
   - Capture the live transcript
   - Send it to Gemini AI
   - Display the generated summary

## Features Included

### ✅ Video Calling
- **Daily.co Integration**: Professional video calling with cloud recording
- **Real-time Controls**: Mute/unmute, video on/off, screen sharing
- **Connection Status**: Visual indicators for connection state

### ✅ Live Transcription
- **Browser Speech Recognition**: Real-time transcription of conversations
- **Multi-language Support**: English and Hindi support
- **Visual Transcript**: Live display of conversation text

### ✅ AI-Powered Summaries
- **Gemini Integration**: Advanced AI summary generation
- **Hindi/English Support**: Summaries in preferred language
- **Structured Output**: Key points, learning outcomes, action items

### ✅ Session Management
- **Database Storage**: All sessions, recordings, and summaries saved
- **User Notes**: Take and save personal notes during sessions
- **Session History**: Track all past learning sessions

### ✅ Cloud Recording Processing
- **Automatic Recording**: Daily.co cloud recording
- **Audio Extraction**: Server-side audio processing with FFmpeg
- **Google Speech-to-Text**: Professional transcription service
- **Cloud Storage**: Secure storage in Google Cloud Storage

## API Endpoints

### POST `/api/generate-summary/`
Generate AI summary from live transcript
```json
{
  "transcript": "conversation text...",
  "session_id": "session_id",
  "room_name": "room_name"
}
```

### POST `/api/process-recording/`
Process Daily recording for transcription and summary
```json
{
  "room_name": "room_name",
  "session_id": "session_id"
}
```

### POST `/api/save-session-notes/`
Save user notes during session
```json
{
  "session_id": "session_id",
  "notes": "user notes text..."
}
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Install FFmpeg using system package manager
   - Ensure it's in your system PATH

2. **Google Cloud permissions**
   - Check service account has correct roles
   - Verify GOOGLE_APPLICATION_CREDENTIALS path

3. **Daily.co connection issues**
   - Verify API key is correct
   - Check domain configuration
   - Ensure cloud recording is enabled

4. **Browser permissions**
   - Allow camera and microphone access
   - Use HTTPS in production (required for media access)

### Debug Mode
Enable additional logging in `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'session_debug.log',
        },
    },
    'loggers': {
        'skills.session_views': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Production Deployment

### Security Considerations
1. Use HTTPS for all media access
2. Implement proper authentication for API endpoints
3. Add rate limiting for AI API calls
4. Use environment variables for all secrets

### Performance Optimization
1. Use webhooks instead of polling for Daily recordings
2. Implement asynchronous processing for transcription
3. Add Redis for caching AI responses
4. Use CDN for static files

### Cost Management
1. Monitor Google Cloud usage
2. Set up billing alerts
3. Implement usage quotas
4. Consider regional deployment for lower latency

## Next Steps

1. **Enhanced UI**: Improve the session interface design
2. **Real-time Collaboration**: Add shared whiteboards and documents
3. **Advanced AI**: Implement conversation analysis and learning insights
4. **Mobile App**: Create native mobile applications
5. **Integration**: Add calendar scheduling and payment processing

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation for Daily.co and Google Cloud
3. Test with minimal configurations first
4. Enable debug logging for detailed error information
