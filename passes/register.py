import ast


def extract_assignments(tree: ast.Module):
    assignments = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            assignments.append(node)
    return assignments


def extract_conditionals(tree: ast.Module):
    conditionals = []
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            conditionals.append(node)
    return conditionals


def extract_subscripts(tree: ast.Module):
    subscripts = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            subscripts.append(node)
    return subscripts


def is_valid_instruction(node: ast.AST):
    if node is not None:
        return "Y"
    else:
        return "N"


# is there a register assignment in the body?
def has_register_write_rd(tree: ast.Module):
    assignments = extract_assignments(tree)
    for assignment in assignments:
        match assignment:
            case ast.Assign(
                targets=[
                    ast.Subscript(
                        value=ast.Attribute(value=ast.Name(id="state"), attr="regfile"),
                        slice=ast.Name(id="rd"),
                        ctx=ast.Store(),
                    )
                ]
            ):
                return True
    return False


def has_register_read_rs1(tree: ast.Module):
    subscripts = extract_subscripts(tree)
    for subscript in subscripts:
        match subscript:
            case ast.Subscript(
                value=ast.Attribute(value=ast.Name(id="state"), attr="regfile"),
                slice=ast.Name(id="rs1"),
                ctx=ast.Load(),
            ):
                return "OP1_RS1"
    return "OP1_X"


def has_register_read_rs2(tree: ast.Module):
    subscripts = extract_subscripts(tree)
    for subscript in subscripts:
        match subscript:
            case ast.Subscript(
                value=ast.Attribute(value=ast.Name(id="state"), attr="regfile"),
                slice=ast.Name(id="rs2"),
                ctx=ast.Load(),
            ):
                return "OP2_RS2"
    return "OP2_X"


def has_register_read_mrs1(tree: ast.Module):
    subscripts = extract_subscripts(tree)
    for subscript in subscripts:
        match subscript:
            case ast.Subscript(
                value=ast.Attribute(value=ast.Name(id="state"), attr="tensor_regfile"),
                slice=ast.Name(id="mrs1"),
                ctx=ast.Load(),
            ):
                return "OP1_MRS1"
    return "OP1_X"


def has_register_read_mrs2(tree: ast.Module):
    subscripts = extract_subscripts(tree)
    for subscript in subscripts:
        match subscript:
            case ast.Subscript(
                value=ast.Attribute(value=ast.Name(id="state"), attr="tensor_regfile"),
                slice=ast.Name(id="mrs2"),
                ctx=ast.Load(),
            ):
                return "OP2_MRS2"
    return "OP2_X"


# is there a register assignment in the body?
def has_register_write_mrd(tree: ast.Module):
    assignments = extract_assignments(tree)
    for assignment in assignments:
        match assignment:
            case ast.Assign(
                targets=[
                    ast.Subscript(
                        value=ast.Attribute(
                            value=ast.Name(id="state"), attr="tensor_regfile"
                        ),
                        slice=ast.Name(id="mrd"),
                        ctx=ast.Store(),
                    )
                ]
            ):
                return True
    return False


# is there a weight buffer assignment in the body?
def has_wb_write(tree: ast.Module):
    assignments = extract_assignments(tree)
    for assignment in assignments:
        match assignment:
            case ast.Assign(
                targets=[
                    ast.Subscript(
                        value=ast.Attribute(
                            value=ast.Name(id="state"), attr="weight_buffers"
                        ),
                        slice=ast.Name(id="wb"),
                        ctx=ast.Store(),
                    )
                ]
            ):
                return True
    return False


def test_register_assignment(tree: ast.Module):
    assignments = extract_assignments(tree)
    for assignment in assignments:
        if (
            len(assignment.targets) == 1
            and isinstance(assignment.targets[0], ast.Subscript)
            and isinstance(assignment.targets[0].value, ast.Name)
            and assignment.targets[0].value.id == "regfile"
        ):
            print(assignment.value)
            return True
    print("0")
    return False


def has_pc_assignment(tree: ast.Module):
    assignments = extract_assignments(tree)
    for assignment in assignments:
        if (
            len(assignment.targets) == 1
            and isinstance(assignment.targets[0], ast.Attribute)
            and isinstance(assignment.targets[0].value, ast.Name)
            and assignment.targets[0].value.id == "state"
            and assignment.targets[0].attr == "pc"
        ):
            return True
    return False


def test_conditional_assignment(tree: ast.Module):
    conditionals = extract_conditionals(tree)
    for conditional in conditionals:
        if len(conditional.test.ops) != 1:
            continue
        if isinstance(conditional.test.ops[0], ast.Eq):
            return "BR_EQ"
        elif isinstance(conditional.test.ops[0], ast.NotEq):
            return "BR_NE"
        elif isinstance(conditional.test.ops[0], ast.Lt):
            return "BR_LT"
        elif isinstance(conditional.test.ops[0], ast.LtE):
            return "BR_LE"
        elif isinstance(conditional.test.ops[0], ast.Gt):
            return "BR_GT"
    return "BR_N"
