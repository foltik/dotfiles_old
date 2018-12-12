### Environment Variables ###
set -U fish_greeting
set -U fish_user_paths ~/.local/bin

# TTY for gpg pinentry
set -gx GPG_TTY (tty)
gpg-connect-agent updatestartuptty /bye >/dev/null

# Load wal colors if installed
if test -d ~/.cache/wal
    cat ~/.cache/wal/sequences &
end

# Load keymap
xkbcomp ~/.config/xkb/map.xkm $DISPLAY

### Aliases ###
function ls
    exa $argv
end
