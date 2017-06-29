Backup restore
==============

Create a backup
---------------

To create a backup, use the `sfmanager </docs/sfmanager.html#backup-and-restore>`_ cli:

.. code-block:: bash

 sfmanager system backup_start
 sfmanager system backup_get


Restore a backup
----------------

**On a running instance of SF**, this command will restore the backup data.

If the backup has been encrypted then follow the section
:ref:`Using GPG to encrypt and decrypt backups <backup_encrypt>` to decrypt it before.

.. code-block:: bash

 ansible-playbook /var/lib/software-factory/ansible/sf_restore.yml -e "backup_file=$(pwd)/sf_backup.tar.gz"

Recover a backup
----------------

The sfconfig.py *recover* and *recover-from-bdir* options are used to
initialise a new Software Factory host from a backup.

Prepare the new Software host
.............................

.. code-block:: bash

  sudo yum install -y https://softwarefactory-project.io/repos/sf-release-2.6.rpm
  sudo yum install -y sf-config

Restore the backup from an archive
..................................

A backup archive is created via the *sfmanager system backup_get* command
or via the Swift and SCP export scripts. If the backup has been
encrypted then follow the section :ref:`Using GPG to encrypt and decrypt backups <backup_encrypt>` to decrypt it before.

.. code-block:: bash

 sfconfig.py --recover ./sf_backup.tar.gz

Restore the backup from the SF backup directory
...............................................

This command expects to find the directory */var/lib/software-factory/backup*
populated with the Software Factory data.

This is case if the Rsync backup method has been used for syncing
backup data on that node and the *scp_backup_directory* was configured on
*/var/lib/software-factory/backup*.

.. code-block:: bash

 sfconfig.py --recover-from-bdir

Export a backup to an external location
---------------------------------------

You can export your backup to an external location for storage, using
a Swift server or a remote SSH connection with SCP or RSYNC. SF will deploy
three scripts for this:

* /usr/local/bin/export_backup_swift.sh
* /usr/local/bin/export_backup_scp.sh
* /usr/local/bin/export_backup_rsync.sh

The script will use some variables from /etc/software-factory/sfconfig.yaml
to configure the backup destination parameters:

.. code-block:: yaml

    backup:
        disabled: True                                # Activate or not the export
        method: swift                                 # Backup method: swift (default), scp or rsync
        os_auth_url:                                  # Authentication URL for Swift
        os_auth_version:                              # Authentication version for Swift
        os_tenant_name:                               # Tenant name for Swift
        os_username:                                  # Username for Swift
        os_password:                                  # Password for Swift
        swift_backup_container: sfbackups             # Swift container to use
        swift_backup_max_retention_secs: 864000       # Retention period for Swift backups
        scp_backup_host: remoteserver.sftests.com     # Remote host for SCP/RSYNC backup
        scp_backup_port: 22                           # Remote port for SCP/RSYNC backup
        scp_backup_user: root                         # Remote user for SCP/RSYNC backup
        scp_backup_directory: /var/lib/remote_backup  # Remote directory to store SCP/RSYNC backups
        scp_backup_max_retention_secs: 864000         # Retention period for SCP backups

SF configures a daily cron jobs to create and export the backup using the
selected method.

The Rsync export does not support any retention periods. Indeed backup data
are synced to the remote location and previously exported backup data
are overwritten.

Configure the remote server for SSH access
------------------------------------------

For the SCP and Rsync export methods the public key */root/.ssh/id_rsa.pub*
must has been appended to the remote server user file *~/.ssh/authorized_keys*.

.. _backup_encrypt:

Using GPG to encrypt and decrypt backups
----------------------------------------

It is recommended to store the backup files encrypted when using external
storage services, since the user and administrative credentials are included
in the backup.

When using the *export_backup_swift.sh* or *export_backup_scp.sh* shell scripts
included in SF, all backups are automatically encrypted using GPG before being
uploaded to the remote location.

The *export_backup_rsync.sh* shell scripts does not encrypt the data
on the remote location so if you selected Rsync this configuration is not
needed.

A special public GPG key is required for this,
and it has to be stored on the SF node. To create this key, do the following:

.. code-block:: bash

 gpg --gen-key  # Use "sfadmin" as name when creating the key
 gpg --export -a sfadmin > sfadmin.pub
 gpg --export-secret-key -a sfadmin > sfadmin.key

Make sure you keep the sfadmin.key in a safe place.

You have to copy this public key to the SF node, and import it as root user.

.. code-block:: bash

 scp sfadmin.pub root@sftests.com:.
 gpg --import sfadmin.pub

If you need to restore from a backup, you need to decrypt the tar.gz file first.

.. code-block:: bash

 gpg -o sf_backup.tar.gz -d sf_backup.tar.gz.gpg

