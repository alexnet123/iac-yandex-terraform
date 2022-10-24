terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
 required_version = ">= 0.13"
}

provider "yandex" {
 
  token     = {={ token }=}
  cloud_id  = {={ cloud_id }=}
  folder_id = {={ folder_id }=}
  zone      = {={ zone }=}

}


#vm1#####################################################
resource "yandex_compute_instance" {={ hostname }=} {
  name = {={ hostname }=}
  platform_id = "standard-v3" #Intel Ice Lake

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = {={ image_id }=}
      size = 10       
  }

}

  network_interface {
    subnet_id = {={ subnet_id }=}
    nat       = true
  }
   
  metadata = {
    user-data = "${file("./meta.yaml")}"
  }

}
#vm1#####################################################


# output "internal_ip_address_vm_1" {
#   value = yandex_compute_instance.vm-1.network_interface.0.ip_address
# }

# output "external_ip_address_vm_1" {
#   value = yandex_compute_instance.vm-1.network_interface.0.nat_ip_address
# }


 resource "local_file" "hosts" {
  content = templatefile("hosts.tmpl",
    {
     external_ip_address_vm1 = yandex_compute_instance.{={ hostname }=}.network_interface.0.nat_ip_address
     user_vm1 = {={ user }=}
     hostname_vm1 = {={ hostname }=}
    }
  )
  filename = "hosts"
}