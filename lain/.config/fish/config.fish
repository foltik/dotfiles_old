### Environment Variables ###
set -U fish_greeting
set -U fish_user_paths ~/.local/bin

# Use all cores for make by default
set -gx MAKEFLAGS -j(nproc)

# TTY for gpg pinentry
set -gx GPG_TTY (tty)
gpg-connect-agent updatestartuptty /bye >/dev/null

# Load wal colors if installed
if test -d ~/.cache/wal
    cat ~/.cache/wal/sequences &
end

# Load autojump if installed
begin
    set -l AUTOJUMP_PATH /usr/share/autojump/autojump.fish
    if test -e $AUTOJUMP_PATH
        source $AUTOJUMP_PATH
    end
end

### Aliases ###
function ls
    exa $argv
end
