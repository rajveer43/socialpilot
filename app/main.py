from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ReplyRequest, ReplyResponse, ErrorResponse
from .services.reply_service import reply_service

app = FastAPI(
    title="Social Media Reply Generator",
    description="API for generating human-like social media replies using Groq LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/reply",
    response_model=ReplyResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate a reply to a social media post",
    description="Generates a human-like reply for the given social media post using Groq LLM"
)
async def generate_reply(request: ReplyRequest):
    try:
        result = await reply_service.generate_and_store_reply(
            platform=request.platform,
            post_text=request.post_text
        )
        return ReplyResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 