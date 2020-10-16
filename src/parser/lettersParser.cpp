#include "parser/lettersParser.hpp"

using namespace Parser;

LettersParser::LettersParser() { regex = std::regex("^[A-Za-z]+"); }

State* LettersParser::Run(State* state) {
    if (state->IsError) {
        return state;
    }

    if (state->Input.empty() || (unsigned int)state->Input.size() < (unsigned int)state->Index + 1) {
        return setErrorState(state, "LettersParser: got unexpected end of input");
    }

    auto toCheck = state->Input.substr(state->Index);
    std::sregex_token_iterator it(toCheck.begin(), toCheck.end(), regex, 0);
    std::sregex_token_iterator end;

    if (it == end) {
        return setErrorState(state, "LettersParser: couldn't match letters at index '" + std::to_string(state->Index) + "'");
    }

    state->Result = *it;
    state->Index = state->Index + it->length();
    state->IsError = false;
    state->Error = "";
    return state;
}