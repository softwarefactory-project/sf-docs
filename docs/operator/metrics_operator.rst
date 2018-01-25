:orphan:

.. _metrics_operator:

Metrics
=======

Understanding metrics architecture
----------------------------------

Software Factory allows operators or users to create and visualize Grafana
dashboards on the Software-Factory web interface.

Two backends are available for Grafana, Influxdb or Graphite. The influxdb
implementation was the first delivered on Software Factory. The Graphite-api
backend was added in version 3.0 to allow users to create dashboards with the
same type of query used by the Openstack Infra team to get Zuul and Nodepool
metrics. These dashboards are stored in the grafana directory on the
project_config_ . The difference between queries is explained in
:ref:`user metrics documentation <metrics_user>`

.. _project_config: https://git.openstack.org/openstack-infra/project-config

Architecture
^^^^^^^^^^^^

.. image:: ../imgs/metric_arch.svg

The metrics are collected by Telegraf. Telegraf could be configured
with input and output plugins. On Software-Factory, the following plugins are
enabled and configured:

* Input plugins

  * statsd plugin to get metrics from Nodepool and Zull
  * system metrics pluging (cpu, memory, hdd)

* Output plugins

  * Influxdb
  * Graphite

System metrics
^^^^^^^^^^^^^^

Three services are deployed to provide system metrics:

* telegraf: an agent collecting system metrics on all nodes defined in the
  architecture file (/etc/software-factory/arch.yaml).
* influxdb: a time series database to store the metrics.
* grafana: a dashboard to get and to visualize dashboards

These services are used to provide a default system metrics dashboard for all
servers declared in arch.yaml.

Zuul and Nodepool metrics
^^^^^^^^^^^^^^^^^^^^^^^^^

By default, zuul and nodepool services will send metrics to a statsd server.
Statsd service is provided by telegraf, using telegraf statsd_ input plugins.

.. _statsd: https://github.com/influxdata/telegraf/tree/master/plugins/inputs/statsd


How to activate
---------------

These components are not deployed by default but can be activated by adding
them in */etc/software-factory/arch.yaml*:

You can deploy grafana and influxdb on a separated host if needed, but grafana
should be on the same host than the gateway role. Telegraf will be
automatically deployed on all nodes defined in the arch.yaml file.

.. code-block:: yaml

 - influxdb
 - graphite-api
 - grafana

Then running sfconfig to deploy all components:

.. code-block:: bash

 # sfconfig

Dashboards access
-----------------

There is a new item on the top menu, on the right side named "Status" to access
the grafana dashboard:

.. image:: ../imgs/metrics.png
   :scale: 50 %

A default dashboard is installed when activate influxdb and grafana role.

By default, all dashboards are read only. Only the admin user can add or modify
a dashboard.
