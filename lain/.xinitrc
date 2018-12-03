#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/x11/xinit/.Xresources
sysmodmap=/etc/x11/xinit/.Xmodmap

# merge in defaults and keymaps
if [ -f $sysresources ]; then xrdb -merge $sysresources; fi
if [ -f $sysmodmap ]; then xmodmap $sysmodmap; fi
if [ -f $userresources ]; then xrdb -merge $userresources; fi
if [ -f $usermodmap ]; then xmodmap $usermodmap; fi

if [ -d /etc/x11/xinit/xinitrc.d ]; then
    for f in /etc/x11/xinit/xinitrc.d/?*.sh ; do
        [ -x "$f" ] && . "$f"
    done
    unset f
fi

# The window manager will open this named pipe, closing it once it exits.
mkfifo "${XDG_RUNTIME_DIR}/x11-wm@${DISPLAY:1:2}"

# Delete the pipe on exit
trap "rm -f ${XDG_RUNTIME_DIR}/x11-wm@${DISPLAY:1:2}" EXIT

# Fork a process that will exit once the pipe is closed
cat < "${XDG_RUNTIME_DIR}/x11-wm@${DISPLAY:1:2}" &

systemctl --user start "x11@${DISPLAY:1:2}.target" &
# Wait for the pipe (window manager) to close
wait
systemctl --user stop "x11@${DISPLAY:1:2}.target" & 
