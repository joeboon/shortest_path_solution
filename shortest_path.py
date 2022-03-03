from collections import namedtuple

class Board():
    rows = []

    def __init__(self, rows):
        self.rows = rows

    def find_start(self):
        start_row = 0
        start_column = 0
        for index, row in enumerate(self.rows):
            if 'S' in row:
                start_row = index
                start_column = row.index('S')
                break
        return start_row, start_column

def extend(paths, board):
    new_paths = []
    for path in paths:
        last_item = path[-1]

        #north
        new_row = last_item.row - 1
        new_column = last_item.column
        if last_item.row > 0:
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else: # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 1)]

        new_paths.append(updated_path)

        #west
        new_row = last_item.row
        new_column = last_item.column - 1
        if last_item.column > 0:
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else:  # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 1)]

        new_paths.append(updated_path)

        #south
        new_row = last_item.row + 1
        new_column = last_item.column
        if last_item.row + 1 < len(board.rows):
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else:  # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 1)]

        new_paths.append(updated_path)

        #east
        new_row = last_item.row
        new_column = last_item.column + 1
        if last_item.column + 1 < len(board.rows[0]): #assumes a rectangular board
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else:  # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 1)]

        new_paths.append(updated_path)

    return new_paths

def eliminate_invalid(paths):
    valid_paths = []
    completed_paths = []
    for path in paths:
        if path[-1].value == 'E':
            completed_paths.append(path)
        elif path[-1].value == 0\
                and len(set(path)) == len(path):
            valid_paths.append(path)

    return valid_paths, completed_paths

def track_paths(board, steps=999999999): # Step number aids with automated testing
    start_row, start_column = board.find_start()

    max_steps = steps
    current_steps = 0

    paths = [[Space(start_row, start_column, 'S')]]
    paths_completed = []

    # go outward from the start and put each result in its own list
    while current_steps < max_steps and paths: #while we're under the step count and there are still paths that don't end in 'E'
        paths = extend(paths, board)

        # if the list ends in 1, an edge, or an already visited node, discard the list
        # and add it to a list of completed paths if it found the end
        paths, completed = eliminate_invalid(paths)
        if completed:
            paths_completed += completed
        current_steps += 1

    return paths, paths_completed

Space = namedtuple('Space', ['row', 'column', 'value'])

def shortest_path(board):
    #choose the shortest path
    _, completed = track_paths(board)

    min_length = len(min(completed, key=len))
    options = [path for path in completed if len(path) == min_length]

    return min_length, options

##############################

def test_extend():
    board = Board([
        [0, 0, 0, 0],
        [1, 1, 0, 'S'],
        [0, 0, 0, 0],
        ['E', 0, 0, 0],
    ])
    updated_paths = extend(paths=[[Space(1, 3, 'S')]], board=board)
    if updated_paths == [
        [Space(row=1, column=3, value='S'), Space(row=0, column=3, value=0)],
        [Space(row=1, column=3, value='S'), Space(row=1, column=2, value=0)],
        [Space(row=1, column=3, value='S'), Space(row=2, column=3, value=0)],
        [Space(row=1, column=3, value='S'), Space(row=1, column=4, value=1)]
    ]:
        print("SUCCESS on EXTENDING PATHS!")
    else:
        raise Exception(f"Whoops, extend returned {updated_paths}.")

test_extend()


def test_eliminate_paths():
    paths = [
        [Space(row=1, column=3, value='S'), Space(0, 3, 0)],
        [Space(row=1, column=3, value='S'), Space(0, 3, 'E')], #completed path
        [Space(row=1, column=3, value='S'), Space(1, 2, 0)],
        [Space(row=1, column=3, value='S'), Space(1, 2, 1)], #off the edge, should be removed
        [Space(row=1, column=3, value='S'), Space(2, 3, 0)],
        [Space(row=1, column=3, value='S'), Space(2, 4, 1)],
        [Space(row=1, column=3, value='S'), Space(2, 4, 0), Space(2, 3, 0), Space(2, 4, 0)], #backtracking, should be removed
    ]
    valid, completed = eliminate_invalid(paths)
    if valid == [
        [Space(row=1, column=3, value='S'), Space(0, 3, 0)],
        [Space(row=1, column=3, value='S'), Space(1, 2, 0)],
        [Space(row=1, column=3, value='S'), Space(2, 3, 0)]
    ] and completed == [
        [Space(row=1, column=3, value='S'), Space(0, 3, 'E')]
    ]:
        print("SUCCESS on ELIMINATING PATHS!")
    else:
        raise Exception(f"Whoops, eliminate_paths returned {valid} and {completed}.")


test_eliminate_paths()


def test_track_paths():
    board = Board([
        [0, 0, 0, 0],
        [1, 1, 0, 'S'],
        [0, 0, 0, 0],
        ['E', 0, 0, 0],
    ])
    paths_so_far, paths_completed = track_paths(board, steps=1)
    if paths_so_far == [
        [Space(row=1, column=3, value='S'), Space(0, 3, 0)],
        [Space(row=1, column=3, value='S'), Space(1, 2, 0)],
        [Space(row=1, column=3, value='S'), Space(2, 3, 0)]
    ] and paths_completed == []:
        print("SUCCESS on TRACKING PATHS!")
    else:
        raise Exception(f"Whoops, track_paths returned {paths_so_far} and {paths_completed}.")

test_track_paths()

def test_find_start():
            board = Board([
                [0, 0, 0, 0],
                [1, 1, 0, 'S'],
                [0, 0, 0, 0],
                ['E', 0, 0, 0],

            ])

            result = board.find_start()

            if result == (1, 3):
                print("SUCCESS on FINDING START!")
            else:
                raise Exception(f"Whoops, find_start should have been (1, 3) but was {result}.")


test_find_start()


def test_shortest_path():
    board = Board([
        ['S', 0, 0, 0],
        [ 1,  1, 0, 0],
        [ 0,  0, 0, 0],
        ['E', 0, 0, 0],

    ])

    min_length, options = shortest_path(board)

    if min_length == 8: #the number of moves counts the start in our implementation
        print("SUCCESS at FINDING THE SHORTEST PATH!")
        print("PATH OPTIONS: ")
        print(options)
    else:
        raise Exception(f"Whoops, shortest path should have been 8 long but was {min_length}.")

test_shortest_path()

