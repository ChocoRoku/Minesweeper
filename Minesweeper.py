from tkinter import *
import Timer
import random as rnd
import time

class Block:
    def __init__(self, value, position):
        self.value = value # This is the distance from the neighbor mine
        self.position = position # This should be a tuple 
        self.is_mine = bool(value // 9) # True if the value is nine and false if its's anything else
        self.button = self.create_button()
        self.is_revealed = False 


    def create_button(self):
        i,j = self.position
        button = Button(root, text='  ', pady=10, padx=10, command=lambda: blockClick((i,j)), fg = 'black', bg='grey')
        button.grid(row=i+2,column=j)

        return button

    def change_button_text(self):
        self.button.config(text=f'{self.value}')
        self.is_revealed = True
        return self.value

def interface(root):
    root.configure(background='#C0C0C0')
    root.title("MineSweeper")   
    root.geometry("315x450")
    global sw
    sw = Timer.StopWatch(root)
    sw.grid(row=0, column=0, columnspan =5)

    global total_num_mines
    mine_num_label = Label(root, text=f'The Number of mines: {total_num_mines}')
    mine_num_label.grid(row=0, column = 5, columnspan=4)

    exit_button = Button(root, text='Exit', command=exit)
    exit_button.grid(row=12, column=2)

def print_field():
    global field
    for i in range(9):
        for j in range(9):
            print(field[i][j].value, end=', ')
        print()

def update_field():
    global field
    for i in range(9):
        for j in range(9):
            field[i][j] = Block(field[i][j].value, field[i][j].position)

def check_num_of_mines(row, column):
    count = 0

    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if (not (i == row and j == column)) and (8 >= i >= 0 and 0 <= j <= 8) and (field[i][j].is_mine):
                count += 1
            
    return count


def blockClick(position):
    global is_first_click
    global field
    row, column = position
    if is_first_click:
        # Build the field:
        
        # Plant Mines in the field:
        # Number of mines
        num_mine = 10
        while num_mine:
            random_spot = (rnd.randint(0,8), rnd.randint(0,8))
            
            while random_spot == position or field[row][column].is_mine:
                # keep generating another random block until a free space found!
                random_spot = (rnd.randint(0,8), rnd.randint(0,8))
            # Plant a mine 
            field[random_spot[0]][random_spot[1]].value = 9

            # Throwing the planted mine away
            num_mine -= 1
        update_field()

        # Put Hints:
        for i in range(9):
            for j in range(9):
                if not field[i][j].is_mine:
                    #check surrounding blocks
                    field[i][j].value = check_num_of_mines(i,j)
        global sw
        sw.Start()
        is_first_click = False
        update_field()    
    else:
        # 2nd, 3rd, 4th, (N)th click
        if field[row][column].is_mine:
            print('You lose!')
        elif field[row][column].value == 0:
            reveal_surround(row, column)


    
    field[row][column].change_button_text()

def reveal_surround(row, column, surround_blocks=[], trash_lst=[], start=0):
    
    # if start==0:
    #     start = time.perf_counter()

    if surround_blocks:
        # if the surround_blocks list is empty..
        trash_lst.append(surround_blocks[0])
        surround_blocks.pop(0)

        
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if((8 >= i >= 0 and 0 <= j <= 8) and (field[i][j] not in trash_lst)):
                if ((not (i == row and j == column)) or field[i][j].is_mine):
                    if ((field[i][j].value == 0) and (field[i][j] not in surround_blocks)):
                        surround_blocks.append(field[i][j])
                    field[i][j].change_button_text()
    # if the list is empty by here, then stop the function!
    if surround_blocks:
        # Let's look down here later....
        #IMPORTANT!!
        reveal_surround(surround_blocks[0].position[0], surround_blocks[0].position[1], surround_blocks)
        

        # in case you wanted to test the function
        # print("Time elapsed:", time.perf_counter() - start)




root = Tk()

global total_num_mines
total_num_mines = 10

# The interface
interface(root)


# field is where we store blocks in a 2D array
global field
field = [[],[],[],[],[],[],[],[],[]]
for i in range(9):
    for j in range(9):
        # Let's just add empty blocks for starters
        # default value: 0 
        temp_block = Block(0, (i,j))
        field[i].append(temp_block)




is_first_click = True


root.mainloop()