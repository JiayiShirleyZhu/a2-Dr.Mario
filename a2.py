import shlex
import user_interface
import game_logic

if __name__ == '__main__':
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
    
    user_interface.render_field(columns, game_state.field)

    while True:
        command = input()
        if command.strip().upper() == 'Q':
            break
        
        if command.strip() == '':
            game_state.time_passed()

        command_lst = shlex.split(command)

        if command_lst[0] == 'F':
            try:
                left_color = command_lst[1]
                right_color = command_lst[2]
                game_state.create_faller(left_color, right_color)
            except IndexError:
                print("Invaild input, please write in the form '[comamnd][left color][right color]'")

        elif command_lst[0] == 'V':
            try:
                row = command_lst[1]
                column = command_lst[2]
                color = command_lst[3]
                game_state.create_virus(row, column, color)
            except IndexError:
                print("Invaild input, please write in the form '[comamnd][row][column][color]'")

        elif command_lst[0] == 'A':
            game_state.faller.rotate_clockwise()

        elif command_lst[0] == 'B':
            game_state.faller.rotate_counterclockwise()

        elif command_lst[0] == '>':
            game_state.faller.move_left()

        elif command_lst[0] == '<':
            game_state.faller.move_right()

        


        


