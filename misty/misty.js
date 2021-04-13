// Waves Misty's right arm!
function waveRightArm () {
    misty.MoveArmDegrees("right", -80, 30); // Right arm up to wave
    misty.Pause(3000); // Pause with arm up for 3 seconds
    misty.MoveArmDegrees("both", 80, 30); // Both arms down
}

function playMove (move) {
    if (move == "ROCK") {
        misty.MoveArms(80, 80, 100, 100);
        // misty.DisplayText("ROCK")
    }
    else if (move == "PAPER") {
        misty.MoveArms(-80, -80, 100, 100);
        // misty.DisplayText("PAPER")
    }
    else if (move == "SCISSORS") {
        misty.MoveArms(-80, 80, 100, 100);
        // misty.DisplayText("SCISSORS")
    }
    misty.UnregisterEvent("reset");
    misty.RegisterTimerEvent("reset", 5000, false);
}

function _reset () {
    misty.MoveArmDegrees("both", 0, 100);
    // misty.DisplayText("")
}

function _playRock () {
    playMove("ROCK")
}

function _playPaper () {
    playMove("PAPER")
}

function _playScissors () {
    playMove("SCISSORS")
}

misty.AddReturnProperty("SerialMessage", "SerialMessage");
misty.RegisterEvent("SerialMessage", "SerialMessage", 50, true);

function _SerialMessage (data) {
    misty.Debug(data);
    try {
        if (data !== undefined && data !== null) {
            var move = data.AdditionalResults[0].Message;
            misty.Debug(move);
            if (move == "START") {
                misty.PlayAudio("start.mp3");
                r = Math.random() * 3;
                move = r < 1 ? "ROCK" : (r < 2 ? "PAPER" : "SCISSORS")
                if (r < 1) {
                    misty.RegisterTimerEvent("playRock", 2000, false);
                }
                else if (r < 2) {
                    misty.RegisterTimerEvent("playPaper", 2000, false);
                }
                else {
                    misty.RegisterTimerEvent("playScissors", 2000, false);
                }
            }
            else if (move == "ROCK" || move == "PAPER" || move == "SCISSORS") {
                var cheat = "FAVOR_MISTY"
                if (cheat == "FAVOR_MISTY") {
                    if (move == "ROCK") {
                        playMove("PAPER")
                    }
                    else if (move == "PAPER") {
                        playMove("SCISSORS")
                    }
                    else if (move == "SCISSORS") {
                        playMove("ROCK")
                    }
                }
                else if (cheat == "FAVOR_HUMAN") {
                    if (move == "ROCK") {
                        playMove("SCISSORS")
                    }
                    else if (move == "PAPER") {
                        playMove("ROCK")
                    }
                    else if (move == "SCISSORS") {
                        playMove("PAPER")
                    }
                }
                else {
                    playMove(move)
                }
            }
            else if (move == "WIN") {
                misty.PlayAudio("win.mp3");
            }
            else if (move == "LOSE") {
                misty.PlayAudio("lose.mp3");
            }
            else if (move == "TIE") {
                misty.PlayAudio("tie.mp3");
            }
            else if (move == "WAVE") {
                waveRightArm();
            }
        }
    }
    catch (exception) {
        misty.Debug("Exception" + JSON.stringify(exception));
    }
}
