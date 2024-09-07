""" Game Logic """

EMPTY = ""
X = "X"
O = "O"


def player(board):
    """ Determine whose turn it is """
    x_count = 0 
    o_count = 0 
    for row in range(3):
        for col in range(3):
            if board[row][col] == X:
                x_count += 1
            elif board[row][col] == O:
                o_count += 1
                
    return X if x_count <= o_count else O


def possible_moves(board):
    """ Return set of possible moves """
    possible_moves = set()
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                possible_moves.add((row, col)) 
    return possible_moves


def check_winner(board):
    """ Returns winner based on the board state """
    for row in range(3):
        # Horizontal
        if board[row] == ['O', 'O', 'O']:
            return O
        elif board[row] == ['X', 'X', 'X']:
            return X

        # Vertical
        x_count = 0
        o_count = 0
        for col in range(3):
            if board[col][row] == 'O':
                o_count += 1
            elif board[col][row] == 'X':
                x_count += 1

            if x_count == 3:
                return X
            if o_count == 3:
                return O

    # Diagonal
    x_countx = 0
    x_county = 0
    o_countx = 0
    o_county = 0

    for i in range(3):
        if board[i][i] == X:
            x_countx += 1
        if board[i][i] == O:
            o_countx += 1
        if board[i][2 - i] == X:
            x_county += 1
        if board[i][2 - i] == O:
            o_county += 1

        if x_countx == 3 or x_county == 3:
            return X
        if o_countx == 3 or o_county == 3:
            return O

    return None


def check_draw(board):
    """ Check if there are no possible moves and winner, return True indicating a draw """
    if check_winner(board) is not None or len(possible_moves(board)) == 0:
        return True
    return False


def evaluate(board):
    """ Provide value based on board results """
    if check_winner(board) is not None:
        result = check_winner(board)
    else:
        # Draw
        return 0

    # 1 for maximizing
    if result == X:
        return 1
    # -1 for minimizing
    elif result == O:
        return -1
    
    
def best_move(board):
    """ Find the best move based on board state """
    if check_draw(board):
        return None
    
    # If maximizing
    if player(board) == X:
        # Set value for lowest possible value, 
        # so that algorithm always consider the moves with small improvements
        best_value = -float('inf')
        best_move = None
        
        for move in possible_moves(board):
            row, col = move
            # Make the move
            board[row][col] = X
            # Update score with Minimax algorithm
            score = minimax(board)
            # Undo the move
            board[row][col] = EMPTY
        
            # If score is higher than the best value, make the move as the best move
            if score > best_value:
                best_value = score
                best_move = move
    # If minimizing, 
    # meaning, preventing the maximizing one get high scores of board state
    else:
        best_value = float('inf')
        best_move = None
        
        for move in possible_moves(board):
            row, col = move
            board[row][col] = O
            score = minimax(board)
            board[row][col] = EMPTY
        
            if score < best_value:
                best_value = score
                best_move = move
    
    return best_move
    
    
def minimax(board):
    """ Minimax algorithm """
    # Base case
    if check_draw(board):
        return evaluate(board)
    
    if player(board) == X:
        best_value = -float("inf")
        
        for move in possible_moves(board):
            row, col = move
            board[row][col] = X
            best_value = max(best_value, minimax(board))
            board[row][col] = EMPTY
    else:
        best_value = float('inf')
        
        for move in possible_moves(board):
            row, col = move
            board[row][col] = O
            best_value = min(best_value, minimax(board))
            board[row][col] = EMPTY
        
    return best_value   
