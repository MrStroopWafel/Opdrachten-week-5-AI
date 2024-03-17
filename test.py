import pygame
from isolation import *
import time

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_occupied = self.is_visited = False
    
    def occupy(self):
        self.is_occupied = True
        self.is_visited = False

    def leave(self):
        self.is_occupied = False
        self.is_visited = True

    def is_empty(self):
        return False if self.is_occupied or self.is_visited else True
    
    def visited_in_past(self):
        return self.is_visited
    
    def rewind (self):
        self.is_occupied = self.is_visited = False
    
class Board:
    def __init__(self):
        self.tiles = [[Tile(row, col) for col in range(ROWS)] for row in range(ROWS)]
        self.max_player_location = [0, 0]
        self.min_player_location = [5, 5]
        self.tiles[0][0].occupy()
        self.tiles[5][5].occupy()
        self.white_queen = pygame.image.load("img\\QueenWhite.png")
        self.white_queen = pygame.transform.scale(self.white_queen, IMAGE_SIZE)
        self.black_queen = pygame.image.load("img\\QueenBlack.png")
        self.black_queen = pygame.transform.scale(self.black_queen, IMAGE_SIZE)

    def get_player_location(self, player):
        if player == 0:
            return self.max_player_location
        else:
            return self.min_player_location
        
    def draw_board(self, win):
        win.fill(GRAY) # fill the window with gray color
        for row in range(ROWS): # draw the white squares
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for row in range(ROWS): # draw mark the visited squared red
            for col in range(ROWS):
                if self.tiles[row][col].visited_in_past():
                    pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        #check if game eneded, if so mark the victor with green and the loser with red; both red for tie;
        if not self.check_options(0, self) and not self.check_options(1, self):
            pygame.draw.rect(win, RED, (self.max_player_location[0] * SQUARE_SIZE, self.max_player_location[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, RED, (self.min_player_location[0] * SQUARE_SIZE, self.min_player_location[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif not self.check_options(0, self):
            pygame.draw.rect(win, RED, (self.max_player_location[0] * SQUARE_SIZE, self.max_player_location[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, GREEN, (self.min_player_location[0] * SQUARE_SIZE, self.min_player_location[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        elif not self.check_options(1, self):
            pygame.draw.rect(win, GREEN, (self.max_player_location[0] * SQUARE_SIZE, self.max_player_location[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(win, RED, (self.min_player_location[0] * SQUARE_SIZE, self.min_player_location[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        #draw the queens
        win.blit(self.white_queen, (self.max_player_location[0] * SQUARE_SIZE, self.max_player_location[1] * SQUARE_SIZE))
        win.blit(self.black_queen, (self.min_player_location[0] * SQUARE_SIZE, self.min_player_location[1] * SQUARE_SIZE))

    def move(self, row, col, player):
        if player == 0:
            player_pos = self.max_player_location
        else:
            player_pos = self.min_player_location

        self.tiles[row][col].occupy()
        self.tiles[player_pos[0]][player_pos[1]].leave()

        if player_pos == self.max_player_location:
            self.max_player_location = [row, col]
        else:
            self.min_player_location = [row, col]

    def back(self, player_pos_old, player):
        if player == 0:
            player_pos = self.max_player_location
        else:
            player_pos = self.min_player_location

        self.tiles[player_pos_old[0]][player_pos_old[1]].occupy()
        self.tiles[player_pos[0]][player_pos[1]].rewind()

        if player_pos == self.max_player_location:
            self.max_player_location = [player_pos_old[0], player_pos_old[1]]
        else:
            self.min_player_location = [player_pos_old[0], player_pos_old[1]]

    def check_move(self, row, col, player, board): #check if move is valid
        if player == 0:
            player_pos = self.max_player_location
        else:
            player_pos = self.min_player_location

        if row == player_pos[0]: # check if move is in the same row
            i = 1 if col > player_pos[1] else -1
            for c in range(player_pos[1] + i, col + i, i): # loop through all in same row
                if board.tiles[row][c].is_empty():
                    if  c == col:
                        #print("Move isn't blocked")
                        return True
                else:
                    #print("Move isn't blocked")
                    return False
                
        elif col == player_pos[1]: # check if move is in the same col
            i = 1 if row > player_pos[0] else -1
            for r in range(player_pos[0] + i, row + i, i): # loop through all in same col
                #print(r, player_pos[0], row, i)
                if board.tiles[r][col].is_empty():
                    if r == row:
                        return True
                else:
                    return False
                
        elif abs(row - player_pos[0]) == abs(col - player_pos[1]): # check if move is in the same diagonal
            i = 1 if row > player_pos[0] else -1
            j = 1 if col > player_pos[1] else -1
            for r, c in zip(range(player_pos[0] + i, row + i, i), range(player_pos[1] + j, col + j, j)): # loop through all in same diagonal and mix both diagonals
                if board.tiles[r][c].is_empty():
                    if r == row and c == col:
                        return True
                else:
                    return False
                
        return False
                
    def check_options(self, player, board): # check all possible moves for a player and returns list of possible moves
        if player == 0:
            player_pos = self.max_player_location
        else:
            player_pos = self.min_player_location
        options = []

        for row in range(ROWS):
                for col in range(ROWS):
                    if self.check_move(row, col, player, board):
                        options.append((row, col))

        return options
    
class MinimaxPlayer:
    def __init__(self, depth, max_player, temp):
        self.depth = depth
        self.max_player = max_player
        self.WIN = temp
        self.best_move = None

    def get_best_move(self):
        return self.best_move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or not board.check_options(0, board) or not board.check_options(1, board): # check if game ended or depth reached
            return self.evaluate(board, self.max_player)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for option in board.check_options(self.max_player, board): # loop through all possible moves
                row, col = option
                player_pos = board.get_player_location(self.max_player)
                board.move(row, col, self.max_player)

                eval = self.minimax(board, depth - 1, alpha, beta, False) # call minimax for the next depth
                board.back(player_pos, self.max_player)  # undo the move
                if eval > max_eval: # check if the move is better than the previous best move
                    max_eval = eval
                    best_move = option
                alpha = max(alpha, eval) # update alpha for pruning
                if beta <= alpha: # pruning check
                    break
            self.best_move = best_move
            return max_eval
        
        else:
            min_eval = float('inf')
            i = 0 if self.max_player else 1
            for option in board.check_options(i, board): # loop through all possible moves
                row, col = option
                player_pos = board.get_player_location(i)
                board.move(row, col, i)

                eval = self.minimax(board, depth - 1, alpha, beta, True) # call minimax for the next depth
                board.back(player_pos, i)  # undo the move
                if eval < min_eval: # check if the move is better than the previous best move
                    min_eval = eval
                beta = min(beta, eval) # beta alpha for pruning
                if beta <= alpha:  # pruning check
                    break
            return min_eval

    def evaluate(self, board, switch): # evaluate the board based on the number of possible moves for each player (heuristic function)
        if switch:
            return len(board.check_options(switch, board)) - len(board.check_options(switch - 1, board))
        else:
            return len(board.check_options(switch, board)) - len(board.check_options(switch + 1, board))   
    
class Game:
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.depth = 6
        self.FPS = 60
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ai_player = 0
        self.ai = MinimaxPlayer(self.depth, self.ai_player, self.WIN)
        pygame.display.set_caption('Isolation')

    def main(self):
        run = True
        clock = pygame.time.Clock()
        player = 0

        while run:
            clock.tick(self.FPS)
            self.board.draw_board(self.WIN)
            pygame.display.update()

            if self.ai_player == player: # check if it's the AI's turn
                self.ai.minimax(self.board, self.depth, float('-inf'), float('inf'), True)
                best_move = self.ai.get_best_move()
                self.board.move(best_move[0], best_move[1], player) 
                if not self.board.check_options(0, self.board) or not self.board.check_options(1, self.board): # check if game ended
                    print("Game Over")
                    self.board.draw_board(self.WIN)
                    pygame.display.update()
                    time.sleep(3)
                    run = False # end the game
                player = 1 if player == 0 else 0 # switch player

            else:
                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos() # get the position of the click
                        row, col = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE # get the row and col of the click
                        if self.board.check_move(row, col, player, self.board):
                            self.board.move(row, col, player) 
                            player = 1 if player == 0 else 0 # switch player
                            
                            if not self.board.check_options(0, self.board) or not self.board.check_options(1, self.board): # check if game ended
                                print("Game Over")
                                self.board.draw_board(self.WIN)
                                pygame.display.update()
                                time.sleep(3)
                                run = False # end the game
        pygame.quit()

game = Game()
game.main()