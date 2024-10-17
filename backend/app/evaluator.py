def evaluate_ast(ast, data):
    if ast['type'] == 'operator':
        left_result = evaluate_ast(ast['left'], data)
        right_result = evaluate_ast(ast['right'], data)
        if ast['operator'] == 'AND':
            return left_result and right_result
        elif ast['operator'] == 'OR':
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {ast['operator']}")
    elif ast['type'] == 'operand':
        operand = ast['operand']
        field = operand['field']
        operator = operand['operator']
        value = operand['value']
        return evaluate_condition(data, field, operator, value)
    else:
        raise ValueError(f"Unknown node type: {ast['type']}")

def evaluate_condition(data, field, operator, value):
    if field not in data:
        return False
    data_value = data[field]

    try:
        data_value = float(data_value)
        value = float(value)
    except ValueError:
        data_value = str(data_value)
        value = str(value)

    if operator == '>':
        return data_value > value
    elif operator == '<':
        return data_value < value
    elif operator == '=':
        return data_value == value
    else:
        raise ValueError(f"Unknown operator: {operator}")