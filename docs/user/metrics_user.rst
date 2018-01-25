.. _metrics_user:

Managing metrics
================

Enabling metrics
----------------
Metrics should be enable by an administrator, please read the :ref:`operator
metrics documentation <metrics_operator>`

Config Repository
-----------------
Users can submit dashboards in the config repository in the metrics directory.
These dashboards are writen in yaml and converted in json with `grafyaml
<https://git.openstack.org/cgit/openstack-infra/grafyaml>`_.

Some examples are provide for Zuul and Nodepool in the metrics directory of the
project config. Simply add a dashboard and submit a review to validate it.

You can find some example of dashboards on the project_config_ project created
by Openstack-infra team.

.. _project_config: https://git.openstack.org/openstack-infra/project-config

.. note::

  Grafyaml can only create dashboards using the *graphite* datasource

There are some differences in the queries used in the project-config and the
implementation provides in Software Factory, you have to check examples on the
config repository.

* The metrics types don't have the same name (gauge, counter and timing in Software Factory):


.. code-block:: yaml

   ...
   targets:
     - target: sumSeries(stats.gauges.nodepool.provider.*.nodes.building)
   type: singlestat
   ...

become:

.. code-block:: yaml

   ...
   targets:
     - target: sumSeries(stats.gauge.nodepool.provider.*.nodes.building)
   type: singlestat
   ...

* Metrics are stored in the /var/lib/carbon/whisper directory:

A file on the disk

.. code-block:: bash

   stats/gauge/zuul/executor/managesf/sftests/com/load_average.wsp

Become the following target:

.. code-block:: yaml

   ...
   targets:
     - target: aliasByNode(stats.gauge.zuul.executor.*.*.*.running_builds, 4)
   ...

.. warning::

    Fqdn are splitted in the carbon directory, eg: /managesf/sftests/com
