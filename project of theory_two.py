from graphviz import Digraph

class CFGParser:
    def __init__(self):#
        self.grammar = {} #Initializes an empty dictionary to store the grammar rules.
        self.start_symbol = '' # Initializes an empty string to store the start symbol of the grammar .The first rule added (via add_rule) automatically sets this.
        self.node_count = 0 #A counter to track nodes when drawing the parse tree (used in _draw_tree).Ensures each node in the tree has a unique ID (e.g., node1, node2)

    def add_rule(self, rule): ## Adds grammar rules in the form A -> B C | D (split into A -> B C and A -> D).
        head, body = rule.split('->')
        head = head.strip() # Removes leading and trailing whitespace from the head of the rule. ex: Turns "S " → "S"
        bodies = [b.strip().split() for b in body.strip().split('|')] # Splits the body of the rule into separate productions  
        #and removes whitespace. ex: Turns "A B | C" → [["A", "B"], ["C"]]
        if not self.start_symbol: 
            self.start_symbol = head 
        if head in self.grammar: # If the head already exists, append the new bodies to the existing list.
            self.grammar[head].extend(bodies) # Extends the list of productions for the head with the new bodies.
        else:
            self.grammar[head] = bodies #Grammar before: {"S": [ ["A", "B"] ]} Add "A -> a" → Grammar after: {"S": [ ["A", "B"] ], "A": [ ["a"] ]}

    def parse_input(self, input_string)# This is the method you call to check if a string (like "a b") is valid according to the grammar rules you added earlier.
        tokens = input_string.strip().split() #Converts the input into a format the parser can work with.
        success, tree, final_pos = self._parse(self.start_symbol, tokens, 0)# Calls the recursive parser starting from the start symbol.
        if success and final_pos == len(tokens): # final pos is The index of the next token to be parsed in the input string. 
            print("Valid string!")
            self._draw_tree(tree)
        else:
            print("Invalid string!")

    def _parse(self, symbol, tokens, pos):#Recursive helper for parsing (top-down approach).This is a helper method that tries to match a part of the input string (tokens) to a grammar rule starting with symbol.
        #The list of input tokens (e.g., ["a", "b"]).The current position in the tokens list
        if symbol not in self.grammar:  # Terminal
            if pos < len(tokens) and symbol == tokens[pos]:
                return True, (symbol, []), pos + 1
            return False, None, pos

        for production in self.grammar[symbol]:
            # Handle epsilon production
            if len(production) == 1 and production[0] == 'ε':
                return True, (symbol, [('ε', [])]), pos
            
            children = []
            current_pos = pos
            matched = True
            for sym in production:
                success, subtree, current_pos = self._parse(sym, tokens, current_pos)
                if not success:
                    matched = False
                    break
                children.append(subtree)
            if matched:
                return True, (symbol, children), current_pos
        return False, None, pos

    def _count_leaves(self, tree): #Counts the number of leaves in the parse tree.
        symbol, children = tree #Unpacks the tree into its symbol and children.
        if not children:# If there are no children, it's a leaf node.
            return 1 
        return sum(self._count_leaves(child) for child in children) #Recursively counts the leaves in each child and sums them up.

    def _draw_tree(self, tree): #Generates a visual parse tree using Graphviz
        dot = Digraph()
        self._add_nodes(dot, tree)
        dot.render('parse_tree', view=True, format='png')
        print("Parse tree saved as 'parse_tree.png'")

    def _add_nodes(self, dot, tree, parent=None): #Helper for constructing the parse tree graph
        symbol, children = tree
        self.node_count += 1
        node_id = f'node{self.node_count}'
        dot.node(node_id, symbol)
        if parent:
            dot.edge(parent, node_id)
        for child in children:
            self._add_nodes(dot, child, node_id)

# ----------------------------

# Usage
parser = CFGParser() # # This triggers __init__()
print("Enter your grammar rules (e.g., 'S -> A | B' or 'A -> ε'). Type 'done' when finished:")
while True:
    rule = input()
    if rule.lower() == 'done':
        break
    parser.add_rule(rule)

input_string = input("Enter a string to parse (tokens separated by space, or empty for epsilon): ")
parser.parse_input(input_string)