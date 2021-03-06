from typing import Any

from parser_combinator.state import State


class BaseParser():
    "base class for parsers"

    def __init__(self, map_method: Any = None):
        self._map_method: Any = map_method

    def run(self, state: State) -> State:
        "base method, override with derived classes. Should return a COPY of the source state"
        raise NotImplementedError("Not Implemented")

    def _set_error_state(self, state: State, error: str) -> State:
        "sets the error state on the given state and returns"
        state.error = error
        state.is_error = True
        return state
