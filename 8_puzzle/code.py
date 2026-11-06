import heapq

# Target Goal State
GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

class PuzzleNode:
    def __init__(self, state, g=0, h=0, parent=None, move=""):
        self.state = state      # 3x3 tuple of tuples representing the board
        self.g = g              # Cost from start to current node
        self.h = h              # Estimated cost from current node to goal
        self.f = g + h          # Total estimated cost
        self.parent = parent    # Reference to parent node for path reconstruction
        self.move = move        # Move taken to reach this state ('Up', 'Down', etc.)

    def __lt__(self, other):
        # Priority Queue comparison based on f(n) value
        return self.f < other.f

def find_zero(state):
    """Finds the (row, col) position of the empty tile (0)."""
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                return r, c

def get_manhattan_distance(state, goal_state=GOAL_STATE):
    """Calculates sum of Manhattan distances of all tiles from their goal positions."""
    # Map values to target coordinates in goal state
    goal_positions = {}
    for r in range(3):
        for c in range(3):
            goal_positions[goal_state[r][c]] = (r, c)

    distance = 0
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:  # Ignore the blank tile
                target_r, target_c = goal_positions[val]
                distance += abs(r - target_r) + abs(c - target_c)
    return distance

def get_neighbors(node):
    """Generates all valid successor states by sliding tiles into the blank space."""
    neighbors = []
    r, c = find_zero(node.state)

    # Possible directions: (row_change, col_change, move_label)
    moves = [
        (-1, 0, "Up"),
        (1, 0, "Down"),
        (0, -1, "Left"),
        (0, 1, "Right")
    ]

    for dr, dc, move_name in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            # Convert tuple of tuples to mutable list of lists
            new_board = [list(row) for row in node.state]
            # Swap blank space with neighboring tile
            new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
            # Convert back to immutable tuple of tuples
            neighbor_state = tuple(tuple(row) for row in new_board)
            neighbors.append((neighbor_state, move_name))

    return neighbors

def solve_8_puzzle(initial_state):
    """Solves the 8-puzzle using A* Search Algorithm."""
    initial_h = get_manhattan_distance(initial_state)
    start_node = PuzzleNode(state=initial_state, g=0, h=initial_h)

    open_set = []
    heapq.heappush(open_set, start_node)
    
    # Store visited states and their lowest g(n) cost
    visited = {initial_state: 0}

    while open_set:
        current_node = heapq.heappop(open_set)

        # Check if goal is reached
        if current_node.state == GOAL_STATE:
            # Reconstruct solution path
            path = []
            curr = current_node
            while curr:
                path.append((curr.move, curr.state))
                curr = curr.parent
            return path[::-1]  # Return reversed path (start to goal)

        # Explore neighbors
        for neighbor_state, move_name in get_neighbors(current_node):
            new_g = current_node.g + 1
            
            # If state not visited or found a shorter path to it
            if neighbor_state not in visited or new_g < visited[neighbor_state]:
                visited[neighbor_state] = new_g
                h = get_manhattan_distance(neighbor_state)
                neighbor_node = PuzzleNode(
                    state=neighbor_state, 
                    g=new_g, 
                    h=h, 
                    parent=current_node, 
                    move=move_name
                )
                heapq.heappush(open_set, neighbor_node)

    return None

def print_board(state):
    """Helper function to display a state nicely."""
    for row in state:
        print(" ".join(str(tile) if tile != 0 else "_" for tile in row))
    print()

# --- Example Execution ---
if __name__ == "__main__":
    # Example starting state
    initial_board = (
        (1, 2, 3),
        (4, 0, 6),
        (7, 5, 8)
    )

    print("Initial State:")
    print_board(initial_board)

    solution = solve_8_puzzle(initial_board)

    if solution:
        print(f"Solved in {len(solution) - 1} moves!\n")
        for step, (move, state) in enumerate(solution):
            if step == 0:
                print("Start:")
            else:
                print(f"Step {step}: Move blank space {move}")
            print_board(state)
    else:
        print("No solution exists for this configuration.")
