from functools import total_ordering

@total_ordering
class Position():
    def __init__(self, line, char):
        self.line = line
        self.char = char

    def __lt__(self, pos):
        return (self.line < pos.line
                or (self.line == pos.line
                    and self.char < pos.char))

    def __eq__(self, pos):
        return (self.line == pos.line
                and self.char == pos.char)

    def clone(self):
        return Position(self.line, self.char) 

class Change():
    def __init__(self, from_pos, to_pos, text):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.text = text

    @property
    def lines(self):
        return self.text.split('\n')

    @property
    def number_new_lines(self):
        return len(self.lines) - 1
    
    def modify(self, pos):
        if self.from_pos > pos:
            return pos.clone()
        if self.to_pos > pos:
            return self.from_pos.clone()
        if self.to_pos.line == pos.line:
            return Position(
                self.from_pos.line + self.number_new_lines,
                self.from_pos.char + len(self.lines[-1])
            )
        return Position(
            (pos.line + self.number_new_lines
             + self.from_pos.line - self.to_pos.line),
            pos.char
        )

