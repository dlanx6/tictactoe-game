import random
from tictactoe import player, check_draw, check_winner, best_move
import tkinter as tk
from tkinter import *


EMPTY = ""
X = "X"
O = "O"


def game_window():
    """ Tkinter Window """
    # Initialize tkinter
    window = tk.Tk()
    window.title("Tic-Tac-Toe")

    # Window size
    window.geometry("400x400")

    # Disable window resizing
    window.resizable(False, False)

    window.update_idletasks()
    # Get width and height info
    width = window.winfo_width()
    height = window.winfo_height()
    # Centralize the window
    # Calculate the position
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    # Update position
    window.geometry(f"{width}x{height}+{x}+{y}")

    return window


class Board:
    def __init__(self, window):
        # Tkinter window
        self.window = window
        # Board layout
        self.layout = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]

        # Frame for label and new game button
        self.frame1 = Frame(self.window)
        self.frame1.pack(fill=tk.BOTH, expand=True)

        self.frame2 = Frame(self.window, height=50)
        self.frame2.pack(fill=tk.BOTH, expand=True)

        # Frame for actual Board game
        self.frame3 = Frame(self.window, padx=70, pady=10)
        self.frame3.pack(fill=tk.BOTH, expand=True)

        # Parent row and column influence to widgets
        for i in range(3):
            self.frame3.grid_rowconfigure(i, weight=1)
            self.frame3.grid_columnconfigure(i, weight=1)

        # Widgets
        self.create_labels()
        self.create_buttons()
        

    def create_labels(self):
        """ Create labels """
        # Game label
        # Game always starts with the player of X
        self.game_label = tk.Label(
            self.frame1, text="", height=2, width=12, font=("Arial", 16)
        )
        # Place in frame
        self.game_label.pack()

        # Player 1 Label
        self.player_label = tk.Label(
            self.frame2,
            text="Player: 0",
            height=2,
            width=12,
            font=("Arial", 12),
            anchor="w",
        )
        # Place in frame
        self.player_label.place(x=67, y=3)

        # Player 2 Label
        self.ai_label = tk.Label(
            self.frame2,
            text="Player AI: 0",
            height=2,
            width=12,
            font=("Arial", 12),
            anchor="w",
        )
        # Place in frame
        self.ai_label.place(x=241, y=3)


    def create_buttons(self):
        """ Create buttons """
        # Button for "New Game"
        self.game_button = tk.Button(
            self.frame1,
            text="New Game",
            height=1,
            width=12,
            font=("Arial", 16),
        )
        # Place in frame
        self.game_button.pack()

        # Buttons for grid
        for row in range(len(self.layout)):
            for col in range(len(self.layout)):
                # Pass the window, set the text as none for now, set the height and width of the button,
                # get the same background color as the window, set the relief or the border style of the button.
                button = tk.Button(
                    self.frame3,
                    text=EMPTY,
                    height=5,
                    width=8,
                    relief="solid",
                    font=("Arial", 40, "bold"),
                )
                # Place in frame using grid for organized positioning
                button.grid(row=row, column=col, sticky="nsew")
                self.layout[row][col] = button


    def display(self):
        """ Run tkinter window """
        self.window.mainloop()


class Game: 
    def __init__(self, board):
        self.board = board
    
        # Event handling
        self.board.game_button.config(command=lambda: self.new_game())
        for row in range(3):
            for col in range(3):
                self.board.layout[row][col].config(command=lambda r=row, c=col: self.player_move(r, c))
        
        # Input Layout
        self.inputs = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
    
        # Player setup
        # Randomly picks a symbol for player  
        self.choice = random.choice([X, O]) 
        self.player = self.choice
        self.ai = O if self.player == X else X
        
        print(f"Player: {self.player}")
        print(f"AI: {self.ai}\n")
        
        self.board.game_label.config(text="Player's Turn" if self.player == X else "AI Thinking...")
        
        
        self.player_score = 0
        self.ai_score = 0
        
        if player(self.inputs) == self.ai:
            self.board.window.after(500, self.ai_move)
    
    
    def new_game(self):
        """ Reset board and swap symbols """
        for row in range(3):
            for col in range(3):
                self.board.layout[row][col].config(text=EMPTY ,state="normal")
        
        # Layout copy
        self.inputs = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
    
        # Player setup
        self.temp = self.player
        self.player = self.ai
        self.ai = self.temp
        
        print(f"Player: {self.player}")
        print(f"AI: {self.ai}\n")
        
        self.board.game_label.config(text="Player's Turn" if self.player == X else "AI Thinking...")
    
        if player(self.inputs) == self.ai:
            self.board.window.after(200, self.ai_move)
    
    
    def player_move(self, row, col): 
        """ Button handling for user """                  
        if player(self.inputs) == self.player:
            self.make_input(row, col)
            
    def ai_move(self):
        """ Generate move for AI """
        if player(self.inputs) == self.ai and check_winner != None:
            print(f"Best move: {best_move(self.inputs)}\n")
            row, col = best_move(self.inputs)
            self.make_input(row, col)
    
    
    def make_input(self, row, col):
        """ Display input in board """                
        # Player move
        if player(self.inputs) == self.player:
            self.board.layout[row][col].config(text=self.player, state="disabled", disabledforeground="red" if self.player == 'X' else "blue")  
            self.inputs[row][col] = self.player
            self.board.game_label.config(text="AI Thinking...")
            self.board.window.after(500, self.ai_move)
        # AI move     
        elif player(self.inputs) == self.ai:
            self.board.layout[row][col].config(text=self.ai, state="disabled", disabledforeground="red" if self.ai == 'X' else "blue")
            self.inputs[row][col] = self.ai
            self.board.game_label.config(text="Player's Turn")      
        
        print(f"{self.inputs[0]}\n{self.inputs[1]}\n{self.inputs[2]}\n")
        # Check for winner
        if check_winner(self.inputs):
            for i in range(3):
                for j in range(3):
                    self.board.layout[i][j].config(state="disabled")
            self.board.game_label.config(text="Player Wins!" if self.player == check_winner(self.inputs) else "AI Wins!")
            self.update_score(check_winner(self.inputs))
        else:
            # Check for draw
            if check_draw(self.inputs):
                # Disable all buttons
                for i in range(3):
                    for j in range(3):
                        self.board.layout[i][j].config(state="disabled")
                self.board.game_label.config(text="Draw!") 
    
    
    def update_score(self, winner):
        """ Update score of the winner"""
        if winner == self.player:
            self.player_score += 1
            self.board.player_label.config(text=f"Player: {self.player_score}")
        else:
            self.ai_score += 1
            self.board.ai_label.config(text=f"Player AI: {self.ai_score}")
        

def main():
    window = game_window()
    board = Board(window)
    Game(board)

    # Run game
    board.display()


if __name__ == "__main__":
    main()
