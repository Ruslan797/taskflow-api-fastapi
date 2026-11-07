from google.genai import types


MAX_HISTORY_MESSAGES = 10

conversation_memory: dict[int, list[types.Content]] = {}


def get_conversation(
    user_id: int,
) -> list[types.Content]:
    return conversation_memory.get(user_id, [])


def add_to_conversation(
    user_id: int,
    content: types.Content,
) -> None:
    history = conversation_memory.setdefault(
        user_id,
        [],
    )

    history.append(content)

    if len(history) > MAX_HISTORY_MESSAGES:
        del history[:-MAX_HISTORY_MESSAGES]