import random

class Board:
    def __init__(self):
        # Initializes a board, creates the matrix and sets the dimension.
        self.matrix = [[None]*3 for i in range(3)]
        self.dimension = 3

    def __str__(self):
        # Stringifys the board for easy display, allows use of print()
        out = ""
        for lst in self.matrix:
            out += str(lst) + "\n"
        return out

    def as_list(self):
        # converts the Board to a list for unittests
        out = []
        for lst in self.matrix:
            for x in lst:
                out += x
        return out

    def __iter__(self):
        # creates an iterator for the board
        lst = self.as_list()
        for item in lst:
            yield item

    def __bool__(self):
        # returns True if the board has a non-None value
        for lst in self.matrix:
            for val in lst:
                if val is not None:
                    return True
        return False

    def get_spot(self, down, over):
        if self.matrix[down][over] is not None:
            return self.matrix[down][over]
        return None

    def get_all_openings(self):
        # returns a list of tuples of all open coordinates
        openings = []
        for x in range(self.dimension):
            for y in range(self.dimension):
                if not self.matrix[x][y]:
                    openings.append((x, y))
        return openings

    def __getitem__(self, location):
        # returns the item at a single-integer location. The board is numbered 0-8.
        assert(location <= (self.dimension**2))
        return self.matrix[location//self.dimension][location%self.dimension]

    def __setitem__(self, location, val):
        # sets the item at a single-integer location
        assert(location < (self.dimension**2))
        if self.get_spot(location//self.dimension, location%self.dimension) != None:
            raise ValueError('This place is already taken. To override this place, use `set_val()`')
        self.matrix[location//self.dimension][location%self.dimension] = val

    def set_val(self, down, over, val, override=False):
        # sets the value at a coordinate pair
        if not override and self.get_spot(down, over) == None:
            self.matrix[down][over] = val
        else:
            raise ValueError('This place is already taken')

    def clear(self):
        # empties the board (sets all locations to None).
        self.matrix = [[None]*self.dimension for i in range(self.dimension)]

    def check_win(self):
        # checks all locations within a single board for winners. if a winner is found, it returns who won. else False
        # row check
        for row in self.matrix:
            if row[0] == row[1] == row[2] and row[0] != None:
                return row[0]

        # column check
        for x in range(self.dimension):
            if self.matrix[0][x] == self.matrix[1][x] == self.matrix[2][x] and self.matrix[0][x] != None:
                return self.matrix[0][x]

        # diagonal checks
            if self.matrix[0][0] == self.matrix[1][1] == self.matrix[2][2] and self.matrix[0][0] != None:
                return self.matrix[0][0]
            elif self.matrix[0][2] == self.matrix[1][1] == self.matrix[2][0] and self.matrix[0][2] != None:
                return self.matrix[0][2]
        # else
        return False

    @staticmethod
    def location_to_coordinates(location, dimension=3):
        # returns a tuple containing the (down, over) coordinates of a location
        return (location//dimension, location%dimension)

class Cube:
    class Row:
        empty = "empty"
        def __init__(self, key=None):
            self.coords = []
            self.vals = []
            self.key = key

        def as_dict(self):
            # returns the Row as a dict
            out = {}
            for coord, val in zip(self.coords, self.vals):
                out[coord] = val
            return out

        def __iter__(self):
            # iterates through the Row
            for coord, val in zip(self.coords, self.vals):
                yield (coord, val)

        def __str__(self):
            # returns the Row as a string (printed like a dict)
            return str(self.as_dict())

    allowed = ['x', 'o']
    def __init__(self):
        # initializes a 3**3 board
        self.boards = [Board(), Board(), Board()]

    def __str__(self):
        # stringifies the cube
        out = ""
        for x in range(3):
            out += "---Board {0}---\n".format(str(x))
            out += str(self.boards[x]) + "\n"
        return out

    def get_available_spaces(self):
        # returns a dict that contains all open spaces - each value is a list of tuples of spaces
        spaces = {}
        for x in range(3):
            spaces[x] = self.boards[x].get_all_openings()
        return spaces

    def check_wins(self):
        # checks for a winner on the board
        # first check the 3 board objects
        for board in self.boards:
            result = board.check_win()
            if result != False:
                return result
        else:
            # 3D vertical checks
            for x in range(9):
                if self.boards[0][x] == self.boards[1][x] == self.boards[2][x] and self.boards[0][x] != None:
                    return self.boards[0][x]

            # 3D diagonal checks (yay!)
            # straight diagonals
            for x in range(3):
                if self.boards[0][x*3 + 0] == self.boards[1][x*3 + 1] == self.boards[2][x*3 + 2] and self.boards[0][x*3 + 0] != None:
                    return self.boards[0][x*3 + 0]
                elif self.boards[0][x*3 + 2] == self.boards[1][x*3 + 1] == self.boards[2][x*3 + 0] and self.boards[0][x*3 + 2] != None:
                    return self.boards[0][x*3 + 2]
                elif self.boards[0][x] == self.boards[1][3 + x] == self.boards[2][6 + x] and self.boards[0][x] != None:
                    return self.boards[0][0][x]
                elif self.boards[0][2 + x] == self.boards[1][1 + x] == self.boards[2][x] and self.boards[0][2 + x] != None:
                    return self.boards[0][2][x]
            # diagonal diagonals
            if self.boards[0][0] == self.boards[1][4] == self.boards[2][8] and self.boards[0][0] != None:
                return self.boards[0][0][0]
            elif self.boards[0][2] == self.boards[1][4] == self.boards[2][6] and self.boards[0][2] != None:
                return self.boards[0][0][2]
            elif self.boards[0][6] == self.boards[1][4] == self.boards[2][2] and self.boards[0][6] != None:
                return self.boards[0][2][0]
            elif self.boards[0][8] == self.boards[1][4] == self.boards[2][6] and self.boards[0][8] != None:
                return self.boards[0][2][2]
        return False

    def play_move(self, board, down, over, player):
        # adds a new item to the board
        assert(player in ['x', 'o'])
        self.boards[board].set_val(down, over, player)

    def clear(self):
        # clears all boards
        for board in self.boards:
            board.clear()

    def analyze_cube(self):
        # returns all rows of a cube
        # if a space is occupied, it displays its value
        # else, it displays its coordinates as a tuple (board, down, over)
        rows = []
        key_count = 0
        for b in range(3):
            for r in range(3):
                row = Cube.Row(key_count)
                key_count += 1
                for s in range(3):
                    result = self.boards[b].get_spot(r, s)
                    row.coords.append((b, r, s))
                    if result != None:
                        row.vals.append(result)
                    elif result == None:
                        row.vals.append(Cube.Row.empty)
                rows.append(row)
        for b in range(3):
            for c in range(3):
                row = Cube.Row(key_count)
                key_count += 1
                for s in range(3):
                    result = self.boards[b].get_spot(s, c)
                    row.coords.append((b, s, c))
                    if result != None:
                        row.vals.append(result)
                    elif result == None:
                        row.vals.append(Cube.Row.empty)
                rows.append(row)
        for x in range(9):
            row = Cube.Row(key_count)
            key_count += 1
            coordinates = Board.location_to_coordinates(x)
            n1 = self.boards[0][x]
            n2 = self.boards[1][x]
            n3 = self.boards[2][x]
            row.vals.append(n1)
            row.vals.append(n2)
            row.vals.append(n3)
            for y in range(3):
                row.coords.append((y, coordinates[0], coordinates[1]))
            rows.append(row)

        # diagonals
        for x in range(3):
            # first set
            row1 = Cube.Row(key_count)

            key_count += 1
            row1.vals.append(self.boards[0][x*3 + 0])
            row1.vals.append(self.boards[1][x*3 + 1])
            row1.vals.append(self.boards[2][x*3 + 2])
            coords1 = Board.location_to_coordinates(x*3 + 0)
            coords2 = Board.location_to_coordinates(x*3 + 1)
            coords3 = Board.location_to_coordinates(x*3 + 2)
            row1.coords.append((0, coords1[0], coords1[1]))
            row1.coords.append((1, coords2[0], coords2[1]))
            row1.coords.append((2, coords3[0], coords3[1]))
            rows.append(row1)

            # second set
            row2 = Cube.Row(key_count)
            key_count += 1
            row2.vals.append(self.boards[0][x*3 + 2])
            row2.vals.append(self.boards[1][x*3 + 1])
            row2.vals.append(self.boards[2][x*3 + 0])
            coords4 = Board.location_to_coordinates(x*3 + 2)
            coords5 = Board.location_to_coordinates(x*3 + 1)
            coords6 = Board.location_to_coordinates(x*3 + 2)
            row2.coords.append((0, coords4[0], coords4[1]))
            row2.coords.append((1, coords5[0], coords5[1]))
            row2.coords.append((2, coords6[0], coords6[1]))
            rows.append(row2)

            # third set
            row3 = Cube.Row(key_count)
            key_count += 1
            row3.vals.append(self.boards[0][x])
            row3.vals.append(self.boards[1][3 + x])
            row3.vals.append(self.boards[2][6 + x])
            coords7 = Board.location_to_coordinates(x)
            coords8 = Board.location_to_coordinates(3 + x)
            coords9 = Board.location_to_coordinates(6 + x)
            row3.coords.append((0, coords7[0], coords7[1]))
            row3.coords.append((1, coords8[0], coords8[1]))
            row3.coords.append((2, coords9[0], coords9[1]))
            rows.append(row3)

            # fourth set
            row4 = Cube.Row(key_count)
            key_count += 1
            row4.vals.append(self.boards[0][2 + x])
            row4.vals.append(self.boards[1][1 + x])
            row4.vals.append(self.boards[2][x])
            coords10 = Board.location_to_coordinates(2 + x)
            coords11 = Board.location_to_coordinates(1 + x)
            coords12 = Board.location_to_coordinates(x)
            row4.coords.append((0, coords10[0], coords10[1]))
            row4.coords.append((1, coords11[0], coords11[1]))
            row4.coords.append((2, coords12[0], coords12[1]))
            rows.append(row4)

        # fifth set
        row5 = Cube.Row(key_count)
        key_count += 1
        row5.vals.append(self.boards[0][0])
        row5.vals.append(self.boards[1][4])
        row5.vals.append(self.boards[2][8])
        coords13 = Board.location_to_coordinates(0)
        coords14 = Board.location_to_coordinates(4)
        coords15 = Board.location_to_coordinates(8)
        row5.coords.append((0, coords13[0], coords13[1]))
        row5.coords.append((1, coords14[0], coords14[1]))
        row5.coords.append((2, coords15[0], coords15[1]))
        rows.append(row5)

        # sixth set
        row6 = Cube.Row(key_count)
        key_count += 1
        row6.vals.append(self.boards[0][2])
        row6.vals.append(self.boards[1][4])
        row6.vals.append(self.boards[2][6])
        coords16 = Board.location_to_coordinates(2)
        coords17 = Board.location_to_coordinates(4)
        coords18 = Board.location_to_coordinates(6)
        row6.coords.append((0, coords16[0], coords16[1]))
        row6.coords.append((1, coords17[0], coords17[1]))
        row6.coords.append((2, coords18[0], coords18[1]))
        rows.append(row6)

        # seventh set
        row7 = Cube.Row(key_count)
        key_count += 1
        row7.vals.append(self.boards[0][6])
        row7.vals.append(self.boards[1][4])
        row7.vals.append(self.boards[2][2])
        coords19 = Board.location_to_coordinates(6)
        coords20 = Board.location_to_coordinates(4)
        coords21 = Board.location_to_coordinates(2)
        row7.coords.append((0, coords19[0], coords19[1]))
        row7.coords.append((1, coords20[0], coords20[1]))
        row7.coords.append((2, coords21[0], coords21[1]))
        rows.append(row7)

        # eighth set
        row8 = Cube.Row(key_count)
        key_count += 1
        row8.vals.append(self.boards[0][6])
        row8.vals.append(self.boards[1][4])
        row8.vals.append(self.boards[2][2])
        coords22 = Board.location_to_coordinates(6)
        coords23 = Board.location_to_coordinates(4)
        coords24 = Board.location_to_coordinates(2)
        row8.coords.append((0, coords22[0], coords22[1]))
        row8.coords.append((1, coords23[0], coords23[1]))
        row8.coords.append((2, coords24[0], coords24[1]))
        rows.append(row8)

        return rows

    def random_open_space(self):
        # returns a random open space in the Cube
        opens = []
        for b in range(3):
            for r in range(3):
                for s in range(3):
                    status = self.boards[b].get_spot(r,s)
                    print(status)
                    if status == None:
                        opens.append((b,r,s))
                    else:
                        continue
        return random.choice(opens)

class Player:
    # a class to manage players in games
    def __init__(self, name, piece, computer=False):
        assert(piece in Cube.allowed)
        self.name = name
        self.piece = piece
        self.computer = computer