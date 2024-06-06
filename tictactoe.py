import random
class OneMove:
    def __init__(self, board, row, column):
        self.board = board
        self.row = row
        self.column = column


class TTT3D:
    def __init__(self):
        self.humanFirst = True
        self.difficulty = 2
        self.lookAheadCounter = 0
        self.totalLooksAhead = 2
        self.humanScore = 0
        self.computerScore = 0
        self.finalWin = [0, 0, 0]
        self.win = False
        self.humanPiece = 'X'
        self.computerPiece = 'O'
        self.config = [[['-' for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        for i in range(3):
            print(f"Layer {i + 1}:")
            for j in range(3):
                print(" ".join(self.config[i][j]))
            print("")

    def selectPiece(self):
        piece = input("Select your piece (X/O): ").upper()
        if piece == 'X':
            self.humanPiece = 'X'
            self.computerPiece = 'O'
        else:
            self.humanPiece = 'O'
            self.computerPiece = 'X'

    def selectFirst(self):
        first = input("Do you want to go first? (yes/no): ").lower()
        self.humanFirst = first == 'yes'

    def selectDifficulty(self):
        difficulty = input("Select difficulty (easy/medium/hard): ").lower()
        if difficulty == 'easy':
            self.difficulty = 1
            self.totalLooksAhead = 1
        elif difficulty == 'medium':
            self.difficulty = 2
            self.totalLooksAhead = 2
        else:
            self.difficulty = 3
            self.totalLooksAhead = 6

    def newGame(self):
        self.clearBoard()
        if not self.humanFirst:
            self.computerMove()

    def humanMove(self):
        while True:
            move = input("Enter your move (layer,row,column): ")
            i, j, k = map(int, move.split(','))
            if self.config[i][j][k] == '-':
                self.config[i][j][k] = self.humanPiece
                break
            else:
                print("Invalid move. Try again.")

    def computerMove(self):
        if self.difficulty == 3:
            self.computerPlays()
        else:
            self.computerPlayRandom()

    def contains(a, k):
        # Step through array
        for i in a:
            # Compare elements
            if k == i:
                return True
        return False


    def computerPlayRandom(self):
        import random
        random.seed()
        row = random.randint(0, 2)
        column = random.randint(0, 2)
        board = random.randint(0, 2)
        self.config[board][row][column] = self.computerPiece


    def computerPlays(self):
        bestScore = -1000
        hValue = 0
        nextMove = OneMove(0,0,0)
        bestScoreBoard = -1
        bestScoreRow = -1
        bestScoreColumn = -1

        # Low number so the first bestScore will be the starting bestScore
        bestScore = -1000
        # Walk through the entire game board
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if self.config[i][j][k] == '-':
                        # Creating a new move on every empty position
                        nextMove.board = i
                        nextMove.row = j
                        nextMove.column = k

                        if self.checkWin(self.computerPiece, nextMove):
                            # Leave the piece there if it is a win and end the game
                            self.config[i][j][k] = self.computerPiece
                            print("   I win! Press New Game to play again.")
                            self.win = True
                            computerScore += 1
                            break

                        else:
                            # This is where the method generates all the possible counter moves potentially made
                            # by the human player
                            if self.difficulty != 1:
                                hValue = self.lookAhead(self.humanPiece, -1000, 1000)
                            else:
                                # If the player is on easy, just calculate the heuristic value for every current possible move, no looking ahead
                                hValue = self.heuristic()

                            self.lookAheadCounter = 0

                            # CPU chooses the best hValue out of every move
                            if hValue >= bestScore:
                                bestScore = hValue
                                bestScoreBoard = i
                                bestScoreRow = j
                                bestScoreColumn = k
                                self.config[i][j][k] = '-'
                            else:
                                self.config[i][j][k] = '-'

        # If there is no possible winning move, make the move in the calculated best position.
        if not self.win:
            self.config[bestScoreBoard][bestScoreRow][bestScoreColumn] = self.computerPiece


    def lookAhead(self, c, a, b):
        # Alpha and beta values that get passed in
        alpha = a
        beta = b

        # If you still want to look ahead
        if self.lookAheadCounter <= self.totalLooksAhead:

            self.lookAheadCounter += 1
            # If you are going to be placing the computer's piece this time
            if c == self.computerPiece:
                hValue = 0
                nextMove = OneMove(0,0,0)

                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            if self.config[i][j][k] == '-':
                                nextMove = OneMove(0,0,0)
                                nextMove.board = i
                                nextMove.row = j
                                nextMove.column = k

                                if self.checkWin(self.computerPiece, nextMove):
                                    self.config[i][j][k] = '-'
                                    return 1000
                                else:
                                    # Recursive look ahead, placing human pieces next
                                    hValue = self.lookAhead(self.humanPiece, alpha, beta)
                                    if hValue > alpha:
                                        alpha = hValue
                                        self.config[i][j][k] = '-'
                                    else:
                                        self.config[i][j][k] = '-'

                                # Break out of the look if the alpha value is larger than the beta value, going down no further
                                if alpha >= beta:
                                    break

                return alpha

            # If you are going to be placing the human's piece this time
            else:
                hValue = 0
                nextMove = OneMove(0,0,0)

                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            if self.config[i][j][k] == '-':
                                nextMove.board = i
                                nextMove.row = j
                                nextMove.column = k

                                if self.checkWin(self.humanPiece, nextMove):
                                    self.config[i][j][k] = '-'
                                    return -1000
                                else:
                                    # Recursive look ahead, placing computer pieces next
                                    hValue = self.lookAhead(self.computerPiece, alpha, beta)
                                    if hValue < beta:
                                        beta = hValue
                                        self.config[i][j][k] = '-'
                                    else:
                                        self.config[i][j][k] = '-'

                                # Break out of the look if the alpha value is larger than the beta value, going down no further
                                if alpha >= beta:
                                    break

                return beta

        # If you are at the last level of nodes you want to check
        else:
            return self.heuristic()


    def heuristic(self):
        return (self.checkAvailable(self.computerPiece) - self.checkAvailable(self.humanPiece))


    def checkWin(self, c, pos):
        if pos is not None:
            self.config[pos.board][pos.row][pos.column] = c

        # Win table
        wins = [
            # Rows on single board
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20],
            [21, 22, 23], [24, 25, 26],

            # Columns on single board
            [0, 3, 6], [1, 4, 7], [2, 5, 8], [9, 12, 15], [10, 13, 16], [11, 14, 17], [18, 21, 24],
            [19, 22, 25], [20, 23, 26],

            # Diagonals on single board
            [0, 4, 8], [2, 4, 6], [9, 13, 17], [11, 13, 15],
            [18, 22, 26], [20, 22, 24],

            # Straight down through boards
            [0, 9, 18], [1, 10, 19], [2, 11, 20], [3, 12, 21], [4, 13, 22], [5, 14, 23], [6, 15, 24],
            [7, 16, 25], [8, 17, 26],

            # Diagonals through boards
            [0, 12, 24], [1, 13, 25], [2, 14, 26], [6, 12, 18], [7, 13, 19], [8, 14, 20], [0, 10, 20],
            [3, 13, 23], [6, 16, 26], [2, 10, 18], [5, 13, 21], [8, 16, 24], [0, 13, 26], [2, 13, 24],
            [6, 13, 20], [8, 13, 18],
        ]

        # Array that indicates all the spaces on the game board
        gameBoard = [0] * 27

        # Counter from 0 to 49, one for each win combo
        counter = 0

        # If the space on the board is the same as the input char, set the corresponding location
        # in gameBoard to 1.
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if self.config[i][j][k] == c:
                        gameBoard[counter] = 1
                    else:
                        gameBoard[counter] = 0
                    counter += 1

        # For each possible win combination
        for i in range(49):
            # Resetting counter to see if all 3 locations have been used
            counter = 0
            for j in range(3):
                # For each individual winning space in the current combination
                if gameBoard[wins[i][j]] == 1:
                    counter += 1

                    self.finalWin[j] = wins[i][j]
                    # If all 3 moves of the current winning combination are occupied by char c
                    if counter == 3:
                        return True

        return False


    def checkAvailable(self, c):
        winCounter = 0

        # Win table
        wins = [
            # Rows on single board
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20],
            [21, 22, 23], [24, 25, 26],

            # Columns on single board
            [0, 3, 6], [1, 4, 7], [2, 5, 8], [9, 12, 15], [10, 13, 16], [11, 14, 17], [18, 21, 24],
            [19, 22, 25], [20, 23, 26],

            # Diagonals on single board
            [0, 4, 8], [2, 4, 6], [9, 13, 17], [11, 13, 15],
            [18, 22, 26], [20, 22, 24],

            # Straight down through boards
            [0, 9, 18], [1, 10, 19], [2, 11, 20], [3, 12, 21], [4, 13, 22], [5, 14, 23], [6, 15, 24],
            [7, 16, 25], [8, 17, 26],

            # Diagonals through boards
            [0, 12, 24], [1, 13, 25], [2, 14, 26], [6, 12, 18], [7, 13, 19], [8, 14, 20], [0, 10, 20],
            [3, 13, 23], [6, 16, 26], [2, 10, 18], [5, 13, 21], [8, 16, 24], [0, 13, 26], [2, 13, 24],
            [6, 13, 20], [8, 13, 18],
        ]

        # Array that indicates all the spaces on the game board
        gameBoard = [0] * 27

        # Counter from 0 to 49, one for each win combo
        counter = 0

        # If the space on the board is the same as the input char, set the corresponding location
        # in gameBoard to 1.
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if self.config[i][j][k] == c or self.config[i][j][k] == '-':
                        gameBoard[counter] = 1
                    else:
                        gameBoard[counter] = 0

                    counter += 1

        # For each possible win combination
        for i in range(49):
            # Resetting counter to see if all 3 locations have been used
            counter = 0
            for j in range(3):
                # For each individual winning space in the current combination
                if gameBoard[wins[i][j]] == 1:
                    counter += 1

                    self.finalWin[j] = wins[i][j]
                    # If all 3 moves of the current winning combination are occupied by char c
                    if counter == 3:
                        winCounter += 1

        return winCounter

    def isDraw(self):
        return all(self.config[i][j][k] != '-' for i in range(3) for j in range(3) for k in range(3))

    def clearBoard(self):
        self.config = [[['-' for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.win = False

    def playGame(self):
        self.selectPiece()
        self.selectFirst()
        self.selectDifficulty()
        while True:
            self.newGame()
            self.printBoard()
            while not self.win and not self.isDraw():
                if self.humanFirst:
                    self.humanMove()
                    self.printBoard()
                    if self.checkWin(self.humanPiece, None):
                        print("You win! Press New Game to play again.")
                        self.humanScore += 1
                        self.win = True
                    elif self.isDraw():
                        print("It's a draw! Press New Game to play again.")
                    else:
                        self.computerMove()
                        self.printBoard()
                else:
                    self.computerMove()
                    self.printBoard()
                    if self.checkWin(self.computerPiece, None):
                        print("I beat you! Press New Game to play again.")
                        self.computerScore += 1
                        self.win = True
                    elif self.isDraw():
                        print("It's a draw! Press New Game to play again.")
                    else:
                        self.humanMove()
                        self.printBoard()
                        if self.checkWin(self.humanPiece, None):
                            print("You win! Press New Game to play again.")
                            self.humanScore += 1
                            self.win = True
                        elif self.isDraw():
                            print("It's a draw! Press New Game to play again.")

            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != 'yes':
                break
            self.clearBoard()

if __name__ == "__main__":
    game = TTT3D()
    game.playGame()
