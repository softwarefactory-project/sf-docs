Backup restore
==============

Software Factory provides an Ansible playbook *sf_backup* that aim to retrieve
services data into a single directory on the install-server:
*/var/lib/software-factory/backup*. Then this directory can be extracted onto
a backup server.

The *sfconfig* command provides a *recover* method that aim to setup a
Software Factory with the backuped data from */var/lib/software-factory/backup*.

Create a backup
---------------

To run the backup playbook, from this install-server use the following command:

.. code-block:: bash

  # ansible-playbook /var/lib/software-factory/ansible/sf_backup.yml

.. note:: The sf-ops https://softwarefactory-project.io/r/software-factory/sf-ops
   repository from the Software Factory project provides a backup playbook that
   fetch the backup directory from a Software Factory instance and store it
   locally.

Recover a backup
----------------

On a fresh deployment, *recover* will deploy the backup and run the Software Factory
setup tasks.

Prior to run that command, on the install-server node:

 - Install the package sf-release (same version than your previous deployment)
 - Install the sf-config package
 - Copy your backuped data to the */var/lib/software-factory/backup* directory
 - Verify that the arch in */etc/software-factory/arch.yml* is as expected for
   your deployment. You can compare to the backuped arch.ymk file from
   */var/lib/software-factory/backup/install-server/etc/software-factory/arch.yml*

The recover will run:

 - install tasks
 - data recovering tasks
 - setup tasks
 - validation tasks

.. code-block:: bash

  # sfconfig --recover
