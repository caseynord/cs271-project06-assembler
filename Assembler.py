import re

import Code


class Assembler:

    def __init__(self):
        self.memory_index = 16  # first register for non-reserved memory
        self.symbol_table = Code.symbols  # initialize symbol table with built-ins

    def allocate_memory(self, symbol):
        self.symbol_table[symbol] = self.memory_index
        self.memory_index += 1
        return self.symbol_table[symbol]

    def build_symbol_table(self, normalized_data_list):
        line_number = 0
        for line in normalized_data_list:
            if line[0] == "(":
                new_symbol = line[1:-1]
                self.symbol_table[new_symbol] = line_number
            else:
                line_number += 1

    def assemble_c_instruction(self, line):
        c_instruction = re.split('=|;', line)
        dest_code = Code.dest.get(c_instruction[0], "dest_FAIL")
        comp_code = Code.comp.get(c_instruction[1], "comp_FAIL")
        jump_code = Code.jump.get(c_instruction[2], "jump_FAIL")
        return "111" + comp_code + dest_code + jump_code

    def assemble_a_instruction(self, line):
        if line[1].isalpha():  # start at index one because @ is NOT alpha
            symbol = line[1:]
            a_instruction = self.symbol_table.get(line[1:], -1)
            if a_instruction == -1:  # this is a user defined variable (not in Code.symbols)
                a_instruction = self.allocate_memory(symbol)
        else:
            a_instruction = int(line[1:])
        binary_output = str("{0:b}".format(a_instruction))
        return "0" * (16 - len(binary_output)) + binary_output

    def assemble_line(self, line):
        if line[0] == "@":
            return self.assemble_a_instruction(line)
        else:
            return self.assemble_c_instruction(line)

    def assemble(self, normalized_data_list):
        assembled_data = []
        self.build_symbol_table(normalized_data_list)
        for line in normalized_data_list:
            if line[0] != "(":
                assembled_data.append(self.assemble_line(line))
        return assembled_data

    def print_assembler_data(self, flag, normalized_data_list):
        """prints assembler data"""
        print_list = []
        if flag == "a":
            print_list = self.assemble(normalized_data_list)
        for line in print_list:
            print(line)

    def write_to_file(self, input_filename, normalized_data_list):
        output_filename = input_filename.split('.', 1)[0]
        output_file = open(output_filename + ".hack", "w")
        assembled_output = self.assemble(normalized_data_list)
        for line in assembled_output:
            output_file.write(line + "\n")
