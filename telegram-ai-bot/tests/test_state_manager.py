import pytest
from src.bot.state_manager import StateManager

@pytest.mark.asyncio
async def test_state_separation_per_user():
    """Ensure that conversation histories are strictly isolated between different users."""
    # 1. Arrange: Create a fresh, clean instance of the StateManager for this test
    manager = StateManager()
    user_a = 11111
    user_b = 22222

    #  Add messages for User A and a different message for User B
    await manager.add_message(user_id=user_a, role="user", content="Hello, I am User A")
    await manager.add_message(user_id=user_b, role="user", content="Hello, I am User B")

    #  Verify that histories are completely separated
    history_a = await manager.get_history(user_a)
    history_b = await manager.get_history(user_b)

    assert len(history_a) == 1
    assert history_a[0]["content"] == "Hello, I am User A"
    
    assert len(history_b) == 1
    assert history_b[0]["content"] == "Hello, I am User B"



@pytest.mark.asyncio
async def test_clear_history():
    """Ensure that clearing history only affects the target user and empties their history."""
    manager = StateManager()
    user_a = 11111
    user_b = 22222

    # Add messages for both users
    await manager.add_message(user_id=user_a, role="user", content="Secret message A")
    await manager.add_message(user_id=user_b, role="user", content="Secret message B")

    # Clear history only for User A
    await manager.clear_history(user_a)

    # Fetch updated histories
    history_a = await manager.get_history(user_a)
    history_b = await manager.get_history(user_b)

    # Assertions: User A should be empty, User B must remain untouched
    assert len(history_a) == 0
    assert len(history_b) == 1
    assert history_b[0]["content"] == "Secret message B"


@pytest.mark.asyncio
async def test_get_history_for_non_existent_user():
    """Ensure that fetching history for a user who hasn't interacted yet returns an empty list."""
    manager = StateManager()
    unknown_user = 99999

    history = await manager.get_history(unknown_user)
    
    # Assert that it returns a safe, empty list instead of raising a KeyError or returning None
    assert isinstance(history, list)
    assert len(history) == 0


@pytest.mark.asyncio
async def test_clear_history_for_non_existent_user():
    """Ensure that clearing history for a non-existent user does not raise any exceptions."""
    manager = StateManager()
    unknown_user = 99999

    # This should execute safely without crashing the application
    await manager.clear_history(unknown_user)
    
    # Verify it's still empty and safe
    history = await manager.get_history(unknown_user)
    assert len(history) == 0


@pytest.mark.asyncio
async def test_multi_turn_conversation_sequence():
    """Ensure that the conversation history maintains correct chronological order and roles."""
    manager = StateManager()
    user_id = 55555

    # Simulate a full back-and-forth conversation sequence
    turns = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
        {"role": "user", "content": "Tell me a joke"},
        {"role": "assistant", "content": "Why did the chicken cross the road?"}
    ]

    for turn in turns:
        await manager.add_message(user_id=user_id, role=turn["role"], content=turn["content"])

    history = await manager.get_history(user_id)

    # Assert the length matches exactly
    assert len(history) == 4

    # Assert that the order and content are preserved perfectly
    for i in range(len(turns)):
        assert history[i]["role"] == turns[i]["role"]
        assert history[i]["content"] == turns[i]["content"]