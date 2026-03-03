from insn.instruction import instr
from insn.operations import ArchState, load, zero_extend


class InstructionType:
    SCALAR = 0
    VECTOR = 1
    MATRIX_IPT = 2
    MATRIX_SYSTOLIC = 3
    DMA = 4
    BARRIER = 5


@instr(name="matmul.mxu1", instruction_type=InstructionType.MATRIX_IPT)
def matmul_mxu_1(mrd: int, mrs1: int, mrs2: int, state: ArchState):
    state.tensor_regfile[mrd] = state.tensor_regfile[mrs1] @ state.tensor_regfile[mrs2]


@instr(name="beq", instruction_type=InstructionType.SCALAR)
def beq(rs1: int, rs2: int, bimm12: int, state: ArchState):
    if state.regfile[rs1] == state.regfile[rs2]:
        state.pc = state.pc + bimm12


# @instr3
# def lw(rd: int, imm12: int, rs1: int, state: ArchState):
#     addr = state.regfile[rs1] + imm12
#     tmp = (
#         state.mem[addr] << 24
#         | state.mem[addr + 1] << 16
#         | state.mem[addr + 2] << 8
#         | state.mem[addr + 3]
#     )
#     state.regfile[rd] = tmp


# @instr
# def lh(rd: int, imm12: int, rs1: int, state: ArchState):
#     addr = state.regfile[rs1] + imm12
#     tmp = state.mem[addr]
#     tmp = (tmp << 8) | state.mem[addr + 1]
#     state.regfile[rd] = tmp


# # @instr
# # def lhu(rd: int, imm12: int, rs1: int, state: ArchState):
# #     tmp = zero_extend(load(addr=state.regfile[rs1] + imm12, size=2, state=state))
# #     state.regfile[rd] = tmp


# @instr
# def sb(rs1: int, imm12: int, rs2: int, state: ArchState):
#     addr = state.regfile[rs1] + imm12
#     state.mem[addr] = state.regfile[rs2] & 0xFF
