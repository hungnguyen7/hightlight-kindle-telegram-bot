#!/bin/bash

# Script to keep a process running after an SSH session ends
# Usage: ./run_in_background.sh [nohup|tmux|screen] "your_command"

if [ $# -ne 2 ]; then
    echo "Usage: $0 [nohup|tmux|screen] \"your_command\""
    exit 1
fi

METHOD=$1
COMMAND=$2

case $METHOD in
    nohup)
        echo "Running command with nohup..."
        nohup $COMMAND > output.log 2>&1 &
        echo "Command is running in the background with nohup. Output is redirected to output.log."
        ;;
    
    tmux)
        echo "Running command inside a new tmux session..."
        tmux new-session -d "$COMMAND"
        echo "Command is running inside a tmux session. Use 'tmux attach' to reattach to the session."
        ;;

    screen)
        echo "Running command inside a new screen session..."
        screen -dm bash -c "$COMMAND"
        echo "Command is running inside a screen session. Use 'screen -r' to reattach to the session."
        ;;

    *)
        echo "Invalid method. Please choose from [nohup|tmux|screen]."
        exit 1
        ;;
esac
