.. _operator:

======================
Operator documentation
======================

This chapter documents how to deploy and manage a Software Factory instance.

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

Operation
=========
.. toctree::
   :maxdepth: 1

   Configure access control <access_control>
   migration
   upgrade
   Backup and restore mechanismes <backup_restore>
   deepdive

.. These pages are used as reference for all internal links
.. in the documenation
.. toctree::
   :maxdepth: 1
   :hidden:

   architecture
   deployment
   configure
   image_build
