Backup restore
==============

Create a backup
---------------

To create a backup, use the following command:

  * ansible-playbook /var/lib/software-factory/ansible/sf_backup.yml

You can find the tgz generated on /var/lib/software-factory/backup.tar.gz


Restore a backup
----------------

On a running instance, restore will restore the backup data::

  * ansible-playbook /var/lib/software-factory/ansible/sf_restore.yml -e "backup_file=$(pwd)/sf_backup.tar.gz"

This is used to undo actions on a live system.


Recover a backup
----------------

On a fresh instance, recover will re-deploy the backup::

  * sfconfig.py --recover ./sf_backup.tar.gz

This is used to migrate the services from one instance to another. If you have
gerrit replication enabled, you should use the flag
'--disable-external-resources' to disable the replication during the
recovery process.

Export a backup to an external location
---------------------------------------

You can export your backup to an external location for storage, using
a Swift server or a remote SSH connection with SCP. SF will deploy
two scripts for this:

* /usr/local/bin/export_backup_swift.sh
* /usr/local/bin/export_backup_scp.sh

The script will use some variables from /etc/software-factory/sfconfig.yaml
to configure the backup destination parameters:

.. code-block:: yaml
    backup:
        disabled: True
        method: swift                                 # Backup method: swift (default) or scp
        os_auth_url:                                  # Authentication URL for Swift
        os_auth_version:                              # Authentication version for Swift
        os_tenant_name:                               # Tenant name for Swift
        os_username:                                  # Username for Swift
        os_password:                                  # Password for Swift
        swift_backup_container: sfbackups             # Swift container to use
        swift_backup_max_retention_secs: 864000       # Retention period for Swift backups
        scp_backup_host: remoteserver.sftests.com     # Remote host for SCP backup
        scp_backup_port: 22                           # Remote port for SCP backup
        scp_backup_user: root                         # Remote user for SCP backup
        scp_backup_directory: /var/lib/remote_backup  # Remote directory to store SCP backups
        scp_backup_max_retention_secs: 864000         # Retention period for SCP backups

SF will configure a daily cron job to create and export the backup using the
selected method.

Using GPG to encrypt and decrypt backups
----------------------------------------

It is recommended to store the backup files encrypted when using external
storage services, since the user and administrative credentials are included
in the backup.

When using the export_backup_swift.sh or export_backup_scp.sh shell scripts
included in SF, all backups are automatically encrypted using GPG before being
uploaded to the remote location. A special public GPG key is required for this,
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

