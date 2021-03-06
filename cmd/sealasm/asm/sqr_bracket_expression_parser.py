from typing import List, Tuple, Dict, Any

import parser_combinator as parser

from asm.variable_parser import VariableParser
from asm.operator_parser import OperatorParser
from asm.parenthesis_expression_parser import ParenthesisExpressionParser
from asm.map_methods import _sqr_expr_as_type, _hex_value_as_type, _operator_value_as_type, \
    _var_value_as_type, _parenthesis_expr_as_type


class SqrBracketState():
    "enum for SqrBracketExpressionParser state machine, only used within the context of this file"
    EXPECT_ELEMENT: int = 0
    EXPECT_OPERATOR: int = 1
    END: int = 2


class SqrBracketExpressionParser(parser.BaseParser):
    "parses square bracket expressions for the SealASM grammer"

    def __init__(self, runner: parser.Runner, map_method: Any = None):
        self._runner: parser.Runner = runner
        self._whitespace_opt = parser.WhitespaceParser(optional=True)
        super().__init__(map_method)

    def run(self, state: parser.State) -> parser.State:
        "state machine for processing square-bracket expressions"
        if state.is_error:
            return state

        # get opening and optional whitespace
        state = self._runner.run(parser.CharParser(locate="["), state.source, state=state)
        if state.is_error:
            return state

        state = self._runner.run(self._whitespace_opt, state.source, state=state)
        if state.is_error:
            return state

        # process expression
        expr: List[parser.State] = []
        sm_state = SqrBracketState.EXPECT_ELEMENT

        while sm_state != SqrBracketState.END:
            # all added states to 'expr' list are copies to avoid overwrites
            if sm_state == SqrBracketState.EXPECT_ELEMENT:
                state, sm_state = self._expect_element(expr, state)
            elif sm_state == SqrBracketState.EXPECT_OPERATOR:
                state, sm_state = self._expect_operator(expr, state)

        if state.is_error:
            return state

        return parser.State(source=state.source, result=expr, index=state.index).map(self._map_method)

    def _expect_element(self, expr: List[parser.State], state: parser.State) -> Tuple[parser.State, int]:
        "processes the next element from a choice of parsers, skips any whitespace"
        state = self._runner.choice(
            (
                SqrBracketExpressionParser(self._runner, map_method=_sqr_expr_as_type),     # type: ignore
                ParenthesisExpressionParser(self._runner, map_method=_parenthesis_expr_as_type),
                parser.HexParser(map_method=_hex_value_as_type),
                VariableParser(self._runner, map_method=_var_value_as_type),
            ),
            state.source,
            state=state
        )

        if state.is_error:
            return state, SqrBracketState.END

        expr.append(parser.State(state=state))
        return self._runner.run(self._whitespace_opt, state.source, state=state), SqrBracketState.EXPECT_OPERATOR

    def _expect_operator(self, expr: List[parser.State], state: parser.State) -> Tuple[parser.State, int]:
        "checks if the next char is a closing bracket, if not it expects an operator, skips any whitespace"
        state = self._runner.peek(parser.CharParser(), state.source, state=state)
        if state.is_error:
            return state, SqrBracketState.END

        sm_state = SqrBracketState.EXPECT_ELEMENT

        if state.result == "]":
            # consume and skip optional whitespace, flag to exit state machine
            state = self._runner.run(parser.CharParser(), state.source, state=state)
            state = self._runner.run(self._whitespace_opt, state.source, state=state)
            sm_state = SqrBracketState.END
        else:
            # get operator, keep expect element flag for state machine
            state = self._runner.run(OperatorParser(self._runner), state.source, state=state).map(_operator_value_as_type)
            if state.is_error:
                return state, SqrBracketState.END
            expr.append(parser.State(state=state))

        return self._runner.run(self._whitespace_opt, state.source, state=state), sm_state
