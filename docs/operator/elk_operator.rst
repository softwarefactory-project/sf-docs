.. _elk-operator:

ELK service
===========

Software Factory bundles an ELK stack based on :ref:`Opendistro for Elasticsearch <opendistro>`
to ease searching through the logs artifacts of jobs. Once activated,
the console log of every build is exported through logstash and
then searchable via Kibana.

A Software Factory user might want to export more artifacts
than the job's console. Indeed a job may generate additional
log files. In that case a custom zuul *post-run* job must be defined.
In order to do so a user must refer to :ref:`Export logs artifacts to logstash <zuul-artifacts-export-logstash>`

How to activate
---------------

These services are not deployed by default but can be activated by adding
the following components in */etc/software-factory/arch.yaml*:

.. code-block:: yaml

 - elasticsearch
 - logstash
 - job-logs-gearman-client
 - job-logs-gearman-worker
 - kibana

Then running:

.. code-block:: bash

 # sfconfig

The Kibana interface should be accessible via the Software Factory top menu under
the name Kibana.


Manage indices
--------------

Query the list and usage of index using:

.. code-block:: bash

   curl http://elasticsearch:9200/_cat/indices?v


Delete old/unused index using:

.. code-block:: bash

   curl -X DELETE http://elasticsearch:9200/INDEX-NAME
