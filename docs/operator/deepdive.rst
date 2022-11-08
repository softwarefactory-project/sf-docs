.. _deepdive:

Internals
=========

The goal of this document is to describe Software Factory's internals.

Organisation
------------

The project is divided into many repositories, available on the
https://softwarefactory-project.io gerrit software-factory/ namespace,
and replicated on github at https://github.com/softwarefactory-project :

* sf-release: The release rpm to install the repository
* sf-config: The configuration/upgrade process
* sf-docs: The documentation
* sf-ci: The SF testing framework
* sf-elements: Diskimage builder elements
* sfinfo: The rpm distribution informations
* ...

All the components are packaged using **distgit** repositories.


Ansible usage
-------------

The arch.yaml file describes what roles should run on which instances. Then
based on this information, the sfconfig process generates all the necessary
playbooks to configure and maintain the deployment:

* The **sfconfig.yml** playbook runs the install, setup, config_update
  tasks to deploy the services on a fresh instance.
* The **sf_configrepo_update.yml** playbook applies the config project
  configuration, it is the playbook executed by the *config-update* job.
* The **sf_backup.yml** playbook collects all the services' data in
  /var/lib/software-factory/backup
* The **get_logs.yml** playbook collects all the services' logs,
  it's mostly used for sf-ci logs collections.
* The **sf_erase.yml** playbook disables and can remove all the services'
  data, it is used to uninstall services.


The system configuration
------------------------

The *sfconfig* script drives the system configuration. This script does the following actions:

* Generates secrets such as internal passwords, ssh keys and tls certificats,

* Ensures configuration files are up-to-date, this script
  checks for missing section and makes sure the defaults value are present. This is particularly
  useful when after an upgrade, a new component configuration has been added

* Generates Ansible inventory and configuration playbook based on the arch.yaml file.

* Generates and execute an Ansible playbook based on the action (e.g. setup, recover, upgrade, ...)

* Waits for ssh access to all instances

* Run testinfra tests

* All the generated data is written in /var/lib/software-factory:

  * ansible/ contains the playbooks and the group_vars.

  * bootstrap-data/ contains file secrets such as tls certificats or ssh keys.

  * sql/ contains database creation scripts.

That system configuration process is re-entrant and needs to be executed everytime the settings are changed.

Then SF is meant to be a self-service system, thus project configuration is done through the config-repo.


The config-repo
---------------

Once SF is up and running, the user configuration of Software Factory happens
via the config-repo:

* zuul/: Zuul configuration
* nodepool/: Nodepool configuration
* gerritbot/: IRC notification for gerrit event configuration,
* gerrit/: Gerrit replication endpoint configuration, and
* mirrors/: mirror2swift configuration.
* resources/: Platform wide groups, projects, repositories definitions.
* dashboard/: Custom Gerrit dashboard configuration
* policies/: ManageSF API ACLs definition

This is actually managed through SF CI system, thanks to the config-update job.
This job is actually an ansible playbook that will:

* Reload zuul configuration (hot reload without losing in-progress tasks),
* Reload nodepool, gerritbot and gerrit replication, and
* Set mirror2swift configuration for manual or next periodic update.
* Apply resources definitions (create repositories, update groups, ...)

Containerized services
----------------------

Some services are containerized since SF-3.7:

* elk stack
* gerrit
* nodepool services
* zuul services

Services are managed by systemd, configuration files are located on /etc/$service and logs are located on /var/log/$service

You can find the command used to create the container on /usr/local/bin/container-$service.sh

If you need to interact with a container, you can first list them

.. code-block:: bash

    [root@managesf.$fqdn ~]# podman ps
    CONTAINER ID  IMAGE                                                   COMMAND               CREATED       STATUS           PORTS  NAMES
    27bf06e712eb  quay.io/software-factory/nodepool-builder-ubi:5.0.0-2   /usr/local/bin/no...  30 hours ago  Up 30 hours ago         nodepool-builder
    5593621f6c1c  quay.io/software-factory/zuul-web-ubi:5.0.0-0           /usr/local/bin/zu...  30 hours ago  Up 28 hours ago         zuul-web
    71bb6b0795d2  quay.io/software-factory/zuul-executor-ubi:5.0.0-0      /usr/local/bin/zu...  30 hours ago  Up 28 hours ago         zuul-executor
    ac8a57cd93bb  quay.io/software-factory/zuul-scheduler-ubi:5.0.0-0     /usr/local/bin/zu...  30 hours ago  Up 28 hours ago         zuul-scheduler
    7b9fce44add3  quay.io/software-factory/nodepool-launcher-ubi:5.0.0-2  /usr/local/bin/no...  30 hours ago  Up 30 hours ago         nodepool-launcher
    29bd9915f524  quay.io/software-factory/gerrit:3.4.3-0                 /bin/bash             30 hours ago  Up 30 hours ago         gerrit

You can login on a container using

.. code-block:: bash

    [root@managesf.$fqdn ~]# podman exec -ti $container_name /bin/bash # or /bin/sh

You can execute a command on a container using

.. code-block:: bash

    [root@managesf.sftests.com ~]# podman exec -ti nodepool-builder nodepool image-list
    +----------+-----------+----------+-------+---------------------+-------------------+-------+-----+
    | Build ID | Upload ID | Provider | Image | Provider Image Name | Provider Image ID | State | Age |
    +----------+-----------+----------+-------+---------------------+-------------------+-------+-----+
    +----------+-----------+----------+-------+---------------------+-------------------+-------+-----+
