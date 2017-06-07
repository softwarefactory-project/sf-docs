Deploy Software Factory
=======================

Requirements
------------

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


Local deployment
----------------

On a CentOS system:

.. code-block:: bash

  $ sudo yum install -y https://softwarefactory-project.io/repos/sf-release-2.6.rpm
  $ sudo yum update -y
  $ sudo yum install -y sf-config
  $ sudo sfconfig.py


Configuration
.............

The sfconfig process uses 2 configuration files to deploy software-factory:

* /etc/software-factory/sfconfig.yaml :ref:`Main configuration documentation<sfconfig>`
* /etc/software-factory/arch.yaml :ref:`Architecture configuration<sf-arch>`


OpenStack based deployment
--------------------------

To simplify and speed up the deployment process, a pre-built image should be used.
A new diskimage is created for each release, and it can be rebuilt locally to,
see :ref:`Image building<sfdib>`.


Install image
.............

SF image needs to be uploaded to Glance:

.. code-block:: bash

 $ curl -O http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/softwarefactory-C7.0-2.6.0.img.qcow2
 $ glance image-create --progress --disk-format qcow2 --container-format bare --name sf-2.6.0 --file softwarefactory-C7.0-2.6.0.img.qcow2


Deploy with Heat
................

Heat templates are available to automate the deployment process of different reference architecture.

They all requires:

* the SF image UUID
* the external Neutron network UUID (using "neutron net-list")
* the FQDN of the deployment (domain parameter)
* a key-pair name (you should have already created it on your account)

.. code-block:: bash

 $ wget http://46.231.132.68:8080/v1/AUTH_b50e80d3969f441a8b7b1fe831003e0a/sf-images/softwarefactory-C7.0-2.6.0-allinone.hot
 $ heat stack-create --template-file ./softwarefactory-C7.0-2.6.0-allinone.hot -P "key_name=SSH_KEY;domain=FQDN;image_id=GLANCE_UUID;external_network=NETWORK_UUID;flavor=m1.large" sf_stack

Once the stack is created jump to the section :ref:`Configuration and reconfiguration <reconfiguration>`.


Deploy with Nova
................

When Heat is not available, SF can also be deployed manually using the Nova CLI, or
using the web UI of your cloud provider.

Once the VM is created jump to the section :ref:`Configuration and reconfiguration <reconfiguration>`.
Don't forget to manage by yourself the security groups for the SF deployment :ref:`Network Access <network-access>`.


.. _reconfiguration:

Configuration and reconfiguration
---------------------------------

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
--------------

All network access goes through the main instance (called gateway). The FQDN
used during deployment needs to resolved to the instance IP. SF network
access goes through TCP ports:

* 22 for ssh access to reconfigure and update deployment
* 80/443 for web interface, all services are proxyfied on the managesf instance
* 29418 for gerrit access to submit code review

Note that Heat deployment and LXC deployment automatically configure
security group rules to allow these connections to the gateway.


SSL Certificates
----------------

By default, SF creates a self-signed certificate. To use another certificate,
you need to copy the provided files to /var/lib/software-factory/bootstrap-data/certs and
apply the change with the sfconfig.py script.

* gateway.crt: the public certificate
* gateway.key: the private key
* gateway.chain: the TLS chain file



Access Software Factory
-----------------------

The Dashboard is available at https://FQDN and admin user can authenticate
using "Internal Login". If you used the default domain *sftests.com* then
SF allows (user1, user2, user3) with the default "userpass" password to connect.

If you need more information about authentication mechanisms on SF please refer to
:ref:`Software Factory Authentication <authentication>`.


.. _root-password:

Root password consideration
---------------------------

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
