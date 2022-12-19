terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
 required_version = ">= 0.13"
}

provider "yandex" {
 
  token     = "{={ token }=}"
  cloud_id  = "{={ cloud_id }=}"
  folder_id = "{={ folder_id }=}"
  zone      = "{={ zone }=}"

}


#vm1#####################################################

resource "yandex_compute_instance" "vm" {
  count = 2
   name = "{={ hostname }=}${count.index}"
  platform_id = "standard-v3" #Intel Ice Lake

  resources {
    cores  = {={ vm_Vcpu }=}
    memory = {={ vm_memory }=}
  }

  boot_disk {
    initialize_params {
      image_id = "{={ image_id }=}"
      size = {={ vm_disk_size }=}       
  }

}

  network_interface {
    subnet_id = yandex_vpc_subnet.sub_net1.id
    #nat       = true
  }
   
  metadata = {
    user-data = "${file("./meta.yaml")}"
  }

}
#vm1#####################################################


#net####################################################
resource "yandex_vpc_network" "net1" {
name = "net1"
}
#net####################################################

#sub_net################################################
resource "yandex_vpc_subnet" "sub_net1" {
name = "sub_net1"
zone = "{={ zone }=}"
network_id = yandex_vpc_network.net1.id
v4_cidr_blocks = ["10.11.1.0/24"]
}
#sub_net################################################


#target group############################################

resource "yandex_lb_target_group" "balancergr1" {
  name           = "balancergr1"

  target {
    subnet_id    = yandex_vpc_subnet.sub_net1.id
    address   = yandex_compute_instance.vm[0].network_interface.0.ip_address
  }

  target {
    subnet_id    = yandex_vpc_subnet.sub_net1.id
    address   = yandex_compute_instance.vm[1].network_interface.0.ip_address
  }

}

#target group############################################


#balancer################################################

resource "yandex_lb_network_load_balancer" "balancer" {
  name = "balancer"
  listener {
    name = "balancer-listener"
    port = 80
    # external_address_spec {
    #   ip_version = "ipv4"
    # }
  }
  attached_target_group {
    target_group_id = yandex_lb_target_group.balancergr1.id
    healthcheck {
      name = "http"
        http_options {
          port = 80
          path = "/"
        }
    }
  }
}

#balancer################################################



# output "internal_ip_address_vm_1" {
#   value = yandex_compute_instance.vm-1.network_interface.0.ip_address
# }

# output "external_ip_address_vm_1" {
#   value = yandex_compute_instance.vm-1.network_interface.0.nat_ip_address
# }


 resource "local_file" "hosts" {
  content = templatefile("hosts.tmpl",
    {
     external_ip_address_vm0 = yandex_compute_instance.vm[0].network_interface.0.nat_ip_address
     user_vm0 = "{={ user }=}"
     hostname_vm0 = "{={ hostname }=}0"
     external_ip_address_vm1 = yandex_compute_instance.vm[1].network_interface.0.nat_ip_address
     user_vm1 = "{={ user }=}"
     hostname_vm1 = "{={ hostname }=}1"
    }
  )
  filename = "{={ hosts_path }=}"
}
