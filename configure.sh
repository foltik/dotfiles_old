#!/bin/zsh

# Print Header
lnh() {
	print -Pn '%B%F{green}### '
	print -n $1
	print -P ' ###%f%b'
}

# Print subheader
ln() {
	print -Pn '%B%F{yellow}>>> '
	print -n $1
	print -P '%f%b'
}

pac_install() {
    if ! (pacman -Q $1 >/dev/null 2>&1);
    then
        ln "Installing $1 from Official Repos..."
        sudo pacman -S $1 --noconfirm
    fi;
}

aur_install() {
    if ! (pacman -Q $1 >/dev/null 2>&1);
    then
        ln "Installing $1 from AUR..."
        yaourt -S $1 --noconfirm
    fi;
}

svc_install() {
    sudo cp -v "$1" '/etc/systemd/system'
}

svc_install_user() {
    sudo cp -v "$1" '/etc/systemd/user'
}

svc_enable() {
    sudo systemctl enable $1
}

svc_enable_user() {
    systemctl --user enable $1
}

install_i3() {
    lnh "Installing i3"

    ln "Installing Packages"
    aur_install i3-gaps
    aur_install i3blocks-gaps-git
    aur_install i3lock
    aur_install i3lock-fancy-dualmonitors-git
    pac_install compton

	ln "Installing Services"
    svc_install cfg/systemd/system/suspend@.service # suspend locker
    svc_install_user cfg/systemd/user/locker.service # xautolock

	ln "Enabling Services"
	sudo systemctl daemon-reload
    svc_enable suspend@$USER.service
    svc_enable_user locker.service

	ln  "Installing Configuration Files"
	cp -v cfg/compton/config ~/.config/compton/config
	cp -v cfg/termite/ncmpcpp_config ~/.config/termite/ncmpcpp_config

	ln "Installing Tools"
	mkdir -pv ~/Documents/tools
	cp -v cfg/i3/tools/wallpaper.sh ~/Documents/tools/
	cp -v cfg/wallpapers/wallpaper* ~/Pictures/

	lnh "Select a Platform"
	platform_opt=("Desktop" "Laptop")
	select opt in "${platform_opt[@]}"
	do
		case $opt in
			"Desktop")
                lnh "Platform Not Supported with i3"
                exit
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
	ln "Installing Laptop Configuration Files"
	cp -v cfg/i3blocks/laptop/config ~/.config/i3blocks/config
	cp -rv cfg/i3blocks/laptop/blocks ~/.config/i3blocks/blocks
}

configure_common() {
	ln "Installing Common Configuration Files"
	# powerlevel9k
	sudo git clone https://github.com/bhilburn/powerlevel9k.git /usr/share/oh-my-zsh/themes/powerlevel9k
	
    # zsh
    cp -v cfg/zshrc ~/.zshrc
	
    # neovim
    cp -v cfg/nvim/init.vim ~/.config/nvim
	nvim +PlugInstall +qall
	
    # mpd
    awk '{gsub(/lain/,"'$USER'")}1' cfg/mpd/mpd.conf > mpd.conf.temp && mv mpd.conf.temp cfg/mpd/mpd.conf
	cp -rv cfg/mpd ~/.config/mpd
	
    # beets
    mkdir -pv ~/Music/beets
	cp -rv cfg/beets ~/.config/beets

    # ncmpcpp
    cp -v cfg/ncmpcpp/config ~/.ncmpcpp/

    ln "Installing Common Services"
    svc_enable_user mpd
    svc_enable NetworkManager
}

lnh "Select a Window Manager"
wm_opt=("Gnome" "i3")
select opt in "${wm_opt[@]}"
do
	case $opt in
		"Gnome")
            lnh "Window Manager Not Supported"
            exit
			break
			;;
		"i3")
			install_i3
			break
			;;
		*) echo "Invalid Option";;
	esac
done

configure_common
