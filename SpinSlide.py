"""
 Show how to use a sprite backed by a graphic.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/vRB_983kUMc
"""
 
import pygame
from pygame.locals import *
import random
import copy
import math


BLACK = (0, 0, 0)
PI = 3.141592653

pygame.init()
 
# Set the width and height of the screen [width, height]
size = (900, 800)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Slider Puzzle")
 
# Loop until the user clicks the close button.
done = False
pause = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def gray(c):
    return (c, c, c)

BACKGROUND = gray(100)

# tile Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (235, 0, 0)
GREEN = (0, 204, 0)
ORANGE = (235,145,0)
BLACK_C = gray(30)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
PERU = (150,75,25)
SALMON = (255, 160, 122)
ORCHID = (218, 112, 214)
TURQUOISE = (0, 134, 139)
BANANA =  (227, 207, 87)

tile_colors = [WHITE, BLUE, RED, GREEN, ORANGE, BLACK_C, YELLOW, MAGENTA, PERU, SALMON, ORCHID, TURQUOISE, BANANA]

def draw_check(x, y, size, color = (255,215,0)): # draws the checks for each level indicating completion
    angle_down = math.radians(45)
    angle_up   = math.radians(65)

    l_wid = size//2
    down_len = 1.0*size
    up_len   = 2.5*size

    bottom_x = x + math.cos(angle_down)*down_len
    bottom_y = y + math.sin(angle_down)*down_len

    pygame.draw.line(screen, color, (x, y), (bottom_x, bottom_y), l_wid)
    pygame.draw.line(screen, color, (bottom_x, bottom_y), (bottom_x + math.cos(angle_up)*up_len, bottom_y - math.sin(angle_up)*up_len), l_wid)


tile_size = 60

outlined_squares = False

mouse_pos = (0,0)
start_mouse_pos = (0,0)
dragging_factor = 2

