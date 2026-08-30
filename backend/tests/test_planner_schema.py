import pytest

from backend.app.schemas.planner_schema import (
    DrawingPlan,
    DrawingPlanStep,
)


def test_drawing_plan_step():

    step = DrawingPlanStep(
        step=1,
        title="Establish the composition",
        category="placement",
        instruction="Mark the overall placement.",
        purpose="Establish the subject position.",
        difficulty="beginner",
        confidence=0.95,
        confidence_level="high",
    )

    assert step.step == 1
    assert step.confidence == 0.95


def test_drawing_plan():

    plan = DrawingPlan(
        step_count=1,
        steps=[
            DrawingPlanStep(
                step=1,
                title="Establish the composition",
                category="placement",
                instruction="Mark the overall placement.",
                purpose="Establish the subject position.",
                difficulty="beginner",
                confidence=0.95,
                confidence_level="high",
            )
        ],
    )

    assert plan.step_count == 1
    assert len(plan.steps) == 1


def test_invalid_confidence():

    with pytest.raises(ValueError):
        DrawingPlanStep(
            step=1,
            title="Test",
            category="placement",
            instruction="Test",
            purpose="Test",
            difficulty="beginner",
            confidence=1.5,
            confidence_level="high",
        )