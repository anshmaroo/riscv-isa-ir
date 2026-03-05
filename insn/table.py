from types import NoneType
from typing import Callable
import inspect
import ast
import atexit
import passes.functional_unit
import passes.register
import passes.mem

# Global registry accumulating decode table rows
_decode_table: list[dict] = []


def _generate_chisel_table():
    if not _decode_table:
        return

    col_headers = [
        "valid",
        "br_type",
        "rs1",
        "rs2",
        "rd",
        "mrs1",
        "mrs2",
        "mrd",
        "pc",
        "instr_type",
        "alu_op",
        "vpu_op",
    ]

    # Compute column widths
    name_width = max(len(r["name"]) for r in _decode_table)
    col_widths = {h: len(h) for h in col_headers}
    for row in _decode_table:
        for h in col_headers:
            col_widths[h] = max(col_widths[h], len(str(row[h])))

    def fmt_row(name, values: dict, arrow="->") -> str:
        name_part = f"    {name:<{name_width}}"
        vals = ", ".join(str(values[h]).ljust(col_widths[h]) for h in col_headers)
        return f"{name_part} {arrow} List({vals})"

    # Header comment
    header_vals = {h: h for h in col_headers}
    print("\n// Auto-generated decode table")
    print("// " + fmt_row("instruction", header_vals, arrow="  ").lstrip())
    print("val table: Array[(BitPat, List[BitPat])] = Array(")

    rows = []
    for row in _decode_table:
        rows.append(fmt_row(row["name"], row))
    print(",\n".join(rows))
    print(")")


def instr(fn: Callable = None, *, name=None, instruction_type=None):
    def _run(fn):
        func_name = fn.__name__
        instr_name = (name or func_name).upper()

        src = inspect.getsource(fn)
        tree = ast.parse(src)

        # Valid
        valid = passes.register.is_valid_instruction(tree)

        # BR_TYPE
        br_type = passes.register.test_conditional_assignment(tree)

        # Register reads/writes
        rs1 = passes.register.has_register_read_rs1(tree)
        rs2 = passes.register.has_register_read_rs2(tree)
        rd = passes.register.has_register_write_rd(tree)
        mrs1 = passes.register.has_register_read_mrs1(tree)
        mrs2 = passes.register.has_register_read_mrs2(tree)
        mrd = passes.register.has_register_write_mrd(tree)

        # PC update
        pc = passes.register.has_pc_assignment(tree)

        # Functional unit
        instr_type_val = passes.functional_unit.instruction_type(tree)

        # ALU op
        alu_op = passes.functional_unit.scalar_alu_op(tree)
        match type(alu_op).__name__:
            case "NoneType":
                alu_op_str = "ALU_OP_X"
            case _:
                alu_op_str = f"ALU_OP_{type(alu_op).__name__.upper()}"

        # VPU op
        vpu_op = passes.functional_unit.vector_op(tree)

        def _bool(v) -> str:
            if v is True:
                return "Y"
            if v is False:
                return "N"
            return str(v) if v is not None else "X"

        _decode_table.append(
            {
                "name": instr_name,
                "valid": _bool(valid),
                "br_type": str(br_type) if br_type is not None else "BR_X",
                "rs1": _bool(rs1),
                "rs2": _bool(rs2),
                "rd": _bool(rd),
                "mrs1": _bool(mrs1),
                "mrs2": _bool(mrs2),
                "mrd": _bool(mrd),
                "pc": _bool(pc),
                "instr_type": (
                    str(instr_type_val) if instr_type_val is not None else "X"
                ),
                "alu_op": alu_op_str,
                "vpu_op": ("VPU_OP_" + str(vpu_op).upper()) if vpu_op is not None else "VPU_X",
            }
        )

        return fn

    if fn is not None:
        return _run(fn)
    else:
        return _run



