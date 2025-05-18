"""
This module implements a LangChain-based agent system for generating social media replies.
The agent uses a chain of specialized tools to analyze posts, create personas, and generate
contextually appropriate replies. This approach allows for more sophisticated and nuanced
responses by breaking down the reply generation process into distinct steps:

1. Post Analysis: Analyzes sentiment, tone, and key topics
2. Persona Creation: Generates a contextually appropriate responder persona
3. Reply Generation: Creates the final reply using the analysis and persona

The agent uses the Groq LLM API with the Llama 4 model for all operations.
"""

# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.agents import initialize_agent, AgentType, Tool
# from langchain.schema import HumanMessage

# load_dotenv()

# # Initialize Groq LLM
# def get_groq_llm():
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         raise ValueError("GROQ_API_KEY environment variable is not set")
#     return ChatGroq(
#         api_key=api_key,
#         model_name="meta-llama/llama-4-scout-17b-16e-instruct",
#         temperature=0.7
#     )

# # Define tools for the agent
# analyze_tool = Tool(
#     name="analyze_post",
#     func=lambda post: get_groq_llm().invoke(
#         [HumanMessage(content=f"Analyze sentiment, tone, topics for: {post}")]
#     ).content,
#     description="Analyze sentiment, tone, and key topics of a social media post"
# )

# persona_tool = Tool(
#     name="create_persona",
#     func=lambda ctx: get_groq_llm().invoke(
#         [HumanMessage(content="Generate a detailed persona based on: " + ctx)]
#     ).content,
#     description="Create a responder persona based on analysis and platform"
# )

# reply_tool = Tool(
#     name="generate_reply",
#     func=lambda args: get_groq_llm().invoke(
#         [HumanMessage(content=args)]
#     ).content,
#     description="Generate the final reply using analysis, persona, and platform guidelines"
# )

# # Instantiate an agent with tools
# agent = initialize_agent(
#     tools=[analyze_tool, persona_tool, reply_tool],
#     llm=get_groq_llm(),
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# class LLMService:
#     def __init__(self):
#         self.agent = agent

#     async def generate_reply(self, platform: str, post_text: str) -> str:
#         # Kick off the agent, passing platform and text as context
#         input_str = f"Platform: {platform}\nPost: {post_text}"
#         result = self.agent.run(input_str)
#         return result

# # Singleton instance
# try:
#     llm_service = LLMService()
# except Exception as e:
#     print(f"Error initializing LLMService: {e}")
#     llm_service = None




"""
This module implements a sophisticated prompt chain approach for generating social media replies using the Groq LLM API.
The system employs a multi-step process to create contextually appropriate and platform-specific responses:

1. Post Analysis Chain:
   - Analyzes sentiment, tone, and key topics
   - Identifies emotional context and themes
   - Provides structured analysis for downstream processing

2. Persona Generation Chain:
   - Creates platform-specific personas
   - Defines personality traits and communication style
   - Establishes response patterns and interests

3. Reply Generation Chain:
   - Combines analysis and persona insights
   - Applies platform-specific guidelines
   - Generates natural, contextually appropriate responses

The system uses temperature and token controls to maintain response quality:
- Analysis: Low temperature (0.3) for consistent analysis
- Persona: Medium temperature (0.5) for creative but controlled persona generation
- Reply: Higher temperature (0.7) with penalties for natural variation

This approach ensures responses are:
- Platform-appropriate
- Contextually relevant
- Naturally varied
- Authentically human-like
"""

import os
from groq import Groq
from dotenv import load_dotenv
from typing import Dict, Any, List
import httpx

load_dotenv()

my_client = httpx.Client(timeout=60.0)

