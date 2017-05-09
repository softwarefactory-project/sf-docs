Backup restore
==============

Create a backup
---------------

To create a backup, use the `sfmanager </docs/sfmanager.html#backup-and-restore>`_ cli::

  * sfmanager system backup_start
  * sfmanager system backup_get


Restore a backup
----------------

On a running instance, restore will restore the backup data::

  * ansible-playbook /var/lib/software-factory/ansible/sf_restore.yml -e "backup_file=$(pwd)/sf_backup.tar.gz"

This is used to undo actions on a live system.


Recover a backup
----------------

On a fresh instance, recover will re-deploy the backup::

  * sfconfig.py --recover ./sf_backup.tar.gz

This is used to migrate the services from one instance to another.
