class Board():
    rows = []

    def __init__(self, rows):
        self.rows = rows
        
    def columns(self, index):
        return [row[index] for row in self.rows]

    def find_start(self):
        start_row = 0
        start_column = 0
        for index, row in enumerate(self.rows):
            if 'S' in row:
                start_row = index
                start_column = row.index('S')
                break
        return start_row, start_column


def test_find_start():
    board = Board([
        [ 0,  0, 0, 0],
        [ 1, 1, 0, 'S'],
        [ 0,  0, 0, 0],
        ['E', 0, 0, 0],

    ])

    result = board.find_start()

    if result == (1, 3):
        print("SUCCESS!")
    else:
        raise Exception(f"Whoops, find_start should have been (1, 3) but was {result}.")


test_find_start()

def test_column():
    board = Board([
        ['S', 0, 0, 0],
        [ 1,  1, 0, 0],
        [ 0,  0, 0, 0],
        ['E', 0, 0, 0],

    ])

    result = board.columns(1)

    if result == [0, 1, 0, 0]:
        print("SUCCESS!")
    else:
        raise Exception(f"Whoops, columns should have been [0, 1, 0, 0] but was {result}.")

test_column()

def shortest_path(board):
    # Find start
    # go outward from the start and put each result in its own list
    # if the list ends in 1 or an already visited node, discard the list
    # go until all remaining lists end in 'E'
    # select the shortest one

    return 0

def test_shortest_path():
    board = Board([
        ['S', 0, 0, 0],
        [ 1,  1, 0, 0],
        [ 0,  0, 0, 0],
        ['E', 0, 0, 0],

    ])

    result = shortest_path(board)

    if result == 7:
        print("SUCCESS!")
    else:
        raise Exception(f"Whoops, shortest path should have been 7 but was {result}.")

test_shortest_path()

