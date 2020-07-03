.. _nodepool-operator:

.. note::

  This is a lightweight documentation intended to get operators started with setting
  up the Nodepool service. For more insight on what Nodepool can do, please refer
  to its upstream documentation_.

.. _documentation: https://zuul-ci.org/docs/nodepool

Operate nodepool
================

* The configuration is located in /etc/nodepool
* The logs are written to /var/log/nodepool


Architecture
------------

Minimal
.......

The **nodepool-launcher** component is required in the architecture file to
enable nodepool.


Podman containers
.................

A new minimal kubernetes driver using podman container is available through the
**hypervisor-k1s** component.

To use the kubernetes container driver, add the **hypervisor-k1s** component to the
architecture file or check the
:ref:`k1s manual setup<nodepool-manual-operator-k1s>` below.

.. _nodepool-operator-dib:

Diskimage-builder
.................

To manage custom images through the config repository, built using diskimage-builder
(DIB), add the **nodepool-builder** component in the architecture file.

.. tip::

  With diskimage-builder, Software Factory users can customize test images without
  the need for specific authorizations on the OpenStack project. And since custom
  images definitions are subject to reviews on the config repository, operators
  can choose to allow or reject these images.

DIB can build images from scratch using elements, and it is also possible to use
a local image as a base and add elements on top of it (this is mandatory for
RHEL image, check :ref:`nodepool user documentation <nodepool-user-rhel>`). The
operator can store base images on the host where the **nodepool-builder**
service is deployed in */var/lib/nodepool/images*.


.. _nodepool-autohold:

Accessing test resources on failure (autohold)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To get a persistent shell access to test resources, use the autohold feature:

* From the zuul-scheduler host, run this command (the --change argument is optional):

.. code-block:: bash

   zuul autohold --tenant <tenant-name> --project <project-name> --job <job-name> --reason "text-string" [--change <change-id>]

* Check the hold is registered using `zuul autohold-list`

* Wait for a job failure and get the node ip using `nodepool list --detail | grep "text-string"`

* Connect to the instance using `ssh -i ~zuul/.ssh/id_rsa <username>@<ip>`, the username can be `zuul` or `zuul-worker` depending on how the label has been built. You can add more public keys and share the access.

* Once you are done with the instance, run `nodepool delete <nodeid>`


.. _nodepool-operator-password:

Storing registration password to build RHEL image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To provide the password environment variable to the nodepool-builder service,
you have add image name and registration password in
/etc/software-factory/sfconfig.yaml:

.. code-block:: bash

   nodepool:
     ...
     dib_reg_passwords:
       - image_name: rhel-7
         reg_password: rhsm_password

Then run sfconfig --skip-install to finish the configuration.

Add a cloud provider
--------------------

To add a cloud provider, an OpenStack cloud account is required.
It is highly recommended to use a project dedicated to
Nodepool.

The slave instances inherit the project's "default" security group for access
rules. Therefore the project's "default" security group must allow incoming SSH
traffic (TCP/22) and incoming log stream port (TCP/19885) from the zuul-executor
node. Please refer to `OpenStack's documentation
<https://docs.openstack.org/nova/queens/admin/security-groups.html>`_ to find out
how to modify security groups.

In order to configure an OpenStack provider you need
to copy the *clouds.yaml* file to /etc/software-factory/ and set this configuration
in sfconfig.yaml:

.. code-block:: yaml

 nodepool:
   clouds_File: /etc/software-factory/clouds.yaml

To apply the configuration you need to run again the sfconfig script.

You should be able to validate the configuration via the nodepool client by checking if
Nodepool is able to authenticate on the cloud account.

.. code-block:: bash

 $ nodepool list
 $ nodepool image-list


See the :ref:`Nodepool user documentation<nodepool-user>` for configuring additional
settings on the providers as well as defining labels and diskimages.

As an administrator, it can be really useful to check
/var/log/nodepool to debug the Nodepool configuration.

.. _nodepool-operator-k1s:

Setup a k1s provider using the hypervisor-k1s role
..................................................

The role **hypervisor-k1s** can be added to the architecture file. This role
will install the requirements and configure the node.
This role must be installed on a Centos 7 instance.

Please refer to :ref:`Extending the architecture<architecture_extending>` for
adding a node to the architecture, then run sfconfig.

.. warning::

  The k1s provider doesn't enforce network isolation and test containers need to run on
  a dedicated instance/network. sfconfig will refuse to install this role on a
  server where Software Factory services are running. Nevertheless you can
  bypass this protection by using the sfconfig's
  option *--enable-insecure-slaves*.

.. note::

  Note that *config/nodepool/_local_hypervisor_k1s.yaml* and
  *config/nodepool/_pods.yaml* will by automatically updated in the config repository,
  making the k1s provider(s) and the default pod (test container) available in Nodepool.

