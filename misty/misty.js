
function playMove(move) {
  if (move == "ROCK") {
    misty.MoveArmDegrees("both", 80, 100);
  } else if (move == "PAPER") {
    misty.MoveArmDegrees("both", -80, 100);
  } else if (move == "SCISSORS") {
    misty.MoveArmDegrees("left", -80, 100);
    misty.MoveArmDegrees("right", 80, 100);
  }
}

misty.AddReturnProperty("SerialMessage", "SerialMessage");
misty.RegisterEvent("SerialMessage", "SerialMessage", 50, true);

function _SerialMessage(data) {
  misty.Debug(data);  
  try {
      if(data !== undefined && data !== null) {
          var move = data.AdditionalResults[0].Message;
          misty.Debug(move);
          playMove(move)
      }
  }
  catch(exception) {
      misty.Debug("Exception" + JSON.stringify(exception));
  }
}