# LBOB Job-Centric UI Layout Design Plan

## 🎯 **DESIGN PHILOSOPHY: ADAPTIVE & INTELLIGENT**

Keep LBOB experience natural while intelligently adapting to job context through conversation.

## 🔄 **UI STATE TRANSITIONS**

### **State 1: Initial Load (Current LBOB)**
```
┌─────────────────────────────────────────────────┐
│                                                 │
│               LBOB (Large)                      │
│            "Ready to help!"                     │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │         Chat Input Box                  │    │
│  │    "Type your message..."               │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### **State 2: After First Message (Expanded Chat)**
```
┌──────────────────┬──────────────────────────────┐
│                  │  ┌─────────────────────────┐ │
│   LBOB (Small)   │  │      Job Context        │ │
│     🤖           │  │  Job: Fire Alarm Insp   │ │
│                  │  │  Customer: ABC Mfg      │ │
│                  │  │  📍 Industrial Blvd     │ │
│                  │  └─────────────────────────┘ │
│                  │                              │
│                  │  ┌─────────────────────────┐ │
│                  │  │   Conversation History  │ │
│                  │  │                         │ │
│                  │  │ Tech: "Issues at ABC"   │ │
│                  │  │ LBOB: "I see you're     │ │
│                  │  │       working on..."    │ │
│                  │  │                         │ │
│                  │  └─────────────────────────┘ │
│                  │                              │
│                  │  ┌─────────────────────────┐ │
│                  │  │ 💬 [Type message...]    │ │
│                  │  │ 📎 🎤 📷 📁            │ │
│                  │  └─────────────────────────┘ │
└──────────────────┴──────────────────────────────┘
```

### **State 3: Multi-Job Tabs (When Multiple Jobs Referenced)**
```
┌──────────────────┬──────────────────────────────┐
│                  │ 📋 Fire Alarm │ 🚪 Access │   │
│   LBOB (Small)   │ ─────────────────────────── │
│     🤖           │  ┌─────────────────────────┐ │
│                  │  │    Active Job Info      │ │
│                  │  │  Fire Alarm Inspection  │ │
│                  │  │  ABC Manufacturing      │ │
│                  │  └─────────────────────────┘ │
│                  │                              │
│                  │  ┌─────────────────────────┐ │
│                  │  │   Conversation          │ │
│                  │  │   (Scrollable)          │ │
│                  │  └─────────────────────────┘ │
│                  │                              │
│                  │  ┌─────────────────────────┐ │
│                  │  │ Input + Attachments     │ │
│                  │  └─────────────────────────┘ │
└──────────────────┴──────────────────────────────┘
```

## 📱 **RESPONSIVE BREAKPOINTS**

### **Desktop (1200px+)**
- LBOB: 25% width when small, 60% when large
- Chat: 75% width when expanded
- Job tabs: Horizontal tabs at top

### **Tablet (768px - 1199px)**
- LBOB: 30% width when small
- Chat: 70% width when expanded
- Job tabs: Horizontal tabs, smaller text

### **Mobile (< 768px)**
- LBOB: Small fixed size in corner
- Chat: Full width
- Job tabs: Dropdown/select instead of tabs

## 🔧 **TECHNICAL IMPLEMENTATION**

### **CSS Grid Layout**
```css
.main-container {
    display: grid;
    grid-template-columns: var(--lbob-width) 1fr;
    grid-template-rows: auto 1fr auto;
    transition: grid-template-columns 0.3s ease;
}

/* Initial state - large LBOB */
.initial-state {
    --lbob-width: 60%;
}

/* Expanded state - small LBOB */
.expanded-state {
    --lbob-width: 25%;
}

.lbob-container {
    grid-column: 1;
    transition: all 0.3s ease;
}

.chat-container {
    grid-column: 2;
    display: flex;
    flex-direction: column;
}
```

### **Chat Box Expansion Logic**
```javascript
// Trigger expansion after first message
function handleFirstMessage() {
    const container = document.querySelector('.main-container');
    container.classList.remove('initial-state');
    container.classList.add('expanded-state');

    // Show job context if detected
    if (detectedJobInfo) {
        showJobContext(detectedJobInfo);
    }

    // Initialize conversation history
    initializeConversationHistory();
}

