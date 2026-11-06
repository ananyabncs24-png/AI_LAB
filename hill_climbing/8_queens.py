import random

def get_h_cost(board):
    # Calculate the number of attacking pairs of queens
    h = 0
    n = len(board)
    for i in range(n):
      for j in range(i + 1, n):
        # Same row
        if board[i] == board[j]:
          h += 1
        # Same diagonal
        offset = j - i
        if board[i] == board[j] - offset or board[i] == board[j] + offset:
          h += 1
    return h

def get_best_neighbor(board):
    n = len(board)
    current_h = get_h_cost(board)
    best_board = list(board)
    best_h = current_h
    
    for col in range(n):
      for row in range(n):
        if board[col] == row:
          continue
        neighbor = list(board)
        neighbor[col] = row
        neighbor_h = get_h_cost(neighbor)
        if neighbor_h < best_h:
          best_h = neighbor_h
          best_board = neighbor
          
    return best_board, best_h

def hill_climbing_8_queens():
    # Generate a random initial state
    # board[i] = row index of the queen in column i
    board = [random.randint(0, 7) for _ in range(8)]
    steps = 0
    
    while True:
      steps += 1
      neighbor, neighbor_h = get_best_neighbor(board)
      
      # If no neighbor is better, we reached a peak (local or global minimum)
      if neighbor_h >= get_h_cost(board):
        break
      board = neighbor
      
    return board, get_h_cost(board), steps

# Run the hill climbing algorithm until we find a global minimum (h = 0)
attempts = 0
while True:
    attempts += 1
    solution, h_cost, steps = hill_climbing_8_queens()
    if h_cost == 0:
        print(f"Solution found in {attempts} attempt(s)!")
        print("Board configuration (columns 0 to 7):", solution)
        print("Final heuristic cost:", h_cost)
        break

# Helper function to print the board visually
def print_board(board):
    for r in range(8):
        line = ""
        for c in range(8):
            if board[c] == r:
                line += " Q "
            else:
                line += " . "
        print(line)

print("\nVisual representation:")
print_board(solution)
