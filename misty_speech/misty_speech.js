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