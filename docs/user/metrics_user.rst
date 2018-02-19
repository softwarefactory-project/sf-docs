.. _metrics_user:

Add custom dashboards
=====================

User can submit dashboards for Grafana within the metrics directory in the
config repository. These dashboards are written in yaml and will be converted
for Grafana using `grafyaml <https://docs.openstack.org/infra/grafyaml/>`_.

The default dashboards for Zuul and Nodepool should not be modified. They are
automatically generated using `sf-graph-render
<https://softwarefactory-project.io/r/gitweb?p=software-factory/sf-config.git;a=blob;f=sfconfig/tools/graph_render.py;h=6f2f03c50066b62ab10ea65fd41e43b7564aa086;hb=HEAD>`_,
and are stored in /var/lib/software-factory/metrics.

Users don't have access to Influxdb *telegraf* database. Only admin user could
provides all the series available on the database to allow user to create their
queries.

The dashboards _nodepool.yaml and _zuul.yaml could be used to understand how to
create user defined dashboards.

When a user submit a dashboard within the config repo. The dashboard will be
validated by the config-update job using the following command:

.. code-block:: bash

   grafana-dashboard validate $dashboard

When the dashboard is merged, it will be updated on Grafana using the following command:

.. code-block:: bash

   grafana-dashboard update $dashboard


It could be useful to use grafyaml to validate a dashboard before submitting it.
