.. note::

  This is a lightweight documentation intended to get operators started with setting
  up the Zuul3 service. For more insight on what Zuul3 can do, please refer
  to its upstream documentation_.

.. _documentation: https://docs.openstack.org/infra/zuul/feature/zuulv3/

Operate zuul3
=============

The zuul(V3) service is installed with rh-python35 software collections:

* The configuration is located in /etc/zuul3
* The logs are written to /var/log/zuul3
* The services are prefixed with rh-python35-

A convenient wrapper for the command line is installed in /usr/bin/zuul3.

By default, no merger are being deployed because the executor service
can perform merge task. However, a merger can also be deployed to speed
up start time when there are many projects defined.


Configure an external gerrit (use Software Factory as a Third-Party CI)
-----------------------------------------------------------------------

Refer to the :ref:`Third-Party-CI Quick Start guide <tpci-quickstart>`


Use openstack-infra/zuul-jobs
-----------------------------

The zuul-scheduler can automatically import all the jobs defined in
the openstack-infra/zuul-jobs repository. Use this command line to enable
its usage:

.. code-block:: bash

    sfconfig --zuul3-upstream-jobs


Troubleshooting non starting jobs
---------------------------------

* First check that the project is defined in /etc/opt/rh/rh-python35/zuul/main.yaml
* Then check in scheduler.log that it correctly requested a node and submitted a
  job to the executor
* When zuul reports *PRE_FAILURE* or *POST_FAILURE*,
  then the executor's debugging needs to be turned on
* Finally passing all loggers' level to DEBUG in
  /etc/opt/rh/rh-python35/zuul/scheduler-logging.yaml then restarting the service
  rh-python35-zuul-scheduler might help to debug.


Troubleshooting the executor
----------------------------

First you need to enable the executor's *keepjob* option so that ansible logs are available on dist:

.. code-block:: bash

    /opt/rh/rh-python35/root/bin/zuul-executor -c /etc/zuul3/zuul.conf keep

Then next job execution will be available in /tmp/systemd-private-*-rh-python35-zuul-executor.service-*/tmp/

In particular, the work/ansible/job-logs.txt usually tells why a job failed.

When done with debugging, deactivate the keepjob option by running:

.. code-block:: bash

    /opt/rh/rh-python35/root/bin/zuul-executor -c /etc/opt/rh/rh-python35/zuul/zuul.conf nokeep