The zuul-executors hosts need to be allowed to connect to the k1s hosts
via 9023/TCP.

.. _nodepool-manual-operator-k1s:

Define and use container images with the k1s provider
.....................................................

A new container image must be stored in the *config/containers/* directory.
The filename must be *Dockerfile*.

You need to ensure that the following lines are part of the new Dockerfile:

.. code-block:: bash

  RUN mv /etc/sudoers /etc/sudoers.d/zuul && grep includedir \
    /etc/sudoers.d/zuul > /etc/sudoers && sed -e 's/.*includedir.*//' -i \
    /etc/sudoers.d/zuul && chmod 440 /etc/sudoers
  RUN echo "zuul:x:0:0:root:/root:/bin/bash" >> /etc/passwd

The *config-update* job builds the new container and publish the container
image into the k1s hosts local registry.

.. code-block:: bash

  [root@managesf.sftests.com config]# podman images | grep k1s
  localhost/k1s/centos-7-alt   latest   b205360ccab6   2 hours ago    699 MB
  localhost/k1s/centos-7       latest   c75f523a04de   2 hours ago    699 MB

The name of the container image is the directory name of the container.

To make the new container image available to Nodepool then a new label must be
defined and linked to k1s providers.

For a new container images called centos-7-alt, edit *config/nodepool/k1s-labels.yaml*:

.. code-block:: yaml

  labels:
  - name: pod-centos-7-alt
    min-ready: 1

  extra-labels:
    - provider: managed-k1s-provider-managesf
      pool: main
      labels:
        - name: pod-centos-7-alt
          image: localhost/k1s/centos-7-alt
          python-path: /bin/python2

The *config-update* job updates the nodepool configuration. Once the job is done, the
new label should appear in Zuul and one container should be ready.

Debug container creation failure
................................

If for some reason containers fail to start, here are some tips to investigate
the errors:

* Look for failure in Nodepool logs: /var/log/nodepool/launcher.log
* Look for failure in k1s logs: journalctl -u k1s
* Inspect podman manually on the k1s host server:

.. code-block:: bash

  podman images
  podman ps -a

.. _restart-nodepool-services:


Restart Nodepool services
-------------------------

The *nodepool_restart.yml* playbook stop and restart Nodepool launcher
services.

.. code-block:: yaml

  ansible-playbook /var/lib/software-factory/ansible/nodepool_restart.yml


Build a Nodepool image locally
------------------------------

If you want to build a custom image with diskimage-builder locally you can
follow this process. The following commands run on fedora 30.

.. warning::

  Using a dedicated virtual machine is recommended. You can delete everything
  after your tests.

We start by installing the required dependencies, and downloading elements we
will need for our build.

.. code-block:: bash

  sudo dnf install -y qemu kpartx yum-utils policycoreutils-python-utils
  python3 -m pip install --user diskimage-builder
  mkdir elements
  git clone https://softwarefactory-project.io/r/config
  git clone https://softwarefactory-project.io/r/software-factory/sf-elements
  cp -Rf config/nodepool/elements/* elements/
  cp -Rf sf-elements/elements/* elements/
  export ELEMENTS_PATH=~/elements
  export PATH=$PATH:~/.local/bin
  mkdir -p /etc/nodepool/scripts

Some elements can require some files during the build. Be sure those files are
present on your host before you run the build.

i.e. `zuul-user` element requires `/var/lib/nodepool/.ssh/zuul_rsa.pub` during
the build. So create this file if you use `zuul-user` element in your image.

.. code-block:: bash

  sudo mkdir -p /var/lib/nodepool/.ssh/
  sudo touch /var/lib/nodepool/.ssh/zuul_rsa.pub

You can now build your image using `disk-image-create` and the nodepool
elements you need

.. code-block:: bash

  disk-image-create -o image_name [nodepool_elements ...]
  disk-image-create -o test zuul-user

You can edit/debug your element and run the build again

.. code-block:: bash

  vi elements/zuul-user/...
  disk-image-create -o test zuul-user


Useful commands
---------------

List slave instances and their status (used, building ...). Use the *--detail**
option to get the public IP of the instances:

.. code-block:: bash

 $ nodepool list

Trigger an diskimage build. The image will be automatically uploaded on the
provider(s) after a successful build:

.. code-block:: bash

 $ nodepool image-build *image-name*

Build logs are available in */var/www/nodepool-log/* on
the nodepool-builder node but also via https://sftests.com/nodepool-log/.

List nodepool instance images available on the configured providers and their
status:

.. code-block:: bash

 $ nodepool image-list

List instance diskimages built by Disk Image Builder (DIB) and their status:

.. code-block:: bash

 $ nodepool dib-image-list
