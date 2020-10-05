import time
import Timer
import numpy as np
import random as rd
from tkinter import *

start = time.perf_counter()

# Ideas:
# How about not assigning anything before the first click since you can't hit a mine on the first click?
# 

class Block:
    def __init__(self, value, position):
        self.value = value # This is the distance from the neighbor mine
        self.position = position # This should be a tuple 
        self.is_mine = value // 9 # True if the value is nine and false if its's anything else
        self.button = self.create_button()


    def create_button(self):
        i,j = self.position
        button = Button(root, text=f'{self.value}', pady=10, padx=10, command=lambda: blockClick((i,j)), fg = 'black', bg='grey')
        button.grid(row=i+2,column=j)

        return button

    def change_button_text(self):
        self.button.config(text=f'{self.value}')
        return 


def set_mines():
    for i in range(mine_num):
        random_row = rd.randint(0,8)
        random_column = rd.randint(0,8)
        if block_lst[random_row][random_column].value != 0:
            while block_lst[random_row][random_column].value == 0:
                random_row = rd.randint(0,8)
                random_column = rd.randint(0,8)

                block_lst[random_row][random_column].value = 9
        else:
            block_lst[random_row][random_column].value = 9

def check_num_mines(row, column):
    # This function checks the surrounding blocks
    # 0,0 0,1 0,2
    # 1,0 1,1 1,2
    # 2,0 2,1 2,2
    count = 0
    
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            # the condition: should be inside the array (field) and cannot be the block itself
            if ((i >= 0 and i <= 8 and j >= 0 and j <= 8) and not (i == row and j == column)):
                if(block_lst[i][j] == 9):
                    count += 1
    return count

def set_distance(row, col):
    print("In:", i,j)
    if block_lst[row][col] != 9:
        block_lst[row][col] = check_num_mines(row,col)
        
    return block_lst[row][row].value

def blockClick(pos):
    global is_first_click
    row, col = pos
    if is_first_click:
        if block_lst[row][col].value == 9:
            block_lst[row][col].value = 0
            print(f'\n\n{block_lst[row][col].value}')
            update_field()
        sw.Start()

    # Check the surrounding blocks
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if not (i == row and j == col) and (i >= 0 and i <= 8 and j >= 0 and j <= 8):
                pass

    

def update_field():
    global block_lst
    for i in range(9):
        for j in range(9):
            block_lst[i][j].value = set_distance(i,j)
            print(block_lst[i][j].value, end=', ')
            block_lst[i][j].change_button_text()
        print()
    print()


root = Tk()

root.configure(background='#C0C0C0')
root.title("MineSweeper")   
root.geometry("315x450")

sw = Timer.StopWatch(root)
sw.grid(row=0, column=0, columnspan =5)


stop_button = Button(root, text='Stop', command=exit)
stop_button.grid(row=12, column=2)



# When you click, change the below boolean
global is_first_click
is_first_click = True

# generate a random number of mines
mine_num = rd.randint(5,8)

# sets the mines randomly!
set_mines()

# Blocks lists to store their data
global block_lst
block_lst = [[],[],[],[],[],[],[],[],[]]
for i in range(9):
    for j in range(9):
        
        print("Out:", i,j)
        block_lst[i].append(Block(field[i][j], (i,j)))
        print(block_lst)
        set_distance(i,j)
        
        
update_field()



stop = time.perf_counter()
# print("\n\n\n\n\n", stop - start)


root.mainloop()