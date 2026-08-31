from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    image_id: str
    message: str = Field(
        min_length=1,
        max_length=1000,
    )


class ChatResponse(BaseModel):
    image_id: str
    message: str
    response: str