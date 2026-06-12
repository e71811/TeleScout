from typing import Dict, List

class StateManager:
    def __init__(self):
        # Main storage mapping user_id (int) to their conversation history (list of dicts)
        self._states: Dict[int, List[Dict[str, str]]] = {}

    async def add_message(self, user_id: int, role: str, content: str) -> None:
        """Adds a new message to the specific user's conversation history."""
        if user_id not in self._states:
            self._states[user_id] = []
            
        message_obj = {"role": role, "content": content}
        self._states[user_id].append(message_obj)

    async def get_history(self, user_id: int) -> List[Dict[str, str]]:
        """Retrieves the complete conversation history for a specific user."""
        if user_id not in self._states:
            return []
        return self._states[user_id]

    async def clear_history(self, user_id: int) -> None:
        """Clears the conversation history for a specific user."""
        if user_id in self._states:
            self._states[user_id].clear()