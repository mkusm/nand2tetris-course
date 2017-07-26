import os
import unittest
import unittest.mock
import tempfile

import python_assembler


class TestArguments(unittest.TestCase):

    def test_no_args(self):
        with unittest.mock.patch('sys.argv', []):
            self.assertRaises(ValueError, python_assembler.assemble)

    def test_too_many_args(self):
        with unittest.mock.patch('sys.argv', ['~/test1.asm', '~/test2.asm']):
            self.assertRaises(ValueError, python_assembler.assemble)

    def test_not_path(self):
        with unittest.mock.patch('sys.argv', ['test.testtest']):
            self.assertRaises(ValueError, python_assembler.assemble)

    def test_wrong_extension(self):
        extension='.txt'
        with tempfile.NamedTemporaryFile(suffix=extension) as tfile:
            tfile.write(b'test')
            with unittest.mock.patch('sys.argv', [tfile.name]):
                self.assertRaises(ValueError, python_assembler.assemble)


class TestLineParsing(unittest.TestCase):

    def test_A_instruction_1(self):
        line = "@1"
        parsed = python_assembler.parse_A_instruction(line)
        expected = ('0' * 15) + '1'
        self.assertEqual(parsed, expected)

    def test_A_instuction_biggest_value(self):
        line = "@32767"
        parsed = python_assembler.parse_A_instruction(line)
        expected = '0' + ('1' * 15)
        self.assertEqual(parsed, expected)

    def test_A_instruction_numbers_too_big(self):
        lines = ["@32768", "@120000", "@99999999"]
        for line in lines:
            with self.assertRaises(
                ValueError, msg=f"Error not raised for {line}"
            ):
                python_assembler.parse_A_instruction(line)


class TestFileAssembly(unittest.TestCase):

    def _assemble_file(self, dir_path, content):
        fname = os.path.join(dir_path, 'test.asm')
        with open(fname, mode='w') as tfile:
            tfile.write(content)

        with unittest.mock.patch('sys.argv', [fname]):
            python_assembler.assemble()
        out_file = os.path.join(dir_path, 'test.hack')
        return out_file

    def test_parse_empty_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            expected_out_file = self._assemble_file(tmpdirname, '')
            with open(expected_out_file) as hackfile:
                result = hackfile.read()
            print(result)

    def test_creates_any_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            expected_out_file = self._assemble_file(tmpdirname, '@1')
            self.assertTrue(os.path.exists(expected_out_file))

    def test_parse_properly_simplest_file(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            expected_out_file = self._assemble_file(tmpdirname, '@1')

            with open(expected_out_file) as hackfile:
                result = hackfile.read()
            expected = ('0' * 15) + '1'

            self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()
