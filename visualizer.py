import pygame
pygame.display.set_caption('N-Queen Visualizer')


# number of queens
N = 6

#font
# font = pygame.font.SysFont("serif", 32*N//8)

#size
GridSize = 75
WIDTH = N * GridSize
WIN=pygame.display.set_mode((WIDTH, WIDTH))

# colors
DARK = (112,162,163)
LIGHT = (177,228,185)

RED = (240,128,128)
GREEN = (120,248,131)
YELLOW = (120,238,248)
PURPLE = (130,120,248)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)


# properties of each square in the grid
class Square:
    def __init__(self,row,col,width,total_rows):
        self.barrier = False
        self.row=row
        self.col=col
        self.x=row * width
        self.y=col * width
        self.total_rows=total_rows
        self.width=width
        self.color = WHITE
        self.color_board = WHITE
    def is_queen(self):
        return self.barrier
    
    def animate(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        pygame.display.flip()
        pygame.time.wait(20)

    def make_open(self,win):
         self.color = GREEN
         self.animate(win)
    def make_closed(self, win):
        self.color = RED
        self.animate(win)
    def make_queen(self,win):
        self.barrier = True
        self.color = BLACK
        self.animate(win)
    def make_checking(self, win):
        self.color = PURPLE
        self.animate(win)
    def reset(self, win):
        self.color = self.color_board
        self.animate(win)
    def remove_queen(self,win):
        self.barrier = False
        self.color = self.color_board
        self.animate(win)

    def draw(self,win):
        if ((self.x+self.y)%2 != 0):
            self.color_board = LIGHT
            pygame.draw.rect(win, LIGHT, (self.x, self.y, self.width, self.width))
        else:
            self.color_board = DARK
            pygame.draw.rect(win, DARK, (self.x, self.y, self.width, self.width))


def algorithm(board, win):
    sol=solveNQUtil(board, 0, win)
    if not sol:
        print("No Solution")
        return False
    else:
        print("Solution Found")
        return True

def isSafe(board, row, col, win):
    block_point_y1 = N
    block_point_x2, block_point_y2 = N,N
    block_point_x3, block_point_y3 = N,N
    flag = True
    flag2 = True
    flag3 = True
    board[row][col].make_open(win)

    # Check this column only upward 
    for i in range(row-1, -1, -1):
        board[i][col].make_checking(win)
        block_point_y1 = i
        if board[i][col].is_queen():
            board[i][col].make_closed(win)
            board[i][col].make_queen(win)
            flag = False
            break


    # Check upper diagonal on left side
    if flag:
        for i, j in (zip(range(row, -1, -1), range(col, -1, -1))):
            board[i][j].make_checking(win)
            block_point_x2, block_point_y2 = i,j
            if board[i][j].is_queen():
                board[i][j].make_closed(win)
                board[i][j].make_queen(win)
                flag2 = False
                break
            
    # Check upper diagonal on right side
    if flag and flag2:
        for i, j in (zip(range(row, -1, -1), range(col, N, 1))):
            board[i][j].make_checking(win)
            block_point_x3, block_point_y3 = i,j
            if board[i][j].is_queen():
                board[i][j].make_closed(win)
                board[i][j].make_queen(win)
                flag3 = False
                break
    
    for i, j in zip(range(block_point_x3, row, 1), range(block_point_y3, col, -1)):
        if not board[i][j].is_queen():
            board[i][j].reset(win)

    for i, j in zip(range(block_point_x2, row, 1), range(block_point_y2, col, 1)):
        if not board[i][j].is_queen():        
            board[i][j].reset(win)

    for i in range(block_point_y1, row, 1):
        if not board[i][col].is_queen():
            board[i][col].reset(win)


    board[row][col].reset(win)
    return flag and flag2 and flag3


def solveNQUtil(board, row, win):
      
    # base case: If all queens are placed
    # then return true
    if row >= N:
        return True
  
    # Consider this column and try placing
    # this queen in all rows one by one
    for i in range(N):
  
        if isSafe(board, row, i, win):
              
            # Place this queen in board[row][i]
            board[row][i].make_queen(win)

            # recur to place rest of the queens
            if solveNQUtil(board, row + 1, win):
                return True
  
            # If placing queen in board[i][col
            # doesn't lead to a solution, then
            # queen from board[i][col]
            board[row][i].remove_queen(win)
  
    # if the queen can not be placed in any row in
    # this column col then return false
    return False

def make_board(rows,width):
    board=[]
    gap=width//rows
    for i in range(rows):
        board.append([])
        for j in range(rows):
            spot=Square(j,i,gap,rows)
            board[i].append(spot)
    return board

def draw(win, board):
   for col in board:
       for spot in col:
           spot.draw(win)
           pygame.display.flip()
           pygame.time.wait(30)


def main(win, width):
    board=make_board(N,width)
    run = True
    started=False
    draw(win,board)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]: #If left mouse button pressed, start algo
                started=True
                #algorithm(lambda: draw(win, grid, ROW, width), grid)
                algorithm(board, win)
            if pygame.mouse.get_pressed()[2]: #will never be used, just for testing
                #grid[0][0].reset()
                started=False

    pygame.display.quit()          
    pygame.quit()

main(WIN, WIDTH)

