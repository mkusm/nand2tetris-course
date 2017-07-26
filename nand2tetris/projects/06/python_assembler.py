import sys
import os


def parse_A_instruction(line):
    number = int(line[1:])

    maximum_A_value = int('1' * 15, 2)
    if number > maximum_A_value:
        raise ValueError('')

    binary = format(number, '016b')
    return binary


def split_C_instruction(line):
    assert line.count('=') in [0, 1]
    assert line.count(';') in [0, 1]
    if '=' in line:
        dest, other = line.split('=')
    else:
        dest = None
        other = line
    if ';' in other:
        comp, jump = other.split(';')
    else:
        comp = other
        jump = None
    return comp, dest, jump


def calculate_comp(comp):
    if not comp:
        raise ValueError('Missing computation')
    a_0_comp_dict = {
        '0':   '101010',
        '1':   '111111',
        '-1':  '111010',
        'D':   '001100',
        'A':   '110000',
        '!D':  '001101',
        '!A':  '110001',
        '-D':  '001111',
        '-A':  '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101'
    }
    binary = a_0_comp_dict.get(comp, False)
    if binary:
        return '0' + binary
    else:
        if not 'M' in comp:
            raise ValueError('Wrong computation')
        comp = comp.replace('M', 'A')
        binary = a_0_comp_dict.get(comp, False)
        if not binary:
            raise ValueError('Wrong computation')
        return '1' + binary


def calculate_dest(dest):
    result = ['0', '0', '0']
    if dest is None:
        return '000'
    if 'M' in dest:
        result[2] = '1'
    if 'D' in dest:
        result[1] = '1'
    if 'A' in dest:
        result[0] = '1'
    result = "".join(result)
    return result

def calculate_jump(jump):
    jumps = (None, 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP')
    for index, jump_expected in enumerate(jumps):
        if jump_expected == jump:
            return format(index, '03b')
    else:
        raise ValueError(f"Jump {jump} is not valid")

def parse_C_instruction(line):
    assert len(line) > 0
    comp, dest, jump = split_C_instruction(line)
    comp = calculate_comp(comp)
    dest = calculate_dest(dest)
    jump = calculate_jump(jump)
    assert len(comp) == 7
    assert len(dest) == 3
    assert len(jump) == 3
    return '111' + comp + dest + jump


def parse_line(line):
    if line[0] == '@':
        return parse_A_instruction(line)
    else:
        return parse_C_instruction(line)

def check_arguments():
    if not len(sys.argv) == 1:
        raise ValueError('Expected 1 argument, received: ', sys.argv)

    asm_file_path = sys.argv[0]

    if not os.path.exists(asm_file_path):
        raise ValueError('Wrong argument: ', asm_file_path, ', file does not exist')

    asm_file_path = os.path.abspath(asm_file_path)

    _, asm_file_extension = os.path.splitext(asm_file_path)
    if not asm_file_extension == '.asm':
        raise ValueError(
            "Wrong argument: ", sys.argv, ", file's extension should be .asm"
        )

    if os.path.getsize(asm_file_path) == 0:
        raise ValueError("File ", sys.argv, " is empty")

def parse_asm_file(asm_file_path):
    with open(asm_file_path) as asmfile:
        asm_file_content = asmfile.read()
    asm_file_lines = asm_file_content.splitlines()

    parsed = []
    for line in asm_file_lines:
        if line:
            parsed.append(parse_line(line))
    parsed = "\n".join(parsed)
    return parsed

def get_asm_and_hack_files_paths():
    asm_file_path = os.path.abspath(sys.argv[0])
    asm_file_no_extension, _ = (os.path.splitext(asm_file_path))
    hack_file_path = asm_file_no_extension + '.hack'
    return asm_file_path, hack_file_path

def assemble():
    check_arguments()
    asm_file_path, hack_file_path = get_asm_and_hack_files_paths()
    parsed_content = parse_asm_file(asm_file_path)
    with open(hack_file_path, 'w') as hackfile:
        hackfile.write(parsed_content)
    assert os.path.exists(hack_file_path)


if __name__ == "__main__":
    assemble()
