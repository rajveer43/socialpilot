from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class ReplyRequest(BaseModel):
    platform: Literal["twitter", "linkedin", "instagram"] = Field(
        ..., description="The social media platform"
    )
    post_text: str = Field(..., description="The text of the post to reply to")

class ReplyResponse(BaseModel):
    reply: str = Field(..., description="The generated reply")
    platform: str = Field(..., description="The social media platform")
    post_text: str = Field(..., description="The original post text")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message") 