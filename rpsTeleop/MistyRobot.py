# Last Update Jan 14 2021
import requests
from time import sleep

class MistyRobot:
    """This is a Python Wrapper for Misty's RESTful calls and websockets"""

    def __init__(self, ip, debug=False):
        self.ip = ip
        self.debug = debug

    def moveArms(self, leftPosition, rightPosition, leftVelocity, rightVelocity):
        msg_body = {
            "LeftArmPosition": leftPosition,
            "RightArmPosition": rightPosition,
            "LeftArmVelocity": leftVelocity,
            "RightArmVelocity": rightVelocity
        }

        response = requests.post(
            'http://' + self.ip + '/api/arms/set', params=msg_body).json()
        if response["status"] == "Success":
            return response["result"]
        elif response["status"] == "Failed":
            print("Error trying to move arms: ", response["error"])
        else:
            print("Error: Failed to move arms.")

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

    def playAudio(self, audio):
        msg_body = {
            "Filename": "../audio" + audio
        }

        response = requests.post(
            'http://' + self.ip + '/api/audio/play', params=msg_body).json()
        if response["status"] == "Success":
            return response["result"]
        elif response["status"] == "Failed":
            print("Error trying to drive: ", response["error"])
        else:
            print("Error: Failed to drive.")