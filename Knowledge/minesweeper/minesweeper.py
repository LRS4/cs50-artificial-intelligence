import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty 2d array with no mines
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
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.

        Where the board cells set length is equal to the count (of board
        cells which are mines) then those cells are certainly mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        Where the count (of board cells which are mines) is zero then
        the board cells are certainly safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine. Must check all cells in the sentence.

        This method should:
            1) If cell is in the sentence, the method should update the 
               sentence so that cell is no longer in the sentence, but still
               represents a logically correct sentence given that cell is 
               known to be a mine.
            2) If cell is not in the sentence, then no action is necessary.
        """
        if cell not in self.cells:
            return

        self.cells = self.cells.remove(cell)

        if len(self.cells) == 0:
            self.count = 0
        else:
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe. Must check all cells in the sentence.

        This method should:
            1) If cell is in the sentence, the method should update the 
               sentence so that cell is no longer in the sentence, but still
               represents a logically correct sentence given that cell is 
               known to be safe.
            2) If cell is not in the sentence, then no action is necessary.
        """
        if cell not in self.cells:
            return

        self.cells.remove(cell)
        
        if len(self.cells) == 0:
            self.count = 0
        else:
            self.count -= 1


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

        This method should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print(f"Adding cell {cell} with count {count} to knowledge")
        self.moves_made.add(cell)
        self.mark_safe(cell)
        self.add_new_sentence_to_knowledge_base(cell, count)
        self.mark_any_additional_cells_as_safe_or_mines()
        self.add_any_new_inferred_sentences()

    def add_new_sentence_to_knowledge_base(self, cell, count):
        sentence = Sentence(self.get_neighbours(cell), count)
        self.knowledge.append(sentence)

    def mark_any_additional_cells_as_safe_or_mines(self):
        knowledge_copy = copy.deepcopy(self.knowledge)

        for sentence in knowledge_copy:
            mines, safes = sentence.known_mines(), sentence.known_safes()
            for cell in sentence.cells:
                if cell in mines:
                    self.mark_mine(cell)
                elif cell in safes:
                    self.mark_safe(cell)

    def add_any_new_inferred_sentences(self):
        pass

    def get_neighbours(self, cell):
        """
        Returns a set with all of the neighbours for a given cell.
        """
        neighbours = set()

        for i in range(self.height):
            for j in range(self.width):
                if (i, j) == cell:
                    continue

                if abs(i - cell[0]) == 1 and abs(j - cell[1]) == 0:
                    neighbours.add((i, j))
                elif abs(i - cell[0]) == 0 and abs(j - cell[1]) == 1:
                    neighbours.add((i, j))
                elif abs(i - cell[0]) == 1 and abs(j - cell[1]) == 1:
                    neighbours.add((i, j))
                else:
                    continue

        return neighbours

    def make_safe_move(self):
        """
        Returns first known safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made. If no safe move can be guaranteed, 
        the method should return None.

        This method may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        candidate_moves = []
        
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made or move not in self.mines:
                    candidate_moves.append(move)

        return random.choice(candidate_moves) if len(candidate_moves) > 0 else None



if __name__ == "__main__":
    ai = MinesweeperAI()
