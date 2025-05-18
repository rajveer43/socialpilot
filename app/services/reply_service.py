from datetime import datetime
from ..services.llm_service import llm_service
from ..database import store_reply

class ReplyService:
    async def generate_and_store_reply(self, platform: str, post_text: str):
        """Generate a reply and store it in the database."""
        try:
            if llm_service is None:
                raise Exception("LLM service is not initialized. Please check your GROQ_API_KEY environment variable.")

            # Generate reply using LLM
            generated_reply = await llm_service.generate_reply(platform, post_text)
            
            # Store in database
            timestamp = datetime.utcnow().isoformat()
            stored_reply = await store_reply(
                platform=platform,
                post_text=post_text,
                generated_reply=generated_reply,
                timestamp=timestamp
            )
            
            return {
                "reply": generated_reply,
                "platform": platform,
                "post_text": post_text,
                "timestamp": timestamp
            }
        except Exception as e:
            raise Exception(f"Error in reply generation process: {str(e)}")

# Create a singleton instance
reply_service = ReplyService() 