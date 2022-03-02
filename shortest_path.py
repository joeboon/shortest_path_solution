class Board():
    rows = []

    def __init__(self, rows):
        self.rows = rows
        
    def columns(self, index):
        return [row[index] for row in self.rows]

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

