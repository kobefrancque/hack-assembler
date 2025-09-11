class Parser:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
        self.index = 0
        self.commands = list()
        
        for line in self.lines:
            processed_line = line.strip().replace(' ', '').split('//')[0]
            if processed_line:
                self.commands.append(processed_line)

        self.current_line = None

    def has_more_commands(self):
        return self.index < len(self.commands)
    
    def advance(self):
        if self.has_more_commands():
            self.current_line = self.commands[self.index]
            self.index += 1

    def command_type(self):
        if self.current_line.startswith('@'):
            return 'A_COMMAND'
        elif any(char in self.current_line for char in ['=', ';']):
            return 'C_COMMAND'
        else:
            return 'L_COMMAND'
        
    def symbol(self) -> str:
        if self.command_type() == 'A_COMMAND':
            return self.current_line.strip('@')
        elif self.command_type() == 'L_COMMAND':
            return self.current_line.strip('()')
        
    def dest(self) -> str | None:
        if self.command_type() == 'C_COMMAND':
            if '=' in self.current_line:
                return self.current_line.split('=')[0]
            else:
                return None
            
    def comp(self) -> str:
        if self.command_type() == 'C_COMMAND':
            if ';' and '=' in self.current_line:
                return self.current_line.split('=')[1].split(';')[0]
            elif '=' in self.current_line:
                return self.current_line.split('=')[1]
            elif ';' in self.current_line:
                return self.current_line.split(';')[0]
            else:
                return self.current_line
            
    def jump(self) -> str | None:
        if self.command_type() == 'C_COMMAND':
            if ';' in self.current_line:
                return self.current_line.split(';')[1]
            else:
                return None
            
    def reset(self):
        self.index = 0