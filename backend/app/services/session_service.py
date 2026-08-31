_sessions = {}


def save_session(
    image_id: str,
    analysis: dict,
    drawing_plan: dict,
) -> None:

    _sessions[image_id] = {
        "analysis": analysis,
        "drawing_plan": drawing_plan,
        "conversation": [],
        "current_step": 1,
    }


def get_session(
    image_id: str,
) -> dict | None:

    return _sessions.get(image_id)


def add_message(
    image_id: str,
    role: str,
    content: str,
) -> None:

    session = _sessions.get(image_id)

    if session is None:
        return

    session["conversation"].append(
        {
            "role": role,
            "content": content,
        }
    )


def get_conversation(
    image_id: str,
) -> list[dict]:

    session = _sessions.get(image_id)

    if session is None:
        return []

    return session["conversation"]
def get_current_step(
    image_id: str,
) -> int | None:

    session = _sessions.get(image_id)

    if session is None:
        return None

    return session["current_step"]


def set_current_step(
    image_id: str,
    step: int,
) -> None:

    session = _sessions.get(image_id)

    if session is None:
        return

    session["current_step"] = step