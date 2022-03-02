class Board():
    rows = []

    def __init__(self, rows):
        self.rows = rows


def shortest_path(board):
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
        print(f"Whoops, shortest path should have been 7 but was {result}.")

test_shortest_path()

