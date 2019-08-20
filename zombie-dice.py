import random
import sys
import time
from pprint import pprint

def initDiceBag():
    diceBag = []
    for i in range(6): diceBag.append('GREEN')
    for i in range(4): diceBag.append('YELLOW')
    for i in range(3): diceBag.append('RED')
    return diceBag

def initScoreboard():
    scoreboard = {}
    while True:
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
        roll = random.randint(1,6)
        # interpret the face based on the color and roll
        # BRAINs are on the low end of the die roll range
        if (   (die[0] == 'G' and roll < 4) # Green 3/6 brains
            or (die[0] == 'Y' and roll < 3) # Yellow 2/6 brains
            or (die[0] == 'R' and roll < 2) # Red 1/6 brains
            ):
            diceFaces.append('BRAIN')
        # SHOTs are on the high end of the die roll range
        elif ( (die[0] == 'G' and roll > 5) # Green 1/6 shots
            or (die[0] == 'Y' and roll > 4) # Yellow 2/6 shots
            or (die[0] == 'R' and roll > 3) # Red 3/6 shots
            ):
            diceFaces.append('SHOT')
        # Everything else is a RUNNER (2/6 probability for each color)
        else:
            diceFaces.append('RUNNER')
    return diceFaces

def getChoice():
    while True:
        print("What would you like to do?")
        print("  1. Roll\n  2. Bank\n  3. Peek\n  4. Quit")
        choice = input("> ")
        if choice in ('1','2','3', '4'):
            return choice
        else:
            continue

def userQuit(scoreboard):
    print("Thanks for playing!")
    printScoreboard(scoreboard)
    sys.exit()

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
            runners.append(myDice[d]) # we just need the color

    myRunners = ''
    for runner in runners:
        myRunners += runner + ', '
    myRunners = myRunners[:-2]
    if myRunners == '':
        myRunners = 'none'
    print("Brains: {}, Shots: {}, Runners: {}"
          .format(keepers.get('Brains'),
                  keepers.get('Shots'),
                  myRunners))

    return myBag, keepers, runners

def printScoreboard(scoreboard):
    print()
    print("Scoreboard: ".center(30, "*"))
    pprint(scoreboard)

def turn(scoreboard, player):

    # Intialize stuff
    diceBag = initDiceBag() # fill the dice bag
    keepers = {'Brains':0, 'Shots':0} # start with no turn score
    myHand = [] # start with no dice in-hand

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
        # 2. Bank
        if userChoice == '2':
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
        # 4. Quit
        if userChoice == '4':
            userQuit(scoreboard)

def mainGame():
    scoreboard = initScoreboard()
    waiting = True
    while waiting:
        for player in scoreboard:
            scoreboard = turn(scoreboard, player)
            print("debug 165: I'm about to check the scoreboad")
            for score in scoreboard.values():
                if score >= 13:
                    print("debut 168: I just found a score that is 13+")
                    return scoreboard, player

scoreboard, playerToBeat = mainGame()
printScoreboard(scoreboard)
print("Player to beat: " + playerToBeat)
