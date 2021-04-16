from RPSRobot import RPSRobot
from time import sleep
import sys

from getch import getche

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

    "HELLO": ['h'],
    "START_ROUND": [' ', KEYCODE['ENTER']],
    "PERSON_RESPONSE": ['1', '2', '3', 'l', ';', '\''],
    "SKIP_TRIAL": ['t']
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

def playGame(conditionInFavorOf, ipAddr="192.168.1.169"):
    conditions = ["control", "robot", "human"]
    if isInteger(conditionInFavorOf):
        conditionInFavorOf = conditions[int(conditionInFavorOf)]
    conditionInFavorOf = conditionInFavorOf.lower()

    assert conditionInFavorOf in conditions, f"Condition must be one of {conditions}"

    possibleMoves = ["rock", "paper", "scissors"]

    misty = RPSRobot(
        ip=ipAddr,
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
            key = getche()

            if key == KEYCODE["ESC"]:
                break

            if key in KEYMAP["START_ROUND"]:
                misty.startAllRounds()
                # print(f"Remember human responses are 1, 2, 3 for {misty.possibleMoves}")

            elif key in KEYMAP["PERSON_RESPONSE"]:
                i = KEYMAP["PERSON_RESPONSE"].index(key) % 3
                person_move = possibleMoves[i]
                misty.checkRoundStatus(person_move)

            elif key in KEYMAP["SKIP_TRIAL"]:
                misty.trialComplete = True
                print("Misty skipping trial: ", misty.trialComplete)
                # misty.startTrialRounds()

            elif key in KEYMAP["HELLO"]:
                misty.waveRightArm()

            # sleep(0.01)
        except KeyboardInterrupt as e:
            break
        except OverflowError as e:
            break

    misty.stop()

if __name__ == "__main__":
    conditionInFavorOf = None if len(sys.argv) <= 1 else sys.argv[1]
    ipAddr = "192.168.1.169" if len(sys.argv) <= 2 else sys.argv[2]

    print("Press <SPACE> to start the trial round, then <SPACE> again to start the actual game.")
    print("After that, just focus on pressing 123/l;' for rock paper scissors!")
    playGame(conditionInFavorOf, ipAddr)
