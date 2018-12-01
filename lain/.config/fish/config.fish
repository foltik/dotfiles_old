### Environment Variables ###
set -U fish_user_paths ~/.local/bin
# Use all cores for make by default
set -gx MAKEFLAGS -j(nproc)
# TTY for gpg pinentry
set -gx GPG_TTY (tty)
gpg-connect-agent updatestartuptty /bye >/dev/null
