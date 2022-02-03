import re
import textwrap
import sys
import pathlib

a_inst = re.compile(r'\s*(@)(\d+)\s*')
c_inst = re.compile(r'\s*(?P<dest>[AMD]*)\=?(?P<comp>[AMD10\-\+\!\&\|]+);?(?P<jump>[JGTEQMPLN]*)\s*')
s_inst = re.compile(r'\s*(@)(\S+)\s*')
l_inst = re.compile(r'\s*\((\S+)\)\s*')

LABEL = "label"
VARIABLE = "variable"

def main():
    if len(sys.argv) != 2:
        print(textwrap.dedent(
            """\
            Usage:
              1st arg: input .asm file
            """))
        sys.exit(1)
    else:
        input_path = pathlib.Path(sys.argv[1])
        if not input_path.exists():
            print(f"Input file '{input_path}' does not exist")
            sys.exit(1)

        output_path = input_path.with_suffix('.hack')
        with open(input_path, 'r') as input_file:
            with open(output_path, 'w') as output_file:
                lines = input_file.readlines()
                codes = assemble(lines)
                output_file.write("\n".join(codes))


def assemble(lines):
    codes = []

    line_num = 0
    for line in lines:
        parsed = parse_line(line)

        if _new_symbol(parsed, LABEL):
            symbol_table[parsed[1]] = line_num
        if not _empty_line_or_label(parsed):
            line_num += 1

    var_address = 16
    for line in lines:
        parsed = parse_line(line)
        if _new_symbol(parsed, VARIABLE):
            symbol_table[parsed[1]] = var_address
            var_address += 1

    for line in lines:
        parsed = parse_line(line)
        if not _empty_line_or_label(parsed):
            codes.append(code(parsed))

    return codes


def parse_line(line):
    m = a_inst.match(line)
    if m is not None:
        return ('@', int(m.group(2)))
    m = c_inst.match(line)
    if m is not None:
        return m.groups()
    m = s_inst.match(line)
    if m is not None:
        return (VARIABLE, m.group(2))
    m = l_inst.match(line)
    if m is not None:
        return (LABEL, m.group(1))
    return ()


def code(command):
    if len(command) > 0 and command[0] == "@":
        return "0{0:015b}".format(command[1])
    if len(command) > 0 and command[0] == VARIABLE:
        return "0{0:015b}".format(symbol_table[command[1]])
    if len(command) == 3:
        return "111" + comp_codes[command[1]] + dest_codes[command[0]] + jump_codes[command[2]]
    else:
        return ""


def _new_symbol(parsed, type):
    return parsed != () and parsed[0] == type and parsed[1] not in symbol_table


def _empty_line_or_label(parsed):
    return parsed == () or (len(parsed) > 0 and parsed[0] == LABEL)


# Symbol table
symbol_table = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
}

# Static codes
comp_codes = {
    "0"  : "0101010",
    "1"  : "0111111",
    "-1" : "0111010",
    "D"  : "0001100",
    "A"  : "0110000",
    "M"  : "1110000",
    "!D" : "0001101",
    "!A" : "0110001",
    "!M" : "1110001",
    "-D" : "0001111",
    "-A" : "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

dest_codes = {
    ""   : "000",
    "M"  : "001",
    "D"  : "010",
    "MD" : "011",
    "A"  : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD": "111",
}

jump_codes = {
    ""   : "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


if __name__ == '__main__':
    main()
