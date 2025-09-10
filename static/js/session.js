// Session Interface with Daily.co Integration and AI Summary
class SessionManager {
    constructor() {
        this.callFrame = nul    async initializeDaily() {
        try {
            // Mock Daily.co for testing - don't actually connect
            console.log('Daily.co initialization disabled for testing');
            this.updateConnectionStatus('connected', 'Mock Session Active');
            return;
            
            // The real Daily.co code would go here when properly configured
            this.updateConnectionStatus('connecting', 'Connecting to session...');
            
            // Create Daily call frame (commented out for testing)      this.isRecording = false;
        this.isMicOn = true;
        this.isVideoOn = true;
        this.transcripts = [];
        this.sessionStartTime = Date.now();
        this.recognition = null;
        
        this.initializeElements();
        this.setupEventListeners();
        this.startTimer();
        this.loadMockTranscript(); // Load mock transcript immediately
        // Disable Daily.co for testing
        // this.initializeDaily();
        // Comment out speech recognition for now
        // this.setupSpeechRecognition();
        
        // Show success message
        this.showNotification('Session interface loaded! Mock transcript ready for AI summary testing.', 'success');
    }

    initializeElements() {
        // Get all DOM elements
        this.elements = {
            callFrame: document.getElementById('call-frame'),
            micBtn: document.getElementById('micBtn'),
            videoBtn: document.getElementById('videoBtn'),
            shareScreenBtn: document.getElementById('shareScreenBtn'),
            recordBtn: document.getElementById('recordBtn'),
            leaveBtn: document.getElementById('leaveBtn'),
            getSummaryBtn: document.getElementById('getSummaryBtn'),
            transcriptContainer: document.getElementById('transcript-container'),
                const model = 'gemini-1.5-flash';
                const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${geminiApiKey}`, {
            summaryLoading: document.getElementById('summary-loading'),
            timerEl: document.getElementById('timer'),
            modal: document.getElementById('summaryModal'),
            modalSummaryText: document.getElementById('modal-summary-text'),
            closeModalBtn: document.querySelector('.close-button'),
                        contents: [
                            {
                                role: 'user',
                                parts: [{ text: prompt }]
                            }
                        ]

    setupEventListeners() {
        // Control buttons
        this.elements.micBtn.addEventListener('click', () => this.toggleMic());
        this.elements.videoBtn.addEventListener('click', () => this.toggleVideo());
        this.elements.shareScreenBtn.addEventListener('click', () => this.toggleScreenShare());
        this.elements.recordBtn.addEventListener('click', () => this.toggleRecording());
        this.elements.leaveBtn.addEventListener('click', () => this.leaveSession());
        this.elements.getSummaryBtn.addEventListener('click', () => this.generateSummary());
        this.elements.saveNotesBtn.addEventListener('click', () => this.saveNotes());

        // Modal controls
        this.elements.closeModalBtn.addEventListener('click', () => this.closeModal());
        window.addEventListener('click', (event) => {
            if (event.target === this.elements.modal) {
                this.closeModal();
            }
        });

        // Toggle panels
        document.getElementById('toggleTranscript').addEventListener('click', () => {
            this.togglePanel('transcript-container');
        });
        document.getElementById('toggleSummary').addEventListener('click', () => {
            this.togglePanel('summary-container');
        });
        document.getElementById('toggleNotes').addEventListener('click', () => {
            this.togglePanel(this.elements.notesArea.parentElement);
        });
    }

    loadMockTranscript() {
        // Use the mock transcript from Django template
        const mockTranscriptText = window.mockTranscript || `Teacher: Welcome to this learning session! Today we'll be covering Python programming fundamentals.
Student: That sounds great! I'm excited to learn about variables and functions in Python.
Teacher: Let's start with variables. In Python, you can create a variable by simply assigning a value to it. For example: name = 'John'
Student: I see! So Python automatically determines the data type? That's different from Java.
Teacher: Exactly! Python is dynamically typed. Now let's talk about functions. Functions in Python are defined using the 'def' keyword.
Student: Can you show me an example of a simple function?
Teacher: Sure! Here's a simple function: def greet(name): return f'Hello, {name}!' This function takes a name parameter and returns a greeting.`;

        const lines = mockTranscriptText.split('\n').filter(line => line.trim());
        
        lines.forEach((line, index) => {
            const [speaker, ...textParts] = line.split(':');
            const text = textParts.join(':').trim();
            
            const transcript = {
                text: text,
                timestamp: Date.now() - (lines.length - index) * 30000, // 30 seconds apart
                speaker: speaker.trim()
            };
            
            this.transcripts.push(transcript);
        });

        // Display transcripts in UI
        const placeholder = this.elements.transcriptContainer.querySelector('.transcript-placeholder');
        if (placeholder) {
            placeholder.remove();
        }

        this.transcripts.forEach(transcript => {
            const transcriptEntry = document.createElement('div');
            transcriptEntry.className = 'transcript-entry';
            transcriptEntry.innerHTML = `
                <div class="transcript-speaker">${transcript.speaker}</div>
                <div class="transcript-text">${transcript.text}</div>
                <div class="transcript-time">${this.formatTime(new Date(transcript.timestamp))}</div>
            `;
            this.elements.transcriptContainer.appendChild(transcriptEntry);
        });

        // Scroll to bottom
        this.elements.transcriptContainer.scrollTop = this.elements.transcriptContainer.scrollHeight;
        
        console.log('Mock transcript loaded with', this.transcripts.length, 'entries');
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    async initializeDaily() {
        try {
            this.updateConnectionStatus('connecting', 'Connecting to session...');
            
            // Create Daily call frame
            this.callFrame = window.DailyIframe.createFrame(this.elements.callFrame, {
                iframeStyle: {
                    position: 'relative',
                    width: '100%',
                    height: '100%',
                    border: 'none',
                    borderRadius: '0'
                },
                showLeaveButton: false,
                showFullscreenButton: false
            });

            // Set up event listeners
            this.callFrame
                .on('joined-meeting', () => {
                    this.updateConnectionStatus('connected', 'Connected');
                    console.log('Joined meeting successfully');
                })
                .on('left-meeting', () => {
                    this.updateConnectionStatus('disconnected', 'Disconnected');
                    window.location.href = '/';
                })
                .on('error', (error) => {
                    console.error('Daily error:', error);
                    this.updateConnectionStatus('disconnected', 'Connection error');
                })
                .on('recording-started', () => {
                    this.isRecording = true;
                    this.elements.recordBtn.classList.add('active');
                    this.showNotification('Recording started');
                })
                .on('recording-stopped', () => {
                    this.isRecording = false;
                    this.elements.recordBtn.classList.remove('active');
                    this.showNotification('Recording stopped');
                })
                .on('participant-joined', (event) => {
                    console.log('Participant joined:', event.participant);
                })
                .on('participant-left', (event) => {
                    console.log('Participant left:', event.participant);
                });

            // Join the room
            if (window.sessionConfig.roomUrl) {
                await this.callFrame.join({ url: window.sessionConfig.roomUrl });
            } else {
                throw new Error('No room URL provided');
            }

        } catch (error) {
            console.error('Failed to initialize Daily:', error);
            this.updateConnectionStatus('disconnected', 'Failed to connect');
            this.showNotification('Failed to connect to video session', 'error');
        }
    }

    setupSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-IN'; // Support for English and Hindi

        this.recognition.onstart = () => {
            console.log('Speech recognition started');
        };

        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            this.updateTranscriptUI(finalTranscript, interimTranscript);
            
            if (finalTranscript) {
                this.transcripts.push({
                    text: finalTranscript,
                    timestamp: Date.now(),
                    speaker: window.sessionConfig.userName
                });
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
        };

        this.recognition.onend = () => {
            if (this.isMicOn) {
                setTimeout(() => this.recognition.start(), 100);
            }
        };

        // Start recognition
        this.recognition.start();
    }

    updateTranscriptUI(finalText, interimText) {
        const placeholder = this.elements.transcriptContainer.querySelector('.transcript-placeholder');
        if (placeholder) {
            placeholder.remove();
        }

        if (finalText) {
            const transcriptEntry = document.createElement('div');
            transcriptEntry.className = 'transcript-entry';
            transcriptEntry.innerHTML = `
                <div class="transcript-speaker">${window.sessionConfig.userName}</div>
                <div class="transcript-text">${finalText}</div>
            `;
            this.elements.transcriptContainer.appendChild(transcriptEntry);
        }

        // Update interim text
        let interimElement = this.elements.transcriptContainer.querySelector('.interim-text');
        if (!interimElement && interimText) {
            interimElement = document.createElement('div');
            interimElement.className = 'interim-text';
            this.elements.transcriptContainer.appendChild(interimElement);
        }
        
        if (interimElement) {
            if (interimText) {
                interimElement.textContent = interimText;
            } else {
                interimElement.remove();
            }
        }

        this.elements.transcriptContainer.scrollTop = this.elements.transcriptContainer.scrollHeight;
    }

    async toggleMic() {
        try {
            if (this.callFrame) {
                if (this.isMicOn) {
                    await this.callFrame.setLocalAudio(false);
                    this.recognition?.stop();
                } else {
                    await this.callFrame.setLocalAudio(true);
                    this.recognition?.start();
                }
            }
            
            this.isMicOn = !this.isMicOn;
            this.elements.micBtn.classList.toggle('muted', !this.isMicOn);
            this.elements.micBtn.innerHTML = this.isMicOn ? 
                '<i class="fas fa-microphone"></i>' : 
                '<i class="fas fa-microphone-slash"></i>';
        } catch (error) {
            console.error('Error toggling microphone:', error);
        }
    }

    async toggleVideo() {
        try {
            if (this.callFrame) {
                await this.callFrame.setLocalVideo(!this.isVideoOn);
            }
            
            this.isVideoOn = !this.isVideoOn;
            this.elements.videoBtn.classList.toggle('active', this.isVideoOn);
            this.elements.videoBtn.innerHTML = this.isVideoOn ? 
                '<i class="fas fa-video"></i>' : 
                '<i class="fas fa-video-slash"></i>';
        } catch (error) {
            console.error('Error toggling video:', error);
        }
    }

    async toggleScreenShare() {
        try {
            if (this.callFrame) {
                const participants = this.callFrame.participants();
                const localParticipant = participants.local;
                
                if (localParticipant.screen) {
                    await this.callFrame.stopScreenShare();
                    this.elements.shareScreenBtn.classList.remove('active');
                } else {
                    await this.callFrame.startScreenShare();
                    this.elements.shareScreenBtn.classList.add('active');
                }
            }
        } catch (error) {
            console.error('Error toggling screen share:', error);
            this.showNotification('Screen sharing failed', 'error');
        }
    }

    async toggleRecording() {
        try {
            if (this.callFrame) {
                if (this.isRecording) {
                    await this.callFrame.stopRecording();
                } else {
                    await this.callFrame.startRecording();
                }
            }
        } catch (error) {
            console.error('Error toggling recording:', error);
            this.showNotification('Recording control failed', 'error');
        }
    }

    async generateSummary() {
        if (this.transcripts.length === 0) {
            this.showNotification('No transcript available for summary generation', 'warning');
            return;
        }

        try {
            this.elements.getSummaryBtn.disabled = true;
            this.elements.getSummaryBtn.textContent = 'Generating...';
            this.elements.summaryLoading.style.display = 'flex';

            // Prepare transcript text
            const fullTranscript = this.transcripts
                .map(t => `${t.speaker}: ${t.text}`)
                .join('\n');

            console.log('Generating summary for transcript:', fullTranscript.substring(0, 100) + '...');

            // Check if we have Gemini API key from Django settings
            const geminiApiKey = window.sessionConfig?.geminiApiKey || 'AIzaSyBCUMFbxVUEDyBeDZtd0xZZKL-3uCeJiaI';
            
            if (!geminiApiKey || geminiApiKey === '') {
                throw new Error('Gemini API key not configured');
            }

            // Use Gemini API directly
            const prompt = `Based on the following transcript from a one-on-one skill-sharing session, please provide a concise, well-structured summary in Hindi and English. The summary should highlight the key topics discussed, main questions asked, and the most important concepts or skills explained. Format it with clear headings and bullet points for readability.

Transcript: "${fullTranscript}"

Please provide the summary in this format:

**सत्र का सारांश / Session Summary**

**मुख्य विषय / Key Topics:**
- [List main topics in Hindi and English]

**सीखने के परिणाम / Learning Outcomes:**
- [What was learned]

**महत्वपूर्ण बातें / Important Points:**
- [Key concepts and facts]

**आगे की योजना / Next Steps:**
- [Recommendations for further learning]`;

            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${geminiApiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [{
                        parts: [{
                            text: prompt
                        }]
                    }]
                })
            });

            if (!response.ok) {
                throw new Error(`Gemini API request failed with status ${response.status}`);
            }

            const data = await response.json();
            
            if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                const summary = data.candidates[0].content.parts[0].text;
                this.displaySummary(summary);
                this.showNotification('AI Summary generated successfully!', 'success');
                
                // Also try to save to Django backend
                this.saveSummaryToBackend(fullTranscript, summary);
            } else {
                throw new Error('Invalid response from Gemini API');
            }

        } catch (error) {
            console.error('Error generating summary:', error);
            
            // Fallback to Django backend
            console.log('Falling back to Django backend...');
            try {
                const fallbackResponse = await this.generateSummaryViaBackend();
                if (fallbackResponse) {
                    return; // Success with backend
                }
            } catch (backendError) {
                console.error('Backend fallback also failed:', backendError);
            }
            
            // Show error message
            this.showNotification('Failed to generate summary. Please check your API key and try again.', 'error');
            
            // Show a basic mock summary as last resort
            this.displayMockSummary();
            
        } finally {
            this.elements.getSummaryBtn.disabled = false;
            this.elements.getSummaryBtn.textContent = 'Get AI Summary';
            this.elements.summaryLoading.style.display = 'none';
        }
    }

    async generateSummaryViaBackend() {
        // Fallback to Django backend
        const fullTranscript = this.transcripts
            .map(t => `${t.speaker}: ${t.text}`)
            .join('\n');

        const response = await fetch('/api/generate-summary/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.sessionConfig.csrfToken
            },
            body: JSON.stringify({
                transcript: fullTranscript,
                session_id: window.sessionConfig.sessionId,
                room_name: window.sessionConfig.roomName
            })
        });

        if (!response.ok) {
            throw new Error(`Backend API error: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.summary) {
            this.displaySummary(data.summary);
            this.showNotification('Summary generated via backend!', 'success');
            return true;
        }
        
        return false;
    }

    async saveSummaryToBackend(transcript, summary) {
        // Try to save to Django backend (non-blocking)
        try {
            await fetch('/api/generate-summary/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.sessionConfig.csrfToken
                },
                body: JSON.stringify({
                    transcript: transcript,
                    summary: summary,
                    session_id: window.sessionConfig.sessionId,
                    room_name: window.sessionConfig.roomName
                })
            });
        } catch (error) {
            console.log('Could not save to backend:', error);
        }
    }

    displayMockSummary() {
        const mockSummary = `**सत्र का सारांश / Session Summary**

**मुख्य विषय / Key Topics:**
- Python programming fundamentals / Python प्रोग्रामिंग के मूल सिद्धांत
- Variables and data types / Variables और data types
- Functions definition and usage / Functions की परिभाषा और उपयोग
- Dynamic typing concepts / Dynamic typing की अवधारणा

**सीखने के परिणाम / Learning Outcomes:**
- Understanding Python variable assignment / Python में variable assignment की समझ
- Function syntax and implementation / Function का syntax और implementation
- Comparison with Java programming / Java programming के साथ तुलना
- Basic Python readability principles / Python की basic readability principles

**महत्वपूर्ण बातें / Important Points:**
- Python is dynamically typed / Python dynamically typed है
- Functions defined with 'def' keyword / Functions को 'def' keyword से define करते हैं
- Simple and readable syntax / सरल और पढ़ने योग्य syntax
- Multiple return values possible / Multiple return values संभव हैं

**आगे की योजना / Next Steps:**
- Practice more Python functions / अधिक Python functions का अभ्यास करें
- Explore loops and control structures / Loops और control structures को समझें
- Build small projects / छोटे projects बनाएं
- Read Python documentation / Python documentation पढ़ें

*यह एक mock summary है। Real AI summary के लिए Gemini API key की जांच करें।*
*This is a mock summary. Please check Gemini API key for real AI summary.*`;

        this.displaySummary(mockSummary);
    }

    displaySummary(summary) {
        // Remove placeholder
        const placeholder = this.elements.summaryContainer.querySelector('.summary-placeholder');
        if (placeholder) {
            placeholder.remove();
        }

        // Display in side panel
        this.elements.summaryContainer.innerHTML = `
            <div class="summary-content">
                ${this.formatSummary(summary)}
            </div>
        `;

        // Display in modal
        this.elements.modalSummaryText.innerHTML = this.formatSummary(summary);
        this.elements.modal.style.display = 'block';
    }

    formatSummary(summary) {
        // Basic formatting for the summary
        return summary
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    async saveNotes() {
        const notes = this.elements.notesArea.value.trim();
        if (!notes) {
            this.showNotification('No notes to save', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/save-session-notes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.sessionConfig.csrfToken
                },
                body: JSON.stringify({
                    session_id: window.sessionConfig.sessionId,
                    notes: notes
                })
            });

            if (response.ok) {
                this.showNotification('Notes saved successfully!', 'success');
            } else {
                throw new Error('Failed to save notes');
            }
        } catch (error) {
            console.error('Error saving notes:', error);
            this.showNotification('Failed to save notes', 'error');
        }
    }

    async leaveSession() {
        if (confirm('Are you sure you want to leave the session?')) {
            try {
                this.recognition?.stop();
                if (this.callFrame) {
                    await this.callFrame.leave();
                }
                window.location.href = '/';
            } catch (error) {
                console.error('Error leaving session:', error);
                window.location.href = '/';
            }
        }
    }

    closeModal() {
        this.elements.modal.style.display = 'none';
    }

    togglePanel(elementId) {
        const element = typeof elementId === 'string' ? 
            document.getElementById(elementId) : elementId;
        
        if (element) {
            const isHidden = element.style.display === 'none';
            element.style.display = isHidden ? 'block' : 'none';
        }
    }

    updateConnectionStatus(status, message) {
        const statusElement = this.elements.connectionStatus.querySelector('.status-indicator');
        statusElement.className = `status-indicator ${status}`;
        statusElement.querySelector('span').textContent = message;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span>${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            left: '50%',
            transform: 'translateX(-50%)',
            zIndex: '1002',
            backgroundColor: type === 'error' ? '#d9534f' : 
                            type === 'success' ? '#5cb85c' : 
                            type === 'warning' ? '#f0ad4e' : '#5bc0de',
            color: 'white',
            padding: '1rem 1.5rem',
            borderRadius: '8px',
            boxShadow: '0 4px 16px rgba(0,0,0,0.2)',
            animation: 'slideDown 0.3s ease'
        });

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);

        // Remove on click
        notification.querySelector('.notification-close').addEventListener('click', () => {
            notification.remove();
        });
    }

    startTimer() {
        let seconds = 0;
        setInterval(() => {
            seconds++;
            const hrs = Math.floor(seconds / 3600).toString().padStart(2, '0');
            const mins = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            this.elements.timerEl.textContent = `${hrs}:${mins}:${secs}`;
        }, 1000);
    }
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideDown {
        from {
            transform: translate(-50%, -100%);
            opacity: 0;
        }
        to {
            transform: translate(-50%, 0);
            opacity: 1;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.2rem;
        cursor: pointer;
        opacity: 0.8;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
`;
document.head.appendChild(notificationStyles);

// Initialize session when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (window.sessionConfig) {
        new SessionManager();
    } else {
        console.error('Session configuration not found');
    }
});
