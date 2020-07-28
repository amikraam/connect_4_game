import random
import time

##Select difficulty for players
##Return 0 for Normal difficulty, 1 for Advanced difficulty

def difficulty():
    normal = 0
    advance = 1
    gridDiff = -1

    diff = input("Please choose difficulty.\n\"N\" for Normal, \"A\" for Advance: ")
    diff = diff.upper()    

    while diff !='N' and diff != 'A':
        diff = input("Please enter \"N\" or \"A\": ")
        diff = diff.upper()

    if diff == 'N':
        print("You have chosen Normal difficulty.\nConnect Four to win.")
        gridDiff = normal
    else:
        print("You have chosen Advanced difficulty\nConnect Five to win.")
        gridDiff = advance

    print()
    return gridDiff

##Allow player to choose game mode
##Return 0 for single player, 1 for multiplayer
def gameMode():
    chooseMode = input("Please select Game Mode.\n\"S\" for Single Player,\"M\" for Multiplayer: ")
    chooseMode = chooseMode.upper()

    while chooseMode != 'S' and chooseMode != 'M':
        chooseMode = input("Please enter \"S\" or \"M\":")
        chooseMode = chooseMode.upper()

    if chooseMode == 'S':
        mode = 0
        print("You have chosen Single Player. Beat the AI to win")
    else:
        mode = 1
        print("You have chosen Multiplayer. Best of luck!")
    print()
    return mode

##Make game grid based on difficulty selected
##6 x 7 if Normal
##6 x 9 if Advance

def makeGrid(difficulty):
    row = 6
    if difficulty == 0:
        col = 7
    else:
        col = 9

    gameGrid = []

    for y in range(col):
        gameRow = []
        for x in range(row):
            #Fill initial list with " "
            gameRow.append(' ')
        gameGrid.append(gameRow)

    return gameGrid

##Draw the grid
def drawGrid(gameGrid):

    gameCol = len(gameGrid)
    gameRow = len(gameGrid[0])

    for n in range(gameCol):
        print("+-",n+1,"-",sep = "",end ="")
        
    print("+",end="")
    print()

    for y in range(gameRow, 0, -1):
        for x in range(gameCol):
            print("| ",gameGrid[x][y-1]," ",sep = "", end = "")

        print("|",end="")
        print()
            
        for z in range(gameCol):
            print("+---",end="")
        print("+",end="")
        print()

##Place a shape into the grid into a specified column
##Inputs:
##    Turn - Turn of current player
##    gameGrid - The gameGrid
##'O' for Player 1, 'X' for Player 2
def placeShape(turn, gameGrid, gameMode):
    space = " "
    
    if (gameMode == 0 and turn == 0) or gameMode == 1:
        if turn == 0:
            shape = 'O'
        else:
            shape = 'X'
        isValid = False
        while isValid == False:
            try:
                #Player inputs desired column
                #Input value subtracted by 1 to match grid index
                putColumn = input("Please enter the desired column:")
                putColumn = int(putColumn)
                putColumn -= 1

                if putColumn <0 or putColumn > len(gameGrid)-1:
                    #Appears if player inputs an invalid column value
                    print("Please enter a valid number")
                else:
                    #Checks whether desired column is full.
                    #Prompts user to input another column if true.
                    if gameGrid[putColumn][len(gameGrid[0])-1] != space:
                        print("Column is full. Please choose another column: ")
                    else:
                        isValid = True
            except ValueError:
                print("Please input a valid number")
    else:
        shape = 'X'
        validColumn = False
        while validColumn == False:
            putColumn = random.randint(0, len(gameGrid)-1)
            if gameGrid[putColumn][len(gameGrid[0])-1] == space:
                validColumn = True

    for y in range(len(gameGrid)):
        if gameGrid[putColumn][y] == space:
            gameGrid[putColumn][y] = shape
            break                            

