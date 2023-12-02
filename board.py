from cell import Cell

debug = False
def print_debug(message):
    if debug:
        print(message)    

class Board():
    def __init__(self, board = 0):
        print_debug("init")
        if board == 0:
            self.cells = [Cell() for i in range(81)]
        else:
            self.cells = [Cell(int(i)) for i in board]
        self.rows = []
        self.columns = []
        self.sectors = []
        self.build_structs()

    def show(self):
        print_debug("show")
        for i in range(9):
            if i == 3 or i == 6:
                print("------+-------+------")
            for j in range(9):
                if j == 3 or j == 6:
                    print("| ", end="")
#                print("{} ".format(str(self.cells[(i *9 + j)])), end = "")
                print("{} ".format(self.cells[(i *9 + j)]), end = "")
            print()

    def enter(self, row_number = -1):
        print_debug("enter")
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
        print_debug("build structs")
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
    
    def update(self):
        print_debug("update")
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

    def find_uniques(self):
        print_debug("find uniques")
        #goes through all the cells in the board. if any of them only have a single .possibles, return the cell
        for cell in self.cells:
            if cell.lock == False and len(cell.possibles) == 1:
                return cell
        return None

    def solve(self):
        print_debug("solve")
        self.update()
        cell = self.find_uniques()
        while cell:
            if cell.lock == True:
                continue
            cell.value = cell.possibles[0]
            cell.lock = True
            self.update()
            cell = self.find_uniques()
        self.show()
            
    def save_board(self):
        pass
        #save the board state as a string of 81 digits

    def load_board(self):
        pass
        #create board from a string of 81 digits
        
    def print_structs(self):
        for row in self.rows:
            print([cell.value for cell in row])
        print()
        for col in self.columns:
            print([cell.value for cell in col])
        print()
        for sect in self.sectors:
            print([cell.value for cell in sect])