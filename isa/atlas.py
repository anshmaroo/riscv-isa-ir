from insn.instruction import instr
from insn.operations import ArchState, load, zero_extend


class InstructionType:
    SCALAR = 0
    VECTOR = 1
    MATRIX_IPT = 2
    MATRIX_SYSTOLIC = 3
    DMA = 4
    BARRIER = 5


# matrix isa
@instr(name="matmul.mxu0", instruction_type=InstructionType.MATRIX_SYSTOLIC)
def matmul_mxu_0(mrd: int, mrs1: int, mrs2: int, state: ArchState):
    state.tensor_regfile[mrd] = state.tensor_regfile[mrs1] @ state.tensor_regfile[mrs2]


@instr(name="matmul.mxu1", instruction_type=InstructionType.MATRIX_IPT)
def matmul_mxu_1(mrd: int, mrs1: int, mrs2: int, state: ArchState):
    state.tensor_regfile[mrd] = state.tensor_regfile[mrs1] @ state.tensor_regfile[mrs2]



# scalar isa
@instr(name="add", instruction_type=InstructionType.SCALAR)
def add(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] + state.regfile[rs2]


@instr(name="sub", instruction_type=InstructionType.SCALAR)
def sub(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] - state.regfile[rs2]


@instr(name="and", instruction_type=InstructionType.SCALAR)
def _and(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] & state.regfile[rs2]


@instr(name="or", instruction_type=InstructionType.SCALAR)
def _or(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] | state.regfile[rs2]


@instr(name="xor", instruction_type=InstructionType.SCALAR)
def xor(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] ^ state.regfile[rs2]


@instr(name="sll", instruction_type=InstructionType.SCALAR)
def sll(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] << state.regfile[rs2]


@instr(name="srl", instruction_type=InstructionType.SCALAR)
def srl(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] >> state.regfile[rs2]


@instr(name="sra", instruction_type=InstructionType.SCALAR)
def sra(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] >> state.regfile[rs2]  # FIXME: signed


@instr(name="slt", instruction_type=InstructionType.SCALAR)
def slt(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] < state.regfile[rs2]  # FIXME: signed


@instr(name="sltu", instruction_type=InstructionType.SCALAR)
def sltu(rd: int, rs1: int, rs2: int, state: ArchState):
    state.regfile[rd] = state.regfile[rs1] < state.regfile[rs2]


@instr(name="beq", instruction_type=InstructionType.SCALAR)
def beq(rs1: int, rs2: int, bimm12: int, state: ArchState):
    if state.regfile[rs1] == state.regfile[rs2]:
        state.pc = state.pc + bimm12


@instr(name="bne", instruction_type=InstructionType.SCALAR)
def bne(rs1: int, rs2: int, bimm12: int, state: ArchState):
    if state.regfile[rs1] != state.regfile[rs2]:
        state.pc = state.pc + bimm12


@instr(name="blt", instruction_type=InstructionType.SCALAR)
def blt(rs1: int, rs2: int, bimm12: int, state: ArchState):
    if state.regfile[rs1] < state.regfile[rs2]:  # FIXME: signed
        state.pc = state.pc + bimm12


@instr(name="bltu", instruction_type=InstructionType.SCALAR)
def bltu(rs1: int, rs2: int, bimm12: int, state: ArchState):
    if state.regfile[rs1] < state.regfile[rs2]:
        state.pc = state.pc + bimm12


@instr(name="jal", instruction_type=InstructionType.SCALAR)
def blt(rs1: int, rs2: int, bimm20: int, state: ArchState):
    state.pc = state.pc + bimm20
