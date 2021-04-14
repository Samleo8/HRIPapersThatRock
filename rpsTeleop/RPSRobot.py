from MistyRobot import MistyRobot
import numpy as np
import os
from time import sleep

class RPSRobot(MistyRobot):
    def __init__(self, ip, conditionInFavorOf, possibleMoves, debug=False):
        self.roundStarted = False
        self.trialComplete = False

        self.currentMoveNum = 0
        self.totalRounds = 20

        self.humanTotalRounds = 0
        self.humanWinTimes = 0

        # Setup conditions and moves
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

        # self.trialComplete = True
        # self.cheatTimes = np.ones(self.totalRounds)

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
        self.playAudio("hello.mp3")

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

    def playMoveWithAudio(self, move):
        self.playAudio("start.mp3")
        sleep(2.5)
        self.playMove(move)

    def playAudioName(self, audioName):
        self.playAudio(audioName + ".mp3")

    def startRound(self):
        if not self.trialComplete:
            self.startTrialRounds()
            return

        if self.roundStarted: 
            return

        if (self.currentMoveNum == self.totalRounds):
            return

        print(f"Starting round {self.currentMoveNum}")

        self.roundStarted = True
        if(self.currentMoveNum == 0):
            self.playAudio("begin.mp3")
            sleep(4)

        self.currentMoveName = self.moveList[self.currentMoveNum]

        if self.debug:
            print("Misty will play", self.currentMoveName)

        self.playMoveWithAudio(self.currentMoveName)

        print("Awaiting input from human...")

    def checkRoundStatus(self, personMove):
        if not self.roundStarted:
            print("Start the round first!")
            return

        print("Person played:", personMove)

        winStatus = self.winStatus(personMove)

        toCheat = self.cheatTimes[self.currentMoveNum]

        if toCheat:
            print(f"Misty is cheating in favour of {self.conditionInFavorOf}!")
            # Condition in favour of human; cheat to lose
            if self.conditionInFavorOf == "human" and winStatus != 'lose':
                move = self.getLosingMove(personMove)
                self.playMove(move)
                sleep(2)
                self.playAudioName('lose')
            # Condition in favour of human; cheat to win
            elif self.conditionInFavorOf == "robot" and winStatus != 'win':
                move = self.getWinningMove(personMove)
                self.playMove(move)
                sleep(2)
                self.playAudioName('win')
            # Cannot cheat because already satisfied
            # NOTE: Extended interaction, keep same round number
            else:
                print("Misty failed to cheat. Game extended by another round.")
                self.currentMoveNum -= 1
                self.playAudioName(winStatus)
                self.humanWinTimes = self.humanWinTimes + int(winStatus == 'lose')
        else:
            self.playAudioName(winStatus)
            self.humanWinTimes = self.humanWinTimes + int(winStatus == 'lose')

        sleep(1)

        self.humanTotalRounds += 1
        self.currentMoveNum += 1
        self.resetArm()
        self.roundStarted = False

        if (self.currentMoveNum == self.totalRounds):
            print(f"Game complete! Human won {self.humanWinTimes} out of {self.humanTotalRounds} played!")

            self.playAudio("finish.mp3")

            sleep(2.5)

            return
        else:
            print("Misty ready for next round!")

    def startTrialRounds(self):
        print("Starting trial...")
        sleep(1.5)

        # NOTE: Person will always play scissors
        for move in self.possibleMoves:
            self.playMoveWithAudio(move)

            sleep(2) # how long before robot responds

            self.playAudioName(self.winStatus("scissors", move))
            self.resetArm()

            sleep(2) # how long before next round

        self.trialComplete = True
        print("Trial complete.")

    def winStatus(self, personMove, robotMove=None):
        mistyMove = self.currentMoveName if robotMove is None else robotMove

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

    def setHeadPosition(self, position):
        self.moveHead(position['roll'], position['pitch'], position['yaw'])
