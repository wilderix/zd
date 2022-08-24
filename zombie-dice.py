import random
import sys
import time


def instructions():
    with open('instructions.txt', 'r') as file:
        instructions_text = file.read()
        instructions = instructions_text.split('<break>')
    for i, instruction in enumerate(instructions):
        print(instruction)
        if i + 1 < len(instructions):
            print("Press enter to continue...")
        else:
            print("Press enter to begin...")
        input()


def initDiceBag():
    diceBag = []
    for i in range(6):
        diceBag.append('GREEN')
    for i in range(4):
        diceBag.append('YELLOW')
    for i in range(3):
        diceBag.append('RED')
    return diceBag


def initScoreboard():
    scoreboard = {}
    while True:
        print()
        players = input("Enter number of players: ")
        try:
            players = int(players)
            break
        except:
            continue
    for i in range(players):
        player = 'Player ' + str(i+1)
        scoreboard[player] = 0
    
    return scoreboard


def drawDice(num, bag):
    # always shake the bag before we get new dice
    random.shuffle(bag)
    # get new dice out of the bag
    draw = []
    for i in range(num):
        draw.append(bag.pop())
    return draw, bag


def rollDice(dice):
    diceFaces = []
    for die in dice:
        roll = random.randint(1, 6)
        # interpret the face based on the color and roll
        # BRAINs are on the low end of the die roll range
        if (
            (die[0] == 'G' and roll < 4)  # Green 3/6 brains
            or (die[0] == 'Y' and roll < 3)  # Yellow 2/6 brains
            or (die[0] == 'R' and roll < 2)  # Red 1/6 brains
        ):
            diceFaces.append('BRAIN')
        # SHOTs are on the high end of the die roll range
        elif (
            (die[0] == 'G' and roll > 5)  # Green 1/6 shots
            or (die[0] == 'Y' and roll > 4)  # Yellow 2/6 shots
            or (die[0] == 'R' and roll > 3)  # Red 3/6 shots
        ):
            diceFaces.append('SHOT')
        # Everything else is a RUNNER (2/6 probability for each color)
        else:
            diceFaces.append('RUNNER')
    return diceFaces


def getChoice():
    while True:
        print("What would you like to do?")
        print("  1. Roll\n  2. Bank\n  3. Peek\n  4. Scoreboard\n  5. Quit")
        choice = input("> ")
        if choice in ('1', '2', '3', '4', '5'):
            return choice
        else:
            continue


def userRoll(diceBag, keepers, hand):
    # draw new dice
    diceNeeded = 3 - len(hand)
    myDice, myBag = drawDice(diceNeeded, diceBag)
    # add them to the runners we kept back
    myDice.extend(hand)
    # roll the new hand of dice
    myRoll = rollDice(myDice)

    # show the roll
    print("You rolled:")
    for i in range(3):
        print("     {} {}".format(myDice[i], myRoll[i]))
        time.sleep(.5)

    # tally the current turn score
    runners = []
    for d in range(3):
        # set the brains aside
        if myRoll[d] == 'BRAIN':
            keepers['Brains'] += 1
        # set the shots aside
        elif myRoll[d] == 'SHOT':
            keepers['Shots'] += 1
        else:
            # keep the runners in case they press their luck
            runners.append(myDice[d])  # we just need the color

    # Make the runners easier to print
    myRunners = ''
    for runner in runners:
        myRunners += runner + ', '
    myRunners = myRunners[:-2]
    if myRunners == '':
        myRunners = 'none'
    print(
            "Brains: {}, Shots: {}, Runners: {}"
            .format(keepers.get('Brains'), keepers.get('Shots'), myRunners))

    return myBag, keepers, runners


def printScoreboard(scoreboard):
    print()
    print(" Scoreboard ".center(30, "*"))
    for player in scoreboard:
        score = str(scoreboard.get(player))
        score = score.rjust(10, '.')
        item = player + score
        print(item.center(30, ' '))


def turn(scoreboard, player, playerToBeat):
    # Intialize stuff
    diceBag = initDiceBag()  # fill the dice bag
    keepers = {'Brains': 0, 'Shots': 0}  # start with no turn score
    myHand = []  # start with no dice in-hand

    # Get the user choice
    while True:
        print()
        print((' '+player+' ').center(26, '*'))
        userChoice = getChoice()
        # 1. Roll
        if userChoice == '1':
            diceBag, keepers, myHand = userRoll(diceBag, keepers, myHand)
            # check to see if they struck out
            if keepers['Shots'] >= 3:
                print("You rolled too many shots!")
                time.sleep(.5)
                print("On to the next player...")
                time.sleep(.5)
                printScoreboard(scoreboard)
                return scoreboard
                break
        # 2. Bank in the main game
        if userChoice == '2' and playerToBeat == '':
            # add their brains to the scoreboard
            scoreboard[player] += keepers.get('Brains')
            printScoreboard(scoreboard)
            return scoreboard
            break
        # 2. Bank in the end game
        if userChoice == '2' and playerToBeat != '':
            scoreToWin = scoreboard.get(playerToBeat) + 1
            potentialScore = scoreboard.get(player) + keepers.get('Brains')
            if potentialScore < scoreToWin:
                print("You cannont bank until you have ")
                print("enough brains to beat {}".format(playerToBeat))
                print("Right now you have {} brains".format(potentialScore))
                print("And you need {} brains.".format(scoreToWin))
                continue
            else:
                # add their brains to the scoreboard
                scoreboard[player] += keepers.get('Brains')
                printScoreboard(scoreboard)
                return scoreboard
                break
        # 3. Peek
        if userChoice == '3':
            print("The bag currently contains these dice: ")
            print(diceBag)
            print("Don't worry. We'll shake the bag before you draw more out.")
        # 4. Scoreboard
        if userChoice == '4':
            printScoreboard(scoreboard)
        # 5. Quit
        if userChoice == '5':
            print("Thanks for playing!")
            printScoreboard(scoreboard)
            sys.exit()


def mainGame():
    scoreboard = initScoreboard()
    waiting = True
    while waiting:
        for player in scoreboard:
            scoreboard = turn(scoreboard, player, '')
            for score in scoreboard.values():
                if score >= 13:
                    return scoreboard, player


def endGame(scoreboard, originalPlayerToBeat):

    # End game header
    print()
    print('*'*30)
    print("You are now in the end game!".center(30, ' '))
    print('*'*30)
    input("Press enter to continue...")
    print()
    print(f"Each player gets one chance to beat {originalPlayerToBeat}.")
    printScoreboard(scoreboard)


    # cycle through the contenders
    for player in scoreboard:
        playerToBeat = max(scoreboard, key=scoreboard.get)
        if player != originalPlayerToBeat:
            scoreboard = turn(scoreboard, player, playerToBeat)

    # Print the final score
    print()
    print('*'*30)
    print(" Final Score ".center(30, '*'))
    print('*'*30)
    printScoreboard(scoreboard)


# Start the game!
print()
print("*"*40)
print("                 ".center(40, "*"))
print("   Zombie Dice   ".center(40, "*"))
print("                 ".center(40, "*"))
print("*"*40)
print()

# Print instructions if the player needs them
while True:
    print("Do you need to see the instructions before you begin? ")
    needInfo = input("y or n >> ")
    if needInfo in ('y', 'n'):
        break
if needInfo[0].lower() == 'y':
    instructions()

# Play the main game
scoreboard, playerToBeat = mainGame()

# Play the end game
endGame(scoreboard, playerToBeat)
