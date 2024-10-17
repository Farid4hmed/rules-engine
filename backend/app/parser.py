from lark import Lark, Transformer, v_args

grammar = """
?start: expression

?expression: expression "AND" expression   -> and_expr
           | expression "OR" expression    -> or_expr
           | "(" expression ")"
           | condition

?condition: field comparator value         -> condition

field: CNAME

comparator: ">" | "<" | "="

value: SIGNED_NUMBER                       -> number
     | ESCAPED_STRING                      -> string

%import common.CNAME
%import common.SIGNED_NUMBER
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='start')

class ASTTransformer(Transformer):
    def and_expr(self, items):
        return {'type': 'operator', 'operator': 'AND', 'left': items[0], 'right': items[1]}

    def or_expr(self, items):
        return {'type': 'operator', 'operator': 'OR', 'left': items[0], 'right': items[1]}

    def condition(self, items):
        field = str(items[0])
        operator = str(items[1])
        value = items[2]
        if isinstance(value, dict):
            value = value['value']
        operand = {'field': field, 'operator': operator, 'value': value}
        return {'type': 'operand', 'operand': operand}

    def number(self, items):
        return {'value': float(items[0])}

    def string(self, items):
        return {'value': str(items[0]).strip('"')}

def parse_rule(rule_string):
    tree = parser.parse(rule_string)
    transformer = ASTTransformer()
    ast = transformer.transform(tree)
    return ast