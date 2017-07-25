#!/bin/zsh

lnh() {
	print -Pn '%B%F{green}### '
	print -n $1
	print -P ' ###%f%b'
}

lnf() {
	print -Pn '%B%F{yellow}>>>%f%b '
}

lnfb() {
	print -P '%B%F{blue}>>> [['
	
lnfbe() {
	print -P '%B%F{blue}<<<

ln() {
	Print -Pn '%B%F{yellow}>>> '
	Print -n $1
	Print -P '%f%b'
}

install_i3() {
	if ! (pacman -Q i3-gaps >/dev/null 2>&1);
	then
		lnh "Installing i3-gaps from AUR..."
		yaourt -S i3-gaps --noconfirm
	fi;

	if ! (pacman -Q i3blocks-gaps-git >/dev/null 2>&1);
	then
		lnh "Installing i3blocks-gaps-git from AUR..."
		yaourt -S i3blocks-gaps-git --noconfirm
	fi;

	if ! (pacman -Q i3lock >/dev/null 2>&1);
	then
		lnh "Installing i3lock"
		pacman -S i3lock --noconfirm
	fi;


	if ! (pacman -Q i3lock-fancy-dualmonitors-git >/dev/null 2>&1);
	then
		lnh "Installing i3lock-fancy"
		yaourt -S i3lock-fancy-dualmonitors-git --noconfirm
	fi;

	if ! (pacman -Q compton >/dev/null 2>&1);
	then
		lnh "Installing Compton..."
		pacman -S compton --noconfirm
	fi;

	### Configuration Files
	lnh  "Installing General Configuration Files"
	# i3
	lnf
	cp -v config/i3/laptop/config ~/.config/i3/config
	# Compton
	lnf
	cp -v config/compton/config ~/.config/compton/config
	# NCMPCPP config
	lnf
	cp -v config/termite/ncmpcpp_config ~/.config/termite/ncmpcpp_config

	### Install Tools
	lnh "Installing General Tools"
	mkdir -p ~/Documents/tools
	# Wallpaper Tool
	lnf
	cp -v config/i3/tools/wallpaper.sh ~/Documents/tools/
	lnf
	cp -v config/wallpapers/wallpaper* ~/Pictures/

	### Install Service Files
	lnh "Installing Services"
	lnf
	sudo cp -v config/systemd/system/suspend@.service /etc/systemd/system/
	lnf
	sudo cp -v config/systemd/user/locker.service /etc/systemd/user
	sudo systemctl daemon-reload
	lnh "Enabling Services"
	lnf
	sudo systemctl enable suspend@$USER.service	
	lnf
	systemctl --user enable locker.service

	echo "Select a Platform"
	platform_opt=("Desktop" "Laptop")
	select opt in "${platform_opt[@]}"
	do
		case $opt in
			"Desktop")
				break
				;;
			"Laptop")
				install_i3_laptop
				break
				;;
			*) echo "Invalid Option";;
		esac
	done
}

install_i3_laptop() {
}

echo "Select a Window Manager"
wm_opt=("Gnome" "i3")
select opt in "${wm_opt[@]}"
do
	case $opt in
		"Gnome")
			echo "gnome"
			break
			;;
		"i3")
			echo "i3"
			install_i3
			break
			;;
		*) echo "Invalid Option";; 
	esac
done
