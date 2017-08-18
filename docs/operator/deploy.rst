#######################
Deploy Software Factory
#######################

Requirements
============

SF deployment needs:

* A CentOS system
* **Minimum** 40GB of hardrive and 4GB of memory
* **Recommended** 80GB of hardrive and 8GB of memory
* A DNS entry for the FQDN of your SF deployment. SF can only be accessed by
  its FQDN (Authentication will fail if accessed via its IP)

Note that SF uses "sftests.com" as default FQDN and if the FQDN doesn't resolve
it needs to be locally set in */etc/hosts* file because the web interface
authentication mechanism redirects browser to the FQDN.

Always make sure to use the last stable release, the example below use the 2.6
version.


Rpm based deployment on CentOS 7
================================

On a CentOS system:

.. code-block:: bash

  $ sudo yum install -y https://softwarefactory-project.io/repos/sf-release-2.6.rpm
  $ sudo yum update -y
  $ sudo yum install -y sf-config
  $ sudo sfconfig.py


Configuration
-------------

The sfconfig process uses 2 configuration files to deploy software-factory:

* /etc/software-factory/sfconfig.yaml :ref:`Main configuration documentation<sfconfig>`
* /etc/software-factory/arch.yaml :ref:`Architecture configuration<sf-arch>`


Image based deployment
======================

OpenStack based deployment
--------------------------

To simplify and speed up the deployment process, a pre-built image should be used.
A new diskimage is created for each release, and it can be rebuilt locally to,
see :ref:`Image building<sfdib>`.


Install image
.............

SF image needs to be uploaded to Glance:

.. code-block:: bash

 $ curl -O http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/sf-2.6.qcow2
 $ glance image-create --progress --disk-format qcow2 --container-format bare --name sf-2.6.0 --file sf-2.6.qcow2

Deploy with Heat
................

Heat templates are available to automate the deployment process of different reference architecture.

They all requires:

* the SF image UUID
* the external Neutron network UUID (using "neutron net-list")
* the FQDN of the deployment (domain parameter)
* a key-pair name (you should have already created it on your account)

.. code-block:: bash

 $ wget http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/sf-2.6-softwarefactory-project.io.hot
 $ heat stack-create --template-file ./sf-2.6-softwarefactory-project.io.hot -P "key_name=SSH_KEY;domain=FQDN;image_id=GLANCE_UUID;external_network=NETWORK_UUID;flavor=m1.large" sf_stack

Once the stack is created jump to the section :ref:`Configuration and reconfiguration <reconfiguration>`.


Deploy with Nova
................

When Heat is not available, SF can also be deployed manually using the Nova CLI, or
using the web UI of your cloud provider.

Once the VM is created jump to the section :ref:`Configuration and reconfiguration <reconfiguration>`.
Don't forget to manage by yourself the security groups for the SF deployment :ref:`Network Access <network-access>`.


Kvm based deployment
--------------------

Prerequisites
.............

Ensure the following packages are installed (example for CentOS7 system)

.. code-block:: bash

  $ sudo yum install -y libvirt virt-install genisoimage qemu-img
  $ sudo systemctl start libvirtd && sudo systemctl enable libvirtd

Prepare the sf image
....................

SF image needs to be downloaded on your kvm host

.. code-block:: bash

  $ curl -O https://softwarefactory-project.io/releases/sf-2.6/sf-2.6.qcow2
  $ sudo mv sf-2.6.qcow2 /var/lib/libvirt/images
  $ sudo qemu-img resize /var/lib/libvirt/images/sf-2.6.qcow2 +20G

Prepare the cloud-init configuration files
..........................................

It's possible to use cloud-init without running a network service by providing
the meta-data and user-data files to the local vm on a iso9660 filesystem.

First, you have to adapt the following values:

.. code-block:: bash

  $ my_hostname=managesf
  $ my_domain=sfests.com
  $ my_ssh_pubkey=$(cat ~/.ssh/id_rsa.pub)

* create the user-data file

