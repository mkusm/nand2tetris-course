import os
import unittest
import unittest.mock
import tempfile

import python_assembler


class TestArguments(unittest.TestCase):

    def test_no_args(self):
        with unittest.mock.patch('sys.argv', ['f']):
            self.assertRaises(ValueError, python_assembler.assemble)

    def test_too_many_args(self):
        with unittest.mock.patch('sys.argv', ['f', '~/test1.asm', '~/test2.asm']):
            self.assertRaises(ValueError, python_assembler.assemble)

    def test_not_path(self):
        with unittest.mock.patch('sys.argv', ['f', 'test.testtest']):
            self.assertRaises(ValueError, python_assembler.assemble)

    def test_wrong_extension(self):
        extension='.txt'
        with tempfile.NamedTemporaryFile(suffix=extension) as tfile:
            tfile.write(b'test')
            with unittest.mock.patch('sys.argv', ['f', tfile.name]):
                self.assertRaises(ValueError, python_assembler.assemble)


class TestLineParsingInstructionA(unittest.TestCase):

    def _test_A_instruction(self, line, expected):
        parsed = python_assembler.Parser._parse_A_instruction(line)
        self.assertEqual(parsed, expected)

    def test_1(self):
        line = "@1"
        expected = ('0' * 15) + '1'
        self._test_A_instruction(line, expected)

    def test_13107(self):
        line = "@13107"
        expected = "0011" + "0011" + "0011" + "0011"
        self._test_A_instruction(line, expected)

    def test_biggest_value(self):
        line = "@32767"
        expected = '0' + ('1' * 15)
        self._test_A_instruction(line, expected)

    def test_numbers_too_big(self):
        lines = ["@32768", "@120000", "@99999999"]
        for line in lines:
            with self.assertRaises(
                ValueError, msg=f"Error not raised for {line}"
            ):
                python_assembler.Parser('')._parse_A_instruction(line)

class TestLineParsingInstructionC(unittest.TestCase):

    def _test_instruction_C(self, line, expected_result):
        result = python_assembler.Parser.parse_C_instruction(line)
        self.assertEqual(expected_result, result)

    def test_simplest_1(self):
        line = 'D=0'
        expected = '1110' '1010' '1001' '0000'
        self._test_instruction_C(line, expected)

    def test_simplest_2(self):
        line = 'D=1'
        expected = '1110' '1111' '1101' '0000'
        self._test_instruction_C(line, expected)

    def test_1(self):
        line = 'M=D+M'
        expected = '1111' '0000' '1000' '1000'
        self._test_instruction_C(line, expected)

    def test_2(self):
        line = '0;JMP'
        expected = '1110' '1010' '1000' '0111'
        self._test_instruction_C(line, expected)


class TestInstructionCHelperFunctions(unittest.TestCase):

    def _test_split(self, line, expected_result):
        result = python_assembler.Parser('').split_C_instruction(line)
        self.assertEqual(expected_result, result)

    def test_split_C_no_dest(self):
        line = 'M;JEQ'
        expected = ('M', None, 'JEQ')
        self._test_split(line, expected)

    def test_split_C_no_jump(self):
        line = 'D=0'
        expected = ('0', 'D', None)
        self._test_split(line, expected)

    def test_split_C_full(self):
        line = 'AM=M|D;JGT'
        expected = ('M|D', 'AM', 'JGT')
        self._test_split(line, expected)

    def test_calculate_dest(self):
        mnemonic_to_binary = (
            (None,  '000'),
            ('M',   '001'),
            ('D',   '010'),
            ('MD',  '011'),
            ('A',   '100'),
            ('AM',  '101'),
            ('AD',  '110'),
            ('AMD', '111'),
        )
        for mnemonic, expected in mnemonic_to_binary:
            result = python_assembler.Parser('').calculate_dest(mnemonic)
            self.assertEqual(
                result, expected,
                f'For {mnemonic} expected {expected}, got {result}'
            )

    def test_calculate_jump(self):
        mnemonic_to_binary = (
            (None,  '000'),
            ('JGT', '001'),
            ('JEQ', '010'),
            ('JGE', '011'),
            ('JLT', '100'),
            ('JNE', '101'),
            ('JLE', '110'),
            ('JMP', '111'),
        )
        for mnemonic, expected in mnemonic_to_binary:
            result = python_assembler.Parser('').calculate_jump(mnemonic)
            self.assertEqual(
                result, expected,
                f'For {mnemonic} expected {expected}, got {result}'
            )

    def test_calculate_comp(self):
        partial_mnemonic_to_binary = (
            ('0',   '0101010'),
            ('A',   '0110000'),
            ('M',   '1110000'),
            ('M-D', '1000111'),
            ('D&A', '0000000'),
        )
        for mnemonic, expected in partial_mnemonic_to_binary:
            result = python_assembler.Parser('').calculate_comp(mnemonic)
            self.assertEqual(
                result, expected,
                f'For {mnemonic} expected {expected}, got {result}'
            )

