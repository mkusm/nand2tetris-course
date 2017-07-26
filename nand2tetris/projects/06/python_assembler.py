import sys
import os



def parse_A_instruction(line):
    number = int(line[1:])

    maximum_A_value = int('1' * 15, 2)
    if number > maximum_A_value:
        raise ValueError('')

    binary = format(number, '016b')
    return binary


def parse_C_instruction(line):
    pass


def parse_line(line):
    if line[0] == '@':
        return parse_A_instruction(line)
    else:
        return parse_C_instruction(line)


def assemble():
    if not len(sys.argv) == 1:
        raise ValueError('Expected 1 argument, received: ', sys.argv)

    asm_file_path = sys.argv[0]

    if not os.path.exists(asm_file_path):
        raise ValueError('Wrong argument: ', sys.argv, ', file does not exist')

    asm_file_path = os.path.abspath(asm_file_path)
    asm_file_no_extension, asm_file_extension = (
        os.path.splitext(asm_file_path)
    )

    if not asm_file_extension == '.asm':
        raise ValueError(
            "Wrong argument: ", sys.argv, ", file's extension should be .asm"
        )


    parsed = []

    with open(asm_file_path) as asmfile:
        for line in asmfile:
            parsed.append(parse_line(line))

    hack_file_path = asm_file_no_extension + '.hack'

    with open(hack_file_path, 'w') as hackfile:
        for line in parsed:
            hackfile.write(line)

    assert os.path.exists(hack_file_path)


if __name__ == "__main__":
    assemble()
