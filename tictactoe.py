#FFFFFFimport sys
import copy

class GameState(object):
    depth = 0
    score = 0 # All branching state values added up
    childStates = [] #GameStates

    state = ["_"]*9

def populate(game, turn):
    i = 0
    children = []
    while i <= 8:
        if game.state[i] == "_":
            z = GameState()
            z.depth = game.depth + 1
            temp = copy.copy(game.state)
            temp[i] = copy.copy(opposite(turn))
            z.state = temp
            children.append(copy.copy(z))
        i += 1
    return children



def isFinal(game):
    s = game.state
    if s[0] == s[1] == s[2] and s[0] != "_": #Horizontal wincons
        return True
    if s[3] == s[4] == s[5] and s[3] != "_":
        return True
    if s[6] == s[7] == s[8] and s[6] != "_":
        return True

    if s[0] == s[3] == s[6] and s[0] != "_": #Vertical wincons
        return True
    if s[1] == s[4] == s[7] and s[1] != "_":
        return True
    if s[2] == s[5] == s[8] and s[2] != "_":
        return True

    if s[0] == s[4] == s[8] and s[0] != "_": #Diagonal wincons
        return True
    if s[2] == s[4] == s[6] and s[2] != "_":
        return True
    if s[0] != "_" and s[1] != "_" and s[2] != "_" and s[3] != "_" and s[4] != "_" and s[5] != "_" and s[6] != "_" and s[7] != "_" and s[8] != "_":
        return True
    return False

def findValue(game):
    s = game.state
    val = 0
    val += findValOfLine([s[0], s[1], s[2]]) #Top row
    val += findValOfLine([s[3], s[4], s[5]]) #Middle row
    val += findValOfLine([s[6], s[7], s[8]]) #Bottom row

    val += findValOfLine([s[0], s[3], s[6]]) #Left column
    val += findValOfLine([s[1], s[4], s[7]]) #Middle column
    val += findValOfLine([s[2], s[5], s[8]]) #Right column

    val += findValOfLine([s[0], s[4], s[8]]) #Main diagonal
    val += findValOfLine([s[2], s[4], s[6]]) #Alternate diagonal

    return val

def findValOfLine(line):
    if line[0] == line[1] == line[2] and line[0] == "x":
        return float('inf')
    elif line[0] == line[1] == line[2] and line[0] == "o":
        return -float('inf')
    elif (line[0] == line[1] and line[0] == "x") or (line[1] == line[2] and line[1] == "x") or (line[0] == line[2] and line[0] == "x"):
        return 10
    elif (line[0] == line[1] and line[0] == "o") or (line[1] == line[2] and line[1] == "o") or (line[0] == line[2] and line[0] == "o"):
        return -10
    return 0

def opposite(xo):
    if xo == "x":
        return "o"
    elif xo == "o":
        return "x"
    return xo

def minimax(node, depth, turn):
    if depth == 0 or isFinal(node) == True:
        return findValue(node)
    children = populate(node, opposite(turn))
    if turn == "x":
        bestScore = -float('inf')
        for c in children:
            score = minimax(c, depth - 1, opposite(turn))
            # print(score)
            if score > bestScore:
                bestScore = score
        return bestScore
    if turn == "o":
        bestScore = float('inf')
        for c in children:
            score = minimax(c, depth - 1, opposite(turn))
            # print(score)
            if score < bestScore:
                bestScore = score
        return bestScore

def printBoard(node):
    x = node.state
    print("Current state of the board:\n")
    print(x[0] + x[1] + x[2])
    print(x[3] + x[4] + x[5])
    print(x[6] + x[7] + x[8])

def findBestMove(node, depth, turn):
    bestMoveVal = 9999
    bestMove = 0
    for n in populate(node, opposite(turn)):
        p = minimax(n, depth - 1, opposite(turn))
        if p < bestMoveVal:
            bestMoveVal = p
            bestMove = n
    # print("bestmove")
    # print(bestMoveVal)
    return bestMove

currentgame = GameState()
diff = input("Enter a number from 1 to 9. 9 is the highest difficulty; 1 is the lowest.")
print("You are X.")
print("When it is your turn, type in the number corresponding to the space you want.\n1 2 3\n4 5 6\n7 8 9")
while not isFinal(currentgame):
    printBoard(currentgame)
    x_loc = int(input("Where would you like to place your X? Enter the number.")) - 1
    if currentgame.state[x_loc] == "_":
        # print(currentgame.state)
        temp = copy.copy(currentgame)
        temp.state[x_loc] = "x"
        currentgame = copy.copy(temp)
        # print(temp.state)
    else:
        print("There is already a piece here!")
        continue
    if isFinal(currentgame):
        break
    printBoard(currentgame)
    print("The CPU is thinking...")
    currentgame = findBestMove(currentgame, int(diff), "o")
printBoard(currentgame)
print("Game value:" + str(findValue(currentgame)))
print("\nThat's the game!")
if findValue(currentgame) > 0:
    print("Overall, x did better.")
elif findValue(currentgame) < 0:
    print("Overall, o did better.")
else:
    print("The match was overall very equal.")