from dataclasses import dataclass
import ctypes


@dataclass
class ArchState:
    mem: dict[ctypes.c_uint32, ctypes.c_uint8]
    regfile: list[ctypes.c_uint64]
    tensor_regfile: list[list[ctypes.c_uint32]]
    pc: ctypes.c_uint32
    npc: ctypes.c_uint32


# load the value from the memory at addr into the register rd
def load(addr: ctypes.c_uint32, size: int, state: ArchState):
    tmp = 0
    for i in range(size):
        tmp = (tmp << 8) | state.mem[addr + i]
    return tmp


# store the value of data into the memory at addr
def store(addr: ctypes.c_uint32, size: int, data: ctypes.c_uint32, state: ArchState):
    for i in range(size):
        state.mem[addr + i] = (data >> (i * 8)) & 0xFF


# zero extend the value of data to the size of the register
def zero_extend(data: ctypes.c_uint32):
    return data


def sign_extend(data: ctypes.c_uint32):
    return data
