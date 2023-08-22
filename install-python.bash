cd /data/data/com.termux/files/home

cat << "EOF" | sed -r 's/^(\t| )*//g' > install-python.bash
#!/bin/bash

main () {
    DO "update_packages"
    DO "install_packages"
    DO "install_ubuntu"
    DO "change_ubuntu_startup"
    DO "change_termux_startup"
    DO "ask_to_restart_termux"
}

ask_to_restart_termux () {
    ECHO "Please exit termux and open it again to continue the installation. Pressing enter will exit termux."
    read
    exit
}

change_termux_startup () {
    home_path="/data/data/com.termux/files/home"
    sed -ir '/#startup/d' $home_path/.bashrc
    cat << "EOF2" >> $home_path/.bashrc
        source /data/data/com.termux/files/home/startup.bash #startup
    EOF2
}

change_ubuntu_startup () {
    ubuntu_path="/data/data/com.termux/files/home/ubuntu-in-termux/ubuntu-fs/root"
    sed -ir '/#first_startup/d' $ubuntu_path/.bashrc
    cat << "EOF2" >> $ubuntu_path/.bashrc
        sed -ir '/#first_startup/d' /data/data/com.termux/files/home/ubuntu-in-termux/ubuntu-fs/root/.bashrc #first_startup
        source /data/data/com.termux/files/home/install-python-2.bash #first_startup
    EOF2
}

install_ubuntu () {
    clone_path="/data/data/com.termux/files/home/ubuntu-in-termux"
    DO "git clone https://github.com/MFDGaming/ubuntu-in-termux.git $clone_path"
    ubuntu_installer_path="$clone_path/ubuntu.sh"
    chmod +x $ubuntu_installer_path
    cd $clone_path
    yes | DO "bash $ubuntu_installer_path"
}

install_packages () {
    yes | (
        DO "apt install git"
        DO "apt install proot"
        DO "apt install wget"
    )
}

update_packages () {
    yes | (
        DO "apt update"
        DO "apt upgrade"
        DO "apt update"
    )
}

DO () {
    str="$@"
    ECHO "$str"
    $str
}

ECHO () {
    str="$@"
    echo -e "\n\e[1;31m$str\e[m\n"
}

main
EOF





cat << "EOF" | sed -r 's/^(\t| )*//g' > install-python-2.bash
#!/bin/bash

main () {
    DO "update_packages"
    DO "install_packages"
    DO "exit_ubuntu"
}

exit_ubuntu () {
    exit
}

install_packages () {
    yes | (
        DO "install_vim"
        DO "apt install python3-pip"
        DO "apt install mypy"
        DO "apt install git"
        DO "install_expect"
    )
}

install_expect () {
    DO "ln -fs /usr/share/zoneinfo/$ZONE_INFO /etc/localtime"
    DO "DEBIAN_FRONTEND=noninteractive apt install tzdata"
    DO "dpkg-reconfigure --frontend noninteractive tzdata"
    DO "apt install expect"
}

install_vim () {
    DO "apt install vim"
    sed -ir '/"autoset/d' /usr/share/vim/vimrc
    echo 'set shiftwidth=4 tabstop=4 "autoset' >> /usr/share/vim/vimrc
}

update_packages () {
    yes | DO "apt update"
}

DO () {
    str="$@"
    ECHO "$str"
    $str
}

ECHO () {
    str="$@"
    echo -e "\n\e[1;31m$str\e[m\n"
}

main
EOF




cat << "EOF" | sed -r 's/^(\t| )*//g' > startup.bash
#!/bin/bash

main () {
    DO "clear_screen"
    DO "start_ubuntu"
    DO "exit_termux"
}

exit_termux () {
    ECHO "Press enter to exit termux."
    read
    exit
}

start_ubuntu () {
    cd /data/data/com.termux/files/home/ubuntu-in-termux
    ./startubuntu.sh
}

clear_screen () {
    clear
    ECHO "Screen cleared."
}

DO () {
    str="$@"
    ECHO "$str"
    $str
}

ECHO () {
    str="$@"
    echo -e "\n\e[1;31m$str\e[m\n"
}

main
EOF

chmod +x install-python.bash
chmod +x install-python-2.bash
chmod +x startup.bash
source install-python.bash
