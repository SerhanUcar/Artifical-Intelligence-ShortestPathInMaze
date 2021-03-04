import tkinter as tk
from time import time

############################### Hasan Serhan Uçar and Berhan Kurt ########################################

'''
    @screen = this variable represent the screen where we are going to draw the maze
    @canvas = help us to draw our maze
'''
screen=tk.Tk()
screen.title("BFS Algorithm")
draw=tk.Canvas(width=400, height=800, background="black")
draw.grid(column=0, row=0)

maze = ([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [ -1,-2,-1,-1,0,0,0,0,-1,0,0,0,-1,0,-1,0,0,0,0,-3,0,-1,-1],
    [ 0,0,0,-1,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,-1,-1,-1,0,-1,-1],
    [ 0,-1,0,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,0,-1,0,-1,-1],
    [ 0,-1,-1,0,-1,0,-1,0,0,0,-1,0,-1,0,0,0,-1,-1,0,-1,0,-1,-1],
    [ 0,-1, 0,0,-1,0,-1,0,-1,-1,-1,0,-1,0,-1,0,0,0,0,-1,0,-1,-1],
    [ -1,-1,0,-1,-1,-1,-1,0,-1,0,-1,0,-1,0,-1,-1,-1,-1,0,-1,-1,-1,-1],
    [ -1,-1,0,-1,0,0,0,0,-1,0,0,0,-1,0,0,-1,-1,-1,0,-1,0,-1,-1],
    [ -1,-1,0,-1,0,-1,-1,-1,-1,0,-1,-1,-1,-1,0,-1,0,-1,0,-1,0,-1,-1],
    [ -1,-1,0,-1,0,0,0,0,-1,0,0,0,0,0,0,-1,0,-1,0,-1, 0,-1,-1],
    [ -1,-1,0,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [ -1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,-1],
    [ -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])

# This function returns the value that is save on the position that is required
'''
    @value = value saved in that position
'''
def getValue(x, y):
    value = maze[x][y]
    return value
    
# This returns the position where the @num asked is located respect the exes x and y
'''
    @num = the number that is needed to be found
    @coordenades = the location where the number is
'''
def getPosition(num):
    coordenades = [0,0]
    for i in range(13):
        for j in range(23):
            if(maze[i][j] == num):
                coordenades = [i,j]
                break

    return coordenades

# We need this function to see if we have arrived to the beggining to the maze, to calculate the best way
'''
    @beggining = is a boolean variable that lets us know if the beggining has been found
    @valueLeft = value which is stored on the left of the cell specified
    @valueRight = value which is stored on the right of the cell specified
    @valueUp = value which is stored above the cell specified
    @valueDown = value which is stored behind the cell specified
    -2 == START POINT
'''
def arrivedBeggining(x,y):
    beggining = False
    valueLeft = getValue(x-1,y)
    valueRight = getValue(x+1,y)
    valueUp = getValue(x,y-1)
    valueDown = getValue(x,y+1)

    if (valueLeft == -2) or (valueRight == -2) or (valueUp == -2) or (valueDown == -2):
        beggining = True

    return beggining


# This function is used to find wich nearCells can be visited and that ones that can be visited are saved in an @nearCells
'''
    @nearCells[] =  array that saves wich places can be visited and wich one can not, the last position is the @cont 
    @cont = represents which number represents each neightbour cell
    @x = where is located on the exe x the cell which we want to know its nearCells
    @y = where is located on the exe x the cell which we want to know its nearCells
    @i = which position on the array is going to be saved each cell
'''
def getArrayNeightbours(x, y, cont,maze):
    nearCells = [0] * 5
    valueLeft = getValue(x-1,y)
    valueRight = getValue(x+1,y)
    valueUp = getValue(x,y-1)
    valueDown = getValue(x,y+1)

    i = 0
    if valueUp == 0:
        cont+=1
        nearCells[i] = cont
        setValue(x,y-1,cont,maze)
        i+=1
        nearCells[4] = cont
    if valueRight == 0:
        cont+=1
        nearCells[i] = cont
        setValue(x+1,y,cont,maze)
        i+=1
        nearCells[4] = cont
    if valueDown == 0:
        cont+=1
        nearCells[i] = cont
        setValue(x,y+1,cont,maze)
        i+=1
        nearCells[4] = cont
    if valueLeft == 0:
        cont+=1
        nearCells[i] = cont
        setValue(x-1,y,cont,maze)
        i+=1
        nearCells[4] = cont    
    nearCells = removeCeros(nearCells)
    return nearCells


# We need this to going little by little putting numbers along the maze
'''
    @number = number that is going to be save in the @x and @y specified
'''
def setValue(x, y, number, maze):
    maze[x][y] = number

# We delete the ceros of the array nearCells to avoid mistaked, first we check how many 0s are there, then we delete them
'''
    @times = how many times the element 0 is stored
'''
def removeCeros(nearCells):
    times = nearCells.count(0)
    for i in range(times):
        nearCells.remove(0)

    return nearCells

# Algorithm that looks for the GOAL
'''
    @start = we have to use this to see where we have to begin
    @begin_x = is used because in that way the loop for (of the exe x) starts from the beginning (-2) and don't lose time
    @begin_y = the same that @begin_x but for the exe y
    @longWay = will save all the possible ways to arrive to the goal (-3)
    @neight = will be used to prove which nearCells of each positions can be visited
    @new_pos = where is located the cell that we are going to visit
    @numVisited = number of the cell that we want to visit
    @nrCell = the number that represents each cell
    @finished = boolean used to skip of the loop in case that all the cells has been visited
'''
def fifo():
    # Positions
    start = getPosition(-2)
    begin_x = start[0]
    begin_y = start[1]
    x = begin_x
    y = begin_y
    # Auxiliar variables
    new_pos = [0,0]
    longWay = []
    nrCell = 0 #represents the number that is going to be in that cell
    numVisited = 0  #cell that is going to be visited
    finished = False
    while(finished != True):
        neight = getArrayNeightbours(x,y,nrCell,maze)

        if len(neight) != 0:    #if it is 0 that means all the nearCells of that cells has been visited
            # We storage in longway all the possible ways to visit the maze
            longWay = longWay + neight
            # The remove is needed because if we don't use it the last number of the array @neight is going to be repeted
            longWay.remove(neight[len(neight)-1])

            nrCell = len(longWay)

        if (numVisited > len(longWay)-1): #in case that this is true means that all the cells has been visited
            finished = True
        else:    #if still cells without being visited we visit the neighbours of the next element of the array @longWay
            new_pos = getPosition(longWay[numVisited])    #we see where if located the next cell that we want to visit

            x = new_pos[0]
            y = new_pos[1] 
            numVisited += 1

        

# Here we time the algorithm to see wich one is better FIFO or LIFO  
start_time = time()
fifo()
elapsed_time = time() - start_time
print("Time of FIFO execution: %.10f seconds." % elapsed_time)

# In this function we draw the maze in @screen
'''
    @nrRaws = number of raws of the maze
    @nrColumns = number of columns of the maze 
    @contX = help us to draw in an specific point the rectangule in the exis x
    @contY = the same as contX but on the exis Y
    @x = position on the exe x
    @y = position on the exe y
'''
def drawMaze(nrRaws, nrColumns):   
    contX = 0
    contY = 0
    for x in range(nrRaws):
        contX = x * 30
        for y in range(nrColumns):
            contY = y * 30
            if (maze[x][y] == -1):
                draw.create_rectangle(contX, contY, contX+30, contY+30, fill="grey")
            elif (maze[x][y] == -2):
                draw.create_rectangle(contX, contY, contX+30, contY+30, fill="green")
                draw.create_text(contX,contY,text="S", anchor=tk.NW, fill="blue")
            elif (maze[x][y] == -3):
                draw.create_rectangle(contX, contY, contX+30, contY+30, fill="red")
                draw.create_text(contX,contY,text="F", anchor=tk.NW, fill="green")
            else:
                draw.create_rectangle(contX, contY, contX+30, contY+30, fill="white")
                draw.create_text(contX,contY,text=maze[x][y], anchor=tk.NW)

drawMaze(13, 23)

screen.mainloop()


############################## MAZE WITH THE SHORTEST WAY #######################################




# We create another screen to see how the algorithm solve the problem
screen2=tk.Tk()
screen2.title("Shortest Way With BFS Algorithm")
draw2=tk.Canvas(width=400, height=800, background="black")
draw2.grid(column=0, row=0)
# This function is made to get the value of the neightbour cells of an specefied cell
def onlyVisiting(x,y):
    nearCells = [0] * 4
    valueLeft = getValue(x-1,y)
    valueRight = getValue(x+1,y)
    valueUp = getValue(x,y-1)
    valueDown = getValue(x,y+1) 

    nearCells[0] = valueLeft
    nearCells[1] = valueRight
    nearCells[2] = valueUp
    nearCells[3] = valueDown

    nearCells = removeWalls(nearCells)
    nearCells = removeCeros(nearCells)

    return nearCells

# Here we remove the -1 elements that represents walls, which we don't care
def removeWalls(array):
    times = array.count(-1)
    for i in range(times):
        array.remove(-1)

    return array

# This algorithm find the shortest way to arrive from the start to the goal
'''
    @goal = represents the cell where is the end of the maze
    @final_x = exe x where the @goal is located
    @final_y = exe y where the @goal is located
    @way = array that is going to save the cells that represents the shortest way
    @arrayAux = array that is needed to save the @nearCells returned by onlyVisiting
    @minor = represents the minor number of the array @arrayAux
    @new_position = represents the cell from where we are going to look for the next @minor 
'''
def best_way():
    goal = getPosition(-3)
    final_x = goal[0]
    final_y = goal[1]
    x = final_x
    y = final_y

    way = [] 
    # cont = 0
    while(arrivedBeggining(x,y) != True):
        arrayAux = onlyVisiting(x,y)
        if arrayAux.count(-3) > 0: arrayAux.remove(-3) 
        menor = min(arrayAux)
        
        way.append(menor)

        new_postion = getPosition(menor)
        x = new_postion[0]
        y = new_postion[1]

    return way

shortest = best_way()
print(len(best_way()))

maze_optimiced = ([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [ -1,-2,-1,-1,0,0,0,0,-1,0,0,0,-1,0,-1,0,0,0,0,-3,0,-1,-1],
    [ 0,0,0,-1,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,-1,-1,-1,0,-1,-1],
    [ 0,-1,0,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,-1,0,0,-1,0,-1,-1],
    [ 0,-1,-1,0,-1,0,-1,0,0,0,-1,0,-1,0,0,0,-1,-1,0,-1,0,-1,-1],
    [ 0,-1, 0,0,-1,0,-1,0,-1,-1,-1,0,-1,0,-1,0,0,0,0,-1,0,-1,-1],
    [ -1,-1,0,-1,-1,-1,-1,0,-1,0,-1,0,-1,0,-1,-1,-1,-1,0,-1,-1,-1,-1],
    [ -1,-1,0,-1,0,0,0,0,-1,0,0,0,-1,0,0,-1,-1,-1,0,-1,0,-1,-1],
    [ -1,-1,0,-1,0,-1,-1,-1,-1,0,-1,-1,-1,-1,0,-1,0,-1,0,-1,0,-1,-1],
    [ -1,-1,0,-1,0,0,0,0,-1,0,0,0,0,0,0,-1,0,-1,0,-1, 0,-1,-1],
    [ -1,-1,0,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,0,-1,0,-1,-1],
    [ -1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,-1],
    [ -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1])

# With this function we are going to put the shortest way in a "new maze"
'''
    @array = auxiliar array that saves @way
    @pos = position that we are going to visit and set the value of @way[i]
    @pos_x = where is located on the exe x @pos
    @pos_y = where is located on the exe x @pos
'''
def getNewMaze():
    array = best_way()

    for i in range(len(array)):
        pos = getPosition(array[i])
        pos_x = pos[0]
        pos_y = pos[1]
        setValue(pos_x,pos_y,array[i],maze_optimiced)

getNewMaze()

# Similar as drawMaze() but here only draws the shortest way
def drawMazeOptimiced(nrRaws, nrColumns):   
    contX = 0
    contY = 0
    for x in range(nrRaws):
        contX = x * 30
        for y in range(nrColumns):
            contY = y * 30
            if (maze_optimiced[x][y] == -1):
                draw2.create_rectangle(contX, contY, contX+30, contY+30, fill="grey")
            elif (maze_optimiced[x][y] == -2):
                draw2.create_rectangle(contX, contY, contX+30, contY+30, fill="yellow")
                draw2.create_text(contX,contY,text="S", anchor=tk.NW, fill="blue")
            elif (maze_optimiced[x][y] == -3):
                draw2.create_rectangle(contX, contY, contX+30, contY+30, fill="red")
                draw2.create_text(contX,contY,text="F", anchor=tk.NW, fill="black")
            elif (maze_optimiced[x][y] == 0):
                draw2.create_rectangle(contX, contY, contX+30, contY+30, fill="white")               
            else:
                draw2.create_rectangle(contX, contY, contX+30, contY+30, fill="green")
                draw2.create_text(contX,contY,text=maze_optimiced[x][y], anchor=tk.NW)

drawMazeOptimiced(13,23)
screen2.mainloop()

########## NEW MAZE SOLVED BY LIFO #######
