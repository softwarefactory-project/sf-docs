Configure nodepool(V3)
======================

The nodepool(V3) service is installed with the rh-python35 software collections:

* The configuration is located in /etc/nodepool3
* The logs are written to /var/log/nodepool3
* The services are prefixed with rh-python35-

A convenient wrapper for the command line is installed in /usr/bin/nodepool3.

... Use a local build of nodepool-doc instead of external link

For further details, please check the upstream documentation_.

.. _documentation: https://docs.openstack.org/infra/nodepool/feature/zuulv3


Required architecture
---------------------

For a minimal deployment, limited to containerized nodes, only the **nodepool3-launcher**
and **hypervisor-oci** components are required in the architecture file.

In order to use virtual nodes based on diskimage, the **nodepool3-builder**
component must be present in the architecture file.

Add a cloud provider
--------------------

To do this, an account on an OpenStack cloud is required and credentials need to
be known by Nodepool. It is highly recommended to use a project dedicated to
Nodepool, into which the slave instances will be spawned.

The slave instances inherit the project's "default" security group for access
rules. Therefore the project's "default" security group must **at least** allow
incoming SSH traffic (TCP/22) from the zuul-executor node. More permissive access
can be considered if others should be allowed to SSH into test nodes. Please
refer to `OpenStack's documentation <https://docs.openstack.org/nova/pike/admin/security-groups.html>`
to find out how to modify security groups.

In order to configure Nodepool to define a provider (an OpenStack cloud account) you need
to adapt sfconfig.yaml. Indeed you need to add the cloud client information
(auth url, login, password...) to the sfconfig.yaml.
See the :ref:`Nodepool user documentation<nodepool-user>` for additional provider settings
such as labels and diskimages.

Below is an example of configuration.

.. code-block:: yaml

 nodepool3:
   providers:
     - name: default
       auth_url: http://localhost:5000/v2.0
       project_id: 'tenantname'
       username: 'user'
       password: 'secret'
       region_name: ''
       # Uncomment and set domain-related values when using a keystone v3 authentication endpoint
       # user_domain_name: Default
       # project_domain_name: Default

To apply the configuration you need to run again the sfconfig script.

You should be able to validate the configuration via the nodepool client by checking if
Nodepool is able to authenticate on the cloud account.

.. code-block:: bash

 $ nodepool3 list
 $ nodepool3 image-list


See the :ref:`Nodepool user documentation<nodepool-user>` for configuring additional
settings on the providers as well as defining labels and diskimages.

As an administrator, it can be really useful to check
/var/log/nodepool3 to debug the Nodepool configuration.


Setup the OCI container provider
--------------------------------

The role **hypervisor-oci** can be added to the architecture file. This role will
install the requirements and configure the node to provide Open Container with *runc*.
It is only compatible with centos 7. Containers *bind mount* the local host
filesystem, that means you don't have to configure an image, what is installed on
the instance is available inside the containers. The role can be defined on multiple
nodes in order to scale.

Note that the OCI provider doesn't provide network isolation and slave needs to run an
a dedicated instance/network. sfconfig will refuses to install this role on the internal
network where Software Factory services are running. Nevertheless you can bypass this
protection by using the sfconfig's option *--enable-insecure-slaves*.

Please refer to :ref:`Extending the architecture<architecture_extending>` for adding a node
to the architecture then run sfconfig.

Note that *config/nodepoolV3/_local_hypervisor_oci.yaml* will by automatically updated
making OCI provider(s) available in Nodepool.

Please make sure the TCP port range 22022 to 65535 is open to incoming traffic
on the **hypervisor-oci** node(s).


Useful commands
---------------

List instances slave instances and their status (used, building ...). Use the *--detail**
option to get the public IP of the instances:

.. code-block:: bash

 $ nodepool3 list

Trigger an diskimage build. The image will be automatically uploaded on the provider(s)
after a successful build:

.. code-block:: bash

 $ nodepool3 image-build *image-name*

Logs of build diskimage processes are available in */var/www/nodepool3-log/* on
the nodepool3-builder node but also via https://sftests.com/nodepool3-log/.

List nodepool instance images available on the configured providers and their
status:

.. code-block:: bash

 $ nodepool3 image-list

List instance diskimages built by Disk Image Builder (DIB) and their status:

.. code-block:: bash

 $ nodepool3 dib-image-list
