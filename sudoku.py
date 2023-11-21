'''The Python code provided defines a class named CustomSudoku that can be used to create and solve custom 
Sudoku puzzles. The class generates a random Sudoku puzzle with a given number of missing digits. By entering 
values in diagonal boxes and then retracing to solve the puzzle, it assures a valid initial state. The code 
also offers methods for printing the Sudoku grid and solving the puzzle by backtracking. The main programme 
initialises a CustomSudoku instance, produces and fills a Sudoku puzzle, prints the initial puzzle, solves it, 
and prints the finished Sudoku grid. Overall, the code provides a Sudoku puzzle creation and solving tool with
a graphical user interface.'''

# Import necessary libraries
import random
import math

# Define a class for creating and solving custom Sudoku puzzles
class CustomSudoku:
    # Initialize the Sudoku object with the specified size and number of missing digits
    def __init__(self, size, missingDigits):

        self.boardSize = size
        self.numMissingDigits = missingDigits
        
        # Calculate the square root of the board size
        sqrtBoardSizeD = math.sqrt(size)
        self.squareRootSize = int(sqrtBoardSizeD)
        
        # Initialize the game board as a 2D list filled with zeros
        self.gameBoard = [[0] * size for _ in range(size)]
        
    # Fill the Sudoku board with initial values
    def fillSudokuValues(self):
        # Fill values in the diagonal boxes
        self.diag_filling()
        
        # Fill the remaining cells using backtracking
        self.fillRemainingCells(0, self.squareRootSize)
        
        # Randomly remove digits to create the puzzle
        self.removeDigitsRandomly()
        
    # Fill values in the diagonal boxes
    def diag_filling(self):

        for i in range(0, self.boardSize, self.squareRootSize):
            self.box_filling(i, i)
            
    # Check if a number is not present in a box
    def isNumberNotInBox(self, rowStart, colStart, num):

        for i in range(self.squareRootSize):
            for j in range(self.squareRootSize):

                if self.gameBoard[rowStart + i][colStart + j] == num:
                    return False
                
        return True
    
    # Fill values in a specific box, ensuring no repetition in rows, columns, or the box itself
    def box_filling(self, row, col):

        for i in range(self.squareRootSize):
            for j in range(self.squareRootSize):

                num = self.generateRandomNumber(self.boardSize)

                while not self.isNumberNotInBox(row, col, num):
                    num = self.generateRandomNumber(self.boardSize)

                self.gameBoard[row + i][col + j] = num
                
    # Generate a random number between 1 and the given range
    def generateRandomNumber(self, num):
        return random.randint(1, num)
    
    # Check if it is safe to place a number at a specific cell
    def isSafeToPlace(self, i, j, num):
        return self.notInRow(i, num) and self.notInCol(j, num) and self.isNumberNotInBox(i - i % self.squareRootSize, j - j % self.squareRootSize, num)
    
    # Check if a number is not present in a specific row
    def notInRow(self, i, num):

        for j in range(self.boardSize):
            if self.gameBoard[i][j] == num:
                return False
            
        return True
    
    # Check if a number is not present in a specific column
    def notInCol(self, j, num):

        for i in range(self.boardSize):
            if self.gameBoard[i][j] == num:
                return False
            
        return True
    
    # Fill the remaining cells using backtracking
    def fillRemainingCells(self, i, j):
        # Move to the next row if the end of the current row is reached

        if j >= self.boardSize and i < self.boardSize - 1:
            i += 1
            j = 0
            
        # Return True if the entire board is filled
        if i >= self.boardSize and j >= self.boardSize:
            return True
        
        # Adjust the starting point for specific cases
        if i < self.squareRootSize:

            if j < self.squareRootSize:
                j = self.squareRootSize

        elif i < self.boardSize - self.squareRootSize:

            if j == (i // self.squareRootSize) * self.squareRootSize:
                j += self.squareRootSize

        else:

            if j == self.boardSize - self.squareRootSize:
                i += 1
                j = 0

                if i >= self.boardSize:
                    return True
        
        # Try placing numbers in the current cell
        for num in range(1, self.boardSize + 1):

            if self.isSafeToPlace(i, j, num):
                self.gameBoard[i][j] = num

                # Recursively fill the remaining cells
                if self.fillRemainingCells(i, j + 1):
                    return True
                
                # Backtrack if a solution is not found
                self.gameBoard[i][j] = 0

        return False
    
    # Remove digits randomly to create the puzzle
    def removeDigitsRandomly(self):

        count = self.numMissingDigits
        while count != 0:
            # Generate a random cell index

            cellId = self.generateRandomNumber(self.boardSize * self.boardSize) - 1

            i = cellId // self.boardSize
            j = cellId % 9

            if j != 0:
                j -= 1

            # Remove a digit if the cell is not empty
            if self.gameBoard[i][j] != 0:
                count -= 1
                self.gameBoard[i][j] = 0
                
    # Print the Sudoku grid
    def printSudokuGrid(self):

        for i in range(self.boardSize):

            for j in range(self.boardSize):

                print(str(self.gameBoard[i][j]) + " ", end="")

            print()

        print()
        
    # Check if it is safe to place a number at a specific cell during backtracking
    def isSafePlacement(self, row, col, num):

        for i in range(9):

            if self.gameBoard[i][col] == num or self.gameBoard[row][i] == num:
                return False
            
            if self.gameBoard[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                return False
            
        return True
    
    # Solve the Sudoku puzzle using backtracking
    def solveSudokuBacktracking(self, i, j):
        # Move to the next row if the end of the current row is reached
        if j == self.boardSize:

            if i == self.boardSize - 1:
                return True
            
            j = 0
            i += 1
            
        # Skip filled cells
        if self.gameBoard[i][j] != 0:
            return self.solveSudokuBacktracking(i, j + 1)
        
        # Try placing numbers in the current cell
        for num in range(1, self.boardSize + 1):

            if self.isSafePlacement(i, j, num):
                self.gameBoard[i][j] = num

                # Recursively solve the remaining cells
                if self.solveSudokuBacktracking(i, j + 1):
                    return True
                
                # Backtrack if a solution is not found
                self.gameBoard[i][j] = 0

        return False
    
    # Wrapper function to solve the Sudoku puzzle
    def solveSudoku(self):
        self.solveSudokuBacktracking(0, 0)
        return

# Main program
print("----------WELCOME TO SUDOKU SOLVER----------")
print()
size = 9
missingDigits = random.randint(1, size * size)

# Create a Sudoku object
sudoku = CustomSudoku(size, missingDigits)

# Generate and fill a Sudoku puzzle
sudoku.fillSudokuValues()

# Print the initial puzzle
print("Here is your randomly generated Sudoku:")
print()
sudoku.printSudokuGrid()
print()

# Solve the Sudoku puzzle
sudoku.solveSudoku()
print("Sudoku solved with values 1-9:")
print()

# Print the solved Sudoku
sudoku.printSudokuGrid()
print()
print("Thank You")
print()
