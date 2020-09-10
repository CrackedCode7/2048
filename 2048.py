import random
import numpy as np
import tkinter as tk

def update_colors(mat):
    for i in range(4):
        for j in range(4):
            if int(entries["row" + str(i+1) + "col" + str(j+1)].get()) == 2:
                entries["row" + str(i+1) + "col" + str(j+1)]['bg'] = 'magenta'

def new_game():

    # Create matrix with zeros
    mat = np.zeros((4,4), dtype=int)

    # Choose random number to serve as check for inserting 4 vs. 2
    global insert_four_num
    insert_four_num = random.randint(0,9)
    
    # Add two numbers to begin the game
    add_new(mat)
    add_new(mat)

    # Print initial matrix
    print(mat)

    return mat

def add_new(mat):

    # Pick two random numbers to insert
    r = random.randint(0, 3) 
    c = random.randint(0, 3)

    # Loop until r and c give an entry that is zero
    while(mat[r][c] != 0): 
        r = random.randint(0, 3) 
        c = random.randint(0, 3) 
  
    # Place a 2 or 4 at the empty cell
    insert_four_check = random.randint(0,9)

    if insert_four_check == insert_four_num:
        mat[r][c] = 4
    else:
        mat[r][c] = 2

def get_current_state(mat): 

    # If a cell contains 2048, print that the player wins
    for i in range(4): 
        for j in range(4): 
            if(mat[i][j]== 2048): 
                return 'WON'
  
    # If there is still an empty cell, print that the game is not over 
    for i in range(4): 
        for j in range(4): 
            if(mat[i][j]== 0): 
                return 'GAME NOT OVER'
  
    # If no cell is empty, but a move can be made, print that the game is not over
    for i in range(4): 
        for j in range(4): 
            if(mat[i][j]== mat[i + 1][j] or mat[i][j]== mat[i][j + 1]): 
                return 'GAME NOT OVER'
  
    # Else print that the player has lost the game 
    return 'LOST'

def compress(mat):

    # Create variable to check if there were any changes
    changed = False
  
    # Create empty matrix
    new_mat = [] 
  
    # with all cells empty 
    new_mat = np.zeros((4,4), dtype=int) 
          
    # Shift all entries to extreme left
    for i in range(4): 
        pos = 0
        for j in range(4):
            if(mat[i][j] != 0): 
                new_mat[i][pos] = mat[i][j]  
                if(j != pos):
                    changed = True
                pos += 1

    return new_mat, changed 

def merge(mat):

    # Create variable to check if there were any changes
    changed = False

    # Merge adjacent cells
    for i in range(4):
        for j in range(3): 
            if(mat[i][j] == mat[i][j + 1] and mat[i][j] != 0): 
                mat[i][j] = mat[i][j] * 2
                mat[i][j + 1] = 0

                changed = True
  
    return mat, changed

def reverse(mat): # Reverse the content of each row (to move right)

    new_mat =[] 
    for i in range(4): 
        new_mat.append([]) 
        for j in range(4): 
            new_mat[i].append(mat[i][3 - j]) 
    return new_mat 
 
def transpose(mat): # Transpose matrix (used in moving up/down)

    new_mat = [] 
    for i in range(4): 
        new_mat.append([]) 
        for j in range(4): 
            new_mat[i].append(mat[j][i]) 
    return new_mat 
  
def move_left(grid): # Define function that runs when the player moves left

    # First compress the grid 
    new_grid, changed1 = compress(grid) 
  
    # Then merge the cells
    new_grid, changed2 = merge(new_grid) 
    changed = changed1 or changed2 
  
    # Compress again after merging
    new_grid, _ = compress(new_grid) 

    return new_grid, changed 
  
def move_right(grid): # Define function that runs when the player moves right

    # Same as move left, but need to reverse
    new_grid = reverse(grid) 
  
    # Then move left 
    new_grid, changed = move_left(new_grid) 
  
    # Then reverse again
    new_grid = reverse(new_grid)

    return new_grid, changed 

