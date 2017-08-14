.. _nodepool-user:

Nodepool configuration
======================

Diskimages and labels definition are done via the config repository of SF.

Clone the config repository of SF from Gerrit and modify the file "config/nodepool/nodepool.yaml"
as below.

.. code-block:: yaml

  diskimages:
    - name: dib-centos-7
      elements:
        - centos-minimal
        - nodepool-minimal
        - sf-zuul-worker

  labels:
    - name: centos-7
      image: centos-7
      min-ready: 1
      providers:
        - name: default

  providers:
    - name: default
      cloud: default
      clean-floating-ips: true
      image-type: raw
      max-servers: 10
      boot-timeout: 120
      pool: nova
      rate: 10.0
      networks:
        - name: slave-net-name
      images:
        - name: centos-7
          diskimage: dib-centos-7
          username: jenkins
          min-ram: 1024


By committing this change on the config repository, SF will perform a file syntax
validation and will allow you (or not) to merge the change (by CR +2 and W +2). Once merged
the new configuration of nodepool will be loaded by the Nodepool service. And you should
see on the declared provider the following:

 * A VM is spawned (with the term "template" in its name)
 * After the run of the base.sh script, the VM is snapshoted
 * The VM is destroyed and the snapshot is available
 * At least one VM is spawned based on the snapshot
 * A floating ip is attached to the new VM
 * The new VM is attached to Jenkins as slave

Using the config repository, SF users can provide custom build scripts for Jenkins slave
as well as custom labels for their jobs' needs. As already said slaves are destroyed after
each job. This can have some advantages:

 * A clean VM for each job
 * A job have full system access (root)


Using extra elements
--------------------

All `diskimage-builder elements <https://docs.openstack.org/developer/diskimage-builder/elements.html>`_
as well as `sf-elements <https://softwarefactory-project.io/r/gitweb?p=software-factory/sf-elements.git;a=tree;f=elements>`_
are available for nodepool image. For example you can:

* Replace *centos7* by *fedora* or *gentoo* to change the base os
* Use *selinux-permissive* to set selinux in permissive mode
* Use *pip-and-virtualenv* to install package from pypi
* Use *source-repositories* to provisioned a git repository


Adding custom elements
----------------------

To customize an image, new diskimage builder elements can added to the nodepool/elements directory.
For example, to add python34 to a centos system, you need to create this element:

.. code-block:: bash

  mkdir nodepool/elements/python34-epel
  echo -e 'epel\npackage-installs' > nodepool/elements/python34-epel/element-deps
  echo 'python34:' > nodepool/elements/python34-epel/packages.yaml


Then you can add the 'python34-epel' element to an existing image.

Read more about diskimage builder elements `here <https://docs.openstack.org/developer/diskimage-builder/developer/developing_elements.html>`_.
Or look at some example from `sf-elements <https://softwarefactory-project.io/r/gitweb?p=software-factory/sf-elements.git;a=tree;f=elements>`_.


CLI
---

The CLI utility *sfmanager* can be used to interact with nodes that are currently running. The
following actions are supported:

* list nodes, with status information like id, state, age, ip address, base image
* hold a specific node, so that it is not destroyed after it has been consumed for a job
* add a SSH public key to the list of authorized keys on the node, allowing a user to do
  remote operations on the node
* schedule a node for deletion
* list available images

These operations might require specific authorizations defined within SF's policy engine.

You can refer to sfmanager's contextual help for more details.
