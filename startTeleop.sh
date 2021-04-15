#!/bin/bash

if [ -z $1 ];
    echo "Need to specify condition of who Misty cheats in favor of <control, robot,  human>!"
    exit
fi

cd teleop
python playGame $1 $2
cd ..
