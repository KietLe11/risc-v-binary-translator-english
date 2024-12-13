from decoding import *
from formatting import *


def inst_type(instruction):
    format_type = ''
    opcode = instruction[25:len(instruction) + 1]

    if opcode == '1101111': format_type = 'UJ'
    elif opcode == '1100011': format_type = 'SB'
    elif opcode == '0100011': format_type = 'S'
    elif opcode == '0110111' or opcode == '0010111': format_type = 'U'
    elif opcode == '0000011' or opcode == '1100111' or opcode == '0010011': format_type = 'I'
    elif opcode == '0110011': format_type = 'R'

    return format_type


def inst_decode(instruction, options):
    format_type = inst_type(instruction)

    match format_type:
        case 'R':
            contents = {}
            contents['funct7'], contents['rs2'], contents['rs1'], contents['funct3'], contents['rd'], contents['opcode'] = decode_R(instruction)

            return format_R(contents, options)
        case 'SB':
            contents = {}
            contents['imm_cycle_32'], contents['rs2'], contents['rs1'], contents['funct3'], contents['imm_offset'], contents['opcode'] = decode_SB(instruction)

            return format_SB(contents, options)
        case 'S':
            contents = {}
            contents['imm_cycle_32'], contents['rs2'], contents['rs1'], contents['funct3'], contents['imm_offset'], contents['opcode'] = decode_S(instruction)

            return format_S(contents, options)
        case 'I':
            imm, rs1, funct3, rd, opcode = decode_I(instruction)
            contents = {}
            # If it’s 001 or 101, it’s a logical shift and therefore has different formatting
            if ((opcode == '0010011' and (funct3 != '001' and funct3 != '101')) or opcode == '0000011'):
                contents['imm'] = imm
                contents['rs1'] = rs1
                contents['funct3'] = funct3
                contents['rd'] = rd
                contents['opcode'] = opcode
            # Logical shifts have the formatting of R-type instructions
            # shamt = shift amount
            else:
                funct7, shamt, rs1, funct3, rd, opcode = decode_R(instruction)
                contents['funct7'] = funct7
                contents['shamt'] = shamt
                contents['rs1'] = rs1
                contents['funct3'] = funct3
                contents['rd'] = rd
                contents['opcode'] = opcode

            return format_I(contents, options)
        case 'U':
            return 'U and UJ functions not implemented'
        case 'UJ':
            return 'U and UJ functions not implemented'


def main():
    print('Interactive or file reading? (i/l)')
    choice = input()
    if choice == 'l':
        print('File path: ')
        address = input()
        print('Options (sb/sx): ')
        op = input()

        instructions = open(address, 'r')

        while True:
            inst = instructions.readline().strip()
            if not inst: break

            print(inst_decode(f'{inst:0>32}', op))

        instructions.close()

    elif choice == 'i':
        print('Will the instructions be in binary or hexadecimal? (b/x)')
        response = input()
        print('Options (sb/sx): ')
        op = input()
        match response:
            case 'b':
                while True:
                    print('Instruction (to exit, type s): ')
                    inst = input().strip()
                    if (inst == 's'): break

                    print(inst_decode(f'{inst:0>32}', op))
            case 'x':
                while True:
                    print('Instruction (to exit, type s): ')
                    inst = input().strip()
                    if (inst == 's'): break

                    hex_to_bin = f'{bin(int(inst, 16))[2:]:0>32}'
                    print(inst_decode(hex_to_bin, op))


if __name__ == '__main__':
    main()