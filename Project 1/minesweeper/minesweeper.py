import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count # count of number of mines in self.cells

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()
        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.

        if cell is in the sentence, function should update the sentence so that cell is no longer in the sentence, but still represent correct sentence
        given that cell is known to be a mine.

        if cell is not in sentence, no action required.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
    

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.

        if cell is in the sentence, function should update the sentence so that cell is no longer in the sentence, but still represent correct sentence
        given that cell is known to be safe.

        if cell is not in sentence, no action required.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.mark_safe(cell)
        # 3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`

        # find neighbours of the current cell
        neighbours = set()
        neighbours.add((cell[0] - 1, cell[1])) # top
        neighbours.add((cell[0] + 1, cell[1])) # bottom
        neighbours.add((cell[0], cell[1] + 1)) # right
        neighbours.add((cell[0], cell[1] - 1)) # left
        neighbours.add((cell[0] - 1, cell[1] + 1)) # diag up right
        neighbours.add((cell[0] - 1, cell[1] - 1)) # diag up left
        neighbours.add((cell[0] + 1, cell[1] - 1)) # diag down left
        neighbours.add((cell[0] + 1, cell[1] + 1)) # diag down right

        valid_cells = set()
        for n in neighbours:
            # check whether cell is valid in board
            if 0 <= n[0] < self.height and 0 <= n[1] < self.width:
                # check if cell is safe: has not been travelled to before, and not a mine
                if n not in self.moves_made and n not in self.mines:
                    valid_cells.add((n[0], n[1]))
                if n in self.mines:
                    count -= 1

        self.knowledge.append(Sentence(valid_cells, count))

        #  4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge.copy():
            safe_sentence = sentence.known_safes().copy()
            for safe in safe_sentence:
                self.mark_safe(safe)
            mine_sentence = sentence.known_mines().copy()
            for mine in mine_sentence:
                self.mark_mine(mine)

        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        # set1 = count1 and set2 = count2 where set1 is a subset of set2, then we can construct the new sentence set2 - set1 = count2 - count1
        for set1 in self.knowledge:
            for set2 in self.knowledge:
                if set1 is set2:
                    continue
                if set1 == set2: 
                    self.knowledge.remove(set2)
                    continue
                if set1.cells.issubset(set2.cells):
                    new = Sentence(set2.cells - set1.cells, set2.count - set1.count)
                    if new not in self.knowledge:
                        self.knowledge.append(new)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        available = self.safes - self.moves_made
        if len(available) > 0:
            return random.choice(tuple(available))
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # if there are no moves left
        if len(self.mines) + len(self.moves_made) == self.height * self.width:
            return None

        while True:
            row = random.randrange(self.height)
            col = random.randrange(self.width)
            if (row, col) not in self.moves_made and (row, col) not in self.mines:
                return (row, col)
