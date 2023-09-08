"""
This code provides a basic framework for a parser named `CompilerParser` designed to transform a sequence of tokens into a parse tree. The tokens are expected to represent syntactical constructs in some programming language, and the parser is intended to capture the hierarchical structure of these constructs in the form of a tree.

Classes and Main Functionalities:
1. `ParseException`: 
    - A custom exception class raised when an encountered token does not match the expected syntax during parsing.

2. `CompilerParser`:
    - `__init__(self, tokens)`: Initializes the parser with a list of tokens and sets the current token index to 0.
    - `next(self)`: Advances the current token index to point to the next token.
    - `current(self)`: Returns the current token based on the current token index.
    - `have(self, expectedType, expectedValue)`: Checks if the current token matches the expected type and value.
    - `mustBe(self, expectedType, expectedValue)`: Verifies if the current token matches the expected type and value. If true, it returns the current token and advances to the next one; otherwise, raises a ParseException.
    - There are other stub methods like `compileProgram`, `compileClass`, etc., which are placeholders intended to be filled out with logic for parsing specific constructs.

Sample Usage:
In the `__main__` section, an example usage is provided. A list of tokens representing a basic class structure in some programming language is created. This list is then passed to an instance of the `CompilerParser` which attempts to parse the tokens and generate a parse tree. If any errors are encountered during parsing, a message indicating a parsing error is printed.
"""



from ParseTree import *

class CompilerParser:

    def __init__(self, tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.tokens = tokens
        self.current_idx = 0

    # ... [the other methods remain unchanged]

    def next(self):
        """
        Advance to the next token
        """
        if self.current_idx < len(self.tokens) - 1:
            self.current_idx += 1

    def current(self):
        """
        Return the current token
        @return the token
        """
        if 0 <= self.current_idx < len(self.tokens):
            return self.tokens[self.current_idx]
        return None

    def have(self, expectedType, expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        curr = self.current()
        return curr and curr.getType() == expectedType and curr.getValue() == expectedValue

    def mustBe(self, expectedType, expectedValue=None):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        if self.have(expectedType, expectedValue):
            current_token = self.current()
            self.next()
            return current_token
        raise ParseException(f"Expected token of type {expectedType} and value {expectedValue} but got {self.current().getType()} with value {self.current().getValue()}.")

if __name__ == "__main__":

    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword", "class"))
    tokens.append(Token("identifier", "MyClass"))
    tokens.append(Token("symbol", "{"))
    tokens.append(Token("symbol", "}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")