##Check grid for win conditions
def checkWin(gameGrid,turn,difficulty):
    if turn == 0:
        shape = 'O'
    else:
        shape = 'X'

    if difficulty == 0:
        winConnect = 4
    else:
        winConnect = 5

    won = False
    
    gameCol = len(gameGrid)
    gameRow = len(gameGrid[0])

    checkVertical = []

    #Create Vertical List
    for x in range(gameCol):
        #Create Vertical
        checkVertical.append(gameGrid[x])

    #Check Vertical
    for x in range(len(checkVertical)):
        if won == True:
            break
        startRange = 0
        for row in range(len(checkVertical[x])-winConnect+1):
            endRange = startRange + winConnect
            count = 0
            for y in range(startRange,endRange):
                if checkVertical[x][y] == shape:
                    count +=1
                if count >= winConnect:
                    won = True
                    break
            startRange+=1

    
    if not won:
        #Create Horizontal List
        checkHorizontal = []
        for y in range(gameRow):
            hList = []
            for x in range(gameCol):
                hList.append(gameGrid[x][y])

            checkHorizontal.append(hList)

        #Check Horizontal
        for x in range(len(checkHorizontal)):
            if won == True:
                break
            startRange = 0
            for row in range(len(checkHorizontal[x])-winConnect+1):
                endRange = startRange + winConnect
                count = 0
                for y in range(startRange,endRange):
                    if checkHorizontal[x][y] == shape:
                        count +=1
                    if count >= winConnect:
                        won = True
                        break
                startRange+=1
                
    if not won:
        #Create Diagonal List
        checkDiag = []

        xStart = 0
        yStart = 1
        diagCol = gameCol-1
        diagRow = gameRow-1
        xEnd = diagCol
        yEnd = diagRow

        while xStart <= diagCol:
            diagListXLR = []
            x = xStart
            y = 0

            while y <= diagRow:
                if x <= diagCol:
                    diagListXLR.append(gameGrid[x][y])
                x += 1
                y += 1
            if len(diagListXLR) >= winConnect:
                checkDiag.append(diagListXLR)

            xStart+=1
        
        while yStart <= diagRow:
            diagListYLR = []
            x = 0
            y = yStart

            while y <=diagRow:
                if x < diagCol:
                    diagListYLR.append(gameGrid[x][y])
                x+=1
                y+=1
            if len(diagListYLR) >= winConnect:
                checkDiag.append(diagListYLR)

            yStart+=1

        while xEnd >= 0:
            diagListXRL = []
            x = xEnd
            y = 0

            while y <= diagRow:
                if x >=0:
                    diagListXRL.append(gameGrid[x][y])
                x-=1
                y+=1

            if len(diagListXRL) >= winConnect:
                checkDiag.append(diagListXRL)
            xEnd -=1

        xEnd = diagCol
        yStart = 1

        while yStart <= diagRow:
            diagListYRL = []
            x = xEnd
            y = yStart

            while y <= diagRow:
                if x >=0:
                    diagListYRL.append(gameGrid[x][y])
                x -=1
                y +=1
            if len(diagListYRL) >= winConnect:
                checkDiag.append(diagListYRL)
            yStart +=1

        #Check Diagonal
        for x in range(len(checkDiag)):
            if won == True:
                break
            startRange = 0
            for row in range(len(checkDiag[x])-winConnect+1):
                endRange = startRange + winConnect
                count = 0
                for y in range(startRange,endRange):
                    if checkDiag[x][y] == shape:
                        count +=1
                    if count >= winConnect:
                        won = True
                        break
                startRange+=1

    return won

#Check final element of each column
#Return true if no ' ' found. False otherwise
def checkDraw(gameGrid):
    
    gameRow = len(gameGrid[0])
    gameCol = len(gameGrid)
    space = ' '
    isDraw = False

    drawList = []

    for x in range(gameCol):
        drawList.append(gameGrid[x][gameRow-1])

    if space not in drawList:
        isDraw = True

    return isDraw

##Main game section

print("Welcome to Connect Four!")

##looper variable checks whether game will be replayed. True by default
looper = True
while looper:
    diffi = difficulty()
    gMode = gameMode()
    grid = makeGrid(diffi)

    if diffi == 0:
        winCondition = 4
    else:
        winCondition = 5

    player1 = 0
    player2 = 1
    rando = random.randint(0,100)
    print("Randomizing Start Turn...")
    time.sleep(1)
    if rando <= 50:
        turn = 0
        print("Player 1 start\n")
    else:
        turn = 1
        print("Player 2 start\n")

    win = False
    isDraw = False
    num = 1
    time.sleep(0.5)
    print("Beginning Game...\n")
    time.sleep(2)
    while not win or not isDraw:
        
        if win or isDraw:
            break
        for cycle in range(2):
            print("Turn", num)
            if turn == player1:
                print("Player 1 Turn")
            else:
                print("Player 2 Turn")
                if gMode == 0:
                    print("Computer is thinking...")
                    time.sleep(3)

            placeShape(turn,grid, gMode)
            drawGrid(grid)
            if num >= winCondition:
                win = checkWin(grid,turn, diffi)
                if win:
                    break
                else:
                    isDraw = checkDraw(grid)

                    if isDraw:
                        break

            if turn == player1:
                turn = player2
            else:
                turn = player1
            print()

        if win or isDraw:
            break
        
        num +=1

        

        print()
        
    if win:
        if turn == player1:
            print("Player 1 wins!")
        else:
            if gMode == 0:
                print("Computer wins!")
            else:
                print("Player 2 wins!")
        print("Total attempts:",num)        
        if (gMode == 0 and turn == player1) or (gMode ==1):
            if num > 15:
                print("You can do better")
            elif num < 10:
                print("You have the talent!")
            else:
                print("Not too bad")
        else:
            print("Better luck next time!")
    else:
        print("Draw Game!")

    ##Prompt player for replay
    playAgain = input("Play again? Type \"Y\" for yes. Otherwise, type anything else to exit: ")
    playAgain = playAgain.upper()
    if playAgain == "Y":
        looper = True
    else:
        looper = False
        print("Thank you for playing!")
        time.sleep(1)


