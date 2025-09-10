import os
import json
import requests
import uuid
import tempfile
import subprocess
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.contrib import messages
from google.cloud import storage, speech
from google.cloud.speech import enums
from google.cloud.speech import types
import google.generativeai as genai

# Session models (you'll need to add these to your models.py)
from .models import Session, SessionRecording, SessionSummary, SessionNotes


class DailyAPI:
    """Daily.co API integration for video calling and recording"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'DAILY_API_KEY', None)
        self.domain = getattr(settings, 'DAILY_DOMAIN', None)
        self.base_url = "https://api.daily.co/v1"
        
        if not self.api_key:
            raise ValueError("DAILY_API_KEY not set in settings")
    
    def create_room(self, room_name=None, exp_time=None):
        """Create a Daily room for the session"""
        if not room_name:
            room_name = f"session-{uuid.uuid4().hex[:8]}"
        
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
        
        response = requests.post(f"{self.base_url}/rooms", 
                               headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create room: {response.text}")
    
    def get_recordings(self, room_name):
        """Get recordings for a room"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {'room_name': room_name, 'limit': 50}
        
        response = requests.get(f"{self.base_url}/recordings", 
                              headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json().get('recordings', [])
        else:
            raise Exception(f"Failed to get recordings: {response.text}")
    
    def get_recording_access_link(self, recording_id):
        """Get download link for a recording"""
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        response = requests.get(f"{self.base_url}/recordings/{recording_id}/access-link",
                              headers=headers)
        
        if response.status_code == 200:
            return response.json().get('url')
        else:
            raise Exception(f"Failed to get access link: {response.text}")


class CloudTranscriptionService:
    """Google Cloud Speech-to-Text integration"""
    
    def __init__(self):
        # Initialize Google Cloud Storage and Speech clients
        self.storage_client = storage.Client()
        self.speech_client = speech.SpeechClient()
        self.bucket_name = getattr(settings, 'GCS_BUCKET_NAME', None)
        
        if not self.bucket_name:
            raise ValueError("GCS_BUCKET_NAME not set in settings")
    
    def extract_audio_from_video(self, video_path, audio_path):
        """Extract audio from video using ffmpeg"""
        try:
            # Convert to 16kHz mono WAV for best transcription accuracy
            cmd = [
                'ffmpeg', '-i', video_path,
                '-ac', '1',  # mono
                '-ar', '16000',  # 16kHz sample rate
                '-y',  # overwrite output file
                audio_path
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e}")
            return False
    
    def upload_to_gcs(self, file_path, blob_name):
        """Upload file to Google Cloud Storage"""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(blob_name)
        
        with open(file_path, 'rb') as f:
            blob.upload_from_file(f)
        
        return f"gs://{self.bucket_name}/{blob_name}"
    
    def transcribe_audio(self, gcs_uri, language_code='hi-IN'):
        """Transcribe audio using Google Speech-to-Text"""
        audio = types.RecognitionAudio(uri=gcs_uri)
        
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
            alternative_language_codes=['en-IN', 'en-US'],
            enable_automatic_punctuation=True,
            enable_word_time_offsets=True,
            model='latest_long'
        )
        
        # Use long running recognize for files > 1 minute
        operation = self.speech_client.long_running_recognize(config, audio)
        response = operation.result(timeout=600)  # 10 minutes timeout
        
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript + " "
        
        return transcript.strip()


