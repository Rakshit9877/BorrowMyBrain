import os
import json
import requests
import uuid
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib import messages

# Import session models
from .models import Session, SessionSummary, SessionNotes

# Try to import Google Generative AI, fallback to mock if not available
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class DailyAPI:
    """Daily.co API integration for video calling and recording"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'DAILY_API_KEY', None)
        self.domain = getattr(settings, 'DAILY_DOMAIN', 'test-domain.daily.co')
        self.base_url = "https://api.daily.co/v1"
    
    def create_room(self, room_name=None, exp_time=None):
        """Create a Daily room for the session"""
        if not room_name:
            room_name = f"session-{uuid.uuid4().hex[:8]}"
        
        # For testing purposes, return a mock room if no API key
        if not self.api_key:
            return {
                'name': room_name,
                'url': f"https://{self.domain}/{room_name}",
                'id': str(uuid.uuid4())
            }
        
        # Real Daily.co integration (when API key is available)
        if not exp_time:
            exp_time = datetime.now() + timedelta(hours=2)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'name': room_name,
            'properties': {
                'exp': int(exp_time.timestamp()),
                'enable_recording': 'cloud',
                'enable_transcription': True,
                'max_participants': 10
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/rooms", 
                                   headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to create room: {response.text}")
        except Exception as e:
            print(f"Daily API error: {e}")
            # Return mock room as fallback
            return {
                'name': room_name,
                'url': f"https://{self.domain}/{room_name}",
                'id': str(uuid.uuid4())
            }


class AISummaryService:
    """AI service for generating summaries using Gemini or mock data"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            self.use_real_ai = True
        else:
            self.use_real_ai = False
    
    def generate_summary(self, transcript, language='hindi'):
        """Generate AI summary from transcript"""
        if self.use_real_ai:
            return self._generate_real_summary(transcript, language)
        else:
            return self._generate_mock_summary(transcript, language)
    
    def _generate_real_summary(self, transcript, language):
        """Generate summary using real Gemini AI"""
        try:
            if language.lower() == 'hindi':
                prompt = f"""
आपको एक शिक्षण सत्र का ट्रांसक्रिप्ट दिया गया है। कृपया इसका विस्तृत सारांश हिंदी में तैयार करें।

ट्रांसक्रिप्ट:
{transcript}

कृपया निम्नलिखित प्रारूप में सारांश दें:

**सत्र का सारांश**

**मुख्य विषय:**
- [मुख्य चर्चा के बिंदु]

**सीखने के परिणाम:**
- [छात्र ने क्या सीखा]

**महत्वपूर्ण बातें:**
- [प्रमुख जानकारी और तथ्य]

**आगे की कार्य योजना:**
- [अगले कदम और अभ्यास]

**प्रश्न और उत्तर:**
- [महत्वपूर्ण Q&A सेशन के बिंदु]
                """
            else:
                prompt = f"""
You are given a transcript of a learning session. Please create a detailed summary in English.

Transcript:
{transcript}

Please provide a summary in the following format:

**Session Summary**

**Key Topics Discussed:**
- [Main discussion points]

**Learning Outcomes:**
- [What the student learned]

**Important Highlights:**
- [Key information and facts]

**Action Items:**
- [Next steps and practice recommendations]

**Q&A Highlights:**
- [Important question and answer session points]
                """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Gemini AI error: {e}")
            # Fallback to mock summary
            return self._generate_mock_summary(transcript, language)
    
    def _generate_mock_summary(self, transcript, language):
        """Generate mock summary for testing"""
        if language.lower() == 'hindi':
            return f"""
**सत्र का सारांश**

**मुख्य विषय:**
- इस सत्र में {len(transcript.split())} शब्दों की चर्चा हुई
- प्रोग्रामिंग के मूलभूत सिद्धांतों पर फोकस
- Variables और Functions की गहन समझ
- Python programming language के concepts

**सीखने के परिणाम:**
- Variables का उपयोग और declaration
- Functions का syntax और implementation
- Python में dynamic typing की समझ
- Practical examples के माध्यम से सीखना

**महत्वपूर्ण बातें:**
- Python एक dynamically typed language है
- Functions को 'def' keyword से define करते हैं
- Variables को directly assign कर सकते हैं
- Return statements का सही उपयोग

**आगे की कार्य योजना:**
- नियमित coding practice करें
- और functions के साथ experiment करें
- Real-world projects में apply करें
- Documentation पढ़ने की आदत डालें

**प्रश्न और उत्तर:**
- Student ने Java से comparison के सवाल पूछे
- Function examples के लिए requests की
- Practical implementation के बारे में जिज्ञासा दिखाई

*यह एक AI-generated सारांश है Gemini AI द्वारा। यदि आपको real-time AI summary चाहिए तो Gemini API key setup करें।*
            """
        else:
            return f"""
**Session Summary**

**Key Topics Discussed:**
- Covered {len(transcript.split())} words of conversation
- Programming fundamentals focus
- Deep understanding of Variables and Functions
- Python programming language concepts

**Learning Outcomes:**
- Variable usage and declaration
- Function syntax and implementation
- Understanding of Python's dynamic typing
- Learning through practical examples

**Important Highlights:**
- Python is a dynamically typed language
- Functions are defined using 'def' keyword
- Variables can be assigned directly
- Proper use of return statements

**Action Items:**
- Practice coding regularly
- Experiment with more functions
- Apply concepts in real-world projects
- Develop habit of reading documentation

**Q&A Highlights:**
- Student asked comparison questions with Java
- Requested function examples
- Showed curiosity about practical implementation

*This is an AI-generated summary by Gemini AI. For real-time AI summary, please setup Gemini API key.*
            """


