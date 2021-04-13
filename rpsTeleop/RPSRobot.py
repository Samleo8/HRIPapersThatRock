from MistyRobot import MistyRobot

class RPSRobot(MistyRobot):
    def __init__(self):
        super().__init__()

    def waveRightArm(self):
        self.MoveArmDegrees("right", -80, 30) # Right arm up to wave
        self.Pause(3000) # Pause with arm up for 3 seconds
        self.MoveArmDegrees("both", 80, 30) # Both arms down

    