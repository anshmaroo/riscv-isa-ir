import ast


# which functional unit does this instruction need?
def functional_unit(tree: ast.Module):
    func_def = next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    )

    for decorator in func_def.decorator_list:
        if isinstance(decorator, ast.Call):  # @instr(...)  with arguments
            for keyword in decorator.keywords:
                if keyword.arg == "instruction_type":
                    return ast.unparse(keyword.value)
    return None
