from MistyRobot import MistyRobot
import numpy as np
from time import sleep
import os
import curses
import sys


class RPSRobot(MistyRobot):
    def __init__(self, ip, conditionInFavorOf, possibleMoves, debug=False):
        self.roundStarted = False
        self.currentMoveNum = 0
        self.totalRounds = 20

        self.humanTotalRounds = 0
        self.humanWinTimes = 0

        # Setup conditions and moves
        assert conditionInFavorOf in conditions, f"Condition must be one of {conditions}"
        self.conditionInFavorOf = conditionInFavorOf
        print("Misty will cheat in favour of:", conditionInFavorOf)

        self.currentMoveName = ""
        self.possibleMoves = possibleMoves
        self.moveList = np.random.choice(self.possibleMoves, self.totalRounds)
        # print(self.moveList)

        # Cheating conditions
        self.cheatTimes = np.zeros(self.totalRounds)
        cheatRounds = np.array([4, 8, 15]) - 1

        if conditionInFavorOf != 'control':
            self.cheatTimes[cheatRounds] = 1

        # Init parent robot actions
        super().__init__(ip, debug)

        # Audio population
        audioDir = "../audio"
        for filename in os.listdir(audioDir):
            self.uploadAudio(
                os.path.join(audioDir, filename), filename, apply=True
            )

        self.populateAudio()

        self.resetArm()

    def waveRightArm(self):
        misty.playAudio("hello.mp3")

        self.moveArmDegrees("right", -80, 30)  # Right arm up to wave
        sleep(1)
        self.moveArmDegrees("right", -35, 30)  # Right arm up to wave

        sleep(3)  # sleep 3 seconds

        self.resetArm()

    def resetArm(self):
        self.moveArmDegrees("both", 0, 100)
        sleep(1)

    def playMove(self, move):
        move = move.lower()

        vel = 100
        if (move == "rock"):
            self.moveArms(80, 80, vel, vel)
        elif (move == "paper"):
            self.moveArms(-80, -80, vel, vel)
        elif (move == "scissors"):
            self.moveArms(-80, 80, vel, vel)

    def playAudioName(self, audioName):
        self.playAudio(audioName + ".mp3")

    def startRound(self):
        if self.roundStarted: 
            return

        self.roundStarted = True
        if(self.currentMoveNum == 0):
            self.playAudio("begin.mp3")
            sleep(5)

        self.playAudio("start.mp3")

        sleep(3)

        self.currentMoveName = self.moveList[self.currentMoveNum]

        if self.debug:
            print("Misty will play", misty.currentMoveName)

        self.playMove(self.currentMoveName)

    def checkRoundStatus(self, personMove):
        print("Person played:", personMove)

        winStatus = self.winStatus(personMove)

        toCheat = self.cheatTimes[self.currentMoveNum]

        if toCheat:
            # Condition in favour of human; cheat to lose
            if self.conditionInFavorOf == "human" and winStatus != 'lose':
                self.playMove(self.getLosingMove())
                sleep(2)
                misty.playAudioName('lose')
            # Condition in favour of human; cheat to win
            elif self.conditionInFavorOf == "robot" and winStatus != 'win':
                self.playMove(self.getWinningMove())
                sleep(2)
                misty.playAudioName('win')
            # Cannot cheat because already satisfied
            # NOTE: Extended interaction, keep same round number
            else:
                self.currentMoveNum -= 1
        else:
            misty.playAudioName(winStatus)
            self.humanWinTimes = self.humanWinTimes + int(winStatus == 'lose')

        sleep(5)

        self.humanTotalRounds += 1
        self.currentMoveNum += 1
        self.resetArm()
        self.roundStarted = False

        if (self.currentMoveNum == self.totalRounds):
            print(f"Game complete with {self.totalRounds} rounds played!")

            sleep(1)

        else:
            print("Misty ready for next round!")

    def winStatus(self, personMove):
        if not self.roundStarted:
            print("Start the round first!")
            return

        mistyMove = self.currentMoveName

        if (mistyMove == personMove):
            return 'tie'

        if (personMove == self.getLosingMove(mistyMove)):
            return 'win'

        return 'lose'

    def getLosingMove(self, move):
        N = len(self.possibleMoves)
        move_id = self.possibleMoves.index(move)
        return self.possibleMoves[move_id - 1]

    def getWinningMove(self, move):
        N = len(self.possibleMoves)
        move_id = self.possibleMoves.index(move)
        return self.possibleMoves[(move_id+1) % N]


key = ''

# CONSTANT KEYCODES
KEYCODE = {
    "UP": curses.KEY_UP,
    "LEFT": curses.KEY_LEFT,
    "RIGHT": curses.KEY_RIGHT,
    "DOWN": curses.KEY_DOWN,
    "ESC": 27
}

# CHANGE YOUR KEYMAP HERE
KEYMAP = {
    "UP": [ord('w'), KEYCODE['UP']],
    "DOWN": [ord('s'), KEYCODE['DOWN']],
    "LEFT": [ord('a'), KEYCODE['LEFT']],
    "RIGHT": [ord('d'), KEYCODE['RIGHT']],

    # "HELLO": [ord('h'), ord('i')],
    "START_ROUND": [ord(' ')],
    "PERSON_RESPONSE": [ord('1'), ord('2'), ord('3')]
}


def isInteger(n):
    if n is None:
        return False

    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def loop(keyboard):
    while True:
        try:
            key = keyboard.getch()

            if key == KEYCODE["ESC"]:
                break

            if key in KEYMAP["START_ROUND"]:
                print(f"Starting round {misty.currentMoveNum}")
                misty.startRound()
                # print(f"Remember human responses are 1, 2, 3 for {misty.possibleMoves}")

            elif key in KEYMAP["PERSON_RESPONSE"]:
                i = int(chr(key)) - 1
                person_move = possibleMoves[i]
                misty.checkRoundStatus(person_move)

            # elif key in KEYMAP["HELLO"]:
            #     misty.waveRightArm()

            sleep(0.01)
        except KeyboardInterrupt as e:
            break

    curses.endwin()


if __name__ == "__main__":
    conditionInFavorOf = None if len(sys.argv) <= 1 else sys.argv[1]

    conditions = ["control", "robot", "human"]
    if isInteger(conditionInFavorOf):
        conditionInFavorOf = conditions[int(conditionInFavorOf)]

    possibleMoves = ["rock", "paper", "scissors"]

    misty = RPSRobot(
        ip="192.168.1.169",
        conditionInFavorOf=conditionInFavorOf,
        possibleMoves=possibleMoves,
        debug=False
    )

    # Curses stuff
    keyboard = curses.initscr()
    # curses.noecho()
    curses.halfdelay(1)
    keyboard.keypad(True)

    curses.wrapper(loop)
