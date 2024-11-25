from evmdasm import EvmBytecode
import json
import re


def decompile(_bytecode: str):
    disassembler = EvmBytecode(_bytecode)
    opcode = disassembler.disassemble().as_string
    opcode_normalized = opcode.replace(" \n", "\n").replace(" ", " 0x")
    return opcode_normalized.lower()


def tokenize_with_hex_replacement(opcode_str):
    modified_str = re.sub(r"0x[0-9a-fA-F]+", "HEX_CONST", opcode_str)
    tokens = re.split(r"\s+", modified_str)
    return tokens


def get_average_vector(opcode_list, model):
    vectors = [model.wv[word] for word in opcode_list if word in model.wv]
    if vectors:
        return sum(vectors) / len(vectors)
    else:
        return [0] * model.vector_size
