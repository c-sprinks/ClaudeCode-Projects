from langchain_ollama import OllamaLLM
from sqlalchemy.orm import Session
from app.models import Conversation, ConversationMessage, Solution, Equipment, Job, User
from typing import Optional, List, Dict, Any
import json
import re
from datetime import datetime

class AIService:
    def __init__(self):
        self.ollama_llm = OllamaLLM(
            model="llama3.1:8b",
            base_url="http://localhost:11434"
        )

        self.system_prompt = """
        You are LBOB (Lightning Brain On Board), an expert AI assistant for field technicians
        specializing in fire alarm systems, access control, networking, and cyber-security.

        Your expertise includes:
        - Fire alarm panel troubleshooting and programming
        - Access control system installation and maintenance
        - Network configuration and security
        - Cyber-security best practices

        Always provide clear, step-by-step instructions.
        Reference specific equipment models when possible.
        Ask clarifying questions when needed.
        Be helpful, professional, and thorough in your responses.
        """

    def generate_ai_response(
        self,
        db: Session,
        conversation: Conversation,
        user_message: str,
        equipment_id: Optional[int] = None
    ) -> str:
        """Generate AI response using direct LLM approach with job context"""

        try:
            # Get conversation history
            messages = db.query(ConversationMessage).filter(
                ConversationMessage.conversation_id == conversation.conversation_id
            ).order_by(ConversationMessage.timestamp).all()

            # Build enhanced context with job information
            context = self._build_enhanced_context(db, conversation, equipment_id, user_message)

            # Build conversation history string
            history_text = ""
            for msg in messages[-10:]:  # Last 10 messages for context
                if msg.sender_type == "user":
                    history_text += f"Human: {msg.message_text}\n"
                else:
                    history_text += f"LBOB: {msg.message_text}\n"

            # Create complete prompt with job-aware context
            full_prompt = self._create_job_aware_prompt(context, history_text, user_message)

            # Generate response using direct LLM invocation
            response = self.ollama_llm.invoke(full_prompt)

            return response.strip() if isinstance(response, str) else str(response).strip()

        except Exception as e:
            # Log the actual error for debugging
            print(f"AI SERVICE ERROR: {str(e)}")
            print(f"ERROR TYPE: {type(e).__name__}")
            import traceback
            traceback.print_exc()

            # Fallback response if AI service fails
            return f"I'm here to help with your technical issue. You mentioned: '{user_message}'. Could you provide more specific details about what you're experiencing? For example, what type of equipment are you working with and what specific problem are you encountering?"

    def detect_job_references(self, db: Session, user_id: int, message: str) -> Optional[Dict[str, Any]]:
        """Detect job references in user messages"""

        # Get user's jobs for correlation
        user_jobs = db.query(Job).filter(Job.assigned_user_id == user_id).all()

        message_lower = message.lower()

        # Job reference patterns
        patterns = [
            r'(?:job|work|working)\s+(?:at|on)\s+([A-Z][a-zA-Z\s]+(?:building|center|plaza|manufacturing|corp|inc))',
            r'(\w+\s+manufacturing|\w+\s+building|\w+\s+center)',
            r'(?:at|on)\s+([0-9]+\s+[A-Z][a-zA-Z\s]+(?:street|st|avenue|ave|boulevard|blvd|road|rd))',
            r'(?:customer|client)\s+([A-Z][a-zA-Z\s]+)',
            r'job\s+(?:number|#)?\s*([A-Z0-9-]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                reference = match.group(1).strip()

                # Find matching job
                for job in user_jobs:
                    if (reference.lower() in (job.customer_name or "").lower() or
                        reference.lower() in (job.customer_address or "").lower() or
                        reference.lower() in (job.title or "").lower() or
                        reference.lower() in (job.job_number or "").lower()):

                        return {
                            "job_id": job.job_id,
                            "job_number": job.job_number,
                            "title": job.title,
                            "customer_name": job.customer_name,
                            "customer_address": job.customer_address,
                            "status": job.status,
                            "priority": job.priority,
                            "job_type": job.job_type,
                            "description": job.description,
                            "confidence": 0.8  # High confidence for exact matches
                        }

        return None

    def _build_enhanced_context(
        self,
        db: Session,
        conversation: Conversation,
        equipment_id: Optional[int],
        user_message: str
    ) -> Dict[str, Any]:
        """Build enhanced context with job correlation"""

        context = {
            "system_info": self.system_prompt,
            "conversation_title": conversation.title,
            "equipment_info": None,
            "job_info": None,
            "user_jobs": [],
            "relevant_solutions": [],
            "detected_job": None
        }

        # Get user information
        user = db.query(User).filter(User.user_id == conversation.user_id).first()
        if user:
            # Get all user's jobs for reference
            user_jobs = db.query(Job).filter(Job.assigned_user_id == user.user_id).all()
            context["user_jobs"] = [
                {
                    "job_id": job.job_id,
                    "job_number": job.job_number,
                    "title": job.title,
                    "customer_name": job.customer_name,
                    "customer_address": job.customer_address,
                    "status": job.status
                } for job in user_jobs
            ]

            # Detect job references in current message
            detected_job = self.detect_job_references(db, user.user_id, user_message)
            if detected_job:
                context["detected_job"] = detected_job

        # Add current job context if conversation is linked to job
        if conversation.job_id:
            current_job = db.query(Job).filter(Job.job_id == conversation.job_id).first()
            if current_job:
                context["job_info"] = {
                    "job_id": current_job.job_id,
                    "job_number": current_job.job_number,
                    "title": current_job.title,
                    "customer_name": current_job.customer_name,
                    "customer_address": current_job.customer_address,
                    "status": current_job.status,
                    "priority": current_job.priority,
                    "job_type": current_job.job_type,
                    "description": current_job.description
                }

                # Get equipment for this job
                job_equipment = db.query(Equipment).filter(
                    Equipment.job_id == current_job.job_id
                ).all()

                context["job_equipment"] = [
                    {
                        "equipment_id": eq.equipment_id,
                        "name": eq.equipment_name,
                        "manufacturer": eq.manufacturer,
                        "model": eq.model_number,
                        "serial": eq.serial_number,
                        "location": eq.location_description
                    } for eq in job_equipment
                ]

        # Add equipment context if available
        if equipment_id or conversation.equipment_id:
            eq_id = equipment_id or conversation.equipment_id
            equipment = db.query(Equipment).filter(
                Equipment.equipment_id == eq_id
            ).first()

            if equipment:
                context["equipment_info"] = {
                    "equipment_id": equipment.equipment_id,
                    "name": equipment.equipment_name,
                    "manufacturer": equipment.manufacturer,
                    "model": equipment.model_number,
                    "serial": equipment.serial_number,
                    "location": equipment.location_description,
                    "job_id": equipment.job_id
                }

        # Find relevant solutions
        relevant_solutions = db.query(Solution).filter(
            Solution.is_verified == True
        ).order_by(Solution.average_rating.desc()).limit(3).all()

        context["relevant_solutions"] = [
            {
                "title": sol.title,
                "problem": sol.problem_description[:200] + "..." if len(sol.problem_description) > 200 else sol.problem_description,
                "solution": sol.solution_steps[:200] + "..." if len(sol.solution_steps) > 200 else sol.solution_steps
            } for sol in relevant_solutions
        ]

        return context

    def _create_job_aware_prompt(self, context: Dict[str, Any], history_text: str, user_message: str) -> str:
        """Create job-aware prompt with enhanced context"""

        prompt = context["system_info"] + "\n\n"

        # Add current job context if available
        if context.get("job_info"):
            job = context["job_info"]
            prompt += f"""
CURRENT JOB CONTEXT:
- Job Number: {job['job_number']}
- Job Title: {job['title']}
- Customer: {job['customer_name']}
- Address: {job['customer_address']}
- Job Type: {job['job_type']}
- Status: {job['status']}
- Priority: {job['priority']}
- Description: {job['description']}

IMPORTANT: When the user mentions job details, locations, or customer names,
correlate them with this current job information.
"""

        # Add detected job information
        if context.get("detected_job"):
            detected = context["detected_job"]
            if not context.get("job_info") or detected["job_id"] != context["job_info"]["job_id"]:
                prompt += f"""
DETECTED JOB REFERENCE:
The user seems to be referring to: {detected['title']} ({detected['job_number']})
Customer: {detected['customer_name']}
Address: {detected['customer_address']}

NOTE: This appears to be different from the current conversation job.
Ask for clarification or suggest switching context.
"""

        # Add user's jobs for reference
        if context.get("user_jobs"):
            prompt += "\nUSER'S ACTIVE JOBS FOR REFERENCE:\n"
            for job in context["user_jobs"][:5]:  # Limit to 5 most recent
                prompt += f"- {job['job_number']}: {job['title']} at {job['customer_address']}\n"

        # Add equipment context
        if context.get("job_equipment"):
            prompt += "\nJOB EQUIPMENT:\n"
            for eq in context["job_equipment"]:
                prompt += f"- {eq['name']} ({eq['manufacturer']} {eq['model']}) at {eq['location']}\n"

        if context.get("equipment_info"):
            eq = context["equipment_info"]
            prompt += f"\nCURRENT EQUIPMENT FOCUS:\n"
            prompt += f"- {eq['name']} ({eq['manufacturer']} {eq['model']})\n"
            prompt += f"- Serial: {eq['serial']}\n"
            prompt += f"- Location: {eq['location']}\n"

        # Add conversation instructions
        prompt += """
JOB CORRELATION INSTRUCTIONS:
- If user mentions a location/address, match it to current job or reference jobs
- If user mentions customer names, correlate with job customer information
- If user mentions job titles/types, identify which job they're referring to
- If user asks about "this job" or "current job", use the CURRENT JOB CONTEXT
- If user mentions different job details, ask for clarification or suggest job switch
- Always provide job-specific, contextual responses when possible
"""

        # Add conversation history
        if history_text:
            prompt += f"\nCONVERSATION HISTORY:\n{history_text}\n"

        # Add current message
        prompt += f"\nCURRENT MESSAGE: {user_message}\n\n"
        prompt += "RESPONSE (as LBOB, incorporating job context and being helpful):"

        return prompt

    def _build_context(
        self,
        db: Session,
        conversation: Conversation,
        equipment_id: Optional[int]
    ) -> dict:
        """Build context information for AI response"""
        context = {
            "system_info": self.system_prompt,
            "conversation_title": conversation.title,
            "equipment_info": None,
            "relevant_solutions": []
        }

        # Add equipment context if available
        if equipment_id or conversation.equipment_id:
            eq_id = equipment_id or conversation.equipment_id
            equipment = db.query(Equipment).filter(
                Equipment.equipment_id == eq_id
            ).first()

            if equipment:
                context["equipment_info"] = {
                    "name": equipment.equipment_name,
                    "manufacturer": equipment.manufacturer,
                    "model": equipment.model_number,
                    "location": equipment.location_description
                }

        # Find relevant solutions
        relevant_solutions = db.query(Solution).filter(
            Solution.is_verified == True
        ).order_by(Solution.average_rating.desc()).limit(3).all()

        context["relevant_solutions"] = [
            {
                "title": sol.title,
                "problem": sol.problem_description[:200] + "..." if len(sol.problem_description) > 200 else sol.problem_description,
                "solution": sol.solution_steps[:200] + "..." if len(sol.solution_steps) > 200 else sol.solution_steps
            } for sol in relevant_solutions
        ]

        return context

    def _create_complete_prompt(self, context: dict, history_text: str, user_message: str) -> str:
        """Create complete prompt with system info, context, history, and current message"""

        prompt = context["system_info"] + "\n\n"

        prompt += "Current Context:\n"
        prompt += f"- Conversation: {context['conversation_title']}\n"

        if context.get("equipment_info"):
            prompt += f"- Equipment: {context['equipment_info'].get('name', 'Unknown')} "
            prompt += f"({context['equipment_info'].get('manufacturer', '')} {context['equipment_info'].get('model', '')})\n"
            prompt += f"- Location: {context['equipment_info'].get('location', '')}\n"

        prompt += "\nAvailable Solutions Database:\n"
        prompt += self._format_solutions(context["relevant_solutions"])
        prompt += "\n"

        if history_text.strip():
            prompt += "Previous conversation:\n"
            prompt += history_text + "\n"

        prompt += f"Human: {user_message}\n"
        prompt += "LBOB:"

        return prompt

    def _format_solutions(self, solutions: List[dict]) -> str:
        """Format solutions for prompt context"""
        if not solutions:
            return "No relevant solutions found in database."

        formatted = ""
        for i, sol in enumerate(solutions, 1):
            formatted += f"{i}. {sol['title']}\n"
            formatted += f"   Problem: {sol['problem']}\n"
            formatted += f"   Solution: {sol['solution']}\n\n"

        return formatted

# Create global AI service instance
ai_service = AIService()