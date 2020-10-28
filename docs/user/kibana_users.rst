.. _kibana-users:

Introduction
------------

Since Software Factory 3.6, the opensource version of ELK stack has been
replaced with Opendistro for Elasticsearch version [1]_.
The Opendistro ELK stack is a "community-driven 100% open source distribution
of Elasticsearch with advanced security, alerting, SQL support,
automated index management, deep performance analysis, and more."

The main reason why we decide to switch ELK stack to Opendistro is that
we would like to hawve a Role Base Access Controll (RBAC) which is
provided in Opendistro. With that, we are able to give read-only access to
non-privileged users, so our visualizations, indexes, index patterns and others
components in Elasticsearch and Kibana are safe from interference
by third parties.
Before choosing Opendisto, we were comparing all available solutions like:

- Opensource version of Elasticsearch with X-Pack Community Edition
- Secure-Guard
- Readonlyrest

Some of them was not providing so many features, some has license that
are inconvenient for our project. Thats why we choose Opendistro which has
Apache2 license, community and multiple features that we would like to provide
in the future releases of Software Factory.

Main documentation related to :ref:`Opendistro for Elasticsearch you can find here <opendistro>`.

References:
-----------

.. [1] https://opendistro.github.io/
