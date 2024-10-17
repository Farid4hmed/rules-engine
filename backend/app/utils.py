def combine_asts(asts):
    if not asts:
        return None
    combined_ast = asts[0]
    for ast in asts[1:]:
        combined_ast = {
            'type': 'operator',
            'operator': 'AND',
            'left': combined_ast,
            'right': ast
        }
    return combined_ast