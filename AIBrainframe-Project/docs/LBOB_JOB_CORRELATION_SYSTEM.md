# LBOB Job Correlation System Design

## 🧠 INTELLIGENT JOB MATCHING

### Current Conversation Context (Already Available)
```python
# In ai_service.py - conversation already linked to job_id
conversation.job_id  # Direct job reference
conversation.equipment_id  # Equipment reference
```

### Enhanced AI Context with Job Correlation
```python
def generate_ai_response(self, db, conversation, user_message, equipment_id=None):
    context_parts = [self.base_context]

    # Get current job context if conversation is linked to job
    current_job = None
    if conversation.job_id:
        current_job = db.query(Job).filter(Job.job_id == conversation.job_id).first()

        if current_job:
            job_context = f"""
            CURRENT JOB CONTEXT:
            - Job Number: {current_job.job_number}
            - Job Title: {current_job.title}
            - Customer: {current_job.customer_name}
            - Address: {current_job.customer_address}
            - Job Type: {current_job.job_type}
            - Status: {current_job.status}
            - Priority: {current_job.priority}
            - Description: {current_job.description}

            IMPORTANT: When the user mentions job details, locations, or customer names,
            correlate them with this current job information.
            """
            context_parts.append(job_context)

    # Add all user's jobs for reference/correlation
    user_jobs = db.query(Job).filter(Job.assigned_user_id == conversation.user_id).all()
    if user_jobs:
        jobs_reference = "USER'S OTHER JOBS FOR REFERENCE:\n"
        for job in user_jobs:
            jobs_reference += f"- {job.job_number}: {job.title} at {job.customer_address}\n"
        context_parts.append(jobs_reference)

    # Enhanced prompt for job correlation
    correlation_prompt = """
    JOB CORRELATION INSTRUCTIONS:
    - If user mentions a location/address, match it to the current job or reference jobs
    - If user mentions customer names, correlate with job customer information
    - If user mentions job titles/types, identify which job they're referring to
    - If user asks about "this job" or "current job", use the CURRENT JOB CONTEXT
    - If user mentions different job details, ask for clarification or suggest job switch
    """
    context_parts.append(correlation_prompt)
```

## 🗣️ CONVERSATION EXAMPLES

### Example 1: Address Recognition
```
User: "I'm having issues with the fire alarm at the Industrial Boulevard location"
LBOB: "I see you're referring to your current job at ABC Manufacturing, 1234 Industrial Blvd.
       This is the Fire Alarm Annual Inspection job (FA-2025-001). What specific issues
       are you encountering with the fire alarm system there?"
```

### Example 2: Customer Name Recognition
```
User: "The ABC Manufacturing folks are asking about the panel status"
LBOB: "Perfect! Since you're working on the ABC Manufacturing job at 1234 Industrial Blvd,
       I can help with panel status information. Are you referring to the main fire alarm
       control panel or a specific zone panel?"
```

### Example 3: Job Title/Type Recognition
```
User: "How long should this annual inspection take?"
LBOB: "For your current Fire Alarm Annual Inspection at ABC Manufacturing, based on the
       job details showing 2 Siemens panels and 15 smoke detectors, a typical annual
       inspection should take approximately 3-4 hours. This includes testing all devices,
       checking connections, and documenting results."
```

### Example 4: Wrong Job Reference Detection
```
User: "What about the installation at the downtown office?"
LBOB: "I notice you mentioned a downtown office installation, but your current active
       conversation is about the Fire Alarm Annual Inspection at ABC Manufacturing
       (1234 Industrial Blvd). Would you like me to:
       1. Continue with the ABC Manufacturing job, or
       2. Switch to discuss a different job?

       If you'd like to switch jobs, I can help you start a new conversation for
       the downtown office installation."
```

## 🔍 ADVANCED JOB CORRELATION FEATURES

### 1. Fuzzy Matching System
```python
def find_job_by_reference(self, db, user_id, reference_text):
    """Find job by partial name, address, or customer name"""
    user_jobs = db.query(Job).filter(Job.assigned_user_id == user_id).all()

    matches = []
    reference_lower = reference_text.lower()

    for job in user_jobs:
        # Check multiple fields for matches
        if (reference_lower in job.title.lower() or
            reference_lower in job.customer_name.lower() or
            reference_lower in (job.customer_address or "").lower() or
            reference_lower in job.job_number.lower()):
            matches.append(job)

    return matches
```