class AISummaryService:
    """Gemini AI integration for generating session summaries"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in settings")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_summary(self, transcript, language='hindi'):
        """Generate AI summary using Gemini"""
        if language.lower() == 'hindi':
            prompt = f"""
            आपके सामने एक सीखने का सत्र का ट्रांस्क्रिप्ट है। कृपया इसे हिंदी में संक्षेप (summary) करें:

            मुख्य बिंदु:
            - सत्र में क्या मुख्य विषय चर्चा किए गए
            - कौन सी महत्वपूर्ण अवधारणाएं सिखाई गईं
            - क्या प्रश्न पूछे गए और उनके उत्तर

            सीखने के परिणाम:
            - छात्र ने क्या नया सीखा
            - कौन से कौशल विकसित हुए

            आगे की कार्य योजना:
            - अगले कदम क्या होने चाहिए
            - अभ्यास के लिए सुझाव

            ट्रांस्क्रिप्ट: {transcript}
            
            कृपया संक्षेप 200-300 शब्दों में दें और स्पष्ट हेडिंग्स का उपयोग करें।
            """
        else:
            prompt = f"""
            Please provide a comprehensive summary of this learning session transcript in English:

            Key Topics Discussed:
            - Main subjects covered in the session
            - Important concepts taught
            - Questions asked and answers provided

            Learning Outcomes:
            - What the student learned
            - Skills developed during the session

            Action Items:
            - Next steps recommended
            - Practice suggestions

            Transcript: {transcript}
            
            Please provide the summary in 200-300 words with clear headings.
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
            return None


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
        room_name = data.get('room_name')
        
        if not transcript:
            return JsonResponse({'error': 'No transcript provided'}, status=400)
        
        # Initialize AI service
        ai_service = AISummaryService()
        
        # Generate summary
        summary = ai_service.generate_summary(transcript)
        
        if summary:
            # Save summary to database
            if session_id:
                try:
                    session = Session.objects.get(id=session_id)
                    SessionSummary.objects.create(
                        session=session,
                        transcript=transcript,
                        summary=summary,
                        generated_at=datetime.now()
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
    """API endpoint to process Daily recording and generate transcript + summary"""
    try:
        data = json.loads(request.body)
        room_name = data.get('room_name')
        session_id = data.get('session_id')
        
        if not room_name:
            return JsonResponse({'error': 'Room name required'}, status=400)
        
        # Initialize services
        daily_api = DailyAPI()
        transcription_service = CloudTranscriptionService()
        ai_service = AISummaryService()
        
        # Get recordings
        recordings = daily_api.get_recordings(room_name)
        if not recordings:
            return JsonResponse({'error': 'No recordings found'}, status=404)
        
        # Get the latest finished recording
        recording = None
        for rec in recordings:
            if rec.get('status') == 'finished':
                recording = rec
                break
        
        if not recording:
            return JsonResponse({'error': 'No finished recordings found'}, status=404)
        
        # Get download link
        download_url = daily_api.get_recording_access_link(recording['id'])
        
        # Download and process recording
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download video
            video_path = os.path.join(temp_dir, 'recording.mp4')
            audio_path = os.path.join(temp_dir, 'audio.wav')
            
            # Download recording
            response = requests.get(download_url)
            with open(video_path, 'wb') as f:
                f.write(response.content)
            
            # Extract audio
            if not transcription_service.extract_audio_from_video(video_path, audio_path):
                return JsonResponse({'error': 'Failed to extract audio'}, status=500)
            
            # Upload to GCS
            blob_name = f"recordings/{uuid.uuid4().hex}.wav"
            gcs_uri = transcription_service.upload_to_gcs(audio_path, blob_name)
            
            # Transcribe
            transcript = transcription_service.transcribe_audio(gcs_uri)
            
            if not transcript:
                return JsonResponse({'error': 'Failed to transcribe audio'}, status=500)
            
            # Generate summary
            summary = ai_service.generate_summary(transcript)
            
            # Save to database
            if session_id:
                try:
                    session = Session.objects.get(id=session_id)
                    
                    # Save recording info
                    session_recording = SessionRecording.objects.create(
                        session=session,
                        recording_id=recording['id'],
                        download_url=download_url,
                        gcs_uri=gcs_uri
                    )
                    
                    # Save summary
                    SessionSummary.objects.create(
                        session=session,
                        transcript=transcript,
                        summary=summary,
                        generated_at=datetime.now()
                    )
                    
                except Session.DoesNotExist:
                    pass
            
            return JsonResponse({
                'success': True,
                'transcript': transcript,
                'summary': summary
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


# Add a temporary test link to search results
def add_session_test_link(request):
    """Temporary view to test session interface"""
    return redirect('start_session')
