// --- CONFIGURATION ---
// IMPORTANT: Enter your Gemini API Key here
const GEMINI_API_KEY = 'AIzaSyBCUMFbxVUEDyBeDZtd0xZZKL-3uCeJiaI';
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=';

// --- DOM ELEMENTS ---
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const micBtn = document.getElementById('micBtn');
const videoBtn = document.getElementById('videoBtn');
const shareScreenBtn = document.getElementById('shareScreenBtn');
const leaveBtn = document.getElementById('leaveBtn');
const getSummaryBtn = document.getElementById('getSummaryBtn');
const transcriptContainer = document.getElementById('transcript-container');
const summaryContainer = document.getElementById('summary-container');
const timerEl = document.getElementById('timer');
const modal = document.getElementById('summaryModal');
const modalSummaryText = document.getElementById('modal-summary-text');
const closeModalBtn = document.querySelector('.close-button');

// --- STATE ---
let localStream;
let remoteStream;
let peerConnection;
let isMicOn = true;
let isVideoOn = true;
let isScreenSharing = false;
let recognition;
let fullTranscript = '';
let timerInterval;
let seconds = 0;

// --- WEBRTC CONFIGURATION ---
const servers = {
    iceServers: [
        {
            urls: ['stun:stun1.l.google.com:19302', 'stun:stun2.l.google.com:19302'],
        },
    ],
};

// --- INITIALIZATION ---
const init = async () => {
    try {
        // Get local media
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;

        // Setup transcription
        setupSpeechRecognition();

        // Start timer
        startTimer();

        // Placeholder for remote stream
        // In a real app, you'd get this from the signaling server
        remoteVideo.srcObject = new MediaStream(); 

    } catch (error) {
        console.error("Error accessing media devices.", error);
        alert("Could not access your camera and microphone. Please check permissions.");
    }
};

// --- MEDIA CONTROLS ---
micBtn.addEventListener('click', () => {
    isMicOn = !isMicOn;
    localStream.getAudioTracks()[0].enabled = isMicOn;
    micBtn.classList.toggle('active', isMicOn);
    micBtn.innerHTML = isMicOn ? '<i class="fas fa-microphone"></i>' : '<i class="fas fa-microphone-slash"></i>';
    
    if (isMicOn) {
        recognition.start();
    } else {
        recognition.stop();
    }
});

videoBtn.addEventListener('click', () => {
    isVideoOn = !isVideoOn;
    localStream.getVideoTracks()[0].enabled = isVideoOn;
    videoBtn.classList.toggle('active', isVideoOn);
    videoBtn.innerHTML = isVideoOn ? '<i class="fas fa-video"></i>' : '<i class="fas fa-video-slash"></i>';
});

shareScreenBtn.addEventListener('click', toggleScreenSharing);

leaveBtn.addEventListener('click', () => {
    window.location.reload(); // Simple leave action
});

async function toggleScreenSharing() {
    if (!isScreenSharing) {
        try {
            const screenStream = await navigator.mediaDevices.getDisplayMedia({ cursor: true });
            const screenTrack = screenStream.getVideoTracks()[0];

            // Replace video track
            const sender = peerConnection.getSenders().find(s => s.track.kind === 'video');
            if (sender) {
                sender.replaceTrack(screenTrack);
            }
            localVideo.srcObject = screenStream;
            isScreenSharing = true;
            shareScreenBtn.classList.add('active');

            screenTrack.onended = () => {
                toggleScreenSharing(); // Revert back to camera
            };

        } catch (err) {
            console.error("Screen sharing failed:", err);
        }
    } else {
        // Revert to camera
        const cameraTrack = localStream.getVideoTracks()[0];
        const sender = peerConnection.getSenders().find(s => s.track.kind === 'video');
        if (sender) {
            sender.replaceTrack(cameraTrack);
        }
        localVideo.srcObject = localStream;
        isScreenSharing = false;
        shareScreenBtn.classList.remove('active');
    }
}


