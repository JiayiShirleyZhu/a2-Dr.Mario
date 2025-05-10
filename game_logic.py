
class Faller:
    def __init__(self, color1, color2, row, col):
        self.color1 = color1.upper()
        self.color2 = color2.upper()
        self.row = row #锚点的坐标
        self.col = col
        self.state = 'falling' #falling, landed
        self.orientation = 'horizontal'

    def get_positions(self) -> list[tuple]:
        if self.orientation == 'horizontal':
            return [(self.row, self.col), (self.row, self.col + 1)]
        else:
            return [(self.row, self.col), (self.row - 1, self.col)]
    
    
    def move_left(self, game_state) -> bool:
        if 0 < self.col <= game_state.columns:
            self.col -= 1
            return True
        else:
            return False

    def move_right(self, game_state) -> bool:
        if 0 <= self.col < game_state.columns:
            self.col += 1
            return True
        else:
            return False

    def rotate_clockwise(self, game_state) -> None:
        if self.orientation == 'horizontal':
            self.color1, self.color2 = self.color2, self.color1
            self.orientation = 'vertical'
            
        else:
            if not game_state.field[self.row][self.col + 1].isalpha():
                self.orientation = 'horizontal'
            elif self.move_left(game_state):
                self.orientation = 'horizontal'
            else:
                return
 
    def rotate_counterclockwise(self, game_state) -> None:  
        if self.orientation == 'horizontal':
            self.orientation = 'vertical'

        else:
            if not game_state.field[self.row][self.col + 1].isalpha():
                self.color1, self.color2 = self.color2, self.color1
                self.orientation = 'horizontal'
            elif self.move_left(game_state):
                self.color1, self.color2 = self.color2, self.color1
                self.orientation = 'horizontal'
            else:
                return  

    def landed():
        pass
    
    def frozen():
        pass

class GameState:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.field = []
        self.faller = None

    def initialize_field(self, rows: int, columns: int, setting: str, contents: list[str] = None) -> None: 
        self.rows = rows
        self.columns = columns
        self.field = [["" for _ in range(columns)] for _ in range(rows)]

        if setting == 'EMPTY':
            return
        
        elif setting == 'CONTENTS':
            for i, line in enumerate(contents):
                if len(line) != columns:
                    raise ValueError(f"Line {i+1} must have exactly {columns} characters.")
                self.field[i] = ['' if character == ' ' else f'{character}' for character in line]
    
    def time_passed(self):
        pass

    def create_faller(self, color1: str, color2: str):
        row = 1
        if self.columns % 2 != 0: #odd
            col = self.columns // 2
        else:
            col = self.columns // 2 - 1
       
        self.faller = Faller(color1, color2, row, col)

    def create_virus(self, row: int, column: int, color: str):
        self.field[row][column] = color.lower()

    def apply_gravity(self):
        if self.faller is not None and self.faller.state == 'falling':
            if not 0 <= self.faller.row < self.rows or not 0 <= self.faller.col < self.columns:
                raise ValueError("Faller's row or column is out of the range of field")

            if self.faller.row == self.rows - 1:
                self.faller.state = 'landed'

            elif self.field[self.faller.row + 1][self.faller.col].isalpha():   
                self.faller.state = 'landed'
            
            else:
                self.faller.row += 1

        else: 
            for i, lst in enumerate(self.field):
                for j, element in enumerate(lst[::-1]):
                    if element in ('R', 'B', 'Y'):
                        if i + 1 < len(self.field):
                            if self.field[i + 1][j] == '':
                                self.field[i][j] = ''
                                self.field[i + 1][j] = element

    def find_matches(self):
        matched_set = set()
        if self.faller is not None:
            faller_positions = set(self.faller.get_positions())
        else:
            faller_positions = set()

        # horizontal matching
        for r in range(self.rows): #检查lst当中是否有有四个及以上连续的elements
            for c in range(self.columns - 3):
                if self.field[r][c] != '' and all((r, c + k) not in faller_positions for k in range(4)):
                    if (self.field[r][c] == self.field[r][c + 1] == self.field[r][c + 2] == self.field[r][c + 3]):
                        matched_set.update({(r, c), (r, c + 1), (r, c + 2), (r, c + 3)})


        # vertical matching
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if self.field[r][c] != '' and all((r + k, c) not in faller_positions for k in range(4)):
                    if (self.field[r][c] == self.field[r + 1][c] == self.field[r + 2][c] == self.field[r + 3][c]):
                        matched_set.update({(r, c), (r + 1, c), (r + 2, c), (r + 3, c)})

        return matched_set

    def clear_matches(self):
        matched_set = self.find_matches()
        for position in matched_set:
            r = position[0]
            c = position[1]
            if 0 <= r < self.rows and 0 <= c < self.columns:
                self.field[r][c] = ''


    def game_over(self):
        pass


    def has_viruses(self) -> bool:
        count = 0
        for lst in self.field:
            for cell in lst:
                for ch in cell:
                    if ch in ('r', 'b', 'y'):
                        count += 1
        if count != 0:
            return True        
        else:
            return False


