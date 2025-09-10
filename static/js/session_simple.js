// Simplified Session Interface - Focus on AI Summary Testing
class SessionManager {
    constructor() {
        this.transcripts = [];
        this.sessionStartTime = Date.now();
        
        this.initializeElements();
        this.setupEventListeners();
        this.startTimer();
    this.loadMockTranscript();
    this.mockVideoConnection();
    this.bindDailyTranscript();
        
        console.log('Session Manager initialized for AI testing');
    }

    bindDailyTranscript() {
        // Listen for synthetic transcript lines emitted by Daily integration (app-message or future events)
        window.addEventListener('daily-transcript-line', (ev) => {
            const detail = ev.detail || {};
            const text = (detail.text || '').trim();
            const speaker = (detail.speaker || 'Participant').trim();
            if (!text) return;

            const transcript = {
                text: text,
                timestamp: Date.now(),
                speaker: speaker
            };
            this.transcripts.push(transcript);

            const entry = document.createElement('div');
            entry.className = 'transcript-entry';
            entry.innerHTML = `
                <div class="transcript-speaker">${transcript.speaker}</div>
                <div class="transcript-text">${transcript.text}</div>
                <div class="transcript-time">${this.formatTime(new Date(transcript.timestamp))}</div>
            `;
            this.elements.transcriptContainer.appendChild(entry);
            this.elements.transcriptContainer.scrollTop = this.elements.transcriptContainer.scrollHeight;
        });
    }

    initializeElements() {
        // Get all DOM elements
        this.elements = {
            callFrame: document.getElementById('call-frame'),
            getSummaryBtn: document.getElementById('getSummaryBtn'),
            transcriptContainer: document.getElementById('transcript-container'),
            summaryContainer: document.getElementById('summary-container'),
            timerEl: document.getElementById('timer'),
            modal: document.getElementById('summaryModal'),
            modalSummaryText: document.getElementById('modal-summary-text'),
            closeModalBtn: document.querySelector('.close-button'),
            connectionStatus: document.getElementById('connectionStatus'),
            notesArea: document.getElementById('notesArea'),
            saveNotesBtn: document.getElementById('saveNotesBtn')
        };
    }

    setupEventListeners() {
        // Main functionality - AI Summary
        this.elements.getSummaryBtn.addEventListener('click', () => this.generateSummary());
        
        // Modal controls
        if (this.elements.closeModalBtn) {
            this.elements.closeModalBtn.addEventListener('click', () => this.closeModal());
        }
        
        window.addEventListener('click', (event) => {
            if (event.target === this.elements.modal) {
                this.closeModal();
            }
        });

        // Notes functionality
        if (this.elements.saveNotesBtn) {
            this.elements.saveNotesBtn.addEventListener('click', () => this.saveNotes());
        }
    }

    mockVideoConnection() {
        // Simulate successful connection for testing
    this.updateConnectionStatus('connected', 'Connected');
    this.showNotification('Session loaded. Click "Get AI Summary" to generate insights.', 'success');
    }