// --- SPEECH RECOGNITION (TRANSCRIPTION) ---
const setupSpeechRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Your browser does not support Speech Recognition. Transcription will not be available.");
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-IN'; // Can be changed to 'hi-IN' for Hindi

    recognition.onstart = () => {
        console.log('Speech recognition started');
    };

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        
        // Update the UI with the live transcript
        updateTranscriptUI(finalTranscript, interimTranscript);
        
        if(finalTranscript) {
            fullTranscript += finalTranscript + ' ';
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
    };

    recognition.onend = () => {
        console.log('Speech recognition ended. Restarting if mic is on.');
        if (isMicOn) {
            recognition.start(); // Keep it running
        }
    };

    recognition.start();
};

function updateTranscriptUI(final, interim) {
    const placeholder = transcriptContainer.querySelector('.transcript-placeholder');
    if (placeholder) {
        placeholder.remove();
    }
    
    // For a more sophisticated UI, you might manage paragraphs or speaker turns
    // Here we just append
    let existingContent = transcriptContainer.innerHTML.replace(/<span class="interim">.*<\/span>/, '');
    transcriptContainer.innerHTML = existingContent + final + `<span class="interim" style="color: #999;">${interim}</span>`;
    transcriptContainer.scrollTop = transcriptContainer.scrollHeight;
}


// --- GEMINI API INTEGRATION ---
getSummaryBtn.addEventListener('click', async () => {
    if (GEMINI_API_KEY === 'YOUR_GEMINI_API_KEY') {
        alert('Please enter your Gemini API Key in the script.js file.');
        return;
    }
    if (fullTranscript.trim().length < 50) { // Check for minimum length
        alert('Not enough transcription has been recorded to generate a summary.');
        return;
    }

    getSummaryBtn.disabled = true;
    getSummaryBtn.textContent = 'Generating...';

    try {
        const prompt = `Based on the following transcript from a one-on-one skill-sharing session, please provide a concise, well-structured summary. The summary should highlight the key topics discussed, main questions asked, and the most important concepts or skills explained. Format it with clear headings and bullet points for readability. Transcript: "${fullTranscript}"`;

        const response = await fetch(`${GEMINI_API_URL}${GEMINI_API_KEY}`, {
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
            throw new Error(`API request failed with status ${response.status}`);
        }

        const data = await response.json();
        const summary = data.candidates[0].content.parts[0].text;
        
        displaySummary(summary);

    } catch (error) {
        console.error('Error fetching summary from Gemini API:', error);
        summaryContainer.innerHTML = '<p style="color: red;">Failed to generate summary. Please try again later.</p>';
    } finally {
        getSummaryBtn.disabled = false;
        getSummaryBtn.textContent = 'Get Summary';
    }
});

function displaySummary(summary) {
    // Display in the side panel
    const summaryPlaceholder = summaryContainer.querySelector('.summary-placeholder');
    if(summaryPlaceholder) summaryPlaceholder.remove();
    summaryContainer.innerHTML = summary.replace(/\n/g, '<br>'); // Basic formatting

    // Display in the modal
    modalSummaryText.innerHTML = summary.replace(/\n/g, '<br>');
    modal.style.display = 'block';
}


// --- MODAL CONTROLS ---
closeModalBtn.onclick = () => {
    modal.style.display = 'none';
};

window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};


// --- TIMER ---
function startTimer() {
    timerInterval = setInterval(() => {
        seconds++;
        const hrs = Math.floor(seconds / 3600).toString().padStart(2, '0');
        const mins = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
        const secs = (seconds % 60).toString().padStart(2, '0');
        timerEl.textContent = `${hrs}:${mins}:${secs}`;
    }, 1000);
}

// --- START THE APP ---
init();

// Note: A full WebRTC implementation requires a signaling server (e.g., using WebSockets)
// to exchange session descriptions (SDP) and ICE candidates between the two peers.
// This code sets up the local media and UI, but the peerConnection logic is simplified.
// To make it a fully functional 1-on-1 call, you would need to:
// 1. Implement a signaling server (e.g., with Node.js and Socket.IO).
// 2. On user connection, create `peerConnection = new RTCPeerConnection(servers);`
// 3. Add localStream tracks: `localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));`
// 4. Handle `peerConnection.ontrack = event => { remoteVideo.srcObject = event.streams[0]; };`
// 5. Handle `peerConnection.onicecandidate = event => { if (event.candidate) { /* send candidate to other peer via signaling server */ } };`
// 6. Create and exchange offers and answers (SDP) via the signaling server.
