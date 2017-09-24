from livecode import models

def transform_change(change, change_modifier):
    return models.Change(
        change.modify(change_modifier.from_pos),
        change.modify(change_modifier.to_pos),
        text = change.text
    )

def transform(code, changes):
    return str.join('\n', _transform(code.split('\n'), changes))

def _transform(lines, changes):
    '''make changes to lines of text'''
    if len(changes) == 0: return lines
    change = changes[0]
    before = str.join('\n',
        lines[:change.from_pos.line]
        + [lines[change.from_pos.line][:change.from_pos.char]]
    )
    replaced = str.join('\n', change.lines)
    after = str.join('\n',
        [lines[change.to_pos.line][change.to_pos.char:]]
        + lines[change.to_pos.line + 1:]
    )
    result = str.join('', [before, replaced, after])
    return _transform(str.split(result, '\n'), changes[1:])
