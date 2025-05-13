
class HalfCapsule:
    def __init__(self, color, row, col, state, pair = None, orientation = None):
        self.color = color.upper()
        self.row = row # The index of the cell
        self.col = col
        self.state = state #falling, landed, frozen
        self.pair = pair # another HalfCapsule object
        self.pair_orientation = orientation

class GameState:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.field = []
        self.faller = None
        self.half_capsules = []
        self.capsules = []
        self.matched_positions = set()
        self.matching_ready = False
        self.capsule_landed_last_time = False

    def initialize_field(self, rows: int, columns: int, setting: str, contents: list[str] = None) -> None: 
        self.rows = rows
        self.columns = columns
        self.field = [[" " for _ in range(columns)] for _ in range(rows)]

        if setting == 'EMPTY':
            return
        
        elif setting == 'CONTENTS':
            for i, line in enumerate(contents):
                if len(line) != columns:
                    raise ValueError(f"Line {i + 1} must have exactly {columns} characters.")
                for j, character in enumerate(line):
                    self.field[i][j] = ' ' if character == ' ' else character
                    if character.isupper():
                        half_capsule = HalfCapsule(character, i, j, 'falling')
                        self.half_capsules.append(half_capsule)
            self.matched_positions = self.find_matching()
            self.matching_ready = True
                        
    
    def time_passed(self):
        if self.matching_ready:
            self.clear_matching()
            self.matching_ready = False
        
        self.apply_gravity()

        if self.faller and all(hc.state == 'landed' for hc in self.faller) and not self.capsule_landed_last_time:
            self.capsule_landed_last_time = True
            return

        if self.faller and all(hc.state == 'landed' for hc in self.faller) and self.capsule_landed_last_time:
            for half_capsule in self.faller:
                half_capsule.state = 'frozen'
            self.faller = None
            self.capsule_landed_last_time = False

        self.matched_positions = self.find_matching()
        self.matching_ready = True
        
    def create_faller(self, color1, color2):
        if self.faller:
            return "faller exists"
        
        if self.columns % 2 != 0:
            col = self.columns // 2
        else:
            col = self.columns // 2 - 1
        
        if self.field[1][col] != ' ' or self.field[1][col + 1] != ' ':
            return "game over"
        
        if self.field[2][col] == ' ' and self.field[2][col + 1] == ' ':
            half_capsule1 = HalfCapsule(color1, 1, col, 'falling')
            half_capsule2 = HalfCapsule(color2, 1, col + 1, 'falling')
        else:
            half_capsule1 = HalfCapsule(color1, 1, col, 'landed')
            half_capsule2 = HalfCapsule(color2, 1, col + 1, 'landed')
            self.capsule_landed_last_time = True
        half_capsule1.pair = half_capsule2
        half_capsule2.pair = half_capsule1
        half_capsule1.pair_orientation = 'horizontal'
        half_capsule2.pair_orientation = 'horizontal'

        self.field[1][col] = color1
        self.field[1][col + 1] = color2
        self.faller = [half_capsule1, half_capsule2]
        self.capsules.append(self.faller)
    
    def create_virus(self, row, col, color):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.field[row][col] = color.lower()

    def apply_gravity(self):
        for half_capsule in self.half_capsules:# apply gravity on half capsule
            if half_capsule.state == 'falling':
                if half_capsule.row < self.rows - 1 and self.field[half_capsule.row + 1][half_capsule.col] == ' ':
                    self.field[half_capsule.row + 1][half_capsule.col] = half_capsule.color
                    self.field[half_capsule.row][half_capsule.col] = ' '
                    half_capsule.row += 1
                
                if half_capsule.row == self.rows - 1 or self.field[half_capsule.row + 1][half_capsule.col] != ' ':
                    half_capsule.state = 'frozen'
        
        for capsule in self.capsules: # apply gravity on capsule
            if capsule[0].state == 'falling' and capsule[1].state == 'falling':
                if capsule[0].pair_orientation == 'horizontal':
                    if capsule[0].row < self.rows - 1 \
                        and self.field[capsule[0].row + 1][capsule[0].col] == ' ' \
                        and self.field[capsule[1].row + 1][capsule[1].col] == ' ':
                        self.field[capsule[0].row + 1][capsule[0].col] = capsule[0].color
                        self.field[capsule[0].row][capsule[0].col] = ' '
                        capsule[0].row += 1
                        self.field[capsule[1].row + 1][capsule[1].col] = capsule[1].color
                        self.field[capsule[1].row][capsule[1].col] = ' '
                        capsule[1].row += 1
                    if capsule[0].row == self.rows - 1 \
                        or self.field[capsule[0].row + 1][capsule[0].col] != ' ' \
                        or self.field[capsule[1].row + 1][capsule[1].col] != ' ':
                        capsule[0].state = 'landed'
                        capsule[1].state = 'landed'
                else:
                    if capsule[0].row < self.rows - 1 \
                        and self.field[capsule[0].row + 1][capsule[0].col] == ' ':
                        # capsule[0] will always be the bottom left cell
                        self.field[capsule[0].row + 1][capsule[0].col] = capsule[0].color
                        self.field[capsule[1].row + 1][capsule[1].col] = capsule[1].color
                        self.field[capsule[1].row][capsule[1].col] = ' '
                        capsule[0].row += 1
                        capsule[1].row += 1
                    if capsule[0].row == self.rows - 1 \
                        or self.field[capsule[0].row + 1][capsule[0].col] != ' ':
                        capsule[0].state = 'landed'
                        capsule[1].state = 'landed'

    def _can_match(self, half_capsule):
        return half_capsule.state == 'frozen'

    def find_matching(self):
        not_match_lst = []
        matched_set = set()
        for half_capsule in self.half_capsules:
            if not self._can_match(half_capsule):
                not_match_lst.append((half_capsule.row, half_capsule.col))
        for capsule in self.capsules:
            for half_capsule in capsule:
                if not self._can_match(half_capsule):
                    not_match_lst.append((half_capsule.row, half_capsule.col))

        #horizontal matching
        for r in reversed(range(self.rows)): 
            for c in range(self.columns - 3):
                if all((r, c + i) not in not_match_lst for i in range(4)) and \
                    self.field[r][c] != ' ' and \
                    self.field[r][c].upper() == self.field[r][c + 1].upper() == self.field[r][c + 2].upper() == self.field[r][c + 3].upper():
                    matched_set.update({(r, c), (r, c + 1), (r, c + 2), (r, c + 3)})
        
        #vertical matching
        for c in range(self.columns):
            for r in reversed(range(self.rows - 3)):
                if all((r + i, c) not in not_match_lst for i in range(4)) and \
                    self.field[r][c] != ' ' and \
                    self.field[r][c].upper() == self.field[r + 1][c].upper() == self.field[r + 2][c].upper() == self.field[r + 3][c].upper():
                        matched_set.update({(r, c), (r + 1, c), (r + 2, c), (r + 3, c)})

        return matched_set

    def clear_matching(self):
        matched_set = self.find_matching()
        remove_lst1 = []
        for half_capsule in self.half_capsules:
            if (half_capsule.row, half_capsule.col) in matched_set:
                remove_lst1.append(half_capsule)

        for hc in remove_lst1:
            self.half_capsules.remove(hc)
        
        remove_lst2 = []
        for capsule in self.capsules:
            if (capsule[0].row, capsule[0].col) in matched_set and (capsule[1].row, capsule[1].col) in matched_set:
                remove_lst2.append([capsule[0], capsule[1]])
            elif (capsule[0].row, capsule[0].col) in matched_set:
                remove_lst2.append([capsule[0], capsule[1]])
                capsule[1].state = 'falling'
                self.half_capsules.append(capsule[1])
            elif (capsule[1].row, capsule[1].col) in matched_set:
                remove_lst2.append([capsule[0], capsule[1]])
                capsule[0].state = 'falling'
                self.half_capsules.append(capsule[0])
        
        for capsule in remove_lst2:
            self.capsules.remove(capsule)

        for r, c in matched_set:
            self.field[r][c] = ' '

    def move_left(self):
        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].pair_orientation == 'horizontal':
            if c1 > 0 and self.field[r1][c1 - 1] == ' ':
                self.field[r1][c1 - 1] = self.faller[0].color
                self.field[r1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[0].col -= 1
                self.faller[1].col -= 1

            else:
                return 
        else:
            if c1 > 0 and self.field[r1][c1 - 1] == ' ':
                self.field[r1][c1 - 1] = self.faller[0].color
                self.field[r2][c2 - 1] = self.faller[1].color
                self.field[r1][c1] = ' '
                self.field[r2][c2] = ' '
                self.faller[0].col -= 1
                self.faller[1].col -= 1

            else:
                return 
    
    def move_right(self):
        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col
        
        if self.faller[0].pair_orientation == 'horizontal':
            if c2 < self.columns - 1 and self.field[r2][c2 + 1] == ' ':
                self.field[r2][c2 + 1] = self.faller[1].color
                self.field[r2][c2] = self.faller[0].color
                self.field[r1][c1] = ' '
                self.faller[0].col += 1
                self.faller[1].col += 1

            else:
                return 
        else:
            if c1 < self.columns - 1 and self.field[r1][c1 + 1] == ' ':
                self.field[r1][c1 + 1] = self.faller[0].color
                self.field[r2][c2 + 1] = self.faller[1].color
                self.field[r1][c1] = ' '
                self.field[r2][c2] = ' '
                self.faller[0].col += 1
                self.faller[1].col += 1

            else:
                return 

    def rotate_clockwise(self):
        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].pair_orientation == 'horizontal':
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1:
                self.field[r1 - 1][c1] = self.faller[0].color
                self.field[r1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                original_color1 = self.faller[0].color
                self.faller[0].color = self.faller[1].color
                self.faller[1].color = original_color1
                # keep the self.faller[0] always be the bottom left half capsule
                self.faller[1].row -= 1
                self.faller[1].col -= 1
                self.faller[0].pair_orientation = 'vertical'
                self.faller[1].pair_orientation = 'vertical'
            else:
                return
                
        else:
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1 and self.field[r1][c1 + 1] == ' ':
                self.field[r1][c1 + 1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[1].row += 1
                self.faller[1].col += 1
                self.faller[0].pair_orientation = 'horizontal'
                self.faller[1].pair_orientation = 'horizontal'
            elif c1 > 0 and self.field[r1][c1 + 1] != ' ': #wall kick
                self.move_left()
                self.field[r1][c1 - 1] = self.faller[0].color
                self.field[r1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[0].col += 1
                self.faller[1].row += 1
                self.faller[0].pair_orientation = 'horizontal'
                self.faller[1].pair_orientation = 'horizontal'
            else:
                return

    def rotate_counterclockwise(self):
        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].pair_orientation == 'horizontal':
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1:
                self.field[r1 - 1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[1].row -= 1
                self.faller[1].col -= 1
                self.faller[0].pair_orientation = 'vertical'
                self.faller[1].pair_orientation = 'vertical'
            else:
                return
                
        else:
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1 and self.field[r1][c1 + 1] == ' ':
                self.field[r1][c1] = self.faller[1].color
                self.field[r1][c1 + 1] = self.faller[0].color
                self.field[r2][c2] = ' '
                original_color1 = self.faller[0].color
                self.faller[0].color = self.faller[1].color
                self.faller[1].color = original_color1
                self.faller[1].row += 1
                self.faller[1].col += 1
                self.faller[0].pair_orientation = 'horizontal'
                self.faller[1].pair_orientation = 'horizontal'
            elif c1 > 0 and self.field[r1][c1 + 1] != ' ': #wall kick
                self.field[r1 + 1][c1 - 1] = self.faller[1].color
                self.field[r2][c2] = ' '
                original_color1 = self.faller[0].color
                self.faller[0].color = self.faller[1].color
                self.faller[1].color = original_color1
                self.faller[0].col -= 1
                self.faller[1].row += 1
                self.faller[0].pair_orientation = 'horizontal'
                self.faller[1].pair_orientation = 'horizontal'
            else:
                return
    
    def detect_viruses(self) -> bool:
        count = 0
        for lst in self.field:
            for cell in lst:
                if cell in ('r', 'b', 'y'):
                        count += 1
        if count != 0:
            return True        
        else:
            return False