class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
        self.client = Groq(api_key=api_key, http_client=my_client)
        self.model = "meta-llama/llama-4-scout-17b-16e-instruct"

    def _get_platform_prompt(self, platform: str) -> str:
        """Get platform-specific prompt instructions."""
        prompts = {
            "twitter": """You are a Twitter user. Your replies should be:
            - Concise (under 280 characters)
            - Casual and conversational
            - Use emojis naturally
            - Include hashtags when relevant
            - Match the tone of the original post""",
            
            "linkedin": """You are a LinkedIn professional. Your replies should be:
            - Professional and insightful
            - Focus on value and expertise
            - Use industry-specific terminology
            - Maintain a business-appropriate tone
            - Include relevant professional context""",
            
            "instagram": """You are an Instagram user. Your replies should be:
            - Friendly and engaging
            - Use emojis liberally
            - Include relevant hashtags
            - Match the visual/creative nature of Instagram
            - Be authentic and personal"""
        }
        return prompts.get(platform, prompts["twitter"])

    async def _analyze_post(self, post_text: str) -> Dict[str, Any]:
        """Analyze the post's sentiment, tone, and key topics."""
        analysis_prompt = f"""Analyze this social media post and provide:
        1. Sentiment (positive/negative/neutral)
        2. Tone (formal/casual/professional/friendly)
        3. Key topics or themes
        4. Any specific emotions expressed
        
        Post: {post_text}
        
        Provide the analysis in a structured format."""

        messages = [
            {"role": "system", "content": "You are an expert at analyzing social media content."},
            {"role": "user", "content": analysis_prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=200
        )
        return {"analysis": response.choices[0].message.content.strip()}

    async def _generate_persona(self, platform: str, analysis: Dict[str, Any]) -> str:
        """Generate a persona based on platform and post analysis."""
        persona_prompt = f"""Based on the following analysis and platform, create a detailed persona:
        Platform: {platform}
        Analysis: {analysis['analysis']}
        
        Include:
        1. Personality traits
        2. Communication style
        3. Typical interests
        4. Response patterns"""

        messages = [
            {"role": "system", "content": "You are an expert at creating authentic social media personas."},
            {"role": "user", "content": persona_prompt}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    async def generate_reply(self, platform: str, post_text: str) -> str:
        """Generate a human-like reply using a multi-step approach."""
        # Step 1: Analyze the post
        analysis = await self._analyze_post(post_text)
        
        # Step 2: Generate persona
        persona = await self._generate_persona(platform, analysis)
        
        # Step 3: Generate the reply
        platform_prompt = self._get_platform_prompt(platform)
        
        system_prompt = f"""You are an expert at generating human-like social media replies.
        {platform_prompt}
        
        Use this persona to guide your response:
        {persona}
        
        Post analysis:
        {analysis['analysis']}
        
        Follow these steps:
        1. Ensure the reply matches the analyzed sentiment and tone
        2. Incorporate relevant topics from the analysis
        3. Maintain the persona's characteristics
        4. Generate a reply that feels natural and authentic
        
        Avoid:
        - Generic or overly formal language
        - Repetitive patterns
        - AI-like responses
        - Excessive punctuation or emojis
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate a reply to this {platform} post:\n\n{post_text}"}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=150,
                top_p=0.9,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating reply: {str(e)}")

# Create a singleton instance
try:
    llm_service = LLMService()
except ValueError as e:
    print(f"Warning: {str(e)}")
    llm_service = None



"""
This module implements a direct LLM-based approach for generating social media replies.
The approach uses a single-step generation process with platform-specific prompting.

Key characteristics:
- Uses Groq's LLM API with the Llama 4 Scout model
- Implements platform-specific prompting for Twitter, LinkedIn, and Instagram
- Single-step generation process without intermediate analysis
- Configurable generation parameters (temperature, tokens, etc.)
- Simple error handling and singleton pattern

Trade-offs:
+ Simpler implementation with fewer API calls
+ Lower latency due to single-step generation
+ More straightforward error handling
- Less nuanced responses without intermediate analysis
- No explicit sentiment or tone analysis
- Limited context awareness compared to multi-step approaches
"""

# import os
# from groq import Groq
# from dotenv import load_dotenv
# from typing import Dict, Any
# import httpx

# load_dotenv()

# my_client = httpx.Client(timeout=60.0)

# class LLMService:
#     def __init__(self):
#         api_key = os.getenv("GROQ_API_KEY")
#         if not api_key:
#             raise ValueError("GROQ_API_KEY environment variable is not set")
#         self.client = Groq(api_key=api_key, http_client=my_client)
#         self.model = "meta-llama/llama-4-scout-17b-16e-instruct"  

#     def _get_platform_prompt(self, platform: str) -> str:
#         """Get platform-specific prompt instructions."""
#         prompts = {
#             "twitter": """You are a Twitter user. Your replies should be:
#             - Concise (under 280 characters)
#             - Casual and conversational
#             - Use emojis naturally
#             - Include hashtags when relevant
#             - Match the tone of the original post""",
            
#             "linkedin": """You are a LinkedIn professional. Your replies should be:
#             - Professional and insightful
#             - Focus on value and expertise
#             - Use industry-specific terminology
#             - Maintain a business-appropriate tone
#             - Include relevant professional context""",
            
#             "instagram": """You are an Instagram user. Your replies should be:
#             - Friendly and engaging
#             - Use emojis liberally
#             - Include relevant hashtags
#             - Match the visual/creative nature of Instagram
#             - Be authentic and personal"""
#         }
#         return prompts.get(platform, prompts["twitter"])

#     async def generate_reply(self, platform: str, post_text: str) -> str:
#         """Generate a human-like reply using Groq LLM."""
#         platform_prompt = self._get_platform_prompt(platform)
        
#         system_prompt = f"""You are an expert at generating human-like social media replies.
#         {platform_prompt}
        
#         Follow these steps:
#         1. Analyze the post's content and context
#         2. Determine the appropriate tone and style
#         3. Generate a reply that feels natural and authentic
#         4. Ensure the reply matches the platform's characteristics
        
#         Avoid:
#         - Generic or overly formal language
#         - Repetitive patterns
#         - AI-like responses
#         - Excessive punctuation or emojis
#         """

#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": f"Generate a reply to this {platform} post:\n\n{post_text}"}
#         ]

#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=messages,
#                 temperature=0.7,
#                 max_tokens=150,
#                 top_p=0.9,
#                 frequency_penalty=0.5,
#                 presence_penalty=0.5
#             )
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             raise Exception(f"Error generating reply: {str(e)}")

# # Create a singleton instance
# try:
#     llm_service = LLMService()
# except ValueError as e:
#     print(f"Warning: {str(e)}")
#     llm_service = None 