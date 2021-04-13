# Last Update Jan 14 2021
import requests
from time import sleep
import base64


class MistyRobot:
    """This is a Python Wrapper for Misty's RESTful calls and websockets"""

    def __init__(self, ip, debug=False):
        self.ip = ip
        self.debug = debug

    def moveArm(self, arm, position, velocity, units="degrees"):
        arm = arm.lower()
        units = units.lower()

        assert arm == "left" or arm == "right", "Invalid arm requested. Please use 'left' or 'right'"
        assert units == "degrees" or units == "radians" or units == "position", "Invalid unit. Please use 'degrees', 'radians', or 'position'"
        assert 0 < velocity <= 100, "Velocity should be between 0 and 100"

        if(units == "degrees"):
            assert -90 < position <= 90, "Expected value -90< <=90"
        elif(units == "radians"):
            assert -1.5708 < position <= 1.5708, "Expected value -1.5708< <=1.5708"
        else:
            assert 0 <= position <= 10, "Expected value 0 <= >= 10"

        requests.post('http://'+self.ip+'/api/arms',
                      json={"Arm": arm, "Position": position, "Velocity": velocity, "Units": units})

    def moveArms(self, rightArmPosition, leftArmPosition, rightArmVelocity, leftArmVelocity, units="degrees"):
        units = units.lower()

        assert units == "degrees" or units == "radians" or units == "position", "Invalid unit. Please use 'degrees', 'radians', or 'position'"
        assert 0 < rightArmVelocity <= 100 and 0 < leftArmVelocity <= 100, "Velocity should be between 0 and 100"

        if(units == "degrees"):
            assert -90 < rightArmPosition <= 90 and - \
                90 < leftArmPosition <= 90, "Expected value -90< <=90"
        elif(units == "radians"):
            assert -1.5708 < rightArmPosition <= 1.5708 and - \
                1.5708 < leftArmPosition <= 1.5708, "Expected value -1.5708< <=1.5708"
        else:
            assert 0 <= rightArmPosition <= 10 and 0 <= leftArmPosition <= 10, "Expected value 0 <= >= 10"

        requests.post('http://' + self.ip + '/api/arms/set', json={
            "leftArmPosition": leftArmPosition,
            "rightArmPosition": rightArmPosition,
            "leftArmVelocity": leftArmVelocity,
            "rightArmVelocity": rightArmVelocity,
            "units": units
        })

    def moveArmsDegrees(self, rightArmPosition, leftArmPosition, rightArmVelocity, leftArmVelocity):
        self.moveArms(rightArmPosition, leftArmPosition,
                      rightArmVelocity, leftArmVelocity, "degrees")

    def stop(self):
        msg_body = {"motorMask": 7}
        response = requests.post(
            'http://' + self.ip + '/api/halt', params=msg_body).json()
        if response["status"] == "Success":
            return response["result"]
        elif response["status"] == "Failed":
            print("Error trying to stop Misty: ", response["error"])
        else:
            print("Error: Failed to stop.")

    def speak(self, text_to_speak):
        assert isinstance(
            text_to_speak, str), "Error: TTS: Input should be strings"

        msg_body = {"text": text_to_speak, "speechRate": 0.88}
        response = requests.post(
            'http://' + self.ip + '/api/tts/speak', params=msg_body).json()
        if response["status"] == "Success":
            print("Success!", response)
            return response["result"]
        elif response["status"] == "Failed":
            print("Error with local TTS: ", response["error"])
        else:
            print("Error: Failed to speak.")

    def uploadAudio(self, file_name, apply=False, overwrite=False):
        url = 'http://' + self.ip + '/api/audio'
        with open(file_name, 'rb') as f:
            encoded_string = base64.b64encode(f.read()).decode('ascii')
            data = {"FileName": file_name, "Data": encoded_string,
                    "ImmediatelyApply": apply, "OverwriteExisting": overwrite}
            requests.post(url, json=data)

    def playAudio(self, file_name):
        if file_name in self.audio_saved:
            requests.post('http://' + self.ip + '/api/audio/play',
                          json={"AssetId": file_name})
        else:
            print(file_name, "not found on the robot, use <robot_name>.printAudioList() to see the list of saved audio files")
