# Document & File Attachment System Design

## 🗂️ EXISTING FOUNDATION

### Current Database Models (Already Implemented)
```sql
-- Documents table for organized file management
documents (
    document_id, title, description,
    file_path, file_type, file_size,
    equipment_type_id, document_category,
    company_id, uploaded_by, download_count
)

-- Generic attachments for any table
attachments (
    attachment_id, filename, original_filename,
    file_path, file_size, mime_type,
    attached_to_table, attached_to_id,  -- Can attach to jobs, equipment, conversations
    uploaded_by, upload_date
)
```

## 🎯 IMPLEMENTATION PLAN

### Phase 1: Basic File Upload API
```python
# Add to app/routes/attachments.py
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    attached_to_table: str = Form(...),  # "jobs", "equipment", "conversations"
    attached_to_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type and size
    allowed_types = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx', 'txt']
    max_size = 10 * 1024 * 1024  # 10MB

    # Create secure filename and storage path
    secure_filename = f"{uuid4()}_{file.filename}"
    file_path = f"uploads/{attached_to_table}/{attached_to_id}/{secure_filename}"

    # Save file and create database record
    attachment = Attachment(
        filename=secure_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file.size,
        mime_type=file.content_type,
        attached_to_table=attached_to_table,
        attached_to_id=attached_to_id,
        uploaded_by=current_user.user_id
    )
```

### Phase 2: Job-Specific Document Management
```python
# Job document endpoints
@router.get("/jobs/{job_id}/attachments")
def get_job_attachments(job_id: int, ...):
    # Return all files attached to specific job

@router.post("/jobs/{job_id}/upload")
async def upload_job_document(job_id: int, file: UploadFile, ...):
    # Upload file specifically to job

@router.get("/equipment/{equipment_id}/attachments")
def get_equipment_attachments(equipment_id: int, ...):
    # Return all files for specific equipment (manuals, photos, etc.)
```

### Phase 3: AI Context Integration
```python
# Enhance AI service to include document context
def generate_ai_response(self, db, conversation, user_message):
    context_parts = [self.base_context]

    # Add document context if job has attachments
    if conversation.job_id:
        job_attachments = db.query(Attachment).filter(
            Attachment.attached_to_table == "jobs",
            Attachment.attached_to_id == conversation.job_id
        ).all()

        if job_attachments:
            doc_context = "Available job documents:\n"
            for att in job_attachments:
                doc_context += f"- {att.original_filename} ({att.file_type})\n"
            context_parts.append(doc_context)
```

## 🖥️ FRONTEND IMPLEMENTATION

### Job Selection with Document Access
```javascript
// Enhanced job interface showing documents
function displayJobDetails(job) {
    return `
        <div class="job-card">
            <h3>${job.title} (${job.job_number})</h3>
            <p>Customer: ${job.customer_name}</p>
            <p>Status: ${job.status}</p>

            <!-- Document section -->
            <div class="job-documents">
                <h4>Job Documents</h4>
                <div class="document-list" id="docs-${job.job_id}">
                    <!-- Loaded via API call -->
                </div>
                <button onclick="uploadDocument(${job.job_id})" class="upload-btn">
                    📎 Upload Document
                </button>
            </div>

            <button onclick="startJobConversation(${job.job_id})" class="start-chat-btn">
                💬 Chat with LBOB about this job
            </button>
        </div>
    `;
}

// File upload interface
async function uploadDocument(jobId) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.pdf,.jpg,.jpeg,.png,.doc,.docx,.txt';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('attached_to_table', 'jobs');
            formData.append('attached_to_id', jobId);

            const response = await fetch('/attachments/upload', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });

            if (response.ok) {
                loadJobDocuments(jobId); // Refresh document list
            }
        }
    };
    input.click();
}
```

### Document Display in Conversations
```javascript
// Show relevant documents in LBOB chat interface
function displayJobContext(jobId) {
    return `
        <div class="job-context-panel">
            <h4>📋 Job Context</h4>
            <div id="job-details-${jobId}"></div>

            <h4>📎 Available Documents</h4>
            <div id="job-documents-${jobId}" class="document-thumbnails">
                <!-- Document previews with click to view -->
            </div>

            <h4>🔧 Equipment</h4>
            <div id="job-equipment-${jobId}"></div>
        </div>
    `;
}
```

## 📱 MOBILE CONSIDERATIONS

### React Native File Upload
```typescript
// Mobile file upload for job documents
import DocumentPicker from 'react-native-document-picker';
import { launchImageLibrary } from 'react-native-image-picker';

const uploadJobDocument = async (jobId: number) => {
    try {
        const result = await DocumentPicker.pick({
            type: [DocumentPicker.types.pdf, DocumentPicker.types.images],
        });

        const formData = new FormData();
        formData.append('file', {
            uri: result[0].uri,
            type: result[0].type,
            name: result[0].name,
        });
        formData.append('attached_to_table', 'jobs');
        formData.append('attached_to_id', jobId.toString());

        const response = await fetch(`${API_URL}/attachments/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
            body: formData,
        });
    } catch (err) {
        console.log('Document upload error:', err);
    }
};
```

## 🔐 SECURITY CONSIDERATIONS

### File Security
```python
# Secure file handling
ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def secure_filename(filename: str) -> str:
    # Remove dangerous characters, limit length
    import re
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename[:100]  # Limit filename length

def validate_file_type(file: UploadFile) -> bool:
    # Check file extension and mime type
    extension = Path(file.filename).suffix.lower()
    return extension in ALLOWED_EXTENSIONS

# Access control
def check_file_access(user: User, attachment: Attachment, db: Session) -> bool:
    # Verify user has access to the job/equipment this file is attached to
    if attachment.attached_to_table == "jobs":
        job = db.query(Job).filter(Job.job_id == attachment.attached_to_id).first()
        return job and (
            job.assigned_user_id == user.user_id or
            job.company_id == user.company_id
        )
```

## 📊 DOCUMENT CATEGORIES

### Job Documents
- **Permits**: Building permits, work orders
- **Manuals**: Equipment manuals, installation guides
- **Photos**: Equipment photos, site photos, before/after
- **Reports**: Inspection reports, test results
- **Diagrams**: Wiring diagrams, floor plans

### Equipment Documents
- **Manuals**: Manufacturer manuals, technical specs
- **Maintenance**: Maintenance logs, service records
- **Photos**: Equipment photos, label photos
- **Warranties**: Warranty information, service agreements

### Conversation Documents
- **Screenshots**: Error messages, display screens
- **Photos**: Problem areas, equipment issues
- **Sketches**: Hand-drawn diagrams, notes

## 🚀 IMPLEMENTATION PHASES

### Phase 1: Basic Upload (Week 1)
- File upload API endpoints
- Basic frontend upload interface
- Database storage of file metadata

### Phase 2: Job Integration (Week 2)
- Job-specific document management
- Document display in job selection
- Basic AI context integration

### Phase 3: Enhanced Features (Week 3)
- Image preview/thumbnails
- Document search and filtering
- Advanced AI document analysis

### Phase 4: Mobile Support (Week 4)
- React Native file upload
- Mobile document viewing
- Camera integration for photos

The attachment system foundation is already in the database - we just need to build the upload/display interfaces!