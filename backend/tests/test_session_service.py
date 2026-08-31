from backend.app.services.session_service import (
    save_session,
    get_session,
    add_message,
    get_conversation,
    get_current_step,
    set_current_step,
)


def test_save_and_get_session():

    save_session(
        "test-id",
        {"composition": {}},
        {"steps": []},
    )

    session = get_session("test-id")

    assert session is not None
    assert session["analysis"] == {
        "composition": {}
    }
    assert session["drawing_plan"] == {
        "steps": []
    }
    assert session["conversation"] == []


def test_add_message():

    save_session(
        "conversation-test",
        {},
        {},
    )

    add_message(
        "conversation-test",
        "user",
        "What should I draw first?",
    )

    add_message(
        "conversation-test",
        "assistant",
        "Start with the main form.",
    )

    conversation = get_conversation(
        "conversation-test"
    )

    assert len(conversation) == 2

    assert conversation[0]["role"] == "user"
    assert (
        conversation[0]["content"]
        == "What should I draw first?"
    )

    assert conversation[1]["role"] == "assistant"
    assert (
        conversation[1]["content"]
        == "Start with the main form."
    )


def test_missing_session_conversation():

    conversation = get_conversation(
        "does-not-exist"
    )

    assert conversation == []

def test_current_step():

    save_session(
        "progress-test",
        {},
        {
            "steps": [
                {"step": 1},
                {"step": 2},
            ]
        },
    )

    assert get_current_step(
        "progress-test"
    ) == 1

    set_current_step(
        "progress-test",
        2,
    )

    assert get_current_step(
        "progress-test"
    ) == 2