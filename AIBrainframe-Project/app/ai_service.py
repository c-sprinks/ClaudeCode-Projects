from langchain_ollama import OllamaLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from sqlalchemy.orm import Session
from app.models import Conversation, ConversationMessage, Solution, Equipment
from typing import Optional, List
import json
from datetime import datetime

class AIService:
    def __init__(self):
        self.ollama_llm = OllamaLLM(
            model="llama3.1",
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
        """Generate AI response using LangChain and context"""

        try:
            # Get conversation history
            messages = db.query(ConversationMessage).filter(
                ConversationMessage.conversation_id == conversation.conversation_id
            ).order_by(ConversationMessage.timestamp).all()

            # Build context
            context = self._build_context(db, conversation, equipment_id)

            # Create conversation chain with memory
            memory = ConversationBufferMemory()

            # Add previous messages to memory (last 10 for context)
            for msg in messages[-10:]:
                if msg.sender_type == "user":
                    memory.chat_memory.add_user_message(msg.message_text)
                else:
                    memory.chat_memory.add_ai_message(msg.message_text)

            # Create conversation chain
            conversation_chain = ConversationChain(
                llm=self.ollama_llm,
                memory=memory,
                prompt=self._create_prompt_template(context),
                verbose=False
            )

            # Generate response
            response = conversation_chain.predict(input=user_message)

            return response

        except Exception as e:
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

    def _create_prompt_template(self, context: dict) -> PromptTemplate:
        """Create dynamic prompt template with context"""
        template = context["system_info"] + """

        Current Context:
        - Conversation: {conversation_title}
        """

        if context.get("equipment_info"):
            template += """
        - Equipment: {equipment_name} ({equipment_manufacturer} {equipment_model})
        - Location: {equipment_location}
            """

        template += """

        Available Solutions Database:
        {relevant_solutions}

        Human: {input}
        AI Assistant:"""

        partial_variables = {
            "conversation_title": context["conversation_title"],
            "relevant_solutions": self._format_solutions(context["relevant_solutions"])
        }

        if context.get("equipment_info"):
            partial_variables.update({
                "equipment_name": context["equipment_info"].get("name", "Unknown"),
                "equipment_manufacturer": context["equipment_info"].get("manufacturer", ""),
                "equipment_model": context["equipment_info"].get("model", ""),
                "equipment_location": context["equipment_info"].get("location", "")
            })

        return PromptTemplate(
            input_variables=["input"],
            template=template,
            partial_variables=partial_variables
        )

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