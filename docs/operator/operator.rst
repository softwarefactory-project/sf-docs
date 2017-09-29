.. _operator:

======================
Operator documentation
======================

This chapter documents how to deploy and manage a Software Factory deployment.

.. _architecture:

Architecture
============

SF architecture is modular and defined by a single file called arch.yaml. This
file defines the number of nodes, their requirements in term of resources and
how services are distributed. While every services can be dispatched to a
dedicated node, it is advised to use the minimal refarch first, and then do
scale-up as needed (such as moving the SQL database or the ELK stack to
a separate node).

Also you can find some useful hints in the following documentation:

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

Once your instance is ready to use, you will have to prepare the configuration
files and use the tool *sfconfig* to finalize the deployment.

The sfconfig process uses 2 configuration files to configure the
software-factory deployment

* /etc/software-factory/sfconfig.yaml :ref:`Main configuration documentation <sfconfig>`
* /etc/software-factory/arch.yaml :ref:`Architecture configuration <architecture>`

Please, read the :ref:`configuration documentation <configure>` to understand
the configuration process.

Management
==========

.. toctree::
   :maxdepth: 1

* The :ref:`access control documentation <access_control>` explains how to configure the
  Software Factory policy engine to control who can do what on the managesf
  REST API(You can find some useful information on the `sfmanager documentation </docs/sfmanager/>`_)
* You can find the description of the :ref:`upgrade process <upgrade>` to upgrade
  to the last version of Software Factory.
* Finally how to :ref:`backup and restore <backup_restore>` a Software Factory
  deployment.

Software Factory deep dive
==========================

If you need more information about how Software Factory works, you can read
this :ref:`this document who describes SF internals <deepdive>`
