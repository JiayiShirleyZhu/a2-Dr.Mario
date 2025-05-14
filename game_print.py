import game_logic


def print_field(game_state: game_logic.GameState) -> None:
    """
    Prints the current game field, showing all capsules, their states,
    and highlighting matched positions.

    Args:
        game_state (GameState): The current state of the game.
    """
    display_field = []
    for r in range(game_state.rows):
        row_display = []
        for c in range(game_state.columns):
            cell = game_state.field[r][c]
            row_display.append(f" {cell} ")
        display_field.append(row_display)

    for capsule in game_state.capsules:
        if capsule[0].orientation == 'horizontal' and capsule[1].orientation == 'horizontal':
            if capsule[0].state == 'falling':
                display_field[capsule[0].row][capsule[0].col] = f'[{capsule[0].color}-'
                display_field[capsule[1].row][capsule[1].col] = f'-{capsule[1].color}]'
            elif capsule[0].state == 'landed':
                display_field[capsule[0].row][capsule[0].col] = f'|{capsule[0].color}-'
                display_field[capsule[1].row][capsule[1].col] = f'-{capsule[1].color}|'
            elif capsule[0].state == 'frozen':
                display_field[capsule[0].row][capsule[0].col] = f' {capsule[0].color}-'
                display_field[capsule[1].row][capsule[1].col] = f'-{capsule[1].color} '
        elif capsule[0].orientation == 'vertical' and capsule[1].orientation == 'vertical':
            if capsule[0].state == 'falling':
                display_field[capsule[0].row][capsule[0].col] = f'[{capsule[0].color}]'
                display_field[capsule[1].row][capsule[1].col] = f'[{capsule[1].color}]'
            elif capsule[0].state == 'landed':
                display_field[capsule[0].row][capsule[0].col] = f'|{capsule[0].color}|'
                display_field[capsule[1].row][capsule[1].col] = f'|{capsule[1].color}|'

    for r, c in game_state.find_matching():
        display_field[r][c] = f"*{game_state.field[r][c]}*"

    for row in display_field:
        print("|" + ''.join(row) + "|")
    print(' ' + '---' * game_state.columns + ' ')


def level_cleared(game_state: game_logic.GameState) -> None:
    """
    Checks if the level is cleared (no viruses left) and prints a message.

    Args:
        game_state (GameState): The current state of the game.
    """
    if not game_state.detect_viruses():
        print("LEVEL CLEARED")


def game_over() -> None:
    """
    Prints the game over message.
    """
    print("GAME OVER")
