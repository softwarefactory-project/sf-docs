.. _metrics_user:

Add custom dashboards
=====================

User can submit dashboards for grafana within the metrics directory in the
config repository. These dashboards are written in yaml and will be converted
for grafana using `grafyaml <https://docs.openstack.org/infra/grafyaml/>`_.

The default dashboards for zuul and nodepool within the config repository should
not be modified. They are automatically generated using `sf-graph-render <https://softwarefactory-project.io/r/gitweb?p=software-factory/sf-config.git;a=blob;f=sfconfig/tools/graph_render.py;h=6f2f03c50066b62ab10ea65fd41e43b7564aa086;hb=HEAD>`_.

Users don't have access to influxdb metrics database. Only admin user could
provides all the series available on the database to allow user to create their
queries.

The dashboards _nodepool.yaml and _zuul.yaml could be used to understand how to
create user defined dashboards.

When a user submit a dashboard within the config repo. The dashboard will be
validated using

.. code-block:: bash

   grafana-dashboard validate $dashboard

When the dashboard is merged, it will be updated on grafana using

.. code-block:: bash

   grafana-dashboard update $dashboard


It could be useful to use grafyaml to validate dashboard before submitting it.
