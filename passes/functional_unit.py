import ast
import passes.register


# which functional unit does this instruction need?
def instruction_type(tree: ast.Module):
    func_def = next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    )

    for decorator in func_def.decorator_list:
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == "instruction_type":
                    return ast.unparse(keyword.value)
    return None


def scalar_alu_op(tree: ast.Module) -> ast.operator():
    # is there a register assignment in the body?
    assignments = passes.register.extract_assignments(tree)
    for assignment in assignments:
        match assignment:
            case ast.Assign(
                value=ast.BinOp(op=operator)
            ):
                return operator
    return None
