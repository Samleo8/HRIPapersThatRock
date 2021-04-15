# HRI Project: Papers That Rock

Misty robot code for HRI Class

Sample Code (JS): https://github.com/MistyCommunity/JavaScript-SDK/tree/master/Sample%20Code

Remote Command Center: http://sdk.mistyrobotics.com/command-center/index.html

## Teleoperation Instructions

Misty is teleoperated via Python >= 3.6, with code found in the `./teleop` folder. To run the experiment game, enter into the `./teleop` folder and run the following commands:

```
python3 playGame.py <conditionInFavorOf: control|robot|human> [optional IP address]
```

where the first argument specifies what condition Misty will cheat in favor of.

Alternatively, from the main folder, run the bash script

```bash
./startTeleop.sh <conditionInFavorOf: control|robot|human> [optional IP address]
```

### Controls

Once Misty is started, you can start entering input into the terminal window.
Most of the game is automated. To start the 3 trial rounds, press `SPACE`.
Then, to start the actual game, press `SPACE` again. 

From here on, just focus on keying in the opponent's move. For rock paper scissors respectively, key in

```bash
1 2 3
```

or

```bash
L ; '
```

Note that measures are in place to prevent accidental key presses for SPACE.

### Requirements

The libraries required are under `./teleop/requirements.txt`. To install them, just run 

```bash
pip3 install ./teleop/requirements.txt
```