### 2. Equipment Correlation
```python
# If user mentions specific equipment, correlate with job equipment
equipment_list = db.query(Equipment).filter(
    Equipment.job_id == current_job.job_id
).all()

equipment_context = "JOB EQUIPMENT:\n"
for eq in equipment_list:
    equipment_context += f"- {eq.equipment_name} ({eq.manufacturer} {eq.model_number})\n"
    equipment_context += f"  Serial: {eq.serial_number}, Location: {eq.location_description}\n"
```

### 3. Historical Context from Previous Conversations
```python
# Load previous conversations for this job
previous_conversations = db.query(Conversation).filter(
    Conversation.job_id == current_job.job_id,
    Conversation.conversation_id != conversation.conversation_id
).all()

if previous_conversations:
    history_context = "PREVIOUS CONVERSATIONS FOR THIS JOB:\n"
    for prev_conv in previous_conversations[-3:]:  # Last 3 conversations
        messages = db.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == prev_conv.conversation_id
        ).order_by(ConversationMessage.timestamp.desc()).limit(2).all()

        if messages:
            history_context += f"Previous session: {prev_conv.started_at.strftime('%m/%d')}\n"
            for msg in reversed(messages):
                history_context += f"  {msg.sender_type}: {msg.message_text[:100]}...\n"
```

## 🎯 IMPLEMENTATION PHASES

### Phase 1: Basic Job Context (Week 1)
- Add current job information to AI prompts
- Enable recognition of current job details
- Basic correlation with job title, customer, address

### Phase 2: Multi-Job Awareness (Week 2)
- Include all user jobs in context for reference
- Fuzzy matching for partial job references
- Job switching capabilities

### Phase 3: Advanced Correlation (Week 3)
- Equipment correlation within jobs
- Historical conversation context
- Smart suggestions for job clarification

### Phase 4: Predictive Assistance (Week 4)
- Anticipate likely job references
- Proactive context suggestions
- Learn from user patterns

## 💬 UI ENHANCEMENTS FOR JOB CORRELATION

### Job Context Display in Chat
```javascript
// Show current job context prominently in chat interface
function displayCurrentJobContext(job) {
    return `
        <div class="current-job-banner">
            <span class="job-indicator">📋 Current Job:</span>
            <strong>${job.title}</strong> (${job.job_number})
            <br>
            <span class="customer-info">👤 ${job.customer_name}</span>
            <span class="location-info">📍 ${job.customer_address}</span>
        </div>
    `;
}

// Job switching interface
function displayJobSwitchSuggestion(suggestedJobs) {
    return `
        <div class="job-switch-suggestion">
            <p>🤔 Did you mean one of these jobs?</p>
            ${suggestedJobs.map(job => `
                <button onclick="switchToJob(${job.job_id})" class="job-switch-btn">
                    ${job.title} - ${job.customer_name}
                </button>
            `).join('')}
        </div>
    `;
}
```

## 🧠 SMART CORRELATION EXAMPLES

### Scenario: Tech mentions partial information
```
User: "The customer at the industrial building is asking about completion time"

LBOB Analysis:
✓ Current job: ABC Manufacturing at 1234 Industrial Blvd
✓ "industrial building" matches current job address
✓ Provide context-aware response

LBOB Response: "For the ABC Manufacturing job at 1234 Industrial Blvd, based on
the Fire Alarm Annual Inspection scope, I estimate completion by end of day.
The inspection includes testing 2 Siemens panels and 15 smoke detectors.
Are you currently working on the main panel or the zone testing?"
```

### Scenario: Wrong job reference
```
User: "How do I reset the access control system?"

LBOB Analysis:
✓ Current job: Fire Alarm Annual Inspection
✓ User asking about access control (different system)
✓ Check if user has other jobs with access control
✓ Provide clarification

LBOB Response: "I notice you're asking about access control, but your current
active job is the Fire Alarm Annual Inspection at ABC Manufacturing.

I see you also have an access control installation job at Downtown Office.
Would you like to:
1. Continue with the fire alarm inspection, or
2. Switch to discuss the access control job?

Or if you're asking about access control integration with the fire alarm
system at ABC Manufacturing, I can help with that too!"
```

This intelligent correlation system will make LBOB incredibly intuitive - techs can mention any job detail and LBOB will understand exactly what they're working on!