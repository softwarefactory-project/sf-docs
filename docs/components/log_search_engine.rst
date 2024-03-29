.. _log_search_engine:

Jobs log search engine
======================

On Software Factory, a stack could be deployed to provide a log search engine
for CI/CD jobs. When the stack is activated, the following components are
deployed:

* `Opensearch <https://www.opensearch.org/>`_: RESTful search and analytics engine (Open-source fork of Elasticsearch).
* `Logstash <https://www.elastic.co/products/logstash>`_: server-side data processing pipeline.
* `Opensearch Dashboards <https://www.opensearch.org/docs/latest/dashboards/index/>`_: to visualize your Opensearch data (Open-source fork of Kibana).

.. image:: ../user/imgs/opensearch_dashboard.png
   :scale: 36 %

As operator, you can understand how the logging system is implemented on
Software Factory and how to to activate it by following :ref:`elk's operator
documentation <elk-operator>`.

..
   TODO add user documentation
   As users, you can have a look to the :ref:`user documentation <elk-user>`
   to understand how to use or add dashboards.
