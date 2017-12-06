#!/bin/bash

killall -q xwinwrap

idx=$(( (RANDOM % 5) + 1))
if [[ $idx -eq 5 ]];
then
	xwinwrap -ov -fs -- gifview -w WID -a /home/lain/Pictures/wallpaper.gif 2>/dev/null
else
	feh --bg-scale /home/lain/Pictures/wallpaper$idx.jpg
fi
