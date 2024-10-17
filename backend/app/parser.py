from lark import Lark, Transformer, exceptions

grammar = """
?start: expression

?expression: expression "AND" expression   -> and_expr
           | expression "OR" expression    -> or_expr
           | "(" expression ")"
           | condition

?condition: field COMPARATOR value         -> condition

field: CNAME

COMPARATOR: ">" | "<" | "="

value: QUOTED_STRING                      -> string
     | SIGNED_NUMBER                      -> number

%import common.CNAME
%import common.SIGNED_NUMBER
%import common.WS
%ignore WS

QUOTED_STRING: SINGLE_QUOTED_STRING | DOUBLE_QUOTED_STRING
SINGLE_QUOTED_STRING: /'[^']*'/
DOUBLE_QUOTED_STRING: /"[^"]*"/
"""

parser = Lark(grammar, start='start')

# Transformer to convert parse tree to AST
class ASTTransformer(Transformer):
    def and_expr(self, items):
        return {
            'type': 'operator',
            'operator': 'AND',
            'left': items[0],
            'right': items[1]
        }

    def or_expr(self, items):
        return {
            'type': 'operator',
            'operator': 'OR',
            'left': items[0],
            'right': items[1]
        }

    def condition(self, items):
        field = items[0]        
        operator = items[1].value     
        value = items[2]['value']
        operand = {
            'field': field,
            'operator': operator,
            'value': value
        }
        return {
            'type': 'operand',
            'operand': operand
        }

    def field(self, items):
        return items[0].value  

    def string(self, items):
        raw_string = str(items[0])
        if raw_string.startswith("'") and raw_string.endswith("'"):
            return {'value': raw_string[1:-1]}
        elif raw_string.startswith('"') and raw_string.endswith('"'):
            return {'value': raw_string[1:-1]}
        else:

            return {'value': raw_string}

    def number(self, items):
        return {'value': float(items[0])}


def parse_rule(rule_string):
    try:
        tree = parser.parse(rule_string)
        transformer = ASTTransformer()
        ast = transformer.transform(tree)
        return ast
    except exceptions.LarkError as e:
        raise ValueError(f"Failed to parse rule: {e}")