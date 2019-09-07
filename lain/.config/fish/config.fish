### Environment Variables ###
set -U fish_greeting
set -U fish_user_paths ~/.local/bin
set -U FZF_LEGACY_KEYBINDINGS 0

# Mark fish as default shell
set -gx SHELL /usr/bin/fish

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

function ssh
    env TERM=xterm-256color ssh $argv
end

function emacs
    emacsclient -nc $argv
end