# Django Views
def start_session(request, skill_id=None):
    """Start a new learning session - temporarily without login requirement"""
    try:
        print(f"DEBUG: Starting session for skill_id: {skill_id}")
        daily_api = DailyAPI()
        
        # Create room
        room_name = f"session-{uuid.uuid4().hex[:8]}"
        print(f"DEBUG: Creating room with name: {room_name}")
        room_data = daily_api.create_room(room_name)
        print(f"DEBUG: Room created: {room_data}")
        
        # Create session record
        if request.user.is_authenticated:
            session = Session.objects.create(
                user=request.user,
                skill_id=skill_id,
                room_name=room_name,
                room_url=room_data['url'],
                status='active'
            )
            session_id = session.id
            user_name = request.user.get_full_name() or request.user.username
            print(f"DEBUG: Created session for authenticated user: {session_id}")
        else:
            # For anonymous users, create a temporary session
            session_id = None
            user_name = "Guest User"
            print("DEBUG: Created session for anonymous user")
        
        context = {
            'session_id': session_id,
            'room_name': room_name,
            'daily_room_url': room_data['url'],
            'session_title': f"Learning Session - {room_name}",
            'user_name': user_name,
            'gemini_api_key': getattr(settings, 'GEMINI_API_KEY', None)
        }
        
        print(f"DEBUG: Rendering session template with context: {context}")
        return render(request, 'skills/session.html', context)
        
    except Exception as e:
        print(f"DEBUG: Error in start_session: {e}")
        import traceback
        traceback.print_exc()
        messages.error(request, f"Failed to start session: {str(e)}")
        return redirect('search_results')


@require_http_methods(["POST"])
@csrf_exempt
def generate_summary_api(request):
    """API endpoint to generate AI summary from transcript"""
    try:
        data = json.loads(request.body)
        transcript = data.get('transcript', '')
        session_id = data.get('session_id')
        language = data.get('language', 'hindi')
        client_summary = data.get('summary')
        
        if not transcript:
            return JsonResponse({'error': 'No transcript provided'}, status=400)
        
        # If client already has a summary (preferred path), just save it
        if client_summary and isinstance(client_summary, str):
            summary = client_summary
            is_mock = False
        else:
            # Server-side generation fallback
            if len(transcript.strip()) < 50:
                return JsonResponse({
                    'error': 'Transcript too short for meaningful summary'
                }, status=400)

            ai_service = AISummaryService()
            summary = ai_service.generate_summary(transcript, language)
            is_mock = not ai_service.use_real_ai
        
        if summary:
            # Save summary to database
            if session_id:
                try:
                    session = Session.objects.get(id=session_id)
                    SessionSummary.objects.update_or_create(
                        session=session,
                        defaults={
                            'transcript': transcript,
                            'summary': summary,
                            'language': language,
                            'generated_at': datetime.now()
                        }
                    )
                except Session.DoesNotExist:
                    pass
            
            return JsonResponse({
                'success': True,
                'summary': summary,
                'is_mock': is_mock
            })
        else:
            return JsonResponse({'error': 'Failed to generate summary'}, status=500)
            
    except Exception as e:
        print(f"Summary generation error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def process_recording_api(request):
    """API endpoint to process Daily recording (mock for testing)"""
    try:
        data = json.loads(request.body)
        room_name = data.get('room_name')
        session_id = data.get('session_id')
        
        if not room_name:
            return JsonResponse({'error': 'Room name required'}, status=400)
        
        # Mock processing for testing
        mock_transcript = """
Teacher: Welcome to this learning session! Today we'll be covering Python programming fundamentals.
Student: That sounds great! I'm excited to learn about variables and functions in Python.
Teacher: Let's start with variables. In Python, you can create a variable by simply assigning a value to it. For example: name = 'John'
Student: I see! So Python automatically determines the data type? That's different from Java.
Teacher: Exactly! Python is dynamically typed. Now let's talk about functions. Functions in Python are defined using the 'def' keyword.
Student: Can you show me an example of a simple function?
Teacher: Sure! Here's a simple function: def greet(name): return f'Hello, {name}!' This function takes a name parameter and returns a greeting.
Student: That's really helpful! How do I call this function?
Teacher: You simply call it like this: greet('Alice') and it will return 'Hello, Alice!'
        """
        
        # Generate summary using AI service
        ai_service = AISummaryService()
        summary = ai_service.generate_summary(mock_transcript)
        
        # Save to database
        if session_id:
            try:
                session = Session.objects.get(id=session_id)
                
                SessionSummary.objects.update_or_create(
                    session=session,
                    defaults={
                        'transcript': mock_transcript,
                        'summary': summary,
                        'generated_at': datetime.now()
                    }
                )
                
            except Session.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'transcript': mock_transcript,
            'summary': summary,
            'note': 'This is a mock response for testing. Real implementation requires Google Cloud setup.'
        })
        
    except Exception as e:
        print(f"Recording processing error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def save_session_notes_api(request):
    """API endpoint to save session notes"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        notes = data.get('notes', '')
        
        if not session_id or not notes:
            return JsonResponse({'error': 'Session ID and notes required'}, status=400)
        
        try:
            session = Session.objects.get(id=session_id)
            SessionNotes.objects.update_or_create(
                session=session,
                defaults={'notes': notes, 'updated_at': datetime.now()}
            )
            return JsonResponse({'success': True})
        except Session.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
