_sessions = {}


def save_session(
    image_id: str,
    analysis: dict,
    drawing_plan: dict,
) -> None:
    _sessions[image_id] = {
        "analysis": analysis,
        "drawing_plan": drawing_plan,
    }


def get_session(
    image_id: str,
) -> dict | None:
    return _sessions.get(image_id)