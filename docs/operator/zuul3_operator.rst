Configure zuul(V3)
------------------

The zuul(V3) service is installed with rh-python35 software collections:

* The configuration is located in /etc/zuul3
* The logs are written to /var/log/zuul3
* The services are prefixed with rh-python35-

A convenient wrapper for the command line is installed in /usr/bin/zuul3.

By default, no merger are being deployed because the executor service
can perform merge task. However, merger can also be deployed to speed
up start time in case there are many projects defined.

Please check the upstream documentation_.

.. _documentation: https://docs.openstack.org/infra/zuul/feature/zuulv3/


List past jobs and builds
^^^^^^^^^^^^^^^^^^^^^^^^^

The zuul-web service is running with a jobs controller interface you can use
to query Zuul jobs or builds history:

.. code-block:: bash

  $ sudo zuul3 show jobs|builds --help
    usage: zuul show jobs|builds [-h] [--tenant TENANT] [--project PROJECT]
                      [--pipeline PIPELINE] [--change CHANGE]
                      [--patchset PATCHSET] [--ref REF] [--result RESULT]
                      [--uuid UUID] [--job_name JOB_NAME] [--voting VOTING]
                      [--node_name NODE_NAME] [--limit LIMIT] [--skip SKIP]

      --tenant TENANT       filter by tenant
      --project PROJECT     filter by project
      --pipeline PIPELINE   filter by pipeline
      --change CHANGE       filter by change
      --patchset PATCHSET   filter by patchset
      --ref REF             filter by ref
      --result RESULT       filter by result
      --uuid UUID           filter by uuid
      --job_name JOB_NAME   filter by job_name
      --voting VOTING       filter by voting
      --node_name NODE_NAME
                        filter by node_name
      --limit LIMIT         Limit the query
      --skip SKIP           Skip rows


Configure an external gerrit (use Software Factory as a Third-Party CI)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Refers to the :ref:`Third-Party-CI Quick Start guide <tpci-quickstart>`


Use openstack-infra/zuul-jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The zuul-scheduler can automatically import all the jobs defined in
the openstack-infra/zuul-jobs repository. Use this command line to enable
it's usage:

.. code-block:: bash

    sfconfig --zuul3-upstream-jobs


Investigate job not starting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* First check the test project is defined in /etc/opt/rh/rh-python35/zuul/main.yaml
* Then check in scheduler.log that it correctly requested a node and submited a
  job to the executor
* When zuul reports *PRE_FAILURE* or *POST_FAILURE*,
  then the executor debugging needs to be turned on
* Finally passing all loggers' level to DEBUG in
  /etc/opt/rh/rh-python35/zuul/scheduler-logging.yaml then restarting the service
  rh-python35-zuul-scheduler might help to debug.


Troubleshoot executor
^^^^^^^^^^^^^^^^^^^^^

First you need to enable executor keepjob option so that ansible logs are available on dist:

.. code-block:: bash

    /opt/rh/rh-python35/root/bin/zuul-executor -c /etc/zuul3/zuul.conf keep

Then next job execution will be available in /tmp/systemd-private-*-rh-python35-zuul-executor.service-*/tmp/

In particular, the work/ansible/job-logs.txt usually tells why a job failed.

When done with debugging, turn off the job keeping by running:

.. code-block:: bash

    /opt/rh/rh-python35/root/bin/zuul-executor -c /etc/opt/rh/rh-python35/zuul/zuul.conf nokeep
