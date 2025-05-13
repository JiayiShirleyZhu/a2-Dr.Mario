import shlex
import game_print
import game_logic

def get_input_set_field():
    rows = int(input())
    columns = int(input())
    field_setting = input().strip().upper()

    if field_setting == 'EMPTY':
        game_state = game_logic.GameState()
        game_state.initialize_field(rows, columns, 'EMPTY')

    elif field_setting == 'CONTENTS':
        contents = [input() for _ in range(rows)]
        game_state = game_logic.GameState()
        game_state.initialize_field(rows, columns, 'CONTENTS', contents)

    else:
        raise ValueError("Field setting can only be 'EMPTY' or 'CONTENTS'")
    
    return game_state



if __name__ == '__main__':
    game_state = get_input_set_field()

    while True:
        game_print.print_field(game_state)
        game_print.level_cleared(game_state)
        command = input()
        if command.strip().upper() == 'Q':
            break
        
        if command.strip() == '':
            game_state.time_passed()
            continue

        command_lst = shlex.split(command)

        if command_lst[0] == 'F':
            left_color = command_lst[1]
            right_color = command_lst[2]
            game_state.create_faller(left_color, right_color)
            if game_state.game_over:
                game_print.print_field(game_state)
                game_print.game_over()
                break

        elif command_lst[0] == 'V':
            row = int(command_lst[1])
            column = int(command_lst[2])
            color = command_lst[3]
            game_state.create_virus(row, column, color)

        elif command_lst[0] == 'A':
            game_state.rotate_clockwise()
          
        elif command_lst[0] == 'B':
            game_state.rotate_counterclockwise()

        elif command_lst[0] == '<':
            game_state.move_left()

        elif command_lst[0] == '>':
            game_state.move_right()


        
