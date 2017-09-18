#!/usr/bin/env python
"""mythril.py: Ethereum VM bytecode assembler/ disassembler

   http://www.github.com/b-mueller/mythril
"""

from ether import asm
import sys
import argparse
import util


def exitWithError(message):
    print(message)
    sys.exit()


parser = argparse.ArgumentParser(description='Ethereum VM bytecode assembler/ disassembler')

parser.add_argument('-d', '--disassemble',  action='store_true', help='disassemble, use with -c or -t')
parser.add_argument('-a', '--assemble', nargs=1, help='produce bytecode from easm input file', metavar='INPUT FILE')
parser.add_argument('-c', '--code', nargs=1, help='bytecode string ("6060604052...")', metavar='BYTECODE')
parser.add_argument('-t', '--transaction_hash', help='id of contract creation transaction')
parser.add_argument('-o', '--outfile', help='file to write disassembly output to (e.g. "test.easm")')
parser.add_argument('--rpchost', nargs=1, help='RPC host')
parser.add_argument('--rpcport', nargs=1, help='RPC port')

args = parser.parse_args()


if (args.disassemble):

    if (args.code):
        disassembly = asm.disassemble(args.code[0])
    elif (args.transaction_hash):

        try:
            bytecode = util.bytecode_from_blockchain(args.transaction_hash)
        except Exception as e:
            exitWithError("Exception loading bytecode via RPC: " + str(e.message))

        disassembly = asm.disassemble(bytecode)

    else:
        exitWithError("Disassembler: Pass either the -c or -t flag to specify the input bytecode")

    easm_text = asm.disassembly_to_easm(disassembly)

    if (args.outfile):
        util.string_to_file(args.outfile, easm_text)
    else:
        sys.stdout.write(easm_text)

elif (args.assemble):

    easm = util.file_to_string(args.assemble[0])

    disassembly = asm.easm_to_disassembly(easm)

    print("0x" + asm.assemble(disassembly))

else:

    parser.print_help()
