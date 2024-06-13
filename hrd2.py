import heapq
from heapq import heappush, heappop
import copy
from copy import deepcopy
import time
import argparse
import sys

# Piece class represents the individual pieces on the board
class Piece:
    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __eq__(self, other):
        return (self.is_goal == other.is_goal and self.is_single == other.is_single and
                self.coord_x == other.coord_x and self.coord_y == other.coord_y and
                self.orientation == other.orientation)

# Board class represents the game board
class Board:
    def __init__(self, pieces):
        self.width = 4
        self.height = 5
        self.pieces = pieces
        self.grid = []
        self.__construct_grid()

    def __construct_grid(self):
        self.grid = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append('.')
            self.grid.append(row)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = '1'
                self.grid[piece.coord_y][piece.coord_x + 1] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x] = '1'
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = '1'
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = '2'
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def clone(self):
        new_pieces = []
        for piece in self.pieces:
            new_piece = Piece(piece.is_goal, piece.is_single, piece.coord_x, piece.coord_y, piece.orientation)
            new_pieces.append(new_piece)
        return Board(new_pieces)

    def display(self):
        for line in self.grid:
            print(''.join(line))
        print()

# State class represents the state of the game, including the board and metadata
class State:
    def __init__(self, board, f, depth, parent=None):
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = hash(str(board.grid))  # The id for breaking ties.

    def __lt__(self, other):
        return self.f < other.f

# Read the board from a file
def read_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n')
    pieces = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '1':
                if y + 1 < len(lines) and x + 1 < len(line) and lines[y + 1][x] == '1' and lines[y + 1][x + 1] == '1':
                    pieces.append(Piece(True, False, x, y, None))
            elif char == '2':
                pieces.append(Piece(False, True, x, y, None))
            elif char == '<':
                pieces.append(Piece(False, False, x, y, 'h'))
            elif char == '^':
                pieces.append(Piece(False, False, x, y, 'v'))
    return Board(pieces)

"""
# Write the solution path to a file with the step number
def write_to_file(filename, path):
    with open(filename, "w") as f:
        for step, state in enumerate(path, start=1):
            f.write(f"step {step}:\n\n")
            for line in state.board.grid:
                f.write(''.join(line) + '\n')
            f.write('\n')  # Add a blank line after each state for separation
        
"""

# Write the state path to an output file
def write_to_file(filename, path):
    with open(filename, "w") as f:
        for state in path:
            for line in state.board.grid:
                f.write(''.join(line) + '\n')
            f.write('\n')

# Check if the given state is indeed a goal state
def is_goal(board):
    if board.grid[3][1] == '1' and board.grid[3][2] == '1' and board.grid[4][1] == '1' and board.grid[4][2] == '1':
        return True 
    return False

# This is a manhattan heuristic function and returns this heuristic value
def manhattan_heuristic(board):
    for y in range(board.height):
        for x in range(board.width):
            if board.grid[y][x] == '1':
                return abs(x - 1) + abs(y - 3)
    return 0

# Generate the list of possible successor states of the given state
def get_successors(state):
    # this helper function returns true if the given piece can move in the specified direction
    # otherwise returns false
    def can_move(piece, direction):
        y, x = piece.coord_y, piece.coord_x
        piece_width = get_piece_width(piece)
        piece_height = get_piece_height(piece)

        if direction == 'up' and y > 0:
            for horizon in range(piece_width):
                if state.board.grid[y - 1][x + horizon] != '.':
                    return False
            return True

        if direction == 'down' and y + piece_height < state.board.height:
            for horizon in range(piece_width):
                if state.board.grid[y + piece_height][x + horizon] != '.':
                    return False
            return True

        if direction == 'left' and x > 0:
            for vertical in range(piece_height):
                if state.board.grid[y + vertical][x - 1] != '.':
                    return False
            return True

        if direction == 'right' and x + piece_width < state.board.width:
            for vertical in range(piece_height):
                if state.board.grid[y + vertical][x + piece_width] != '.':
                    return False
            return True

        return False # dummy statement, but useful when input argument does not make sense

    # this helper function moves the pieces in the direction and returns a new piece 
    def move_piece(piece, direction):
        new_piece = Piece(piece.is_goal, piece.is_single, piece.coord_x, piece.coord_y, piece.orientation)
        # it suffices to change the coordinate of the top left corner of the piece
        if direction == 'up':
            new_piece.coord_y -= 1
        elif direction == 'down':
            new_piece.coord_y += 1
        elif direction == 'left':
            new_piece.coord_x -= 1
        elif direction == 'right':
            new_piece.coord_x += 1
        return new_piece

    # Get the width of the given piece
    def get_piece_width(piece):
        if piece.is_goal:
            return 2
        if piece.is_single:
            return 1
        if piece.orientation == 'h':
            return 2
        else:
            return 1

    # Get the height of the given piece
    def get_piece_height(piece):
        if piece.is_goal:
            return 2
        if piece.is_single:
            return 1
        if piece.orientation == 'h':
            return 1
        else:
            return 2

    # store all possible successor states in the list and return it
    successors = []
    for piece in state.board.pieces:
        for direction in ['up', 'down', 'left', 'right']:
            if can_move(piece, direction):
                new_board = state.board.clone()
                new_piece = move_piece(piece, direction)
                for i, p in enumerate(new_board.pieces):
                    if p == piece:
                        new_board.pieces[i] = new_piece
                        break
                new_board._Board__construct_grid()
                new_state = State(new_board, state.f, state.depth + 1, state)
                successors.append(new_state)
    return successors

# Generate the path list by following the parents, and then return its reversed version
def reconstruct_path(state):
    path = []
    while state:
        path.append(state)
        state = state.parent
    return path[::-1] # need to reverse this since the original list is followed by parents

# Perform a stack based DFS search
def dfs(initial_state):
    stack = [initial_state]
    # we use hashset to do path-prunning, each access takes O(1) time 
    explored = set()
    while stack:
        state = stack.pop()
        if is_goal(state.board):
            return reconstruct_path(state)
        explored.add(state.id)
        for successor in get_successors(state):
            # avoid path prunning here
            if successor.id not in explored: 
                stack.append(successor)
                explored.add(successor.id)
    return None # in case path is not found

# Perform an A* star search
def astar(initial_state):
    heap = []
    heapq.heappush(heap, initial_state)
    # again, we use hashset to do path-prunning
    explored = set()
    while heap:
        state = heapq.heappop(heap)
        if is_goal(state.board):
            return reconstruct_path(state)
        explored.add(state.id)
        for successor in get_successors(state):
            # avoid path prunning here
            if successor.id not in explored:
                successor.f = successor.depth + manhattan_heuristic(successor.board)
                heapq.heappush(heap, successor)
                explored.add(successor.id)
    return None

# Main function to handle command-line arguments and run the appropriate algorithm
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )

    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    initial_state = State(initial_board, manhattan_heuristic(initial_board), 0)

    if args.algo == 'dfs':
        path = dfs(initial_state)
    elif args.algo == 'astar':
        path = astar(initial_state)
    else:
        print("This search algorithm is not supported.")

    if path:
        write_to_file(args.outputfile, path)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()


