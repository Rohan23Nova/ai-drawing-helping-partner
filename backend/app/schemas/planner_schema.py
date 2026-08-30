from pydantic import BaseModel, Field


class DrawingPlanStep(BaseModel):
    step: int = Field(ge=1)
    title: str
    category: str
    instruction: str
    purpose: str
    difficulty: str
    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )
    confidence_level: str


class DrawingPlan(BaseModel):
    step_count: int = Field(ge=1)
    steps: list[DrawingPlanStep]