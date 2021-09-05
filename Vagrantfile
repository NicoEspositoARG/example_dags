# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "ariflow-lab"
  config.vm.define "airflow-lab"
  config.vm.provision "docker",
    images: ["apache/airflow:2.1.2","postgres:13", "redis:latest"]
  config.vm.provision :shell, path: "bootstrap.sh", :privileged => false
  config.vm.network :forwarded_port, guest: 8080, host: 9090, host_ip: "127.0.0.1"
  config.vm.network :forwarded_port, guest: 5555, host: 5555, host_ip: "127.0.0.1"

  
  config.vm.provider "virtualbox" do |vb|
    vb.name = "airflow-lab"
    vb.memory = "2048"
    vb.cpus = 2
  end

end
