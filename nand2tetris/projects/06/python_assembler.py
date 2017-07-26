import sys
import os

BUILT_IN_SYMBOLS = {
    'SP':     0,
    'LCL':    1,
    'ARG':    2,
    'THIS':   3,
    'THAT':   4,
    'SCREEN': 16384,
    'KBD':    24576
}
for i in range(16):
    label = 'R' + str(i)
    BUILT_IN_SYMBOLS[label] = i


class Parser:
    def __init__(self, asm_file_content):
        self.asm_content = asm_file_content
        self.label_symbols = {}
        self.memory_symbols = {}
        self.next_memory_symbol = 16

    @staticmethod
    def _parse_A_instruction(line):
        number = int(line[1:])

        maximum_A_value = int('1' * 15, 2)
        if number > maximum_A_value:
            raise ValueError('')

        binary = format(number, '016b')
        return binary

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def calculate_jump(jump):
        jumps = (None, 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP')
        for index, jump_expected in enumerate(jumps):
            if jump_expected == jump:
                return format(index, '03b')
        else:
            raise ValueError(f"Jump {jump} is not valid")

    @staticmethod
    def parse_C_instruction(line):
        assert len(line) > 0
        comp, dest, jump = Parser.split_C_instruction(line)
        comp = Parser.calculate_comp(comp)
        dest = Parser.calculate_dest(dest)
        jump = Parser.calculate_jump(jump)
        assert len(comp) == 7
        assert len(dest) == 3
        assert len(jump) == 3
        return '111' + comp + dest + jump

    def get_memory_symbol_value(self, symbol):
        symbol_value_saved = self.memory_symbols.get(symbol, False)
        if not symbol_value_saved:
            self.memory_symbols[symbol] = self.next_memory_symbol
            self.next_memory_symbol += 1
        return self.memory_symbols[symbol]

    def parse_symbol(self, line):
        symbol = line[1:]
        symbol_value = BUILT_IN_SYMBOLS.get(symbol, False)
        if symbol_value is False:
            symbol_value = self.label_symbols.get(symbol, False)
        if symbol_value is False:
            symbol_value = self.get_memory_symbol_value(symbol)
        return '@' + str(symbol_value)

    def parse_line(self, line):
        if '//' in line:
            line = line.split('//')[0]
        if line[0] == '@':
            if not line[1:].isdigit():
                line = self.parse_symbol(line)
            return self._parse_A_instruction(line)
        else:
            return self.parse_C_instruction(line)

    def parse_comments_symbols_and_empty_lines(self, lines):
        i = 0
        while i < len(lines):
            if '//' in lines[i]:
                lines[i] = lines[i].split('//')[0]
            lines[i] = lines[i].strip()
            # remove comments and empty lines
            if lines[i][0:2] == '//' or lines[i] == '':
                del lines[i]
                continue
            # create new label symbols
            if lines[i][0] == '(':
                symbol = lines[i][1:-1]
                self.label_symbols[symbol] = i
                del lines[i]
                continue
            i += 1

    def parse(self):
        parsed_lines = []
        lines_to_parse = self.asm_content.splitlines()
        self.parse_comments_symbols_and_empty_lines(lines_to_parse)
        for line in lines_to_parse:
            parsed_lines.append(self.parse_line(line))
        return '\n'.join(parsed_lines) + '\n'


def check_arguments():
    if not len(sys.argv) == 2:
        raise ValueError('Expected 1 argument, received: ', sys.argv[1:])

    asm_file_path = sys.argv[1]

    if not os.path.exists(asm_file_path):
        raise ValueError('Wrong argument: ', asm_file_path, ', file does not exist')

    asm_file_path = os.path.abspath(asm_file_path)

    _, asm_file_extension = os.path.splitext(asm_file_path)
    if not asm_file_extension == '.asm':
        raise ValueError(
            "Wrong argument: ", asm_file_path, ", file's extension should be .asm"
        )

    if os.path.getsize(asm_file_path) == 0:
        raise ValueError("File ", asm_file_path, " is empty")


def get_asm_and_hack_files_paths():
    asm_file_path = os.path.abspath(sys.argv[1])
    asm_file_no_extension, _ = (os.path.splitext(asm_file_path))
    hack_file_path = asm_file_no_extension + '.hack'
    return asm_file_path, hack_file_path


def assemble():
    check_arguments()
    asm_file_path, hack_file_path = get_asm_and_hack_files_paths()

    with open(asm_file_path) as asmfile:
        asm_file_content = asmfile.read()

    parser = Parser(asm_file_content)
    parsed_content = parser.parse()

    with open(hack_file_path, 'w') as hackfile:
        hackfile.write(parsed_content)

    assert os.path.exists(hack_file_path)


if __name__ == "__main__":
    assemble()
