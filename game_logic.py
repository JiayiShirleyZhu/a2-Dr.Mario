

class HalfCapsule:
    """
    Represents one half of a capsule on the field.

    Args:
        color (str): The color of the half capsule.
        row (int): The row position of the half capsule.
        col (int): The column position of the half capsule.
        state (str): 'falling', 'landed', or 'frozen'.
        orientation (str, optional): if this half capsule form a capsule with another half capsule,
        they will have a orientation indicating whether they are horizontal or vertical.
    """
    def __init__(self, color: str, row: int, col: int, state: str, orientation: str = None) -> None:
        self.color = color.upper()
        self.row = row  # The index of the cell
        self.col = col
        self.state = state  # falling, landed, frozen
        self.orientation = orientation
        self.delay = False  # this is used when half capsule detach from another half capsule


class GameState:
    """
    Keeps track of the game field, current capsules, and matching state.
    """
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.field = []
        self.faller = None  # The currently falling capsule
        self.half_capsules = []
        self.capsules = []
        self.game_over = False
        self.matched_set = set()

    def initialize_field(self, rows: int, columns: int, setting: str, contents: list[str] = None) -> None:
        """
        Sets up the field with given size and content.

        Args:
            rows (int): Number of rows.
            columns (int): Number of columns.
            setting (str): 'EMPTY' or 'CONTENTS'.
            contents (list[str], optional): Field contents.
        """
        self.rows = rows
        self.columns = columns
        self.field = [[" " for _ in range(columns)] for _ in range(rows)]

        if setting == 'EMPTY':
            return

        elif setting == 'CONTENTS':
            for i, line in enumerate(contents):
                if len(line) != columns:
                    raise ValueError(f"Line {i + 1} must have exactly {self.columns} characters.")
                for j, character in enumerate(line):
                    self.field[i][j] = ' ' if character == ' ' else character

            for i in range(self.rows):
                for j in range(self.columns):
                    character = self.field[i][j]
                    if character.isupper():
                        if i == self.rows - 1 or self.field[i + 1][j] != ' ':
                            half_capsule = HalfCapsule(character, i, j, 'frozen')
                        else:
                            half_capsule = HalfCapsule(character, i, j, 'falling')
                        self.half_capsules.append(half_capsule)

            self.find_matching()

    def time_passed(self) -> None:
        """
        Updates the field for one time step.
        """
        self.clear_matching()

        self.apply_gravity()

        if self.faller and self.faller[0].state == 'landed' and self.faller[1].state == 'landed':
            self.faller[0].state = 'frozen'
            self.faller[1].state = 'frozen'
            self.faller = None

        self.find_matching()


    def create_faller(self, color1: str, color2: str) -> None:
        """
        Adds a new falling capsule (which is made of two half capsules) to the field.

        Args:
            color1 (str): The color of the left half.
            color2 (str): The color of the right half.
        """
        if self.faller:
            return

        if self.columns % 2 != 0:
            col = self.columns // 2
        else:
            col = self.columns // 2 - 1

        if self.field[1][col] != ' ' or self.field[1][col + 1] != ' ':
            self.game_over = True

        half_capsule1 = HalfCapsule(color1, 1, col, 'falling')
        half_capsule2 = HalfCapsule(color2, 1, col + 1, 'falling')
        half_capsule1.orientation = 'horizontal'
        half_capsule2.orientation = 'horizontal'

        self.field[1][col] = color1
        self.field[1][col + 1] = color2
        self.faller = (half_capsule1, half_capsule2)
        self.capsules.append(self.faller)

    def test_faller_state(self) -> None:
        """
        Checks and updates the faller's state (falling or landed).
        """
        if self.faller and self.faller[0].state == 'falling' and self.faller[1].state == 'falling':
            if self.faller[0].orientation == 'horizontal':
                if self.faller[0].row == self.rows - 1 \
                    or self.field[self.faller[0].row + 1][self.faller[0].col] != ' ' \
                    or self.field[self.faller[1].row + 1][self.faller[1].col] != ' ':
                    self.faller[0].state = 'landed'
                    self.faller[1].state = 'landed'
            else:
                if self.faller[0].row == self.rows - 1 \
                    or self.field[self.faller[0].row + 1][self.faller[0].col] != ' ':
                    self.faller[0].state = 'landed'
                    self.faller[1].state = 'landed'
            return

        if self.faller and self.faller[0].state == 'landed' and self.faller[1].state == 'landed':
            if self.faller[0].orientation == 'horizontal':
                if 0 <= self.faller[0].row < self.rows - 1 \
                    and self.field[self.faller[0].row + 1][self.faller[0].col] == ' ' \
                    and self.field[self.faller[1].row + 1][self.faller[1].col] == ' ':
                    self.faller[0].state = 'falling'
                    self.faller[1].state = 'falling'
            else:
                if  0 <= self.faller[0].row < self.rows - 1 \
                    and self.field[self.faller[0].row + 1][self.faller[0].col] == ' ':
                    self.faller[0].state = 'falling'
                    self.faller[1].state = 'falling'
            return

    def create_virus(self, row: int, col: int, color: str) -> None:
        """
        Puts a virus on the field at a specific location.

        Args:
            row (int): Row position.
            col (int): Column position.
            color (str): Color of the virus.
        """
        if 0 <= row < self.rows and 0 <= col < self.columns and self.field[row][col] == ' ':
            self.field[row][col] = color.lower()
    
    def _get_hc_row(self, half_capsule: HalfCapsule) -> int:
        """
        Get the row of the half capsule

        Args:
            half_capsule: the half capsule I want to get row of

        Returns:
            row position of the half capsule
        """
        return half_capsule.row

    def _get_capsule_row(self, capsule: tuple[HalfCapsule, HalfCapsule]) -> int:
        """
        Return the larger row number from the two half-capsules in the capsule.
        This helps us apply gravity from bottom to top.

        Args:
            capsule: A tuple of two HalfCapsule objects

        Returns:
            The maximum row value
        """
        return max(capsule[0].row, capsule[1].row)


    def apply_gravity(self) -> None:
        """
        Moves all falling capsules or half capsules down if possible.
        """
        half_capsules_sorted = sorted(self.half_capsules, key=self._get_hc_row, reverse=True)
        capsules_sorted = sorted(self.capsules, key=self._get_capsule_row, reverse=True)
        for half_capsule in half_capsules_sorted:  # apply gravity on half capsule
            if half_capsule.state == 'frozen':
                if half_capsule.row < self.rows - 1 and self.field[half_capsule.row + 1][half_capsule.col] == ' ':
                    half_capsule.state = 'falling'

            if half_capsule.state == 'falling':
                if half_capsule.delay:
                    half_capsule.delay = False
                    continue

                elif (half_capsule.row + 1, half_capsule.col) in self.matched_set:
                    continue
                
                if half_capsule.row < self.rows - 1 and self.field[half_capsule.row + 1][half_capsule.col] == ' ':
                    self.field[half_capsule.row + 1][half_capsule.col] = half_capsule.color
                    self.field[half_capsule.row][half_capsule.col] = ' '
                    half_capsule.row += 1

                if half_capsule.row == self.rows - 1 or self.field[half_capsule.row + 1][half_capsule.col] != ' ':
                    half_capsule.state = 'frozen'

        for capsule in capsules_sorted:  # apply gravity on capsule
            if capsule[0].state == 'falling' and capsule[1].state == 'falling':
                if capsule[0].orientation == 'horizontal':
                    if capsule[0].row < self.rows - 1 \
                        and self.field[capsule[0].row + 1][capsule[0].col] == ' ' \
                        and self.field[capsule[1].row + 1][capsule[1].col] == ' ':
                        self.field[capsule[0].row + 1][capsule[0].col] = capsule[0].color
                        self.field[capsule[0].row][capsule[0].col] = ' '
                        capsule[0].row += 1
                        self.field[capsule[1].row + 1][capsule[1].col] = capsule[1].color
                        self.field[capsule[1].row][capsule[1].col] = ' '
                        capsule[1].row += 1
                else:
                    if capsule[0].row < self.rows - 1 \
                        and self.field[capsule[0].row + 1][capsule[0].col] == ' ':
                        # capsule[0] will always be the bottom left cell
                        self.field[capsule[0].row + 1][capsule[0].col] = capsule[0].color
                        self.field[capsule[1].row + 1][capsule[1].col] = capsule[1].color
                        self.field[capsule[1].row][capsule[1].col] = ' '
                        capsule[0].row += 1
                        capsule[1].row += 1

            elif capsule[0].state == 'frozen' and capsule[1].state == 'frozen':
                if capsule[0].orientation == 'horizontal':
                    if (capsule[0].row + 1, capsule[0].col) in self.matched_set or (capsule[1].row + 1, capsule[1].col) in self.matched_set:  # Avoid a capsule immediately fall into the space left by a just-cleared match.
                        return
                    
                    if capsule[0].row < self.rows - 1 \
                        and self.field[capsule[0].row + 1][capsule[0].col] == ' ' \
                        and self.field[capsule[1].row + 1][capsule[1].col] == ' ':
                        self.field[capsule[0].row + 1][capsule[0].col] = capsule[0].color
                        self.field[capsule[0].row][capsule[0].col] = ' '
                        capsule[0].row += 1
                        self.field[capsule[1].row + 1][capsule[1].col] = capsule[1].color
                        self.field[capsule[1].row][capsule[1].col] = ' '
                        capsule[1].row += 1
                else:
                    if (capsule[0].row + 1, capsule[0].col) in self.matched_set or (capsule[1].row + 1, capsule[1].col) in self.matched_set:
                        return
                    
                    if capsule[0].row < self.rows - 1 \
                        and self.field[capsule[0].row + 1][capsule[0].col] == ' ':
                        # capsule[0] will always be the bottom left cell
                        self.field[capsule[0].row + 1][capsule[0].col] = capsule[0].color
                        self.field[capsule[1].row + 1][capsule[1].col] = capsule[1].color
                        self.field[capsule[1].row][capsule[1].col] = ' '
                        capsule[0].row += 1
                        capsule[1].row += 1

    def _can_match(self, half_capsule: HalfCapsule) -> bool:
        """
        Checks if a half capsule can be matched (must be frozen).

        Args:
            half_capsule (HalfCapsule): The half capsule to check.

        Returns:
            bool: True if it's frozen.
        """
        return half_capsule.state == 'frozen'

    def find_matching(self) -> set[tuple[int, int]]:
        """
        Finds all matched positions on the field.

        Returns:
            set[tuple[int, int]]: Positions that is matched and should be cleared.
        """
        not_match_lst = []
        matched_set = set()
        for half_capsule in self.half_capsules:
            if not self._can_match(half_capsule):
                not_match_lst.append((half_capsule.row, half_capsule.col))
        for capsule in self.capsules:
            for half_capsule in capsule:
                if not self._can_match(half_capsule):
                    not_match_lst.append((half_capsule.row, half_capsule.col))

        # horizontal matching
        for r in reversed(range(self.rows)):
            for c in range(self.columns - 3):
                if all((r, c + i) not in not_match_lst for i in range(4)) and \
                    self.field[r][c] != ' ' and \
                    self.field[r][c].upper() == self.field[r][c + 1].upper() == self.field[r][c + 2].upper() == self.field[r][c + 3].upper():
                    matched_set.update({(r, c), (r, c + 1), (r, c + 2), (r, c + 3)})

        # vertical matching
        for c in range(self.columns):
            for r in reversed(range(self.rows - 3)):
                if all((r + i, c) not in not_match_lst for i in range(4)) and \
                    self.field[r][c] != ' ' and \
                    self.field[r][c].upper() == self.field[r + 1][c].upper() == self.field[r + 2][c].upper() == self.field[r + 3][c].upper():
                    matched_set.update({(r, c), (r + 1, c), (r + 2, c), (r + 3, c)})

        self.matched_set = matched_set
        return matched_set

    def clear_matching(self) -> None:
        """
        Removes all matched items from the field.
        """
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
                remove_lst2.append((capsule[0], capsule[1]))
            elif (capsule[0].row, capsule[0].col) in matched_set:
                remove_lst2.append((capsule[0], capsule[1]))
                capsule[1].state = 'falling'
                capsule[1].delay = True
                self.half_capsules.append(capsule[1])
            elif (capsule[1].row, capsule[1].col) in matched_set:
                remove_lst2.append((capsule[0], capsule[1]))
                capsule[0].state = 'falling'
                capsule[0].delay = True
                self.half_capsules.append(capsule[0])     

        for capsule in remove_lst2:
            self.capsules.remove(capsule)

        for r, c in matched_set:
            self.field[r][c] = ' '

    def move_left(self) -> None:
        """
        Moves the faller to the left (one space).
        """
        if not self.faller:
            return

        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].orientation == 'horizontal':
            if c1 > 0 and self.field[r1][c1 - 1] == ' ':
                self.field[r1][c1 - 1] = self.faller[0].color
                self.field[r1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[0].col -= 1
                self.faller[1].col -= 1

            else:
                return
        else:
            if c1 > 0 and c2 > 0 and self.field[r1][c1 - 1] == ' ' and self.field[r2][c2 - 1] == ' ':
                self.field[r1][c1 - 1] = self.faller[0].color
                self.field[r2][c2 - 1] = self.faller[1].color
                self.field[r1][c1] = ' '
                self.field[r2][c2] = ' '
                self.faller[0].col -= 1
                self.faller[1].col -= 1

            else:
                return

    def move_right(self) -> None:
        """
        Moves the faller to the right (one space).
        """
        if not self.faller:
            return

        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].orientation == 'horizontal':
            if c2 < self.columns - 1 and self.field[r2][c2 + 1] == ' ':
                self.field[r2][c2 + 1] = self.faller[1].color
                self.field[r2][c2] = self.faller[0].color
                self.field[r1][c1] = ' '
                self.faller[0].col += 1
                self.faller[1].col += 1

            else:
                return
        else:
            if c1 < self.columns - 1 and c2 < self.columns - 1 and self.field[r1][c1 + 1] == ' ' and self.field[r2][c2 + 1] == ' ':
                self.field[r1][c1 + 1] = self.faller[0].color
                self.field[r2][c2 + 1] = self.faller[1].color
                self.field[r1][c1] = ' '
                self.field[r2][c2] = ' '
                self.faller[0].col += 1
                self.faller[1].col += 1

            else:
                return

    def rotate_clockwise(self) -> None:
        """
        Rotates the faller clockwise.
        """
        if not self.faller:
            return

        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].orientation == 'horizontal':
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1 and self.field[r1 - 1][c1] == ' ':
                self.field[r1 - 1][c1] = self.faller[0].color
                self.field[r1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                original_color1 = self.faller[0].color
                self.faller[0].color = self.faller[1].color
                self.faller[1].color = original_color1
                # keep the self.faller[0] always be the bottom left half capsule
                self.faller[1].row -= 1
                self.faller[1].col -= 1
                self.faller[0].orientation = 'vertical'
                self.faller[1].orientation = 'vertical'
            else:
                return

        else:
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1 and self.field[r1][c1 + 1] == ' ':
                self.field[r1][c1 + 1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[1].row += 1
                self.faller[1].col += 1
                self.faller[0].orientation = 'horizontal'
                self.faller[1].orientation = 'horizontal'
            elif 0 < r1 < self.rows and 0 < c1 <= self.columns - 1 and self.field[r1][c1 - 1] == ' ':  # wall kick
                self.field[r1][c1 - 1] = self.faller[0].color
                self.field[r1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[0].col -= 1
                self.faller[1].row += 1
                self.faller[0].orientation = 'horizontal'
                self.faller[1].orientation = 'horizontal'
            else:
                return

    def rotate_counterclockwise(self) -> None:
        """
        Rotates the faller counterclockwise.
        """
        if not self.faller:
            return

        r1 = self.faller[0].row
        c1 = self.faller[0].col
        r2 = self.faller[1].row
        c2 = self.faller[1].col

        if self.faller[0].orientation == 'horizontal':
            if 0 < r1 < self.rows and 0 <= c1 < self.columns - 1 and self.field[r1 - 1][c1] == ' ':
                self.field[r1 - 1][c1] = self.faller[1].color
                self.field[r2][c2] = ' '
                self.faller[1].row -= 1
                self.faller[1].col -= 1
                self.faller[0].orientation = 'vertical'
                self.faller[1].orientation = 'vertical'
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
                self.faller[0].orientation = 'horizontal'
                self.faller[1].orientation = 'horizontal'
            elif 0 < r1 < self.rows and 0 < c1 <= self.columns - 1 and self.field[r1][c1 - 1] == ' ':  # wall kick
                self.field[r1][c1 - 1] = self.faller[1].color
                self.field[r2][c2] = ' '
                original_color1 = self.faller[0].color
                self.faller[0].color = self.faller[1].color
                self.faller[1].color = original_color1
                self.faller[0].col -= 1
                self.faller[1].row += 1
                self.faller[0].orientation = 'horizontal'
                self.faller[1].orientation = 'horizontal'
            else:
                return

    def detect_viruses(self) -> bool:
        """
        Check if there are still viruses on the field.

        Returns:
            bool: True if any viruses are still on the field.
        """
        count = 0
        for lst in self.field:
            for cell in lst:
                if cell in ('r', 'b', 'y'):
                    count += 1
        if count != 0:
            return True     
        else:
            return False