class Level():

    def __init__(self, square_dim, board_square_dim, tile_size = tile_size):
        """
        square_dim: the number of squares in each same-colored square
        board_square_dim:   (n, m) where n x m is the num_rows x num_columns of squares
        """
        self.board_square_dim = board_square_dim
        self.s = square_dim  # how many tiles make up each side of each square
        self.num_squares = board_square_dim[0] * board_square_dim[1] # total number of colors / same-colored subsquares
        # a list of top left and bottom right tiles coordinate tuples for each square
        self.squares = []
        for row in range(self.board_square_dim[0]):
            self.squares.append([])
            for col in range(self.board_square_dim[1]):
                self.squares[row].append(((row * self.s, col * self.s),(row*self.s + self.s - 1, col*self.s + self.s - 1)))
        print("-"*20)
        print("self.s = ", self.s)
        print("self.board_square_dim = ", self.board_square_dim)
        print("self.squares = ", str(self.squares))

        self.dim = (self.s * board_square_dim[0], self.s * board_square_dim[1])

        self.tile_size = tile_size
        self.margin = (tile_size)//4
        self.haf_mar = self.margin//2
        self.total_d = self.tile_size + self.margin
        self.haf_total_d = self.total_d * 0.5

        self.outline_width = int(.4*self.margin)
        self.outline_length = self.s*self.total_d

        self.level_colors = []
        num_tiles_per_sqr = self.s**2
        for f in range(self.num_squares):
            self.level_colors.extend([tile_colors[f]]*num_tiles_per_sqr) # make a list of the right number of each color

        self.board = []
        all_colors = self.level_colors
        for row in range(self.dim[0]):
            self.board.append([])
            for _ in range(self.dim[1]):
                self.board[row].append(all_colors.pop(random.randint(0, len(all_colors) - 1))) # randomly assign colors to tiles


        self.x = .5*(size[0] - len(self.board[0])*(self.total_d))
        self.y = .5*(size[1] - len(self.board[0])*(self.total_d))

        self.click_tile = None # (row, col)
        self.dragging = False
        self.moving_row = None # int
        self.moving_col = None # int

        self.moving_row_disp = 0
        self.moving_col_disp = 0

        self.aligning_rows = None # list of ints
        self.aligning_cols = None # list of ints

        self.puzzle_solved = False

    def rotate_square(self, selected, direction):
        """
        :param sq: which square to rotate
        :param direction: either 1 for counter-CC, -1 for CC, or 0 for 180 degrees
        :return: void
        """

        if direction != None:
            sqr = self.squares[selected[0]][selected[1]]
            print("Square in question: ", sqr)

            if direction == 1:

                a = [[self.board[row][col] for col in range(sqr[0][1], sqr[1][1] + 1)] for row in
                     range(sqr[0][0], sqr[1][0] + 1)]

                n = len(a)
                for i in range(int(n / 2)):
                    for j in range(i, n - i - 1):
                        tmp = a[i][j]
                        a[i][j] = a[j][n - i - 1]
                        a[j][n - i - 1] = a[n - i - 1][n - j - 1]
                        a[n - i - 1][n - j - 1] = a[n - j - 1][i]
                        a[n - j - 1][i] = tmp

                for row in range(n):
                    for col in range(n):
                        self.board[sqr[0][0] + row][sqr[0][1] + col] = a[row][col]

            elif direction == -1:

                a = [[self.board[row][col] for col in range(sqr[0][1], sqr[1][1] + 1)] for row in
                     range(sqr[0][0], sqr[1][0] + 1)]

                n = len(a)
                for i in range(int(n / 2)):
                    for j in range(i, n - i - 1):
                        tmp = a[i][j]
                        a[i][j] = a[n - j - 1][i]
                        a[n - j - 1][i] = a[n - i - 1][n - j - 1]
                        a[n - i - 1][n - j - 1] = a[j][n - i - 1]
                        a[j][n - i - 1] = tmp

                for row in range(n):
                    for col in range(n):
                        self.board[sqr[0][0] + row][sqr[0][1] + col] = a[row][col]

            elif direction == 0:
                for n in range(2):
                    self.rotate_square(selected, 1)

    def mouse_col(self, x):
        return int((x - self.x)//self.total_d)

    def mouse_row(self, y):
        return int((y - self.y)//self.total_d)

    def set_click_tile(self, mouse_pos):
        x, y = mouse_pos[0], mouse_pos[1]

        if self.x <= x <= self.x + self.dim[1]*self.total_d - self.margin and self.y <= y <= self.y + self.dim[0]*self.total_d - self.margin:
            levels[current].click_tile = (self.mouse_row(y), self.mouse_col(x))

    def collapse_click_tile(self):
        if self.click_tile != None:
            if mouse_pos != start_mouse_pos:
                x_dist = abs(mouse_pos[0] - start_mouse_pos[0])
                y_dist = abs(mouse_pos[1] - start_mouse_pos[1])
                if x_dist > y_dist:
                    self.moving_row = self.click_tile[0]
                # else:
                #     self.moving_col = self.click_tile[1]
                self.click_tile = None
                self.dragging = True

    def reset_dragging(self):
        self.click_tile = None
        self.dragging = False
        self.moving_row = None
        self.moving_col = None
        self.moving_row_disp = 0
        self.moving_col_disp = 0

    def align_nearest(self):

        if self.moving_row != None:
            horiz_displacement = dragging_factor*(mouse_pos[0] - start_mouse_pos[0]) + self.moving_row_disp

            if horiz_displacement > self.haf_total_d:
                self.shift_row(self.moving_row, 1)
            if horiz_displacement < -self.haf_total_d:
                self.shift_row(self.moving_row, -1)
            
        # elif self.moving_col != None:
        #     vert_displacement = dragging_factor*(mouse_pos[1] - start_mouse_pos[1]) + self.moving_col_disp
        #
        #     if vert_displacement > self.haf_total_d:
        #         self.shift_column(self.moving_col, 1)
        #     elif vert_displacement < -self.haf_total_d:
        #         self.shift_column(self.moving_col, -1)

    def get_neighbor(self, tile, disp): # returns the color of nearby tiles
        return self.board[tile[0] + disp[0]][tile[1] + disp[1]]

    def scramble(self):

        self.level_colors = []
        num_tiles_per_sqr = self.s**2
        for f in range(self.num_squares):
            self.level_colors.extend([tile_colors[f]]*num_tiles_per_sqr)

        self.board = []
        all_colors = self.level_colors
        for row in range(self.dim[0]):
            self.board.append([])
            for col in range(self.dim[1]):
                self.board[row].append(all_colors.pop(random.randint(0, len(all_colors) - 1)))


    def shift_column(self, column, dir = 1):

        if dir == 1:
            last = self.board[self.dim[0] - 1][column]
            for row in range(self.dim[0] - 1, 0, -1):
                self.board[row][column] = self.board[row - 1][column]
            self.board[0][column] = last 

        elif dir == -1:
            first = self.board[0][column]
            for row in range(self.dim[0] - 1):
                self.board[row][column] = self.board[row + 1][column]
            self.board[self.dim[0] - 1][column] = first 

    def shift_row(self, row, dir = 1):

        if dir == 1:
            last = self.board[row][self.dim[1] - 1]
            for column in range(self.dim[1] - 1, 0, -1):
                self.board[row][column] = self.board[row][column - 1]
            self.board[row][0] = last

        elif dir == -1:
            first = self.board[row][0]
            for column in range(self.dim[1] - 1):
                self.board[row][column] = self.board[row][column + 1]
            self.board[row][self.dim[1] - 1] = first

    def set_solved(self):

        i = 0
        for sqr_row in range(self.board_square_dim[0]):
            for sqr_col in range(self.board_square_dim[1]):
                for row in range(self.s*sqr_row, self.s*(sqr_row + 1)):
                    for col in range(self.s*sqr_col, self.s*(sqr_col + 1)):
                        if self.board[row][col] != tile_colors[i]:
                            self.puzzle_solved = False
                            return
                i += 1

        self.puzzle_solved = True

    def draw_board(self):

        if not outlined_squares:
            i = 0
            for row in range(self.board_square_dim[0]):
                for col in range(self.board_square_dim[1]):

                    SHADE = list(tile_colors[i])
                        
                    for f in range(len(SHADE)):
                        SHADE[f] = (2*SHADE[f])/3
                        if SHADE[f] > 255:
                            SHADE[f] = 255

                    NEW = tuple(SHADE)

                    start_x = self.x + col*self.outline_length - self.haf_mar
                    start_y = self.y + row*self.outline_length - self.haf_mar

                    side_l = self.outline_length

                    pygame.draw.rect(screen, NEW, [start_x, start_y, side_l, side_l])

                    i += 1

        if self.dragging:
            # if self.moving_col != None:
            #     column = self.moving_col
            #
            #     vert_displacement = dragging_factor*(mouse_pos[1] - start_mouse_pos[1]) + self.moving_col_disp
            #
            #     for row in range(len(self.board)): # draw each tile in column being dragged
            #         left = self.x + column*self.total_d
            #         top = self.y + row*self.total_d + vert_displacement
            #
            #         over = self.tile_size
            #         down = self.tile_size
            #
            #         TILE_COLOR = self.board[row][column]
            #
            #         if top > self.y + self.dim[0]*self.total_d - self.haf_mar: # if top of tile is below bottom edge
            #             self.moving_col_disp += -self.total_d
            #
            #             self.shift_column(column, 1)
            #
            #             self.draw_board()
            #             break
            #
            #         elif top < self.y - self.tile_size - self.haf_mar: # if top of tile is above top edge
            #             self.moving_col_disp += self.total_d
            #
            #             self.shift_column(column, -1)
            #
            #             self.draw_board()
            #             break
            #
            #         if row == self.dim[0] - 1:
            #             if vert_displacement > self.haf_mar:
            #                 down = self.tile_size - vert_displacement + self.haf_mar
            #
            #                 pygame.draw.rect(screen, TILE_COLOR,[left, self.y - self.haf_mar, over, vert_displacement - self.haf_mar])
            #
            #         elif row == 0:
            #             if vert_displacement < -self.haf_mar:
            #                 top = self.y - self.haf_mar
            #                 down = self.tile_size + vert_displacement + self.haf_mar
            #
            #                 pygame.draw.rect(screen, TILE_COLOR,[left, self.y + (self.dim[0])*self.total_d + vert_displacement, over, -vert_displacement - self.haf_mar])
            #
            #             elif vert_displacement < 0:
            #                 top = self.y + vert_displacement
            #                 down = self.tile_size
            #
            #         pygame.draw.rect(screen, TILE_COLOR,[left, top, over, down], 0)

            if self.moving_row != None:
                row = self.moving_row

                horiz_displacement = dragging_factor*(mouse_pos[0] - start_mouse_pos[0]) + self.moving_row_disp

                for column in range(len(self.board[0])):
                    left = self.x + column*self.total_d + horiz_displacement
                    top = self.y + row*self.total_d 

                    over = self.tile_size
                    down = self.tile_size

                    TILE_COLOR = self.board[row][column]

                    if left > self.x + self.dim[1]*self.total_d - self.haf_mar:
                        self.moving_row_disp += -self.total_d

                        self.shift_row(row, 1)

                        self.draw_board()
                        break

                    elif left < self.x - self.tile_size - self.haf_mar:
                        self.moving_row_disp += self.total_d

                        self.shift_row(row, -1)

                        self.draw_board()
                        break

                    if column == self.dim[1] - 1:
                        if horiz_displacement > self.haf_mar:
                            over = self.tile_size - horiz_displacement + self.haf_mar

                            pygame.draw.rect(screen, TILE_COLOR,[self.x - self.haf_mar, top, horiz_displacement - self.haf_mar, down])

                    elif column == 0:
                        if horiz_displacement < -self.haf_mar:
                            left = self.x - self.haf_mar
                            over = self.tile_size + horiz_displacement + self.haf_mar

                            pygame.draw.rect(screen, TILE_COLOR,[self.x + (self.dim[1])*self.total_d + horiz_displacement, top, -horiz_displacement - self.haf_mar, down])

                        elif horiz_displacement < 0:
                            left = self.x + horiz_displacement
                            over = self.tile_size

                    pygame.draw.rect(screen, TILE_COLOR,[left, top, over, down], 0)

        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                if not(row == self.moving_row or column == self.moving_col): # only draw if not being dragged

                    left = self.x + column*self.total_d
                    top = self.y + row*self.total_d

                    TILE_COLOR = self.board[row][column]
                    pygame.draw.rect(screen, TILE_COLOR,[left, top, self.tile_size, self.tile_size], 0)

        if outlined_squares:
            i = 0
            for row in range(self.board_square_dim[0]):
                for col in range(self.board_square_dim[1]):

                    OUTLINE_COLOR = tile_colors[i]

                    
                    start_x = self.x + col*self.outline_length - self.outline_width/2
                    start_y = self.y + row*self.outline_length - self.outline_width/2

                    end_x = start_x + self.outline_length - self.haf_mar
                    end_y = start_y + self.outline_length - self.haf_mar

                    pygame.draw.line(screen, OUTLINE_COLOR, (start_x, start_y), (start_x, end_y), self.outline_width)
                    pygame.draw.line(screen, OUTLINE_COLOR, (start_x, end_y), (end_x, end_y), self.outline_width)
                    pygame.draw.line(screen, OUTLINE_COLOR, (end_x, end_y), (end_x, start_y), self.outline_width)
                    pygame.draw.line(screen, OUTLINE_COLOR, (end_x, start_y), (start_x, start_y), self.outline_width)

                    i += 1


levels = [] # for storing every Level object. The data in each level object changes as player plays each level.
levels_const = {} # for storing a permanent copy of every level object

level_index = 0
test_ind = 0
for square_size in range(2, 5):
    for row_num in range(1, 4):
        for col_num in range(row_num, 4):
            if not(col_num == row_num == 1):
                levels_const[level_index] = Level(square_dim = square_size, board_square_dim = (row_num, col_num))
                #TESTING
                if square_size == 3 and row_num == 1 and col_num == 2:
                    test_ind = level_index

                level_index += 1


"""
levels_const[1] = Level(dim = (3, 6), square_dim = 3, squares = [(0,0),(0,2)])
levels_const[0] = Level(dim = (9, 9), square_dim = 3, squares = [(row, col) for col in range(0,9,3) for row in range(0,9,3)] )
levels_const[2] = Level(dim = (4, 4), square_dim = 2, squares = [(0,0),(0,2),(2,0),(2,2)], tile_size = 50)
"""

for index in levels_const:
    levels.append(None)
    levels[index] = copy.deepcopy(levels_const[index])

current = test_ind # index of current level
number_of_levels = len(levels)

rot_dir = None
selected = (0,1)
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():

        if event.type == MOUSEBUTTONDOWN:
            start_mouse_pos = pygame.mouse.get_pos()
            levels[current].set_click_tile(start_mouse_pos)

        if event.type == MOUSEBUTTONUP:
            levels[current].align_nearest()
            levels[current].reset_dragging()

        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE: # quit game
                pause = False
                done = True

            if event.key == pygame.K_p:
                pause = True

            while pause:

                for event in pygame.event.get():
                     if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_p:
                            pause = not pause

                        if event.key == pygame.K_ESCAPE: # quit game
                            pause = not pause
                            done = True

            # Square rotation
            if event.key == pygame.K_1:
                rot_dir = 1  # counter-clockwise
            elif event.key == pygame.K_2:
                rot_dir = -1  # clockwise

            # Square rotation
            if event.key == pygame.K_1:
                selected = (0, 0)
                rot_dir = 1  # counter-clockwise
            elif event.key == pygame.K_2:
                selected = (0, 0)
                rot_dir = -1  # clockwise
            elif event.key == pygame.K_9:
                selected = (0, 1)
                rot_dir = 1  # counter-clockwise
            elif event.key == pygame.K_0:
                selected = (0, 1)
                rot_dir = -1  # clockwise

            if event.key == pygame.K_d:
                current = (current + 1)%number_of_levels
            if event.key == pygame.K_s:
                current = (current - 1)%number_of_levels
            if event.key == pygame.K_p or event.key == pygame.K_a:
                levels[current].scramble()

 
    # --- Game logic should go here
    if rot_dir != None: # it is crucial that this is stored before .rotate_square(rot_dir) below so that square info for animation is not destroyed
        pass
        # levels[current].rotating.append(RotatingSquare(levels[current], rot_dir))

    levels[current].set_solved()


    # First, clear the screen to whatever. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BACKGROUND)

    # --- Drawing code should go here


    mouse_pos = pygame.mouse.get_pos()
    levels[current].collapse_click_tile()

    levels[current].draw_board()

    if levels[current].puzzle_solved:
        draw_check(10, 300, 40)

    levels[current].rotate_square(selected, rot_dir)  # sets new board tile values instantaneously
    rot_dir = None

 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()