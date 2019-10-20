class GridPuzzle(object):
    def __init__(self, start, goal, scene):
        self.board = scene
        self.start = start
        self.goal = goal
        self.move = []
        self.f = 0
        self.rows = len(self.board)
        self.cols = len(self.board[0])

    def copy(self):
        puzzle_copy = copy.deepcopy(self)
        return GridPuzzle(puzzle_copy.start, puzzle_copy.goal, puzzle_copy.board)

    def perform_move(self, direction):
        r_loc, c_loc = self.start
        # up
        if direction == 'up' and r_loc - 1 >= 0 and not self.board[r_loc-1][c_loc]:
            self.start[0] = r_loc - 1
            return True
        # down
        if direction == 'down' and r_loc + 1 < self.rows and not self.board[r_loc+1][c_loc]:
            self.start[0] = r_loc + 1
            return True
        # left
        if direction == 'left' and c_loc - 1 >= 0 and not self.board[r_loc][c_loc-1]:
            self.start[1] = c_loc - 1
            return True
        # right
        if direction == 'right' and c_loc + 1 < self.cols and not self.board[r_loc][c_loc+1]:
            self.start[1] = c_loc + 1
            return True
        # up_left
        if direction == 'up_left' and r_loc - 1 >= 0 and c_loc - 1 >= 0 \
                and not self.board[r_loc-1][c_loc-1]:
            self.start[0] = r_loc - 1
            self.start[1] = c_loc - 1
            return True
        # up_right
        if direction == 'up_right' and r_loc - 1 >= 0 and c_loc + 1 < self.cols \
                and not self.board[r_loc-1][c_loc+1]:
            self.start[0] = r_loc - 1
            self.start[1] = c_loc + 1
            return True
        # down_left
        if direction == 'down_left' and r_loc + 1 < self.rows and c_loc - 1 >= 0 \
                and not self.board[r_loc+1][c_loc-1]:
            self.start[0] = r_loc + 1
            self.start[1] = c_loc - 1
            return True
        # down_right
        if direction == 'down_right' and r_loc + 1 < self.rows and c_loc + 1 < self.cols \
                and not self.board[r_loc+1][c_loc+1]:
            self.start[0] = r_loc + 1
            self.start[1] = c_loc + 1
            return True
        return False

    def successors(self):
        choice = ('up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right')
        for move in choice:
            successor = self.copy()
            if successor.perform_move(move):
                yield (tuple(successor.start), successor)

    def euclidean_dis(self):
        return math.sqrt((self.start[0] - self.goal[0]) ** 2 + (self.start[1] - self.goal[1]) ** 2)


def find_path(start, goal, scene):
    if start[0] < 0 or start[1] < 0 or goal[0] < 0 or goal[1] < 0:
        return 'Invalid Input'
    if scene[goal[0]][goal[1]] or scene[start[0]][start[1]]:
        return None
    puzzle = GridPuzzle(list(start), list(goal), scene)
    puzzle.move = puzzle.move + [start]
    open_q = PQ()
    visited = set()
    index = 0
    puzzle.f = puzzle.euclidean_dis()
    open_q.put((puzzle.f, index, puzzle))
    while not open_q.empty():
        get_node = open_q.get()
        parent_node = get_node[2]
        if parent_node.start == list(goal):
            return parent_node.move
        for move, children_node in parent_node.successors():
            if move not in visited:
                index += 1
                children_node.f = parent_node.f + children_node.euclidean_dis()
                children_node.move = parent_node.move + [move]
                visited.add(move)
                open_q.put((children_node.f, index, children_node))
    return None
