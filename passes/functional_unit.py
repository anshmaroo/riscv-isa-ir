import ast

# from isa.test import InstructionType
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
    func_def = next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    )

    for decorator in func_def.decorator_list:
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == "instruction_type":
                    match (ast.unparse(keyword.value)):
                        case "InstructionType.SCALAR":

                            assignments = passes.register.extract_assignments(tree)
                            for assignment in assignments:
                                match assignment:
                                    # is there a register assignment in the body?
                                    case ast.Assign(
                                        # targets=[
                                        #     ast.Subscript(
                                        #         value=ast.Attribute(
                                        #             value=ast.Name(id="state"),
                                        #             attr="regfile",
                                        #         ),
                                        #         slice=ast.Name(id="rd"),
                                        #         ctx=ast.Store(),
                                        #     )
                                        # ],
                                        value=ast.BinOp(op=operator),
                                    ):
                                        return operator

                                    # branches/SLT/STLU
                                    case ast.Assign(
                                        value=ast.Compare(
                                            ops=[cmp_op],
                                        ),
                                    ):
                                        return cmp_op

    return None


def vector_op(tree: ast.Module) -> ast.operator():
    func_def = next(
        node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    )
    for decorator in func_def.decorator_list:
        if isinstance(decorator, ast.Call):
            for keyword in decorator.keywords:
                if keyword.arg == "instruction_type":
                    match (ast.unparse(keyword.value)):
                        case "InstructionType.VECTOR":
                            # is there a register assignment in the body?
                            assignments = passes.register.extract_assignments(tree)
                            for assignment in assignments:
                                match assignment:
                                    # basic arithmetic
                                    case ast.Assign(
                                        value=ast.BinOp(op=operator),
                                    ):
                                        return type(operator).__name__

                                    case ast.Assign(value=ast.Call(func=f)):
                                        if isinstance(f, ast.Name):
                                            func_name = f.id
                                        elif isinstance(f, ast.Attribute):
                                            func_name = f.attr
                                        else:
                                            func_name = "complex_call"

                                        return func_name

    return None
