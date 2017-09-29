:orphan:

.. _configure:

Configuration
=============

.. _sfconfig:

Main configuration file: sfconfig.yaml
======================================

Currently located in /etc/software-factory/sfconfig.yaml,
this is THE SF configuration entry point.

Notice that the configuration is versioned and it is recommended to use git diff and git commit
command to check files modifications.

Ansible roles variable can be over-written in /etc/software-factory/custom-vars.yaml file too.

.. note::

  Any modification to sfconfig.yaml needs to be manually applied with the sfconfig script.
  Run sfconfig after saving the sfconfig.yaml file.


.. _configure_reconfigure:

Configuration and reconfiguration
=================================

* Connect as (root) via SSH to the install-server (the first instance deployed).
* Edit the configuration file /etc/software-factory/sfconfig.yaml (see :ref:`Main configuration documentation<sfconfig>`)

  * set the configuration according to your needs.
  * all parameters are editable and should be self-explanatory.

* Edit the architecture file /etc/software-factory/arch.yaml (see :ref:`Architecture documentation <architecture>`)

  * set the architecture according to your needs.

* Run sfconfig to apply the configuration.

You can find some useful information on the following pages about the services
provides by Software Factory:

.. toctree::
   :maxdepth: 1

   fqdn
   ssl
   auths
   zuul_operator
   nodepool_operator
   gerritbot_operator
   firehose_operator
   gerrit_replication_operator
   resources_operator
   pages_operator
   repoxplorer

.. _configure_network_access:

Network Access
==============

All network access goes through the main instance (called gateway). The FQDN
used during deployment needs to resolved to the instance IP. Software Factory
network access goes through TCP ports:

* 22 for ssh access to reconfigure and update deployment
* 80/443 for web interface, all services are proxyfied on the managesf instance
* 29418 for gerrit access to submit code review

Note that Heat deployment automatically configure security group rules to allow
these connections to the gateway.

.. _configure_access_sf:

Access Software Factory
=======================

The Dashboard is available at https://FQDN and admin user can authenticate
using "Internal Login". If you used the default domain *sftests.com* then
SF allows user "admin" with the default "userpass" password to connect.

If you need more information about authentication mechanisms on SF please refer to
:ref:`authentication documentation <authentication>`.
