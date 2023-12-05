debug = False
def print_debug(message):
    if debug:
        print(message)    

class Cell():
    def __init__(self, value = 0):
        print_debug("Cell.init")
        self.value = value
        self.possibles = [1,2,3,4,5,6,7,8,9]
        self.lock = False
        if self.value != 0:
            self.possibles = []
            self.lock = True
    
    def set_value(self, new_value):
        self.value = new_value
        self.possibles = []
        self.lock = True
    
    def __str__(self):
        return str(self.value)

class Board():
    def __init__(self, board = 0):
        print_debug("Board.init")
        if board == 0:
            self.cells = [Cell() for i in range(81)]
        else:
            self.cells = [Cell(int(i)) for i in board]
        self.rows = []
        self.columns = []
        self.sectors = []
        self.build_structs()
        self.state = ""

    def show(self):
        print_debug("Board.show")
        for i in range(9):
            if i == 3 or i == 6:
                print("------+-------+------")
            for j in range(9):
                if j == 3 or j == 6:
                    print("| ", end="")
#                print("{} ".format(str(self.cells[(i *9 + j)])), end = "")
                print("{} ".format(self.cells[(i *9 + j)]), end = "")
            print()
            
    def show_possibles(self):
        print_debug("Board.show possibles")
        self.update()
        for i in range(9):
            if i == 3 or i == 6:
                print("------+-------+------")
            for j in range(9):
                if j == 3 or j == 6:
                    print("| ", end="")
    #                print("{} ".format(str(self.cells[(i *9 + j)])), end = "")
                print("{} ".format(len(self.cells[(i *9 + j)].possibles)), end = "")
            print()

    def enter(self, row_number = -1):
        print_debug("Board.enter")
        #TODO Reformat this
        #TODO Check entered rows are nine digits long
        if row_number == -1:
            print("Enter known numbers. Use 0 for empty cells.")
            data = []
            #TODO allow breaking early
            for i in range(9):
                data += input("Row {} ".format(i + 1)).replace(" ", "")
            for i in range(81):
                self.cells[i].value = int(data[i])
        else:
            print("Enter known numbers in row {}. Use 0 for empty cells.".format(row_number))
            data = input("Row {} ".format(row_number)).replace(" ", "")
            insert_index = (row_number - 1) * 9
            for number in data:
                self.cells[insert_index] = int(number)
                insert_index += 1

    def build_structs(self):
        print_debug("Board.build structs")
        # Rows
        self.rows = [self.cells[i*9:(i+1)*9] for i in range(9)]
        # Columns
        self.columns = [[self.cells[j*9 + i] for j in range(9)] for i in range(9)]
        # Sectors
        self.sectors = []
        kernel = (-10, -9, -8, -1, 0, 1, 8, 9, 10)
        kernel_centres = (10, 13, 16, 37, 40, 43, 64, 67, 70)
        for centre in kernel_centres:
            temp = []
            for cell in kernel:
                temp.append(self.cells[cell + centre])
            self.sectors.append(temp)

    def print_structs(self):
        for row in self.rows:
            print([cell.value for cell in row])
        print()
        for col in self.columns:
            print([cell.value for cell in col])
        print()
        for sect in self.sectors:
            print([cell.value for cell in sect])
            
    # Go through structures
    # Remove possibles that have values in the struct it is in
    def update(self):
        print_debug("Board.update")
        #go through these structures and remove possibilies from cells
        for row in self.rows:
            #get found numbers
            numbers = [cell.value for cell in row if cell.value != 0]
            #remove these numbers from the possibilities in each cell
            for cell in row:
                cell.possibles = list(set(cell.possibles) - set(numbers))

        for column in self.columns:
            numbers = [cell.value for cell in column if cell.value != 0]
            for cell in column:
                cell.possibles = list(set(cell.possibles) - set(numbers))
                
        for sector in self.sectors:
            numbers = [cell.value for cell in sector if cell.value != 0]
            for cell in sector:
                cell.possibles = list(set(cell.possibles) - set(numbers))

        self.state = "".join([str(cell.value) for cell in self.cells])

    # Returns the first unsolved cell with one possible. Or none.
    def find_uniques(self):
        print_debug("Board.find uniques")
        #goes through all the cells in the board. if any of them only have a single .possibles, return the cell
        for cell in self.cells:
            if cell.lock == False and len(cell.possibles) == 1:
                return cell
        return None

    # Returns boolean whether the board is solved.
    def is_solved(self):
        if "0" not in self.state:
            return True
        else:
            return False 
        
class Sudoku():
    def __init__(self, input = 0):
        print_debug("Sudoku.init")
        self.board = Board(input)
        self.queue = [self.board]
        
    # Return the index of the first len==2 possibles list, or shortest possibles list
    def get_attempt_index(board):
        print_debug("Sudoku.get attempt index")
        length = 9
        index = -1
        for i in range(len(board.cells)):
            if len(board.cells[i].possibles) < length:
                length = len(board.cells[i].possibles)
                index = i
                if length == 2: # Don't waste time looking for another leng 2
                    break
        return index
    
    # Returns a copy of a board with new cell objects
    def copy_board(board):
        print_debug("Sudoku.copy board")
        new_board = Board()
        for i, cell in enumerate(board.cells):
            new_board.cells[i].value = cell.value
            new_board.cells[i].possibles = cell.possibles.copy() # DEBUG CHECK HERE FIRST
            new_board.cells[i].lock = cell.lock
        return new_board

    # If the board is unfinished, and there are no possibles, this board is a dead end.
    # True = deadend. False = live
    def dead_end(current_board):
        accum = []
        for cell in current_board:
            accum += cell.possibles
        return (0 in current_board.cells and len(accum) == 0)

    def solve(self, current_board): # need to call with self.queue.pop(0)
        current_board.update()
        unique = current_board.find_uniques()
        while unique:
            unique.set_value(unique.possibles[0])
            current_board.update()
            unique = current_board.find_uniques()
        # Only branching boards and unsolvales past here
        if current_board.is_solved():
            return current_board
        elif not Sudoku.dead_end(current_board):
            pass
            ## Branch
            # Get the cell with the least possibles
            try_index = Sudoku.get_attempt_index(current_board)
            # Make a copy of the board
            next_board = Sudoku.copy_board(current_board)
            # In one copy pop a value from the possibles and push the board to the queue
            next_value = current_board.cells[try_index].possibles.pop()
            self.queue.append(current_board)
            # In the other copy set the cell's value to the popped value
            next_board.cells[try_index].set_value(next_value)
            # Call solve on that board?
            what_do_with_this = self.solve(next_board)
        else:
            ## Not solved, and a dead end
            return None
            
'''
    def solve(self, current_board):
        print_debug("Sudoku.solve")
        run = False
        while run:
            for cell in current_board.cells:
                if len(cell.possibles) > 0:
                    run = True
                else:
                    run = False
                break
            
            current_board.update()
            cell = current_board.find_uniques()
            if cell: # There is a cell with only one possible 
                cell.value = cell.possibles[0]
                cell.lock = True
            else: # All cells are filled or have multiple possibles
                pass
                # Find the first cell with the least possibles
                # Pop one of these possibles and push the board to the stack
                # Use the popped possible as the value for the cell
                # Call solve on this board?
'''