// Job detection and context display
function detectAndDisplayJob(message, aiResponse) {
    const jobInfo = extractJobInfo(aiResponse);
    if (jobInfo) {
        updateJobContext(jobInfo);
        createJobTab(jobInfo);
    }
}
```

## 📎 **ATTACHMENT INTERFACE**

### **Multi-Input Bar Design**
```html
<div class="input-bar">
    <div class="message-input-container">
        <textarea placeholder="Type your message..." rows="2"></textarea>
    </div>

    <div class="attachment-buttons">
        <button class="attach-btn" title="Upload File">📁</button>
        <button class="voice-btn" title="Voice Message">🎤</button>
        <button class="camera-btn" title="Take Photo">📷</button>
        <button class="gallery-btn" title="Upload Photo">🖼️</button>
    </div>

    <button class="send-btn">Send</button>
</div>
```

### **Attachment Preview**
```html
<div class="attachment-preview" id="attachmentPreview" style="display: none;">
    <div class="preview-items">
        <!-- Dynamic preview items -->
    </div>
    <button class="clear-attachments">Clear All</button>
</div>
```

## 🗂️ **JOB TABS SYSTEM**

### **Tab Creation Logic**
```javascript
class JobTabManager {
    constructor() {
        this.activeTabs = new Map(); // jobId -> tabData
        this.activeJobId = null;
    }

    createTab(jobInfo) {
        const tabId = `job-${jobInfo.job_id}`;

        if (!this.activeTabs.has(jobInfo.job_id)) {
            const tab = {
                id: jobInfo.job_id,
                title: jobInfo.title,
                customer: jobInfo.customer_name,
                conversationHistory: [],
                context: jobInfo
            };

            this.activeTabs.set(jobInfo.job_id, tab);
            this.renderTab(tab);
        }

        this.switchToTab(jobInfo.job_id);
    }

    switchToTab(jobId) {
        this.activeJobId = jobId;
        this.updateActiveTab();
        this.loadConversationHistory(jobId);
        this.updateJobContext(this.activeTabs.get(jobId).context);
    }
}
```

## 🎤 **VOICE & MEDIA FEATURES**

### **Voice Message Recording**
```javascript
class VoiceRecorder {
    async startRecording() {
        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.mediaRecorder = new MediaRecorder(this.stream);

        this.chunks = [];
        this.mediaRecorder.ondataavailable = (e) => this.chunks.push(e.data);
        this.mediaRecorder.onstop = () => this.processRecording();

        this.mediaRecorder.start();
        this.showRecordingUI();
    }

    stopRecording() {
        this.mediaRecorder.stop();
        this.stream.getTracks().forEach(track => track.stop());
    }

    processRecording() {
        const blob = new Blob(this.chunks, { type: 'audio/wav' });
        this.uploadVoiceMessage(blob);
    }
}
```

### **Photo Capture**
```javascript
class PhotoCapture {
    async capturePhoto() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });

            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();

            // Show camera preview modal
            this.showCameraPreview(video, stream);
        } catch (err) {
            // Fallback to file input
            this.showFileInput();
        }
    }
}
```

## 🔄 **CONVERSATION FLOW**

### **Example User Journey**
1. **Tech logs in** → Current LBOB interface
2. **Tech types**: "I'm having issues at ABC Manufacturing"
3. **UI expands** → LBOB shrinks, chat area grows
4. **Job context appears** → "Fire Alarm Inspection - ABC Manufacturing"
5. **LBOB responds** → "I see you're working on the fire alarm inspection..."
6. **Conversation continues** → Full history visible, scrollable
7. **Tech mentions different job** → New tab appears automatically
8. **Tech can switch tabs** → Different job contexts

### **Smart Context Recognition**
```javascript
function analyzeMessage(message, aiResponse) {
    // Extract job indicators from AI response
    const jobPatterns = [
        /working on.*?([A-Z][a-z]+.*?(?:job|inspection|installation))/i,
        /job.*?(\w+[-]\d+)/i,
        /at\s+([A-Z][a-z\s]+(?:Building|Center|Plaza))/i
    ];

    // Check if new job context detected
    const jobInfo = extractJobContext(aiResponse);
    if (jobInfo && jobInfo.job_id !== currentJobId) {
        createJobTab(jobInfo);
        switchToJob(jobInfo.job_id);
    }
}
```

This design keeps LBOB central while intelligently adapting to job context through natural conversation - exactly what you described!