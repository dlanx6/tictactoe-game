import random
import tkinter as tk
from tkinter import *


# Game Board
class Board:
    # Constructor
    def __init__(self, game):
        # Game instance
        self.game = game
        
        # Initialize tkinter
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        
        # Window size
        self.window.geometry("400x400")
        
        # Disable window resizing
        self.window.resizable(False, False)
        
        
        self.window.update_idletasks()
        # Get width and height info
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        # Calculate the position
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        # Update position
        self.window.geometry(f'{width}x{height}+{x}+{y}')
      
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
        
        # Grid for Button references
        self.layout = [
            ['', '', ''],
            ['', '', ''],
            ['', '', ''],
        ]
        
        # Widgets
        self.create_label()
        self.create_buttons()

        
    def create_label(self):
        # Game label
        # Game always starts with the player of X
        self.game_label = tk.Label(
            self.frame1,
            text=f"{self.game.current_player.name}'s Turn",
            height=2,
            width=12,
            font=("Arial", 16)
        )   
        # Place in frame
        self.game_label.pack()
          
        # Player 1 Label
        self.player1_label = tk.Label(
            self.frame2,
            text=f"Player 1: {self.game.player_1.score}",
            height=2,
            width=12,
            font=("Arial", 12),
            anchor="w"
        )   
        # Place in frame
        self.player1_label.place(x=67, y=3)
        
        # Player 2 Label
        self.player2_label = tk.Label(
            self.frame2,
            text=f"Player 2: {self.game.player_2.score}",
            height=2,
            width=12,
            font=("Arial", 12),
            anchor="w"
        )   
        # Place in frame
        self.player2_label.place(x=249, y=3)
        
        
    def create_buttons(self):
        # Button for "New Game"
        self.game_button = tk.Button(
            self.frame1, 
            text="New Game",
            height=1,
            width=12,
            font=("Arial", 16),
            command=lambda : self.game_button_click_handler()
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
                    text="", 
                    height=5, 
                    width=8,  
                    relief="solid",
                    font=("Arial", 40, "bold"),
                    command=lambda r=row, c=col: self.button_click_handler(r, c)
                )         
                # Place in frame using grid for organized positioning      
                button.grid(row=row, column=col, sticky="nsew")
                self.layout[row][col] = button     
        
    
    def game_button_click_handler(self):
        # Reset game, but maintain score
        for row in range(3):
            for col in range(3):
                self.layout[row][col].config(text="" ,state="normal")
                
        self.game.inputs = [
                ['', '', ''],
                ['', '', ''],
                ['', '', '']
        ]
        
        self.symbols = Game.symbols.copy()
        print(f"Symbols: {self.symbols}")
        
        # Player
        self.game.player_1.symbol = random.choice(self.symbols)
        self.symbols.remove(self.game.player_1.symbol)
        print(f"Player 1: {self.game.player_1.symbol}")
        
        # Player AI
        self.game.player_2.symbol = self.symbols[0]
        print(f"Player 2: {self.game.player_2.symbol}\n")
        
        # Determine whose turn it is, based on the symbol they possess
        # (X always plays first, so player with the X plays first)
        self.game.current_player = self.game.player_1 if self.game.player_1.symbol == "X" else self.game.player_2
        
         # Update label for whose turn it is
        self.game_label.config(text=f"{self.game.current_player.name}'s Turn")
    
        
    def button_click_handler(self, row, col):
        # Update the state and display Player symbol on the board
        self.layout[row][col].config(text=self.game.current_player.symbol, state="disabled", disabledforeground="red" if self.game.current_player.symbol == 'X' else "blue")
        
        # Determine Game State
        self.game.move_input(row, col, self.game.current_player)
        print(f"Game inputs:\n{self.game.inputs[0]}\n{self.game.inputs[1]}\n{self.game.inputs[2]}\n")
        
        # Switch turns
        self.game.switch_player()
        
        # Update label for whose turn it is
        self.game_label.config(text=f"{self.game.current_player.name}'s Turn")
        
        # Check for winner
        if self.game.check_win():
            for i in range(3):
                for j in range(3):
                    self.layout[i][j].config(state="disabled")
                    
            self.game_label.config(text=f"{self.game.check_win()} Wins!")
            self.game.update_score(self.game.check_win())
            
            if self.game.check_win() == "Player 1":
                self.player1_label.config(text=f"Player 1: {self.game.player_1.score}")
            else:
                self.player2_label.config(text=f"Player 2: {self.game.player_2.score}")
          
        # Check for draw
        else: 
            if self.is_full():      
                self.game_label.config(text="Draw!")            
 
 
    # Check if all cells are occupied resulting to draw
    def is_full(self):
        for row in self.layout:
            for cell in row:
                if cell.cget("text") == "":
                    return False
        return True    
 
 
    def Display(self):
        # Run application
        self.window.mainloop()
        
   
