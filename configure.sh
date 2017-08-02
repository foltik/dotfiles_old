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
	print -P '%B%F{yellow}[[[%f%b'
}

lnfbe() {
	print -P '%B%F{yellow}]]]'
}

ln() {
	Print -Pn '%B%F{yellow}>>> '
	Print -n $1
	Print -P '%f%b'
}

install_i3() {
	# Install Packages
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

	### Install Service Files
	lnh "Installing Services"
	# Suspend locker
	lnf
	sudo cp -v cfg/systemd/system/suspend@.service /etc/systemd/system/
	# Auto locker
	lnf
	sudo cp -v cfg/systemd/user/locker.service /etc/systemd/user
	sudo systemctl daemon-reload
	lnh "Enabling Services"
	lnf
	sudo systemctl enable suspend@$USER.service
	lnf
	systemctl --user enable locker.service


	### Install Configuration Files
	lnh  "Installing General Configuration Files"
	# Compton
	lnf
	cp -v cfg/compton/config ~/.config/compton/config
	# NCMPCPP ws10 config
	lnf
	cp -v cfg/termite/ncmpcpp_config ~/.config/termite/ncmpcpp_config

	### Install Tools
	lnh "Installing General Tools"
	mkdir -p ~/Documents/tools
	# Wallpaper Tool
	lnf
	cp -v cfg/i3/tools/wallpaper.sh ~/Documents/tools/
	lnfb
	cp -v cfg/wallpapers/wallpaper* ~/Pictures/
	lnfbe

	lnh "Select a Platform"
	platform_opt=("Desktop" "Laptop")
	select opt in "${platform_opt[@]}"
	do
		case $opt in
			"Desktop")
				break
				;;
			"Laptop")
				lnh "Installing i3"
				install_i3_laptop
				break
				;;
			*) echo "Invalid Option";;
		esac
	done
}

install_i3_laptop() {
	lnh "Installing Laptop Configuration Files"
	# i3blocks
	lnf
	cp -v cfg/i3blocks/laptop/config ~/.config/i3blocks/config
	lnf
	mkdir ~/.config/i3blocks/blocks
	lnfb
	cp -v cfg/i3blocks/laptop/blocks/* ~/.config/i3blocks/blocks/
	lnfbe
}

configure_common() {
	lnh "Installing Common Configuration Files"
	# ZSH
	lnf
	cp -v cfg/zshrc ~/.zshrc

	# VIM
	lnf
	cp -v cfg/vimrc ~/.vimrc
	# Install Vim Plugins
	vim +PlugInstall +qall

	# MPD + NCMPCPP
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
			install_i3
			break
			;;
		*) echo "Invalid Option";;
	esac
done
