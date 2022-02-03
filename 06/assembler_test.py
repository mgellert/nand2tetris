import unittest
from assembler import assemble, parse_line, code, VARIABLE, LABEL

class TestParser(unittest.TestCase):

    def test_parse_line(self):
        self.assertEqual(parse_line(""), ())
        self.assertEqual(parse_line("// some comment"), ())
        self.assertEqual(parse_line("@16"), ("@", 16))
        self.assertEqual(parse_line("\t@16\t// some comment"), ("@", 16))
        self.assertEqual(parse_line("MD=D+1"), ("MD", "D+1", ""))
        self.assertEqual(parse_line("0;JMP"), ("", "0", "JMP"))
        self.assertEqual(parse_line(" A=0;JLE"), ("A", "0", "JLE"))
        self.assertEqual(parse_line("(LOOP)"), (LABEL, "LOOP"))
        self.assertEqual(parse_line("@i"), (VARIABLE, "i"))
        self.assertEqual(parse_line("@R0"), (VARIABLE, "R0"))

class TestCode(unittest.TestCase):

    def test_code(self):
        self.assertEqual(code(()), "")
        self.assertEqual(code(("@", 1)), "0000000000000001")
        self.assertEqual(code(("D", "D+A", "")), "1110000010010000")
        self.assertEqual(code((VARIABLE, "R0")), "0000000000000000")


class TestAssemble(unittest.TestCase):

    def test_assemble(self):
        input = [
            "// This file is part of www.nand2tetris.org",
            "// and the book \"The Elements of Computing Systems\"",
            "// by Nisan and Schocken, MIT Press.",
            "// File name: projects/06/max/Max.asm",
            "",
            "// Computes R2 = max(R0, R1)  (R0,R1,R2 refer to RAM[0],RAM[1],RAM[2])",
            "",
            "   @R0",
            "   D=M              // D = first number",
            "   @R1",
            "   D=D-M            // D = first number - second number",
            "   @OUTPUT_FIRST",
            "   D;JGT            // if D>0 (first is greater) goto output_first",
            "   @R1",
            "   D=M              // D = second number",
            "   @OUTPUT_D",
            "   0;JMP            // goto output_d",
            "(OUTPUT_FIRST)",
            "   @R0             ",
            "   D=M              // D = first number",
            "(OUTPUT_D)",
            "   @R2",
            "   M=D              // M[2] = D (greatest number)",
            "(INFINITE_LOOP)",
            "   @INFINITE_LOOP",
            "   0;JMP            // infinite loop",
        ]
        expected = [
            "0000000000000000",
            "1111110000010000",
            "0000000000000001",
            "1111010011010000",
            "0000000000001010",
            "1110001100000001",
            "0000000000000001",
            "1111110000010000",
            "0000000000001100",
            "1110101010000111",
            "0000000000000000",
            "1111110000010000",
            "0000000000000010",
            "1110001100001000",
            "0000000000001110",
            "1110101010000111",
        ]
        self.assertEqual(assemble(input), expected)


if __name__ == '__main__':
    unittest.main()