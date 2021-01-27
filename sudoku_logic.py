import pygame
import time
import random
import csv
import numpy as np
from itertools import islice
import os


# read from CSV, generate board for game
with open('sudoku.csv', mode='r') as csv_file:
    data = csv.reader(csv_file)
    chosen_row = random.choice(list(data))

sudoku_list = list(map(int, str(chosen_row[0])))
# Input list initialization 

# list of length in which we have to split 
length_to_split = [9,9,9,9,9,9,9,9,9]   
sodoku_input = iter(sudoku_list) 
board = [list(islice(sodoku_input, elem)) 
          for elem in length_to_split] 


def print_board(board):
    """Function to print board"""
    for i in range(len(board)):
        if i % 3 ==0 and i !=0:
            print("-------------------")
        for j in range(len(board)):
            if j % 3 == 0 and j !=0:
                print("|", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def empty(board):
    """Defines an empty board"""
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i,j)
    else:
        return "full"

def valid(board, number, position):
    """Checks validity of number passed to board, called by solve function"""

    # check row
    if board[0][1] == 0:
        pass
    for i in range(len(board[0])):
    # if number does not exist in row with the exception of the posi tion for which the new number is placed
        if board[position[0]][i] == number and position[1] != i:
            return False
    
    # check column
    for i in range(len(board)):
    # if number does not exist in row with the exception of the position for which the new number is placed
        if board[i][position[1]] == number and position[0] != i:
            return False

    # check box
    # represent each box through range of 3 
    box_row = position[0] // 3
    box_column = position[1] // 3
    
    for i in range(box_row *3, box_row* 3 + 3):
    # if number does not exist in row with the exception of the position for which the new number is placed
        for j in range(box_column * 3, box_column * 3 + 3):
            if board[i][j] == number and (i , j) != position:
                return False
    return True

def solve(board):
    """Function to solve board, will validate selections with valid function"""

    find = empty(board)
    if empty(board) == "full":
        return True
    else:
        row, column = find

    
    for i in range(1,10):
        if valid(board, i, (row, column)):
            board[row][column] = i 
            pygame.draw.rect(screen, RED, (column*105, row*105, 110, 110))
            text = font_words.render("Checking....", True, RED, BLACK)
            textRect = text.get_rect()
            textRect.center = (1075, 100)
            screen.blit(text, textRect)
            draw_grid()
            clock.tick(15)
            pygame.display.update()
            


            if solve(board):
                pygame.draw.rect(screen, BLACK, (0, 0, 955,955))
                text = font_words.render("Puzzle complete!!", True, RED, BLACK)
                textRect = text.get_rect()
                textRect.center = (1075, 100)
                screen.blit(text, textRect)
                pygame.display.flip()

                return True
            
            #reset if not valid, repeat
            board[row][column] = 0

    return False


##########################GAMEGUI#######################

#colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#settings for display
s_width = 1200
s_height = 955
screen = pygame.display.set_mode([s_width, s_height])
pygame.display.set_caption("Sudoku")
user_input = []
x = 100
y = 200
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#grid size
g_width = 900//9
g_height = 900//9
g_margin = 5
g_center = (900//9 + 15)


#game font
pygame.font.init()
font_number = pygame.font.SysFont("arial", 40)
font_words = pygame.font.SysFont("arial", 20)
font_words2 = pygame.font.SysFont("arial", 30)


def draw_grid():
    """Implements grid, complete with border. Will insert initial values from board variable"""
    for row in range(9):
        for column in range(9):
            #draw alternating (blue, white) grids for UI
            if ((column <3 or column>5) and (row >2 and row <=5) or ((column>2 and column<=5) and (row<3 or row>5))):
                color = WHITE
            else:
                color = BLUE
            pygame.draw.rect(screen, color, [(g_margin + g_width) * column + g_margin, (g_margin+g_height)
            * row + g_margin, g_width, g_height])
        #insert board values
    for row in range(9):
        for column in range(9):
            if board[row][column] != 0:
                text_number = font_number.render(str(board[row][column]), 1, BLACK)
                screen.blit(text_number, [(g_margin + g_width) * column + g_margin*8, (g_margin+g_height)
                * row + g_margin*7, g_width, g_height])

def highlight_cell(pos1, pos2):
    """Function to highlight selected cell, if empty, or able to be deleted"""
    
    clock.tick(60)
 
    color = BLUE
    column = pos1//105
    row = pos2//105
    if (column, row) in user_input:
        #to highlight previously entered items
        clicked = True
        if clicked == True:
            screen.fill(BLACK)
            clicked = False
        pygame.draw.rect(screen, RED, (column*105, row*105, 110, 110))
        pygame.display.update()

    if board[row][column] != 0 and (column, row) not in user_input:
        #will not highlight default board values
        pygame.draw.rect(screen, BLACK, (0, 0, 970,970))
        text = font_words.render("Please select an empty space", True, RED, BLACK)
        textRect = text.get_rect()
        textRect.center = (1075, 100)
        screen.blit(text, textRect)
        pygame.display.flip()
        clicked = False
    if board[row][column] == 0:
        #highlight empty box
        clicked = True
        if clicked == True:
            screen.fill(BLACK)
            clicked = False
        pygame.draw.rect(screen, RED, (column*105, row*105, 110, 110))
    
def insert_value(val, row, column):
    """Calls valid function to check validity of user input, will update board as needed"""
    
    if valid(board, val, (column, row)) == True and board[column][row] < 1:
        #if empty box, update with user input if valid. Append value to user_input list for later use
        #display message
        pygame.draw.rect(screen, BLACK, (0, 0, 970,970))
        text = font_words.render("Input recorded", True, RED, BLACK)
        textRect = text.get_rect()
        textRect.center = (1075, 150)
        screen.blit(text, textRect)
        
        board[column][row] = val
        user_input.append((row,column))
        pygame.display.flip()
        pygame.display.update()        
        
    if val == 0:
        board[column][row] = val
        screen.fill(BLACK)
        pygame.display.update()
        
    if valid(board, val, (column, row)) == False:
        #if not deemed valid, raise message
        pygame.draw.rect(screen, BLACK, (0, 0, 970,970))
        text = font_words.render("Not a valid move!", True, RED, BLACK)
        textRect = text.get_rect()
        textRect.center = (1075, 150)
        screen.blit(text, textRect)
        pygame.display.flip()
        clicked = False
  

def delete_user_input():
    #removes input for backtracking algorithm to complete appropriately
    for (row, column) in user_input:
        board[column][row] = 0


pygame.init()
clock = pygame.time.Clock()

#game loop

screen.fill(BLACK)
while True:
    draw_grid()

    pygame.display.update()
    pos = pygame.mouse.get_pos() 

    #instructions
    text = font_words.render("Select a square, followed by ", True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (1075, 500)
    screen.blit(text, textRect)
    text = font_words.render("typing a number.", True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (1075, 520)
    screen.blit(text, textRect)
    text = font_words.render("DEL = Delete", True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (1075, 550)
    screen.blit(text, textRect)

    #solve button
    button_light =  (170,170,170)
    button_dark = (100,100,100)
    button = pygame.Rect(1000, 750, 150, 50) 
    pygame.draw.rect(screen, (170,170,170), button)

    text = font_words2.render("Solve", True, WHITE)
    textRect = text.get_rect()
    textRect.center = (1075, 775)
    screen.blit(text, textRect)

    if button.collidepoint(pos):
        pygame.draw.rect(screen, (100,100,100), button)
        text = font_words2.render("Solve", True, WHITE)
        textRect = text.get_rect()
        textRect.center = (1075, 775)
        screen.blit(text, textRect)

    #user input
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(pos) == True:
            delete_user_input()
            solve(board)
        if event.type == pygame.MOUSEBUTTONDOWN and pos[0] < 950:
            highlight_cell(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                if (pos[0]//105, pos[1]//105) in user_input:
                    insert_value(0, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_1: 
                val = 1
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_2: 
                val = 2
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_3: 
                val = 3
                insert_value(val, pos[0]//105, pos[1]//105)    
            if event.key == pygame.K_4: 
                val = 4
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_5: 
                val = 5
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_6: 
                val = 6 
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_7: 
                val = 7
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_8: 
                val = 8
                insert_value(val, pos[0]//105, pos[1]//105)
            if event.key == pygame.K_9: 
                val = 9
                insert_value(val, pos[0]//105, pos[1]//105)
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.display.update()
