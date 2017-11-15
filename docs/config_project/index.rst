.. _config-repo:

The config repository (config-project)
--------------------------------------

The config repository is a special project used to configure many Software Factory services.
This enables users to submit configuration changes through the code review system.
Once a change has been approved, the config-update job is run to apply the new configuration.

To make a change in the configuration:

* First clone the repository: git clone http:\/\/<fqdn>/r/config
* Edit the relevant files and commit: git commit
* Submit a change for review: git review
* The configuration will be updated once the change is approved and merged

.. note::

  Files starting by a "_" are default settings and they may be modified by
  an upgrade of Software Factory, thus they **shouldn't be modified manually**.
  Whenever you want to modify them, please propose an update to factory settings
  here:


.. toctree::
   :maxdepth: 2

   zuul3_user
   nodepool3_user
   jenkins_user
   zuul_user
   nodepool_user
   gerritbot_user
   gerrit_replication_user
   access_control_user
   gerritlinks_user
   resources_user
   repoxplorer_user
