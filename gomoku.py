import tkinter as tk
import random

BOARD_SIZE = 15
CELL_SIZE = 30
STONE_RADIUS = 12

class Gomoku:
    def __init__(self, master):
        self.master = master
        self.master.title('Gomoku')
        self.canvas = tk.Canvas(self.master, width=BOARD_SIZE*CELL_SIZE, height=BOARD_SIZE*CELL_SIZE)
        self.canvas.pack()
        self.board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.turn = 1  # 1 for player, -1 for AI
        self.draw_board()
        self.canvas.bind('<Button-1>', self.player_move)
        self.game_over = False

    def draw_board(self):
        for i in range(BOARD_SIZE):
            self.canvas.create_line(CELL_SIZE/2, CELL_SIZE/2 + i*CELL_SIZE,
                                    CELL_SIZE/2 + (BOARD_SIZE-1)*CELL_SIZE, CELL_SIZE/2 + i*CELL_SIZE)
            self.canvas.create_line(CELL_SIZE/2 + i*CELL_SIZE, CELL_SIZE/2,
                                    CELL_SIZE/2 + i*CELL_SIZE, CELL_SIZE/2 + (BOARD_SIZE-1)*CELL_SIZE)

    def draw_stone(self, x, y, color):
        cx = CELL_SIZE/2 + x*CELL_SIZE
        cy = CELL_SIZE/2 + y*CELL_SIZE
        self.canvas.create_oval(cx-STONE_RADIUS, cy-STONE_RADIUS, cx+STONE_RADIUS, cy+STONE_RADIUS,
                                fill=color)

    def player_move(self, event):
        if self.turn != 1 or self.game_over:
            return
        x = int(round((event.x - CELL_SIZE/2)/CELL_SIZE))
        y = int(round((event.y - CELL_SIZE/2)/CELL_SIZE))
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[y][x] == 0:
            self.place_stone(x, y, 1)
            if self.check_win(x, y):
                self.end_game('Player wins!')
                return
            self.turn = -1
            self.master.after(200, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return

        move = self.best_move()
        if move is None:
            empty = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if self.board[y][x] == 0]
            if not empty:
                self.end_game('Draw!')
                return
            move = random.choice(empty)

        x, y = move
        self.place_stone(x, y, -1)
        if self.check_win(x, y):
            self.end_game('Computer wins!')
            return
        self.turn = 1

    def best_move(self):
        empty = [(x, y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if self.board[y][x] == 0]
        # First, see if the AI can win immediately
        for x, y in empty:
            self.board[y][x] = -1
            if self.check_win(x, y):
                self.board[y][x] = 0
                return (x, y)
            self.board[y][x] = 0

        # Then, block the player's winning move
        for x, y in empty:
            self.board[y][x] = 1
            if self.check_win(x, y):
                self.board[y][x] = 0
                return (x, y)
            self.board[y][x] = 0

        return None

    def place_stone(self, x, y, player):
        self.board[y][x] = player
        color = 'black' if player == 1 else 'white'
        self.draw_stone(x, y, color)

    def check_win(self, x, y):
        player = self.board[y][x]
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dx, dy in directions:
            count = 1
            for step in [1, -1]:
                i = 1
                while True:
                    nx = x + dx*i*step
                    ny = y + dy*i*step
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[ny][nx] == player:
                        count += 1
                        i += 1
                    else:
                        break
            if count >= 5:
                return True
        return False

    def end_game(self, message):
        self.game_over = True
        self.canvas.unbind('<Button-1>')
        self.canvas.create_text(BOARD_SIZE*CELL_SIZE/2, BOARD_SIZE*CELL_SIZE/2,
                                text=message, font=('Arial', 24), fill='red')

if __name__ == '__main__':
    root = tk.Tk()
    app = Gomoku(root)
    root.mainloop()
