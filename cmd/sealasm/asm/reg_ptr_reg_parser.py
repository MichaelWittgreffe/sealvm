from typing import Tuple, Any, List, Dict

import parser_combinator as parser

from asm.asm_parser_base import ASMParser
from asm.sqr_bracket_expression_parser import SqrBracketExpressionParser
from asm.map_methods import _register_as_type


class RegPtrRegParser(ASMParser):
    "parses a '{register_ptr}, {register}' instruction for the SealASM grammer"

    def __init__(self, runner: parser.Runner, instruction_mnemonic: str, instruction: str, map_method: Any = None):
        super().__init__(runner, instruction_mnemonic, instruction, map_method=map_method)

    def run(self, state: parser.State) -> parser.State:
        instruction_args: List[Dict[str, Any]] = []

        # get instruction
        state = self._upper_or_lower_string(self._instruction_mnemonic, state.source, state)
        if state.is_error:
            return state

        state = self._whitespace(state)
        if state.is_error:
            return state

        # get source register pointer
        state = self._register(state.source, state, ptr=True).map(_register_as_type)
        if state.is_error:
            return state
        instruction_args.append(self._state_to_ast(state))

        state = self._comma_skip_whitespace(state)
        if state.is_error:
            return state

        # get target register, skip optional whitespace
        state = self._register(state.source, state).map(_register_as_type)
        if state.is_error:
            return state
        instruction_args.append(self._state_to_ast(state))

        state = self._optional_whitespace(state)
        if state.is_error:
            return state

        # setup result tree
        result = {
            "type": self._instruction_mnemonic,
            "value": {
                "instruction": self._instruction,
                "args": instruction_args,
            }
        }
        return parser.State(source=state.source, result=result, index=state.index)
