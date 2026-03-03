from insn.instruction import instr
from insn.operations import ArchState, load, store, zero_extend


# @instr
# def add(rd: int, rs1: int, rs2: int, state: ArchState):
#     state.regfile[rd] = state.regfile[rs1] + state.regfile[rs2]


# @instr
# def addi(rd: int, rs1: int, imm12: int, state: ArchState):
#     state.regfile[rd] = state.regfile[rs1] + imm12


# @instr
# def sub(rd: int, rs1: int, rs2: int, state: ArchState):
#     state.regfile[rd] = state.regfile[rs1] - state.regfile[rs2]


# @instr
# def beq(rs1: int, rs2: int, bimm12: int, state: ArchState):
#     if state.regfile[rs1] == state.regfile[rs2]:
#         state.npc = state.pc + bimm12


# @instr
# def bne(rs1: int, rs2: int, bimm12: int, state: ArchState):
#     if state.regfile[rs1] != state.regfile[rs2]:
#         state.npc = state.pc + bimm12


# @instr
# def jalr(rd: int, rs1: int, imm12: int, state: ArchState):
#     state.regfile[rd] = state.pc + 4
#     state.npc = state.regfile[rs1] + imm12


# @instr
# def lw(rd: int, imm12: int, rs1: int, state: ArchState):
#     addr = state.regfile[rs1] + imm12
#     tmp = state.mem[addr]
#     tmp = (tmp << 8) | state.mem[addr + 1]
#     tmp = (tmp << 8) | state.mem[addr + 2]
#     tmp = (tmp << 8) | state.mem[addr + 3]
#     state.regfile[rd] = tmp


# @instr
# def lh(rd: int, imm12: int, rs1: int, state: ArchState):
#     addr = state.regfile[rs1] + imm12
#     tmp = state.mem[addr]
#     tmp = (tmp << 8) | state.mem[addr + 1]
#     state.regfile[rd] = tmp


# @instr
# def lhu(rd: int, imm12: int, rs1: int, state: ArchState):
#     tmp = zero_extend(load(addr=state.regfile[rs1] + imm12, size=2, state=state))
#     state.regfile[rd] = tmp


# @instr
# def sw(rs1: int, imm12: int, rs2: int, state: ArchState):
#     store(addr=state.regfile[rs1] + imm12, size=4, data=state.regfile[rs2], state=state)


# @instr
# def sh(rs1: int, imm12: int, rs2: int, state: ArchState):
#     store(addr=state.regfile[rs1] + imm12, size=2, data=state.regfile[rs2], state=state)


# @instr
# def sb(rs1: int, imm12: int, rs2: int, state: ArchState):
#     store(addr=state.regfile[rs1] + imm12, size=1, data=state.regfile[rs2], state=state)
