from livecode import services, models

def test_transform():
    code = '''line one
line two
line three'''

    changes = [
        models.Change(
            models.Position(2, 4),
            models.Position(2, 4),
            ' change',
        ),
        models.Change(
            models.Position(0, 0),
            models.Position(0, 4),
            'modification',
        ),
    ]
    
    result = services.transform(code, changes)

    result_lines = result.split('\n')

    assert len(result_lines) == 3
    assert result_lines[0] == 'modification one'
    assert result_lines[1] == 'line two'
    assert result_lines[2] == 'line change three'
