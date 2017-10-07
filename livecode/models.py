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
    def __repr__(self):
        return f'(L{self.line} C{self.char})'
    
    def clone(self):
        return Position(self.line, self.char)
    
    def serialize(self):
        return {
            'line': self.line,
            'ch': self.char,
        }

class Change():
    def __init__(self, from_pos, to_pos, text, id=None):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.text = text
        self.id = id
        
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
            last_line_chars = (
                self.from_pos.char
                if len(self.lines) == 1
                else 0
            )
            return Position(
                self.from_pos.line + self.number_new_lines,
                last_line_chars
                + pos.char - self.to_pos.char
                + len(self.lines[-1])
            )
        return Position(
            (pos.line + self.number_new_lines
             + self.from_pos.line - self.to_pos.line),
            pos.char
        )

    def clone(self):
        return Change(
            self.from_pos,
            self.to_pos,
            self.text,
            self.id
        )
    
    def __repr__(self):
        return (f'Change:{self.id} from: {self.from_pos} '
                f'to: {self.to_pos} text: "{self.text}"')

    def serialize(self):
        return {
            'id': self.id,
            'from': self.from_pos.serialize(),
            'to': self.to_pos.serialize(),
            'text': self.lines,
        }

