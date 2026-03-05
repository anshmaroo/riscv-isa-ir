import ast


def extract_mem_reads(tree: ast.Module):
    mem_reads = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            match node:
                case ast.Subscript(
                    value=ast.Attribute(
                        value=ast.Name(id="state"),
                        attr="mem",
                    ),
                    ctx=ast.Load()
                ):
                    mem_reads.append(node.slice)
    return mem_reads


def extract_mem_writes(tree: ast.Module):
    mem_writes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            match node:
                case ast.Subscript(
                    value=ast.Attribute(
                        value=ast.Name(id="state"),
                        attr="mem",
                    ),
                    ctx=ast.Store()
                ):
                    mem_writes.append(node.slice)
    return mem_writes


def coalesce_mem_ops(mem_ops: list[ast.Subscript]):
    coalescing: dict[str, set[int]] = {}
    for mem_op in mem_ops:
        match mem_op:
            case ast.Name(ctx=ast.Load()):
                coalescing[mem_op.id] = coalescing.get(mem_op.id, set()) | {0}
            case ast.BinOp(
                op=ast.Add(),
                left=ast.Name(ctx=ast.Load()),
            ):
                coalescing[mem_op.left.id] = coalescing.get(mem_op.left.id, set()) | {mem_op.right.value}
    assert len(coalescing) <= 1, "At most one memory read is allowed"
    if len(coalescing) == 1:
        read_ops = coalescing.popitem()[1]
        assert read_ops == set(range(max(read_ops) + 1)), "Memory read size must be consecutive"
        return len(read_ops)
    else:
        return 0


def extract_slice_size(slice_node: ast.Slice) -> str | int | None:
    """
    Matches:
        base : base + size   -> returns param name "size"  (dynamic)
        base : base + 4      -> returns literal 4          (static)
        0    : size          -> returns param name "size"  (dynamic)
        0    : 4             -> returns literal 4          (static)
    """
    match slice_node:
        # state.mem[base : base + size]  or  state.mem[base : base + 4]
        case ast.Slice(
            lower=ast.Name() as lower,
            upper=ast.BinOp(
                op=ast.Add(),
                left=ast.Name(id=lower.id),  # upper starts where lower starts
                right=rhs,
            ),
        ):
            if isinstance(rhs, ast.Name):
                return rhs.id        # dynamic: return param name
            if isinstance(rhs, ast.Constant):
                return rhs.value     # static: return literal
        # state.mem[0 : size]  or  state.mem[0 : 4]
        case ast.Slice(
            lower=ast.Constant(value=0),
            upper=ast.Name() as upper,
        ):
            return upper.id
        case ast.Slice(
            lower=ast.Constant(value=0),
            upper=ast.Constant() as upper,
        ):
            return upper.value
    return None


def extract_slice_mem_ops(tree: ast.Module) -> list[str | int]:
    """
    Finds all slice-based memory accesses (reads or writes) in the tree
    and returns their sizes (param name or literal).
    """
    sizes = []
    for node in ast.walk(tree):
        match node:
            case ast.Subscript(
                value=ast.Attribute(attr="mem"),
                slice=ast.Slice() as s,
            ):
                size = extract_slice_size(s)
                if size is not None:
                    sizes.append(size)
    return sizes


def get_mem_read_size(tree: ast.Module) -> int | str:
    # First try slice-based access
    slice_sizes = extract_slice_mem_ops(tree)
    if slice_sizes:
        assert len(slice_sizes) == 1, "At most one memory slice is allowed"
        return slice_sizes[0]  # str (param name) or int (literal)

    # Fall back to element-wise static access
    mem_reads = extract_mem_reads(tree)
    return coalesce_mem_ops(mem_reads)


def get_mem_write_size(tree: ast.Module) -> int | str:
    slice_sizes = extract_slice_mem_ops(tree)
    if slice_sizes:
        assert len(slice_sizes) == 1, "At most one memory slice is allowed"
        return slice_sizes[0]

    mem_writes = extract_mem_writes(tree)
    return coalesce_mem_ops(mem_writes)