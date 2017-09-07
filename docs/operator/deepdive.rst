Software Factory Internals
==========================

The goal of this document is to describe SF internals.

Organisation
------------

The project is divided into many repositories, available on the
https://softwarefactory-project.io gerrit software-factory/ namespace,
and replicated on github at https://github.com/softwarefactory-project ::

* sf-release: The release rpm to install the repository
* sf-config: The configuration/upgrade process
* sf-docs: The documentation
* sf-ci: The SF testing framework
* sf-elements: Diskimage builder elements
* sfinfo: The rpm distribution informations
* ...

All the components are packaged using **distgit** repositories.


The components
--------------

Below is an overview of all the components integration (shown as dashed boxes) and services
along with their connections to each others.

.. graphviz:: components.dot


The SSO mechanism
-----------------

Below is the sequence diagram of the SSO mechanism.

.. graphviz:: authentication.dot


Ansible usage
-------------

The arch.yaml file describes what roles should run on which instances. Then
based on this information, the sfconfig process generates all the necessary
playbooks to configure and maintain the deployment.


The system configuration
------------------------

The sfconfig script drives the system configuration. This script does the following actions:

* Generates secrets such as internal passwords, ssh keys and tls certificats,
* Ensures configuration files are up-to-date, this script
  checks for missing section and makes sure the defaults value are present. This is particularly
  useful when after an upgrade, a new component configuration has been added
* Generates Ansible inventory and configuration playbook based on the arch.yaml file.
* Generates and execute an Ansible playbook based on the action (e.g. setup, recover, upgrade, ...)
* Waits for ssh access to all instances
* Run testinfra tests
* All the generated data is written in /var/lib/software-factory:
** ansible/ contains the playbooks and the group_vars.
** bootstrap-data/ contains file secrets such as tls certificats or ssh keys.
** sql/ contains database creation scripts.

That system configuration process is re-entrant and needs to be executed everytime settings are changed.

Then SF is meant to be a self-service system, thus project configuration is done through the config-repo.


The config-repo
---------------

Once SF is up and running, the actual configuration of the CI happens in the config-repo:

* jobs/: Jenkins jobs jjb configuration,
* zuul/: CI gating zuul yaml configuration,
* nodepool/: Slave configuration with images and labels definitions,
* gerritbot/: IRC notification for gerrit event configuration,
* gerrit/: Gerrit replication endpoint configuration, and
* mirrors/: mirror2swift configuration.
* resources/: Platform wide groups, projects, repositories definitions.

This is actually managed through SF CI system, thanks to the config-update job.
This job is actually an ansible playbook that will:

* Reconfigure each jenkins using jenkins-jobs-builder,
* Reload zuul configuration (hot reload without losing in-progress tasks),
* Reload nodepool, gerritbot and gerrit replication, and
* Set mirror2swift configuration for manual or next periodic update.