    loadMockTranscript() {
        // Enhanced mock transcript for better AI testing
        const mockTranscriptText = `Teacher: Welcome to this comprehensive Python programming session! Today we'll cover variables, functions, and some advanced concepts.
Student: Thank you! I'm excited to learn Python. I have some experience with Java, so I'm curious about the differences.
Teacher: Great background! Let's start with variables. In Python, you create variables simply by assignment. For example: name = 'Alice', age = 25, is_student = True
Student: That's much simpler than Java! Do I need to declare the data type?
Teacher: No! Python is dynamically typed, meaning it automatically determines the data type. You can even change types: x = 5, then x = 'hello'
Student: Wow, that's very flexible. What about functions? How do they work in Python?
Teacher: Functions use the 'def' keyword. Here's a simple example: def greet(name): return f'Hello, {name}!' Notice the indentation - it's crucial in Python.
Student: The f-string syntax is interesting! Is that for string formatting?
Teacher: Exactly! F-strings are a modern way to format strings. You can also use .format() or % formatting, but f-strings are preferred.
Student: Can functions return multiple values like in some other languages?
Teacher: Yes! Python functions can return tuples: def get_info(): return 'John', 25, 'Engineer'. You can unpack it: name, age, job = get_info()
Student: That's really powerful! What about loops? Are they similar to Java?
Teacher: Python has for and while loops, but they're more elegant. For example: for i in range(5): print(i) or for item in my_list: print(item)
Student: The range() function seems useful. Can I iterate over dictionaries too?
Teacher: Absolutely! for key, value in my_dict.items(): print(key, value) - Python makes iteration very readable and intuitive.
Student: This is amazing! Python seems much more readable than Java. Are there any gotchas I should know about?
Teacher: Main things: indentation matters (use 4 spaces), be careful with mutable default arguments, and remember that everything is an object in Python.
Student: Thank you for this comprehensive overview! I feel much more confident about starting my Python journey now.`;

        const lines = mockTranscriptText.split('\n').filter(line => line.trim());
        
        lines.forEach((line, index) => {
            const [speaker, ...textParts] = line.split(':');
            const text = textParts.join(':').trim();
            
            const transcript = {
                text: text,
                timestamp: Date.now() - (lines.length - index) * 30000,
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

        this.elements.transcriptContainer.scrollTop = this.elements.transcriptContainer.scrollHeight;
        
        console.log('Enhanced mock transcript loaded with', this.transcripts.length, 'entries');
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }

    async generateSummary() {
        if (this.transcripts.length === 0) {
            this.showNotification('No transcript available for summary generation', 'warning');
            return;
        }

        try {
            this.elements.getSummaryBtn.disabled = true;
            this.elements.getSummaryBtn.textContent = 'Generating AI Summary...';

            // Prepare transcript text
            const fullTranscript = this.transcripts
                .map(t => `${t.speaker}: ${t.text}`)
                .join('\n');

            console.log('Generating AI summary for transcript...');

            // Get Gemini API key from session config
            const geminiApiKey = window.sessionConfig?.geminiApiKey || 'AIzaSyBCUMFbxVUEDyBeDZtd0xZZKL-3uCeJiaI';
            
            if (!geminiApiKey || geminiApiKey === '') {
                throw new Error('Gemini API key not configured');
            }

            // Enhanced prompt for better AI summary
            const prompt = `Based on the following transcript from a Python programming learning session, please provide a comprehensive, well-structured summary in both Hindi and English. Focus on the key concepts taught, learning progression, and practical examples discussed.

Transcript: "${fullTranscript}"

Please provide a detailed summary in this format:

**सत्र का विस्तृत सारांश / Comprehensive Session Summary**

**मुख्य विषय / Key Topics Covered:**
- [List all main topics with brief explanations]

**सीखे गए अवधारणाएं / Concepts Learned:**
- [Detailed learning outcomes with examples]

**प्रैक्टिकल उदाहरण / Practical Examples:**
- [Code examples and demonstrations discussed]

**छात्र की प्रगति / Student Progress:**
- [Student's questions and understanding development]

**महत्वपूर्ण बिंदु / Key Takeaways:**
- [Most important concepts to remember]

**अगले कदम / Next Steps:**
- [Recommended practice and further learning]

**तकनीकी विवरण / Technical Details:**
- [Specific Python features and syntax covered]`;

            // Use the current Gemini model endpoint; older 'gemini-pro' returns 404
            const model = 'gemini-1.5-flash-latest';
            const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${geminiApiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    contents: [
                        {
                            role: 'user',
                            parts: [
                                { text: prompt }
                            ]
                        }
                    ]
                })
            });

            if (!response.ok) {
                throw new Error(`Gemini API request failed with status ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            // Robust parsing for Gemini responses (parts array may contain multiple items)
            let summary = '';
            if (data?.candidates?.length) {
                const parts = data.candidates[0]?.content?.parts || [];
                summary = parts.map(p => p.text).filter(Boolean).join('\n').trim();
            }

            if (summary) {
                this.displaySummary(summary);
                this.showNotification('🎉 Real AI Summary generated successfully!', 'success');
                
                // Save to backend (non-blocking)
                this.saveSummaryToBackend(fullTranscript, summary);
            } else {
                throw new Error('Invalid response from Gemini API');
            }

    } catch (error) {
            console.error('Error generating AI summary:', error);
            this.showNotification(`Failed to generate AI summary: ${error.message}`, 'error');
            // Intentionally no mock summary fallback; user should only see real AI summaries
        } finally {
            this.elements.getSummaryBtn.disabled = false;
            this.elements.getSummaryBtn.textContent = 'Get AI Summary';
        }
    }

    async saveSummaryToBackend(transcript, summary) {
        try {
            const response = await fetch('/api/generate-summary/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.sessionConfig?.csrfToken || ''
                },
                body: JSON.stringify({
                    transcript: transcript,
                    summary: summary, // pass through to avoid server-side regeneration
                    session_id: window.sessionConfig?.sessionId,
                    room_name: window.sessionConfig?.roomName
                })
            });
            
            if (response.ok) {
                console.log('Summary saved to backend successfully');
            }
        } catch (error) {
            console.log('Could not save to backend:', error);
        }
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

            if (this.elements.modalSummaryText && this.elements.modal) {
                this.elements.modalSummaryText.innerHTML = this.formatSummary(summary);
                this.elements.modal.style.display = 'block';
            }
    }


    formatSummary(summary) {
        return summary
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    closeModal() {
        this.elements.modal.style.display = 'none';
    }

    async saveNotes() {
        const notes = this.elements.notesArea?.value?.trim();
        if (!notes) {
            this.showNotification('No notes to save', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/save-session-notes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.sessionConfig?.csrfToken || ''
                },
                body: JSON.stringify({
                    session_id: window.sessionConfig?.sessionId,
                    notes: notes
                })
            });

            if (response.ok) {
                this.showNotification('Notes saved successfully!', 'success');
            }
        } catch (error) {
            this.showNotification('Failed to save notes', 'error');
        }
    }

    updateConnectionStatus(status, message) {
        if (this.elements.connectionStatus) {
            this.elements.connectionStatus.className = `connection-status ${status}`;
            this.elements.connectionStatus.innerHTML = `
                <div class="status-indicator">
                    <i class="fas fa-circle"></i>
                    <span>${message}</span>
                </div>
            `;
        }
    }

    startTimer() {
        let seconds = 0;
        setInterval(() => {
            seconds++;
            const hrs = Math.floor(seconds / 3600).toString().padStart(2, '0');
            const mins = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            if (this.elements.timerEl) {
                this.elements.timerEl.textContent = `${hrs}:${mins}:${secs}`;
            }
        }, 1000);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
        
        // Manual close
        notification.querySelector('.notification-close').addEventListener('click', () => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        });
    }
}

// CSS for notifications
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #333;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 1rem;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    
    .notification-success { background: #28a745; }
    .notification-error { background: #dc3545; }
    .notification-warning { background: #ffc107; color: #333; }
    .notification-info { background: #17a2b8; }
    
    .notification-close {
        background: none;
        border: none;
        color: inherit;
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
