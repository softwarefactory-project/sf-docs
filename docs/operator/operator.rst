:orphan:

.. _operator:

======================
Operator documentation
======================

This chapter documents how to deploy and manage a Software Factory deployment.

Quick Start
===========

On a CentOS-7 system, deploy the minimal architecture (install-server, managesf, gerrit, logserver, zuul3, nodepool3)
using this command:

.. code-block:: bash

  # yum install -y https://softwarefactory-project.io/repos/sf-release-2.7.rpm
  # yum update -y
  # yum install -y sf-config
  # sfconfig


.. _tpci-quickstart:

Third-Party-CI Quick Start
==========================

To configure an external gerrit such as review.openstack.org, you'll need
to manually create a user on the remote service service. For openstack.org,
follow `this guide <https://docs.openstack.org/infra/system-config/third_party.html#creating-a-service-account>`_) to configure it.

It's recommended to first deploy a local installation, before adding
the external gerrit. In that case, after your local deployment is validated,
you add the local zuul ssh public key (located here: /var/lib/software-factory/bootstrap-data/ssh_keys/zuul_rsa.pub) to
the remote `user ssh key setting page <https://review.openstack.org/r/#/settings/ssh-keys>`_.
The you run this command:

.. code-block:: bash

  # sfconfig --zuul3-external-gerrit openstack.org#username --zuul3-upstream-jobs

Alternatively you can pre-configure the remote user ssh key and copy the key files
to the install server to deploy everything in one shot using this command:

.. code-block:: bash

  # sfconfig --zuul3-external-gerrit openstack.org#username --zuul3-upstream-jobs --zuul3-ssh-key /path/to/user/private/key

.. _architecture:

Architecture
============

SF architecture is modular and defined by a single file called arch.yaml. This
file defines how services are deployed. Each hosts declare:

* A hostname,
* A ip address,
* A public_url (used for service like zuul-merger),
* A list of components.

For example, to add a new zuul-merger, start a new instance inside the internal
network of the deployment, enable ssh connection by copying the install server
root user public ssh key to the authorized_keys of the new instance and
update the arch.yaml with:

.. code-block:: yaml

  # echo >> /etc/software-factory/arch.yaml << EOF
      - host: zm02
        ip: 192.168.0.XXX
        roles:
          - zuul-merger
  EOF
  # sfconfig

You can find some useful hints in the following documentation:

* :ref:`define the architecture <architecture_config_file>`
* :ref:`extend the architecture <architecture_extending>`
* :ref:`migrate a service to a dedicated instance <architecture_migrate_service>`


Deployment
==========

You can find the :ref:`requirements <deployment_requirements>` to prepare the main Software Factory instance.

There are two main solutions to deploy Software Factory:

* Use the packages provide by the Software Factory team on a fresh centos
  instance, follow the :ref:`rpm based deployment documentation <deployment_rpm_based>`

* Use the image provides by the Software Factory team for each release, follow
  the :ref:`base image deployment documentation <deployment_image_based>`

Configuration
=============

Once the instance is running, you may adjust the configuration
files to change the domain name and admin password.

.. code-block:: bash

  # vim /etc/software-factory/sfconfig.yaml
  # sfconfig --skip-install

Please, read the :ref:`configuration documentation <configure>` to
understand the configuration process.

Management
==========

.. toctree::
   :maxdepth: 1

* The :ref:`access control documentation <access_control>` explains how to configure the
  Software Factory policy engine to control who can do what on the managesf
  REST API(You can find some useful information on the `sfmanager documentation </docs/sfmanager/>`_)
* You can find the description of the :ref:`upgrade process <upgrade>` to upgrade
  to the last version of Software Factory.
* The :ref:`system metrics section <metric_operator>` explains how to set up the
  Software Factory system metrics and status dashboard.
* Finally how to :ref:`backup and restore <backup_restore>` a Software Factory
  deployment.

Software Factory deep dive
==========================

If you need more information about how Software Factory works, you can read
this :ref:`this document who describes SF internals <deepdive>`
