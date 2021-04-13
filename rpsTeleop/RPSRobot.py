from MistyRobot import MistyRobot
import numpy as np
from time import sleep
import os


class RPSRobot(MistyRobot):
    def __init__(self, ip, debug=False):
        self.currentMove = 0
        self.totalMoves = 10

        self.moveList = np.random.choice(
            ["ROCK", "PAPER", "SCISSORS"], self.totalMoves)
        print(self.moveList)

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
        self.moveArmDegrees("right", -80, 30)  # Right arm up to wave
        sleep(3)  # sleep 3 seconds
        self.moveArmDegrees("both", 80, 30)  # Both arms down

    def resetArm(self):
        self.moveArmDegrees("both", 0, 100)
        sleep(1)

    def playMove(self, move):
        move = move.upper()

        if (move == "ROCK"):
            self.moveArms(80, 80, 100, 100)
        elif (move == "PAPER"):
            self.moveArms(-80, -80, 100, 100)
        elif (move == "SCISSORS"):
            self.moveArms(-80, 80, 100, 100)

        sleep(5)
        self.resetArm()

    def startRound(self):
        self.playAudio("start.mp3")

        sleep(3)

        move = self.moveList[self.currentMove]
        self.playMove(move)

        self.currentMove += 1

        if (self.currentMove == self.totalMoves):
            print("Game complete!")


if __name__ == "__main__":
    misty = RPSRobot("192.168.1.169")

    for i in range(misty.totalMoves):
        misty.startRound()
        sleep(5)
