from insn.instruction import instr
from insn.operations import ArchState, load, zero_extend
from math import sin, cos, tanh, exp2, exp, log2, sqrt


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


# vector isa
@instr(name="vadd", instruction_type=InstructionType.VECTOR)
def vadd(mrd: int, mrs1: int, mrs2: int, state: ArchState):
    state.tensor_regfile[mrd] = state = state.tensor_regfile[mrs1] + state.tensor_regfile[mrs2]


@instr(name="vsub", instruction_type=InstructionType.VECTOR)
def vsub(mrd: int, mrs1: int, mrs2: int, state: ArchState):
    state.tensor_regfile[mrd] = state = state.tensor_regfile[mrs1] - state.tensor_regfile[mrs2]


@instr(name="vmul", instruction_type=InstructionType.VECTOR)
def vmul(mrd: int, mrs1: int, mrs2: int, state: ArchState):
    state.tensor_regfile[mrd] = state = state.tensor_regfile[mrs1] * state.tensor_regfile[mrs2]
    

@instr(name="vsqrt", instruction_type=InstructionType.VECTOR)
def vsqrt(mrd: int, mrs1: int, state: ArchState):
    state.tensor_regfile[mrd] = sqrt(state.tensor_regfile[mrs1])


# @instr(name="vrcp", instruction_type=InstructionType.VECTOR)
# def vrcp(mrd: int, mrs1: int, state: ArchState):
#     state.tensor_regfile[mrd] = state = 1 / state.tensor_regfile[mrs1]


@instr(name="vexp", instruction_type=InstructionType.VECTOR)
def vexp(mrd: int, mrs1: int, state: ArchState) -> None:
    state.tensor_regfile[mrd] = exp(state.tensor_regfile[mrs1])

@instr(name="vlog2", instruction_type=InstructionType.VECTOR)
def vlog2(mrd: int, mrs1: int, state: ArchState) -> None:
    state.tensor_regfile[mrd] = log2(state.tensor_regfile[mrs1])


@instr(name="vexp2", instruction_type=InstructionType.VECTOR)
def vexp2(mrd: int, mrs1: int, state: ArchState) -> None:
    state.tensor_regfile[mrd] = exp2(state.tensor_regfile[mrs1])


@instr(name="vsin", instruction_type=InstructionType.VECTOR)
def vsin(mrd: int, mrs1: int, state: ArchState) -> None:
    state.tensor_regfile[mrd] = sin(state.tensor_regfile[mrs1])


@instr(name="vcos", instruction_type=InstructionType.VECTOR)
def vcos(mrd: int, mrs1: int, state: ArchState) -> None:
    state.tensor_regfile[mrd] = cos(state.tensor_regfile[mrs1])


@instr(name="vtanh", instruction_type=InstructionType.VECTOR)
def vtanh(mrd: int, mrs1: int, state: ArchState) -> None:
    state.tensor_regfile[mrd] = tanh(state.tensor_regfile[mrs1])


@instr(name="mv.mm", instruction_type=InstructionType.VECTOR)
def mv_mm(mrd: int, mrs1: int, state: ArchState):
    """
    Vector/matrix move between matrix registers.
    """
    state.tensor_regfile[mrd] = state.tensor_regfile[mrs1]
    # state.write_mrf_f32(args["rd"], state.read_mrf_f32(args["rs1"]))


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
