from RPSRobot import RPSRobot
from time import sleep
import sys

from getch import getch

key = ''

# CONSTANT KEYCODES
KEYCODE = {
    "UP": chr(38),
    "LEFT": chr(37),
    "RIGHT": chr(39),
    "DOWN": chr(40),
    "ESC": chr(27),
    "ENTER": chr(13)
}

# CHANGE YOUR KEYMAP HERE
KEYMAP = {
    "UP": ['w', KEYCODE['UP']],
    "DOWN": ['s', KEYCODE['DOWN']],
    "LEFT": ['a', KEYCODE['LEFT']],
    "RIGHT": ['d', KEYCODE['RIGHT']],

    # "HELLO": ['h', 'i'],
    "START_ROUND": [' '],
    "PERSON_RESPONSE": ['1', '2', '3', 'l', ';', '\''],
    "TRIAL_ROUND": [KEYCODE['ENTER'], 't']
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

def playGame(conditionInFavorOf):
    conditions = ["control", "robot", "human"]
    if isInteger(conditionInFavorOf):
        conditionInFavorOf = conditions[int(conditionInFavorOf)]

    assert conditionInFavorOf in conditions, f"Condition must be one of {conditions}"

    possibleMoves = ["rock", "paper", "scissors"]

    misty = RPSRobot(
        ip="192.168.1.169",
        conditionInFavorOf=conditionInFavorOf,
        possibleMoves=possibleMoves,
        debug=False
    )

    # print("Remember to start the trial first with the  key.")

    misty_head = {
        "roll": 0,
        "pitch": 0,
        "yaw": 0
    }

    while True:
        try:
            key = getch()

            if key == KEYCODE["ESC"]:
                break

            if key in KEYMAP["START_ROUND"]:
                print("space pressed")
                misty.startRound()
                # print(f"Remember human responses are 1, 2, 3 for {misty.possibleMoves}")

            elif key in KEYMAP["PERSON_RESPONSE"]:
                i = KEYMAP["PERSON_RESPONSE"].index(key) % 3
                person_move = possibleMoves[i]
                misty.checkRoundStatus(person_move)

            elif key in KEYMAP["TRIAL_ROUND"]:
                misty.startTrialRounds()

            # elif key in KEYMAP["HELLO"]:
            #     misty.waveRightArm()

            sleep(0.01)
        except KeyboardInterrupt as e:
            break

    misty.stop()

if __name__ == "__main__":
    conditionInFavorOf = None if len(sys.argv) <= 1 else sys.argv[1]
    playGame(conditionInFavorOf)
