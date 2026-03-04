from typing import Callable
import inspect
import ast
import passes.functional_unit
import passes.register
import passes.mem


def instr(fn: Callable = None, *, name=None, instruction_type=None):
    def _run(fn):
        src = inspect.getsource(fn)
        tree = ast.parse(src)

        # extract the function definition
        func_def = next(
            node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        )
        print(f"--- running on {name.upper() or func_name.upper()} ---")

        # Valid
        valid = passes.register.is_valid_instruction(tree)
        print(f"Valid: {valid}")

        # BR_TYPE
        br_type = passes.register.test_conditional_assignment(tree)
        print(f"BR_TYPE: {br_type}")

        # has_register_read_rs1
        rs1 = passes.register.has_register_read_rs1(tree)
        print(f"has_register_read_rs1: {rs1}")

        # has_register_read_rs2
        rs2 = passes.register.has_register_read_rs2(tree)
        print(f"has_register_read_rs2: {rs2}")

        # has_register_write_rd
        rd = passes.register.has_register_write_rd(tree)
        print(f"has_register_write_rd: {rd}")

        # has_register_read_mrs1
        mrs1 = passes.register.has_register_read_mrs1(tree)
        print(f"has_register_read_mrs1: {mrs1}")

        # has_register_read_mrs2
        mrs2 = passes.register.has_register_read_mrs2(tree)
        print(f"has_register_read_mrs2: {mrs2}")

        # has_register_write_mrd
        mrd = passes.register.has_register_write_mrd(tree)
        print(f"has_register_write_mrd: {mrd}")

        # has_pc_update
        pc = passes.register.has_pc_assignment(tree)
        print(f"has_pc_assignment: {pc}")

        # get_mem_read_size
        mem_read_size = passes.mem.get_mem_read_size(tree)
        print(f"get_mem_read_size: {mem_read_size}")

        # get_mem_write_size
        mem_write_size = passes.mem.get_mem_write_size(tree)
        print(f"get_mem_write_size: {mem_write_size}")

        instruction_type = passes.functional_unit.instruction_type(tree)
        print(f"functional unit needed: {instruction_type}")

        alu_op = passes.functional_unit.scalar_alu_op(tree)
        print(f"operator: {type(alu_op).__name__}")
        print()
        return fn

    if fn is not None:
        return _run(fn)  # @instr bare
    else:
        return _run  # @instr(name=..., instruction_type=...)
