import shlex

def render_field(columns: int, field: list[list]) -> None:
    for lst in field:
        print('|', end = '')
        for cell in lst:
            print(f' {cell} ', end = '')
        print('|')
    print(' ' + '---' * columns + ' ')


def level_cleared() -> None:
    print('LEVEL CLEARED')

def game_over():
    print('GAME OVER')
