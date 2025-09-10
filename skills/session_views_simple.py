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

# Import session models (you'll need to add these to your models.py)
from .models import Session, SessionSummary, SessionNotes


class DailyAPI:
    """Daily.co API integration for video calling and recording"""
    
    def __init__(self):
        # For testing, we'll use a mock room URL
        self.api_key = getattr(settings, 'DAILY_API_KEY', 'test_key')
        self.domain = getattr(settings, 'DAILY_DOMAIN', 'test-domain.daily.co')
        self.base_url = "https://api.daily.co/v1"
    
    def create_room(self, room_name=None, exp_time=None):
        """Create a Daily room for the session"""
        if not room_name:
            room_name = f"session-{uuid.uuid4().hex[:8]}"
        
        # For testing purposes, return a mock room
        if not hasattr(settings, 'DAILY_API_KEY') or not settings.DAILY_API_KEY:
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


class MockAISummaryService:
    """Mock AI service for testing without Gemini API"""
    
    def generate_summary(self, transcript, language='hindi'):
        """Generate a mock summary"""
        if language.lower() == 'hindi':
            return f"""
**सत्र का सारांश**

**मुख्य बिंदु:**
- इस सत्र में {len(transcript.split())} शब्दों की चर्चा हुई
- विभिन्न विषयों पर गहन बातचीत
- प्रश्न-उत्तर सत्र सफल रहा

**सीखने के परिणाम:**
- नई जानकारी प्राप्त हुई
- व्यावहारिक कौशल विकसित हुए
- समझ में सुधार हुआ

**आगे की कार्य योजना:**
- नियमित अभ्यास करें
- और गहराई से अध्ययन करें
- अगले सत्र की योजना बनाएं

*यह एक परीक्षण सारांश है। वास्तविक AI सारांश के लिए Gemini API की आवश्यकता है।*
            """
        else:
            return f"""
**Session Summary**

**Key Topics Discussed:**
- Covered {len(transcript.split())} words of conversation
- In-depth discussion on various subjects
- Successful Q&A session

**Learning Outcomes:**
- Gained new knowledge
- Developed practical skills
- Improved understanding

**Action Items:**
- Practice regularly
- Study in more depth
- Plan next session

*This is a test summary. Real AI summary requires Gemini API setup.*
            """


# Django Views
@login_required
def start_session(request, skill_id=None):
    """Start a new learning session"""
    try:
        daily_api = DailyAPI()
        
        # Create room
        room_name = f"session-{request.user.id}-{uuid.uuid4().hex[:8]}"
        room_data = daily_api.create_room(room_name)
        
        # Create session record
        session = Session.objects.create(
            user=request.user,
            skill_id=skill_id,
            room_name=room_name,
            room_url=room_data['url'],
            status='active'
        )
        
        context = {
            'session_id': session.id,
            'room_name': room_name,
            'daily_room_url': room_data['url'],
            'session_title': f"Learning Session - {session.skill.name if session.skill else 'General'}"
        }
        
        return render(request, 'skills/session.html', context)
        
    except Exception as e:
        messages.error(request, f"Failed to start session: {str(e)}")
        return redirect('home')


@require_http_methods(["POST"])
@csrf_exempt
def generate_summary_api(request):
    """API endpoint to generate AI summary from transcript"""
    try:
        data = json.loads(request.body)
        transcript = data.get('transcript', '')
        session_id = data.get('session_id')
        
        if not transcript:
            return JsonResponse({'error': 'No transcript provided'}, status=400)
        
        # Check if transcript is too short
        if len(transcript.strip()) < 50:
            return JsonResponse({
                'error': 'Transcript too short for meaningful summary'
            }, status=400)
        
        # Use mock AI service for testing
        ai_service = MockAISummaryService()
        summary = ai_service.generate_summary(transcript)
        
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
                            'generated_at': datetime.now()
                        }
                    )
                except Session.DoesNotExist:
                    pass
            
            return JsonResponse({
                'success': True,
                'summary': summary
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
        This is a mock transcript generated for testing purposes. 
        In a real implementation, this would be the actual transcription 
        from the Daily.co recording processed through Google Speech-to-Text.
        
        The conversation covered various topics including:
        - Technical concepts and explanations
        - Question and answer sessions
        - Practical examples and demonstrations
        - Learning objectives and outcomes
        """
        
        # Generate mock summary
        ai_service = MockAISummaryService()
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
