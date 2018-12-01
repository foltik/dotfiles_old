# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# Unless we are running bash with a command explicitly (-c), drop into fish
if [ -z "$BASH_EXECUTION_STRING" ]; then
    exec fish
fi