.. code-block:: bash

  $ cat << EOF >> user-data
  hostname: $my_hostname
  fqdn: $my_hostname.$my_domain

  groups:
    - centos

  users:
    - default
    - name: root
      ssh-authorized-keys:
        - $my_ssh_pubkey
    - name: centos
      gecos: RedHat Openstack User
      shell: /bin/bash
      primary-group: centos
      ssh-authorized-keys:
        - $my_ssh_pubkey
      sudo:
        - ALL=(ALL) NOPASSWD:ALL

  write_files:
    - path: /etc/sysconfig/network-scripts/ifcfg-eth0
      content: |
        DEVICE="eth0"
        ONBOOT="yes"
        TYPE="Ethernet"
        BOOTPROTO="none"
        IPADDR=192.168.122.10
        PREFIX=24
        GATEWAY=192.168.122.1
        DNS1=192.168.122.1
    - path: /etc/sysconfig/network
      content: |
        NETWORKING=yes
        NOZEROCONF=no
        HOSTNAME=$my_hostname
    - path: /etc/sysctl.conf
      content: |
        net.ipv4.ip_forward = 1

  runcmd:
    - /usr/sbin/sysctl -p
    - /usr/bin/sed  -i "s/\(127.0.0.1\)[[:space:]]*\(localhost.*\)/\1 $my_hostname.$my_domain $my_hostname \2/" /etc/hosts
    - /usr/bin/systemctl restart network
    - /usr/bin/sed  -i "s/requiretty/\!requiretty/" /etc/sudoers
  EOF

* create the meta-data file

.. code-block:: bash

  $ cat << EOF >> meta-data
  instance-id: $my_hostname-01
  local-hostname: $my_hostname.$my_domain
  EOF

* generate an iso image with user-data and meta-data files

.. code-block:: bash

  $ sudo genisoimage -output /var/lib/libvirt/images/$my_hostname.iso -volid cidata -joliet -rock user-data meta-data

* create a storage disk for the instance

.. code-block:: bash

  $ sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/sf-2.6.qcow2 /var/lib/libvirt/images/$my_hostname.qcow2

* boot the instance

.. code-block:: bash

  $ sudo virt-install --connect=qemu:///system --accelerate --boot hd --noautoconsole --graphics vnc --disk /var/lib/libvirt/images/$my_hostname.qcow2 --disk path=/var/lib/libvirt/images/$my_hostname.iso,device=cdrom --network bridge=virbr0,model=virtio --os-variant rhel7 --vcpus=4 --cpu host --ram 4096 --name $my_hostname

* You can connect to your instance using ssh, it's possible to use "virsh
  console $my_hostname" during the boot process to following the boot sequence.

.. code-block:: bash

  $ ssh 192.168.122.10 -l centos

.. _reconfiguration:

Configuration and reconfiguration
=================================

First time: **Please read** :ref:`Root password consideration<root-password>`.

* Connect as (root) via SSH to the install-server (the first instance deployed).
* Edit the configuration sfconfig.yaml (see :ref:`Main configuration documentation<sfconfig>`)

  * set the configuration according to your needs.
  * all parameters are editable and should be self-explanatory.

* Run configuration script.

.. code-block:: bash

 $ ssh -A root@sf_instance
 [root@managesf ~]# vim /etc/software-factory/sfconfig.yaml
 [root@managesf ~]# sfconfig.py


.. _network-access:

Network Access
==============

All network access goes through the main instance (called gateway). The FQDN
used during deployment needs to resolved to the instance IP. SF network
access goes through TCP ports:

* 22 for ssh access to reconfigure and update deployment
* 80/443 for web interface, all services are proxyfied on the managesf instance
* 29418 for gerrit access to submit code review

Note that Heat deployment and LXC deployment automatically configure
security group rules to allow these connections to the gateway.


SSL Certificates
================

By default, SF creates a self-signed certificate. To use another certificate,
you need to copy the provided files to /var/lib/software-factory/bootstrap-data/certs and
apply the change with the sfconfig.py script.

* gateway.crt: the public certificate
* gateway.key: the private key
* gateway.chain: the TLS chain file



Access Software Factory
=======================

The Dashboard is available at https://FQDN and admin user can authenticate
using "Internal Login". If you used the default domain *sftests.com* then
SF allows user "admin" with the default "userpass" password to connect.

If you need more information about authentication mechanisms on SF please refer to
:ref:`Software Factory Authentication <authentication>`.


.. _root-password:

Root password consideration
===========================

Software Factory image comes with an empty root password. root login is only
allowed via the console (**root login with password is not allowed via SSH**). The
empty root password is a facility for folks booting the SF image via a local
hypervisor (without a metadata server for cloud-init).

It is therefore **highly** recommended to deactivate root login via the console
**even booted on OpenStack**.

In order to do that:

.. code-block:: bash

  # echo "" > /etc/securetty

However setting a strong password is one of your possibility.

In environments such as OpenStack a metadata server is accessible and the user public
key will be installed for root and centos users. So user can access the SF node
via SSH using its private SSH key.

**Outside Openstack, when using a local hypervisor** at first root login via the
console the user need to add its public ssh key in */root/.ssh/authorized_key* in
order to be able to access SF node via SSH.