# PLayers for the game     
class Player:
    def __init__(self, name, symbol, score):
        self.name = name
        self.symbol = symbol
        self.score = score
        
    
class Game:   
    symbols = ['X', 'O']
    
    def __init__(self):
        # Inputs for X and O should be stored here
        # This will be used for game logic
        self.inputs = [
                ['', '', ''],
                ['', '', ''],
                ['', '', '']
        ]
        
        self.symbols = Game.symbols.copy()
        print(f"Symbols: {self.symbols}")
        
        # Player
        self.player_1 = Player("Player 1", random.choice(self.symbols), 0) 
        self.symbols.remove(self.player_1.symbol)
        print(f"Player 1: {self.player_1.symbol}")
        
        # Player AI
        self.player_2 = Player("Player 2", self.symbols[0], 0)
        print(f"Player 2: {self.player_2.symbol}\n")
        
        # Determine whose turn it is, based on the symbol they possess
        # (X always plays first, so player with the X plays first)
        self.current_player = self.player_1 if self.player_1.symbol == "X" else self.player_2
        
    
    def switch_player(self):
        if self.current_player == self.player_2:
            self.current_player = self.player_1
        else:
            self.current_player = self.player_2       
    
    
    def move_input(self, row, col, player):
        if self.inputs[row][col] not in ['Player 1', 'Player 2']:
            self.inputs[row][col] = player.name
    
    
    def check_win(self):
        for row in range(3):
            player1_count = 0
            player2_count = 0
            
            for col in range(3):
                # Check for horizontal lines
                if self.inputs[row] in [['Player 1','Player 1','Player 1'], ['Player 2','Player 2','Player 2']]:
                    return self.inputs[row][col]
                
                # Check for vertical lines
                if self.inputs[col][row] == 'Player 1':
                    player1_count += 1
                    if player1_count == 3:
                        return 'Player 1'   
                elif self.inputs[col][row] == 'Player 2':
                    player2_count += 1
                    if player2_count == 3:
                        return 'Player 2'    
         
         
        player1_diagonalX_count = 0
        player1_diagonalY_count = 0
        
        player2_diagonalX_count = 0
        player2_diagonalY_count = 0
            
        # Check for diagonal lines
        for i in range(3):
            if self.inputs[i][i] == 'Player 1':
                player1_diagonalX_count += 1    
            elif self.inputs[i][i] == 'Player 2':
                player2_diagonalX_count += 1         
    
        for i in range(3):
            if self.inputs[i][2 - i] == 'Player 1':
                player1_diagonalY_count += 1
            elif self.inputs[i][2 - i] == 'Player 2':
                player2_diagonalY_count += 1
              
        if player1_diagonalX_count == 3 or player1_diagonalY_count == 3:
            return 'Player 1'
        elif player2_diagonalX_count == 3 or player2_diagonalY_count == 3:
            return 'Player 2'            
    
    
    def update_score(self, winner):
        if winner == "Player 1":
            self.player_1.score += 1
        else:
            self.player_2.score += 1

  
def main():
    game = Game()
    board = Board(game)

    # Run Application
    board.Display()
    
    
if __name__ == '__main__':
    main()