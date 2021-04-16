#!/bin/bash

if [ -z $1 ]; then
    echo "Need to specify condition of who Misty cheats in favor of <control, robot,  human>!"
    exit
fi

cd teleop
python3 playGame.py $1 $2
cd ..
