:orphan:

#######################
Deploy Software Factory
#######################

.. _deployment_requirements:

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

Always make sure to use the last stable release, the example below use the 2.7
version.


.. _deployment_rpm_based:

Rpm based deployment on CentOS 7
================================

On a CentOS system:

.. code-block:: bash

  $ sudo yum install -y https://softwarefactory-project.io/repos/sf-release-2.7.rpm
  $ sudo yum update -y
  $ sudo yum install -y sf-config
  $ sudo sfconfig

.. _deployment_image_based:

Image based deployment
======================

This documentation describe 3 solutions to install Software Factory using
images provides by the project:

* :ref:`on openstack using heat <deployment_image_based_heat>`
* :ref:`on openstack using nova <deployment_image_based_nova>`
* :ref:`on kvm host using libvirtd <deployment_image_based_kvm>`

OpenStack based deployment
--------------------------

To simplify and speed up the deployment process, a pre-built image should be used.
A new diskimage is created for each release, and it can be rebuilt locally to,
see :ref:`Image building<sfdib>`.


.. _deployment_image_based_install_image:

Prepare the installation image
..............................

The Software Factory base image first needs to be created in Glance:

.. code-block:: bash

  $ curl -O https://softwarefactory-project.io/releases/sf-2.7/sf-2.7.qcow2
  $ openstack image create sf-2.7.0 --disk-format qcow2 --container-format bare --file softwarefactory-C7.0-2.7.0.img.qcow2

.. _deployment_image_based_heat:

Deploying with Heat
...................

Heat templates are available to automate the deployment process of different reference architecture.

These templates require the following parameters:

* ``image_id``: The Software Factory image UUID. This is obtained when
  uploading the `installation image <Prepare the installation image>`_.
* ``external_network``: The external Neutron network UUID. This is obained by
  querying Neutron with ``openstack network list``.
* ``domain``: The fully qualified domain name (FQDN) of the deployment.
* ``key_name``: The name of the keypair to provision on the servers. You can
  import a keypair in Nova with ``openstack keypair create`` or list existing
  keypairs with ``openstack keypair list``.

First, retrieve the template you're interested in, for example 'all in one':

.. code-block:: bash

 $ curl -O https://softwarefactory-project.io/releases/sf-2.7/sf-2.7-allinone.hot

Then, create the Heat stack:

.. code-block:: bash

  $ openstack stack create sf_stack --template softwarefactory-C7.0-2.7.0-allinone.hot \
      --parameter key_name=<key-name> \
      --parameter domain=<fqdn> \
      --parameter image_id=<glance image UUID> \
      --parameter external_network=<neutron external network uuid> \
      --parameter flavor=<flavor>

Once the stack is created jump to the section :ref:`Configuration and reconfiguration <configure_reconfigure>`.


.. _deployment_image_based_nova:

Deploying with Nova
...................

When Heat is not available, Software Factory can also be deployed manually using the Nova CLI, or
using the web UI of your cloud provider. You should first :ref:`install the software
factory image <deployment_image_based_install_image>`

Once the VM is created jump to the section :ref:`Configuration and reconfiguration <configure_reconfigure>`.
Don't forget to manage by yourself the security groups for the SF deployment :ref:`Network Access <configure_network_access>`.

.. _deployment_image_based_kvm:

Kvm based deployment
--------------------

Prerequisites
.............

Ensure the following packages are installed (example for CentOS7 system)

.. code-block:: bash

  $ sudo yum install -y libvirt virt-install genisoimage qemu-img
  $ sudo systemctl start libvirtd && sudo systemctl enable libvirtd

.. note::

  when you start libvirtd, a bridge named virbr0 is created. (using
  192.168.122.0/24 or 192.168.124.0/24 networks).

Prepare the installation image
..............................

SF image needs to be downloaded on your kvm host

.. code-block:: bash

  $ curl -O https://softwarefactory-project.io/releases/sf-2.7/sf-2.7.qcow2
  $ sudo mv sf-2.7.qcow2 /var/lib/libvirt/images
  $ sudo qemu-img resize /var/lib/libvirt/images/sf-2.7.qcow2 +20G

Prepare the cloud-init configuration files
..........................................

It's possible to use cloud-init without running a network service by providing
the meta-data and user-data files to the local vm on a iso9660 filesystem.

First, you have to adapt the following values:

.. code-block:: bash

  $ my_hostname=managesf
  $ my_domain=sftests.com
  $ my_ssh_pubkey=$(cat ~/.ssh/id_rsa.pub)

* create the user-data file

.. code-block:: bash

  $ cat << EOF >> user-data
  #cloud-config
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
        IPADDR=192.168.124.10
        PREFIX=24
        GATEWAY=192.168.124.1
        DNS1=192.168.124.1
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

  $ sudo qemu-img create -f qcow2 -b /var/lib/libvirt/images/sf-2.7.qcow2 /var/lib/libvirt/images/$my_hostname.qcow2

* boot the instance

.. code-block:: bash

  $ sudo virt-install --connect=qemu:///system --accelerate --boot hd --noautoconsole --graphics vnc --disk /var/lib/libvirt/images/$my_hostname.qcow2 --disk path=/var/lib/libvirt/images/$my_hostname.iso,device=cdrom --network bridge=virbr0,model=virtio --os-variant rhel7 --vcpus=4 --cpu host --ram 4096 --name $my_hostname

* You can connect to your instance using ssh, it's possible to use "virsh
  console $my_hostname" during the boot process to following the boot sequence.

.. code-block:: bash

  $ ssh 192.168.124.10 -l centos

Once the virtual machine is available, jump to the section :ref:`Configuration and reconfiguration <configure_reconfigure>`.
