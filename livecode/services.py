from livecode import models, data

def apply_changes(changes, last_changeids):
    if len(last_changeids) == 0: return []
    last_changeid = last_changeids[-1]
    prev_changeids = range(last_changeid, current_changeid)
    raise NotImplementedError

def apply_change(change, last_changeid, max_changeid):
    prev_changeids = range(last_changeid + 1, max_changeid + 1)
    prev_changes = data.get_changes(prev_changeids)
    new_change = transform_change(change, prev_changes)
    new_change.id = data.add_change(new_change)
    return new_change

def transform_change(change, change_modifiers):
    if len(change_modifiers) == 0: return change.clone()
    change_modifier = change_modifiers[0]
    modified_change = models.Change(
        change_modifier.modify(change.from_pos),
        change_modifier.modify(change.to_pos),
        text = change.text
    )
    return transform_change(modified_change, change_modifiers[1:])

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
