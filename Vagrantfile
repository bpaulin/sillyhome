# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "home-dev"

  config.vm.box = "archlinux/archlinux"

  config.vm.network "forwarded_port", guest: 80, host: 9980
  config.vm.network "forwarded_port", guest: 443, host: 9943

  config.vm.provider "virtualbox" do |v|
      v.memory = 4096
      v.cpus = 4
  end
end
