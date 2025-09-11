from src.parser import Parser
from src.code import Code
from src.symbol_table import SymbolTable
import sys

def main():
    if len(sys.argv) != 2:
        print('provide one argument containing basename of file')

    else:
        basename = sys.argv[1]
        parser = Parser(f'{basename}.asm')
        coder = Code()
        symbol_table = SymbolTable()

        # First loop - look for label declarations
        instruction_address = 0
        while parser.has_more_commands():
            parser.advance()
            if parser.command_type() == 'L_COMMAND':
                symbol_table.add_entry(parser.symbol(), instruction_address)    # The instruction after the label declaration is where the label block starts
            else:
                instruction_address += 1    # label declarations are not real instructions and should thus not be considered when we track instruction addresses

        parser.reset()

        # Second loop - translate assembly into machine code
        machine_instructions = list()
        memory_idx = 16     # memory starting at register 16 is dedicated for variables, increase memory index by one every time a new variable is created

        while parser.has_more_commands():
            parser.advance()
            
            if parser.command_type() == 'C_COMMAND':
                dest_field = coder.dest(parser.dest())
                comp_field = coder.comp(parser.comp())
                jump_field = coder.jump(parser.jump())
                machine_instruction = f'111{comp_field}{dest_field}{jump_field}'

                machine_instructions.append(machine_instruction)

            elif parser.command_type() == 'A_COMMAND':
                if parser.symbol().isnumeric():
                    decimal_value = parser.symbol()
                else:
                    if symbol_table.contains(parser.symbol()):
                        decimal_value = symbol_table.get_address(parser.symbol())
                    else:
                        symbol_table.add_entry(parser.symbol(), memory_idx)
                        decimal_value = memory_idx
                        memory_idx += 1

                binary_value = format(int(decimal_value), '015b')
                machine_instruction = f'0{binary_value}'    # 0 = opcode, 15-bit address

                machine_instructions.append(machine_instruction)

        with open(f'{basename}.hack', 'w') as file:
            file.write('\n'.join(machine_instructions))  