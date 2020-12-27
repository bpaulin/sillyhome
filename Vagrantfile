# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "archlinux/archlinux"
  config.vm.network "public_network"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 3072
    vb.cpus = 4
  end
  config.vm.provision "shell", inline: <<-SHELL
    pacman -Syy docker docker-compose --noconfirm
    usermod -a -G docker vagrant
    systemctl enable docker
    systemctl start docker
  SHELL
end
