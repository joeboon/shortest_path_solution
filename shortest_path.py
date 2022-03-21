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
            updated_path = path + [Space(new_row, new_column, 'off_board')]

        new_paths.append(updated_path)

        #west
        new_row = last_item.row
        new_column = last_item.column - 1
        if last_item.column > 0:
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else:  # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 'off_board')]

        new_paths.append(updated_path)

        #south
        new_row = last_item.row + 1
        new_column = last_item.column
        if last_item.row + 1 < len(board.rows):
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else:  # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 'off_board')]

        new_paths.append(updated_path)

        #east
        new_row = last_item.row
        new_column = last_item.column + 1
        if last_item.column + 1 < len(board.rows[0]): #assumes a rectangular board
            updated_path = path + [Space(new_row, new_column, board.rows[new_row][new_column])]
        else:  # Add in a "null value" space that will get this path eliminated for hitting an edge
            updated_path = path + [Space(new_row, new_column, 'off_board')]

        new_paths.append(updated_path)

    return new_paths

def eliminate_invalid(paths, visited_spaces):
    valid_paths = []
    completed_paths = []
    for path in paths:
        if path[-1].value == 'E':
            completed_paths.append(path)
        elif path[-1].value == 0\
                and path[-1] not in visited_spaces:
            valid_paths.append(path)
            visited_spaces.add(path[-1])

    return valid_paths, completed_paths, visited_spaces

def track_paths(board, steps=999999999): # Step number aids with automated testing
    start_row, start_column = board.find_start()

    max_steps = steps
    current_steps = 0

    paths = [[Space(start_row, start_column, 'S')]]
    visited_spaces = {Space(start_row, start_column, 'S')}

    # go outward from the start and put each result in its own list
    while current_steps < max_steps and paths: #while we're under the step count and there are still paths that don't end in 'E'
        paths = extend(paths, board)

        # if the list ends in 1, an edge, or an already visited node, discard the list
        # and add it to a list of completed paths if it found the end
        paths, completed, visited_spaces = eliminate_invalid(paths, visited_spaces)
        if completed:
            return paths, completed
        current_steps += 1

    if current_steps < steps:
        raise Exception("Exhausted all path options and found no routes from start to finish :(.")
    else:
        e = Exception("Exhausted step limit before finding a route.")
        e.paths_in_progress = paths
        e.completed_paths = completed
        raise e

Space = namedtuple('Space', ['row', 'column', 'value'])

def shortest_path(board):
    #choose the shortest path
    _, completed = track_paths(board)

    min_length = len(completed[0])
    options = [path for path in completed]

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
    assert updated_paths == [
            [Space(row=1, column=3, value='S'), Space(row=0, column=3, value=0)],
            [Space(row=1, column=3, value='S'), Space(row=1, column=2, value=0)],
            [Space(row=1, column=3, value='S'), Space(row=2, column=3, value=0)],
            [Space(row=1, column=3, value='S'), Space(row=1, column=4, value='off_board')]
        ], f"Whoops, extend returned {updated_paths}."
    print("SUCCESS on EXTENDING PATHS!")

test_extend()


def test_eliminate_paths():
    paths = [
        [Space(row=1, column=3, value='S'), Space(1, 4, 0), Space(2, 4, 0)],
        [Space(row=1, column=3, value='S'), Space(1, 2, 0), Space(1, 1, 0)],
        [Space(row=1, column=3, value='S'), Space(0, 3, 0), Space(0, 2, 'E')], #completed path
        [Space(row=1, column=3, value='S'), Space(2, 3, 0), Space(3, 3, 1)], #off the edge, should be removed
        [Space(row=1, column=3, value='S'), Space(1, 4, 0), Space(row=1, column=3, value='S')], #backtracking, should be removed
        [Space(row=1, column=3, value='S'), Space(1, 4, 0), Space(0, 3, 0)] # steps on a space reached earlier by another path, should be removed
    ]
    valid, completed, visited = eliminate_invalid(paths, visited_spaces={Space(row=1, column=3, value='S'), Space(1, 4, 0), Space(1, 2, 0), Space(0, 3, 0), Space(2, 3, 0)})
    assert valid == [
            [Space(row=1, column=3, value='S'), Space(row=1, column=4, value=0), Space(row=2, column=4, value=0)],
            [Space(row=1, column=3, value='S'), Space(row=1, column=2, value=0), Space(row=1, column=1, value=0)]
        ], f"Whoops, eliminate_paths returned valid paths {valid}."
    assert completed == [
            [Space(row=1, column=3, value='S'), Space(0, 3, 0), Space(0, 2, 'E')]
        ], f"Whoops, eliminate_paths returned completed paths {completed}."
    assert visited == {
            Space(row=2, column=4, value=0), Space(row=1, column=1, value=0), Space(row=1, column=4, value=0),
            Space(row=0, column=3, value=0), Space(row=2, column=3, value=0), Space(row=1, column=3, value='S'),
            Space(row=1, column=2, value=0)
        }, f"Whoops, eliminate_paths returned visited spaces {visited}."
    print("SUCCESS on ELIMINATING PATHS!")

test_eliminate_paths()


def test_track_paths():
    board = Board([
        [0, 0, 0, 0],
        [1, 1, 0, 'S'],
        [0, 0, 0, 0],
        ['E', 0, 0, 0],
    ])

    try:
        track_paths(board, steps=1)
        raise Exception("This should have excepted.")
    except Exception as e:
        if "step limit" in str(e):
            paths_so_far = e.paths_in_progress
            paths_completed = e.completed_paths

            assert paths_so_far == [
                    [Space(row=1, column=3, value='S'), Space(0, 3, 0)],
                    [Space(row=1, column=3, value='S'), Space(1, 2, 0)],
                    [Space(row=1, column=3, value='S'), Space(2, 3, 0)]
                ], f"Whoops, track_paths returned paths in progress {paths_so_far}."
            assert paths_completed == [
                ], f"Whoops, track_paths returned completed paths {paths_completed}."
            print("SUCCESS on TRACKING PATHS!")
        else:
            raise Exception("There was an exception besides the expected one.")

test_track_paths()


def test_find_start():
    board = Board([
        [0, 0, 0, 0],
        [1, 1, 0, 'S'],
        [0, 0, 0, 0],
        ['E', 0, 0, 0],
    ])

    result = board.find_start()

    assert result == (1, 3), \
        f"Whoops, find_start should have been (1, 3) but was {result}."
    print("SUCCESS on FINDING START!")

test_find_start()


def test_shortest_path():
    board = Board([
        ['S', 0, 0, 0],
        [ 1,  1, 0, 0],
        [ 0,  0, 0, 0],
        ['E', 0, 0, 0],
    ])

    min_length, options = shortest_path(board)

    assert min_length == 8, ( #the number of moves counts the start in our implementation
        f"Whoops, shortest path should have been 8 long but was {min_length}.")

    print("SUCCESS at FINDING THE SHORTEST PATH!")
    print("PATH OPTIONS: ")
    print(options)

test_shortest_path()


def test_shortest_path_failure():
    blocked_board = Board([
        [0, 0, 0, 'S'],
        [ 1,  1, 1, 1],
        [ 0,  0, 0, 0],
        ['E', 0, 0, 0],
    ])

    try:
        shortest_path(blocked_board)
        raise Exception("This should have failed")
    except Exception as e:
        if "Exhausted all path options" in str(e):
            pass
        else:
            raise e

test_shortest_path_failure()


