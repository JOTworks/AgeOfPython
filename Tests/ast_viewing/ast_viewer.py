import ast
import json

def ast_to_dict(node):
    if isinstance(node, ast.AST):
        fields = {field: ast_to_dict(getattr(node, field)) for field in node._fields if hasattr(node, field)}
        return {'_type': node.__class__.__name__, **fields}
    elif isinstance(node, list):
        return [ast_to_dict(item) for item in node]
    else:
        return node

def parse_and_convert_to_json(tree):
    return json.dumps(ast_to_dict(tree), indent=2)

def ast_make_readable(tree):
    for node in ast.walk(tree):
        for field in list(node._fields):
            if field == 'type_ignores':
                continue
            value = getattr(node, field, None)
            if (
                value is None 
                or (isinstance(value, list) and not value) 
                or field == 'ctx' and isinstance(value, ast.Load)
            ):
                delattr(node, field)
    return tree