class TestSymbols(unittest.TestCase):

    def test_parse_symbol_with_built_ins(self):
        line = '@SCREEN'
        expected = '@16384'
        result = python_assembler.Parser('').parse_symbol(line)
        self.assertEqual(result, expected)
        line = '@R7'
        expected = '@7'
        result = python_assembler.Parser('').parse_symbol(line)
        self.assertEqual(result, expected)

    def test_R0(self):
        line = '@R0'
        expected = '@0'
        result = python_assembler.Parser('').parse_symbol(line)
        self.assertEqual(result, expected)

    def test_parse_symbol_with_memory_symbols(self):
        lines = '@a\n@b\n@X'
        parser = python_assembler.Parser(lines)
        lines_to_parse = lines.splitlines()
        for line in lines_to_parse:
            parser.parse_symbol(line)
        self.assertEqual(parser.memory_symbols, {'a': 16, 'b': 17, 'X': 18})
        self.assertEqual(parser.parse_symbol('@a'), '@16')

    def test_built_in_symbols(self):
        line = '@THIS'
        expected = '0000' '0000' '0000' '0011'
        result = python_assembler.Parser('').parse_line(line)
        self.assertEqual(result, expected)

    def test_parse_comments_symbols_and_empty_lines(self):
        lines = '//test\n\n@R1\n     D=A\n@LOOP\n(LOOP)\n@a\n(X)'
        parser = python_assembler.Parser(lines)
        lines_to_parse = lines.splitlines()
        parser.parse_comments_symbols_and_empty_lines(lines_to_parse)
        self.assertEqual(parser.label_symbols, {'LOOP': 3, 'X': 4})

class TestFileAssembly(unittest.TestCase):

    def test_remove_comments_whitespaces_and_labels(self):
        lines = ('//test\n\n@R1\n     D=A\n@LOOP\n// test2\n@a\n//test3\n(X)')
        parser = python_assembler.Parser(lines)
        lines_to_parse = lines.splitlines()
        parser.parse_comments_symbols_and_empty_lines(lines_to_parse)
        self.assertEqual(
            lines_to_parse, ['@R1', 'D=A', '@LOOP', '@a']
        )

    def _assemble_file(self, dir_path, content, filename='test'):
        fname = os.path.join(dir_path, f'{filename}.asm')
        with open(fname, mode='w') as tfile:
            tfile.write(content)
        with unittest.mock.patch('sys.argv', ['f', fname]):
            python_assembler.assemble()
        out_file = os.path.join(dir_path, f'{filename}.hack')
        return out_file

    def _assemble_and_test(self, dir_path, content, expected, filename='test'):
        assembled_file_path = self._assemble_file(dir_path, content, filename)

        with open(assembled_file_path) as hackfile:
            result = hackfile.read()

        self.assertEqual(result, expected)


    def test_parse_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:

            with self.assertRaises(ValueError):
                expected_out_file = self._assemble_file(tmpdirname, '', 'test')

            self.assertFalse(
                os.path.exists(os.path.join(tmpdirname, 'test.hack'))
            )

    def test_creates_any_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            expected_out_file = self._assemble_file(tmpdirname, '@1')
            self.assertTrue(os.path.exists(expected_out_file))

    def test_parse_properly_simplest_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            expected = ('0' * 15) + '1' + '\n'
            self._assemble_and_test(tmpdirname, '@1', expected)

    def test_skip_empty_lines(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            content = '@1\n\n\n@1\n\n@1\n'
            parsed_line = ('0' * 15) + '1'
            expected = f'{parsed_line}\n{parsed_line}\n{parsed_line}\n'
            self._assemble_and_test(tmpdirname, content, expected)

    def test_medium_file(self):
        content = (
            '@1\n'
            'D=A\n'
            '@12\n'
            'M=D\n'
            'D=A\n'
            '\n\n'
            '@128\n'
            'D=A\n'
            'AMD=D-M\n'
            '\n'
            '@5\n'
            '0;JMP\n'
        )
        expected = (
            '0000' '0000' '0000' '0001\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '0000' '1100\n'
            '111' '0001100' '001' '000\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '1000' '0000\n'
            '111' '0110000' '010' '000\n'
            '111' '1010011' '111' '000\n'
            '0000' '0000' '0000' '0101\n'
            '111' '0101010' '000' '111\n'
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            self._assemble_and_test(tmpdirname, content, expected)

    def test_medium_file_with_labels(self):
        content = (
            '@R1\n'
            'D=A\n'
            '@12\n'
            'M=D\n'
            'D=A\n'
            '(TEST_SYMBOL)'
            '\n\n'
            '@128\n'
            'D=A\n'
            'AMD=D-M\n'
            '\n'
            '@TEST_SYMBOL\n'
            '0;JMP\n'
        )
        expected = (
            '0000' '0000' '0000' '0001\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '0000' '1100\n'
            '111' '0001100' '001' '000\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '1000' '0000\n'
            '111' '0110000' '010' '000\n'
            '111' '1010011' '111' '000\n'
            '0000' '0000' '0000' '0101\n'
            '111' '0101010' '000' '111\n'
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            self._assemble_and_test(tmpdirname, content, expected)

    def test_medium_file_with_mixed_symbols_indents_and_comments(self):
        content = (
            '// test comment\n'
            '@R1\n'
            '// test comment\n'
            'D=A\n'
            '@12 // inline comment\n'
            'M=D\n'
            'D=A\n'
            '(TEST_SYMBOL)'
            '\n\n'
            '@test\n'
            '       D=A\n'
            'AMD=D-M\n'
            '\n'
            '@TEST_SYMBOL\n'
            '0;JMP\n'
            '@test\n'
            'D=A        \t// far indented comment\n'
            '@test2\n'
            '\t\tD=A\n'
        )
        expected = (
            '0000' '0000' '0000' '0001\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '0000' '1100\n'
            '111' '0001100' '001' '000\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '0001' '0000\n'
            '111' '0110000' '010' '000\n'
            '111' '1010011' '111' '000\n'
            '0000' '0000' '0000' '0101\n'
            '111' '0101010' '000' '111\n'
            '0000' '0000' '0001' '0000\n'
            '111' '0110000' '010' '000\n'
            '0000' '0000' '0001' '0001\n'
            '111' '0110000' '010' '000\n'
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            self._assemble_and_test(tmpdirname, content, expected)

if __name__ == '__main__':
    unittest.main()
