import tkinter as tk
from tkinter import PhotoImage, messagebox
import tkinter
import chess
import random

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mehtab's Chess Game")
        self.root.geometry("600x600")
        self.is_dark_mode = False
        self.board = chess.Board()
        self.selected_piece = None
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_screen()
        
        title = tk.Label(self.root, text="Ultimate Chess", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white")
        title.pack(fill=tk.BOTH, pady=20)

        singleplayer_button = tk.Button(self.root, text="Singleplayer", command=self.choose_difficulty, font=("Arial", 16), bg="#2196F3", fg="white", activebackground="#1976D2")
        singleplayer_button.pack(pady=20, padx=200, fill=tk.X)

        multiplayer_button = tk.Button(self.root, text="Multiplayer", command=self.start_multiplayer, font=("Arial", 16), bg="#2196F3", fg="white", activebackground="#1976D2")
        multiplayer_button.pack(pady=20, padx=200, fill=tk.X)

        self.theme_button = tk.Button(self.root, text="Toggle Dark/Light Theme", command=self.toggle_theme, font=("Arial", 16), bg="#FF9800", fg="white", activebackground="#F57C00")
        self.theme_button.pack(pady=20, padx=200, fill=tk.X)

        developers_info = tk.Label(self.root, text="Developed And Writtten By : MehtabCodes", font=("Arial", 15, "bold"), bg="#4CAF50", fg="white")
        developers_info.pack(fill=tk.BOTH, side="bottom")

    def choose_difficulty(self):
        self.clear_screen()
        tk.Label(self.root, text="Select Difficulty Level", font=("Arial", 18, "bold")).pack(pady=20)

        easy_button = tk.Button(self.root, text="Easy", command=lambda: self.start_singleplayer('easy'), font=("Arial", 16), bg="#4CAF50", fg="white", activebackground="#388E3C")
        easy_button.pack(pady=10, padx=20, fill=tk.X)

        medium_button = tk.Button(self.root, text="Medium", command=lambda: self.start_singleplayer('medium'), font=("Arial", 16), bg="#FFEB3B", fg="black", activebackground="#FBC02D")
        medium_button.pack(pady=10, padx=20, fill=tk.X)

        hard_button = tk.Button(self.root, text="Hard", command=lambda: self.start_singleplayer('hard'), font=("Arial", 16), bg="#F44336", fg="white", activebackground="#D32F2F")
        hard_button.pack(pady=10, padx=20, fill=tk.X)

    def start_singleplayer(self, difficulty):
        self.clear_screen()
        tk.Label(self.root, text="Singleplayer Mode", font=("Arial", 18, "bold")).pack(pady=20)
        self.difficulty = difficulty
        self.board.reset()
        self.create_game_ui(singleplayer=True)

    def start_multiplayer(self):
        self.clear_screen()
        tk.Label(self.root, text="Multiplayer Mode", font=("Arial", 18, "bold")).pack(pady=20)
        self.board.reset()
        self.create_game_ui(singleplayer=False)

    def create_game_ui(self, singleplayer):
        self.singleplayer = singleplayer
        self.create_board()
        self.update_board_display()

        reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game, font=("Arial", 16), bg="#FF5722", fg="white", activebackground="#D84315")
        reset_button.pack(side=tk.LEFT, padx=10, pady=10)

        declare_button = tk.Button(self.root, text="Declare Game", command=self.declare_game, font=("Arial", 16), bg="#FF5722", fg="white", activebackground="#D84315")
        declare_button.pack(side=tk.LEFT, padx=10, pady=10)

    def create_board(self):
        self.board_frame = tk.Canvas(self.root, width=480, height=480)
        self.board_frame.pack(pady=10)
        
        self.squares = {}
        for r in range(8):
            for c in range(8):
                square_color = '#eee' if (r + c) % 2 == 0 else '#bbb'
                square = self.board_frame.create_rectangle(c * 60, r * 60, (c + 1) * 60, (r + 1) * 60, fill=square_color)
                self.squares[(r, c)] = square

        self.board_frame.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        col = event.x // 60
        row = event.y // 60

        if self.selected_piece and (row, col) in self.squares:
            start_row, start_col = self.selected_piece[1], self.selected_piece[2]
            move = chess.Move.from_uci(f"{chess.square_name(start_col + start_row * 8)}{chess.square_name(col + row * 8)}")
            if move in self.board.legal_moves:
                self.board.push(move)
                if self.singleplayer and not self.board.is_game_over():
                    self.make_move_ai()
                self.selected_piece = None
                self.update_board_display()
                if self.board.is_game_over():
                    self.game_over_message()
            else:
                messagebox.showerror("Invalid Move", "Please make a valid move!")
        else:
            piece = self.board.piece_at(row * 8 + col)
            if piece and ((self.singleplayer and piece.color == chess.WHITE) or not self.singleplayer):
                self.selected_piece = (piece, row, col)
                self.update_board_display()

    def update_board_display(self):
        self.board_frame.delete("piece")
        for r in range(8):
            for c in range(8):
                piece = self.board.piece_at(r * 8 + c)
                if piece:
                    piece_symbol = self.get_piece_symbol(piece)
                    self.draw_piece(c * 60 + 30, r * 60 + 30, piece_symbol)

    def get_piece_symbol(self, piece):
        symbols = {
            chess.PAWN: '♟' if piece.color == chess.BLACK else '♙',
            chess.ROOK: '♜' if piece.color == chess.BLACK else '♖',
            chess.KNIGHT: '♞' if piece.color == chess.BLACK else '♘',
            chess.BISHOP: '♝' if piece.color == chess.BLACK else '♗',
            chess.QUEEN: '♛' if piece.color == chess.BLACK else '♕',
            chess.KING: '♚' if piece.color == chess.BLACK else '♔',
        }
        return symbols[piece.piece_type]

    def draw_piece(self, x, y, symbol):
        self.board_frame.create_text(x, y, text=symbol, font=("Arial", 32), tags="piece")

    def make_move_ai(self):
        if self.difficulty == 'easy':
            move = random.choice(list(self.board.legal_moves))
        elif self.difficulty == 'medium':
            move = self.medium_ai_move()
        else:  # hard
            move = self.hard_ai_move()
        
        self.board.push(move)
        self.update_board_display()

    def medium_ai_move(self):
        valid_moves = list(self.board.legal_moves)
        return self.select_best_move(valid_moves, defensive=False)

    def hard_ai_move(self):
        valid_moves = list(self.board.legal_moves)
        return self.select_best_move(valid_moves, defensive=False)

    def select_best_move(self, valid_moves, defensive=False):
        best_move = None
        best_score = float('-inf')

        for move in valid_moves:
            self.board.push(move)
            score = self.evaluate_board(defensive)
            if score > best_score:
                best_score = score
                best_move = move
            self.board.pop()

        return best_move if best_move else random.choice(valid_moves)

    def evaluate_board(self, defensive):
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                value = self.get_piece_value(piece)
                score += value if piece.color == chess.WHITE else -value
        if not defensive:
            score += self.evaluate_aggressive_moves()
        return score

    def evaluate_aggressive_moves(self):
        score = 0
        for move in self.board.legal_moves:
            if self.board.piece_at(move.to_square) is not None:
                score += self.get_piece_value(self.board.piece_at(move.to_square))
        return score

    def get_piece_value(self, piece):
        values = {
            chess.PAWN: 1,
            chess.ROOK: 5,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.QUEEN: 9,
            chess.KING: 0,
        }
        return values[piece.piece_type]

    def reset_game(self):
        if messagebox.askyesno("Reset Game", "Do you really want to reset the game?"):
            self.board.reset()
            self.update_board_display()

    def declare_game(self):
        if messagebox.askyesno("Declare Game", "Do you really want to declare?"):
            self.create_main_menu()

    def toggle_theme(self):
        if self.is_dark_mode:
            self.root.config(bg="white")
            self.is_dark_mode = False
        else:
            self.root.config(bg="black")
            self.is_dark_mode = True

    def game_over_message(self):
        if self.board.is_checkmate():
            winner = "Black Wins" if self.board.turn else "White Wins"
        else:
            winner = "Draw" if self.board.is_stalemate() else "Game Over"
        messagebox.showinfo("Game Over", winner)
        self.create_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Initialize the app
root = tk.Tk()
app = ChessApp(root)
root.mainloop()
