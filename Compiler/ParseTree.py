"""
The `ParseTree` module provides a foundational structure for constructing hierarchical trees that represent syntactical constructs in source code. This module is particularly useful for capturing the structural nature of programming languages and serves as a basis for compiler or interpreter implementations.

Classes and Main Functionalities:
1. `ParseException`: 
    - A custom exception class used for signaling errors during the parsing process. It is intended to be raised when an encountered sequence of tokens does not fit the expected syntax or grammar.

2. `ParseTree`:
    - A representation of a node in a tree structure.
    - `__init__(self, node_type, value)`: Initializes a node with a specified type and an optional value.
    - `addChild(self, child)`: Appends a child node (another ParseTree instance) to the current node.
    - `getChildren(self)`: Retrieves the children nodes of the current node.
    - `getType(self)`: Obtains the type of the current node which provides context on the kind of syntactical construct the node represents.
    - `getValue(self)`: Fetches the value of the node, typically used for terminal nodes.
    - `__str__(self, depth=0)`: Generates a visual, indented representation of the tree for debugging or display purposes.

3. `Token` (which inherits from `ParseTree`):
    - Represents the smallest unit of syntactic meaning in the source code. It acts as the leaf nodes in the tree structure and typically contains actual lexemes from the source code.

Overall, this module forms the structural backbone for transforming a flat list of tokens (produced by a lexer, for instance) into a hierarchical tree that captures the nested nature of programming languages.

Here's a brief summary of the ParseTree() class' methods:

addChild(child): Adds a ParseTree as a child of the current ParseTree.
getChildren(): Returns the child nodes of the current ParseTree.
getType(): Returns the type of the current ParseTree.
getValue(): Returns the value of the current ParseTree.
__str__(depth=0): Returns a string representation of the ParseTree.
"""

class ParseException(Exception):
    """
    Raised when tokens provided don't match the expected grammar
    Use this with `raise ParseException("My error message")`
    """
    def __init__(self, message="An error occurred while parsing."):
        self.message = message
        super().__init__(self.message)


class ParseTree():
    def __init__(self, node_type, value=""):
        """
        A node in a Parse Tree data structure.
        @param node_type: The type of node.
        @param value: The node's value. Should only be used on terminal nodes/leaves, and empty otherwise.
        """
        self.node_type = node_type
        self.value = value
        self.children = []
    
    def addChild(self, child):
        """
        Adds a ParseTree as a child of this ParseTree.
        @param child: The ParseTree to add.
        """
        self.children.append(child)

    def getChildren(self):
        """
        Get a list of child nodes in the order they were added.
        @return: A list of ParseTrees.
        """
        return self.children

    def getType(self):
        """
        Get the type of this ParseTree Node.
        @return: The type of node.
        """
        return self.node_type

    def getValue(self):
        """
        Get the value of this ParseTree Node.
        @return: The node's value. Should only be used on terminal nodes/leaves, and empty otherwise.
        """
        return self.value

    def __str__(self, depth=0):
        """
        Generate a string from this ParseTree.
        @return: A printable representation of this ParseTree with indentation.
        """        
        # Set indentation
        indent = ""
        for i in range(depth):
            indent += "  \u2502 "
        
        # Generate output
        output = ""
        if self.children:
            # Output if the node has children
            output += indent + self.node_type + "\n"
            for child in self.children:
                output += indent + "  \u2514 " + child.__str__(depth+1)
        else:
            # Output if the node is a leaf/terminal
            output += indent + self.node_type
            if self.value:
                output += " " + str(self.value)
            output += "\n"
        
        return output

    
class Token(ParseTree):
    """
    Token for parsing. Can be used as a terminal node in a ParseTree.
    """
    def __init__(self, token_type, token_value):
        super().__init__(token_type, token_value)