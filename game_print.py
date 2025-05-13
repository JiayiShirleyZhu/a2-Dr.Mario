def print_field(game_state):
    display_field = []
    for r in range(game_state.rows):
        row_display = []
        for c in range(game_state.columns):
            cell = game_state.field[r][c]
            row_display.append(f" {cell} ")
        display_field.append(row_display)

    for capsule in game_state.capsules:
        if capsule[0].pair_orientation == 'horizontal' and capsule[1].pair_orientation == 'horizontal':
            if capsule[0].state == 'falling':
                display_field[capsule[0].row][capsule[0].col] = f'[{capsule[0].color}-'
                display_field[capsule[1].row][capsule[1].col] = f'-{capsule[1].color}]'
            elif capsule[0].state == 'landed':
                display_field[capsule[0].row][capsule[0].col] = f'|{capsule[0].color}-'
                display_field[capsule[1].row][capsule[1].col] = f'-{capsule[1].color}|'
            elif capsule[0].state == 'frozen':
                display_field[capsule[0].row][capsule[0].col] = f' {capsule[0].color}-'
                display_field[capsule[1].row][capsule[1].col] = f'-{capsule[1].color} '
        elif capsule[0].pair_orientation == 'vertical' and capsule[1].pair_orientation == 'vertical':
            if capsule[0].state == 'falling':
                display_field[capsule[0].row][capsule[0].col] = f'[{capsule[0].color}]'
                display_field[capsule[1].row][capsule[1].col] = f'[{capsule[1].color}]'
            elif capsule[0].state == 'landed':
                display_field[capsule[0].row][capsule[0].col] = f'|{capsule[0].color}|'
                display_field[capsule[1].row][capsule[1].col] = f'|{capsule[1].color}|'

    for r, c in game_state.matched_positions:
        display_field[r][c] = f"*{game_state.field[r][c]}*"
    
    for row in display_field:
        print("|" + ''.join(row) + "|")
    print(' ' + '---' * game_state.columns + ' ')

def level_cleared(game_state):
    if not game_state.detect_viruses():
        print("LEVEL CLEARED")

def game_over():
    print("GAME OVER")