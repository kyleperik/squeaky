from livecode import models

def test_modify_sameline_after():
    change = models.Change(
        from_pos = models.Position(0, 2),
        to_pos = models.Position(0, 4),
        text = 'a',
    )

    pos = models.Position(0, 4)
    
    result = change.modify(pos)

    assert result.line == 0
    assert result.char == 3

    
def test_modify_sameline_inside():
    change = models.Change(
        from_pos = models.Position(0, 2),
        to_pos = models.Position(0, 4),
        text = 'a',
    )

    pos = models.Position(0, 3)
    
    result = change.modify(pos)

    assert result.line == 0
    assert result.char == 2


def test_modify_sameline_before():
    change = models.Change(
        from_pos = models.Position(0, 3),
        to_pos = models.Position(0, 4),
        text = 'a',
    )

    pos = models.Position(0, 2)
    
    result = change.modify(pos)

    assert result.line == 0
    assert result.char == 2

    
def test_modify_multiplelines_before():
    change = models.Change(
        from_pos = models.Position(2, 3),
        to_pos = models.Position(5, 4),
        text = 'a',
    )

    pos = models.Position(0, 4)
    
    result = change.modify(pos)

    assert result.line == 0
    assert result.char == 4
    
def test_modify_multiplelines_inside():
    change = models.Change(
        from_pos = models.Position(2, 3),
        to_pos = models.Position(5, 4),
        text = 'a',
    )

    pos = models.Position(2, 5)
    
    result = change.modify(pos)

    assert result.line == 2
    assert result.char == 3
    
def test_modify_multiplelines_after_lineof():
    change = models.Change(
        from_pos = models.Position(2, 3),
        to_pos = models.Position(5, 4),
        text = 'a',
    )

    pos = models.Position(5, 6)

    result = change.modify(pos)

    assert result.line == 2
    assert result.char == 4

def test_modify_multiplelines_after():
    change = models.Change(
        from_pos = models.Position(2, 3),
        to_pos = models.Position(5, 4),
        text = 'a',
    )

    pos = models.Position(6, 6)

    result = change.modify(pos)

    assert result.line == 3
    assert result.char == 6