def move_up(grid): # Define function that runs when the player moves up

    # Same as move left, but needs transposed 
    new_grid = transpose(grid) 
    
    # Then move left
    new_grid, changed = move_left(new_grid) 
  
    # Then transpose again
    new_grid = transpose(new_grid)

    return new_grid, changed 

def move_down(grid): # Define function that runs when the player moves down

    # Same as move right, but needs transposed 
    new_grid = transpose(grid) 
  
    # Then move right 
    new_grid, changed = move_right(new_grid) 
  
    # Then transpose again
    new_grid = transpose(new_grid)

    return new_grid, changed

''' BEGIN CODE TO RUN THE PROGRAM '''

# GUI Stuff

def set_entries():
    for i in range(4):
        for j in range(4):
            entries["row" + str(i+1) + "col" + str(j+1)].delete(0, tk.END)
            entries["row" + str(i+1) + "col" + str(j+1)].insert(0, mat[i][j])

root = tk.Tk()

entries = {}
for i in range(4):
    for j in range(4):
        entries["row" + str(i+1) + "col" + str(j+1)] = tk.Entry(root, justify='center', font=('arial', 30), bg='Red')
        entries["row" + str(i+1) + "col" + str(j+1)].grid(row=i, column=j, ipady=85)

mat = new_game()
set_entries()
update_colors(mat)

def move_up_command():

    global mat
    current_mat = list(mat)
        
    # Move up
    mat, flag = move_up(mat)
    if flag == False:
        print("No change was made, try another move")
        mat = list(current_mat)
        for line in mat:
            print(line)

    # Get the current state and print it 
    status = get_current_state(mat) 
    print(status) 

    # If game not over then continue
    if(status == 'GAME NOT OVER'): 
        add_new(mat)

        for line in mat:
            print(line)
        
        set_entries()

    # Else break the loop  
    else: 
        root.destroy()

def move_down_command():

    global mat
    current_mat = list(mat)

    # Move down
    mat, flag = move_down(mat)
    if flag == False:
        print("No change was made, try another move")
        mat = list(current_mat)
        for line in mat:
            print(line)
        #continue

    # Get the current state and print it
    status = get_current_state(mat) 
    print(status)

    # If game not over then continue
    if(status == 'GAME NOT OVER'): 
        add_new(mat)
    
        for line in mat:
            print(line)
        
        set_entries()
    
    # Else break the loop
    else: 
        root.destroy()

def move_left_command():

    global mat
    current_mat = list(mat)

    # Move left
    mat, flag = move_left(mat)
    if flag == False:
        print("No change was made, try another move")
        mat = list(current_mat)
        for line in mat:
            print(line)
        #continue

    # Get the current state and print it
    status = get_current_state(mat) 
    print(status)

    # If game not over then continue
    if(status == 'GAME NOT OVER'): 
        add_new(mat)
    
        for line in mat:
            print(line)
        
        set_entries()
    
    # Else break the loop
    else: 
        root.destroy()

def move_right_command():

    global mat
    current_mat = list(mat)

    # Move right
    mat, flag = move_right(mat)
    if flag == False:
        print("No change was made, try another move")
        mat = list(current_mat)
        for line in mat:
            print(line)
        #continue

    # Get the current state and print it
    status = get_current_state(mat) 
    print(status)

    # If game not over then continue
    if(status == 'GAME NOT OVER'): 
        add_new(mat)
    
        for line in mat:
            print(line)
        
        set_entries()
    
    # Else break the loop
    else: 
        root.destroy()

up_button = tk.Button(root, command=move_up_command, text="Move Up")
up_button.grid(row=4, column=1)

down_button = tk.Button(root, command=move_down_command, text="Move Down")
down_button.grid(row=6, column=1)

left_button = tk.Button(root, command=move_left_command, text="Move Left")
left_button.grid(row=5, column=0)

right_button = tk.Button(root, command=move_right_command, text="Move Right")
right_button.grid(row=5, column=2)

root.mainloop()
