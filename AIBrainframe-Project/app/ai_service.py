from langchain_ollama import OllamaLLM
from sqlalchemy.orm import Session
from app.models import Conversation, ConversationMessage, Solution, Equipment
from typing import Optional, List
import json
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
        """Generate AI response using direct LLM approach"""

        try:
            # Get conversation history
            messages = db.query(ConversationMessage).filter(
                ConversationMessage.conversation_id == conversation.conversation_id
            ).order_by(ConversationMessage.timestamp).all()

            # Build context
            context = self._build_context(db, conversation, equipment_id)

            # Build conversation history string
            history_text = ""
            for msg in messages[-10:]:  # Last 10 messages for context
                if msg.sender_type == "user":
                    history_text += f"Human: {msg.message_text}\n"
                else:
                    history_text += f"LBOB: {msg.message_text}\n"

            # Create complete prompt with history
            full_prompt = self._create_complete_prompt(context, history_text, user_message)

            # Generate response using direct LLM invocation (bypasses ConversationChain validation)
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