.. _third_party_ci_guide:

Deploy a third-party CI with Software Factory
---------------------------------------------

In this guide, we will create a third-party CI with Software Factory including:

* Service configurations
* Zuul pipeline and base job
* Extra services such as `log-classify`_ and `log_search_engine`_

Requirements
............

To complete this guide you will need:

* A CI account on the external code review system
* One or more CentOS instance(s) to deploy the services
* An optional resources provider account (OpenStack, OpenShift, AWS)

CI account
..........

The third-party CI needs a CI account to report build result.


OpenStack
~~~~~~~~~

To configure an external gerrit such as review.opendev.org, you'll need
to manually create a user on the remote gerrit. For openstack.org,
follow `this guide <https://docs.openstack.org/infra/system-config/third_party.html#creating-a-service-account>`_ to configure it.


GitHub
~~~~~~

TBD

Pagure
~~~~~~

TBD


CI services
...........


The third-party CI needs CentOS instance to run.
See the `deployment_requirements`_ section for resources requirements per services.

It is recommended to start with an all-in-one installation that can be scale-up once the services are working.
For example, here are some options:

===== ===== ====== ==========================================
 Ram   CPU   Disk   Services
===== ===== ====== ==========================================
 4GB    1    40GB   Bare minimal: Zuul / Nodepool / Zookeeper
 4GB    2    80GB   Above + logserver
 8GB    4   120GB   Above + elasticsearch / logstash / kibana
===== ===== ====== ==========================================

Initial configuration
~~~~~~~~~~~~~~~~~~~~~

TBD

Configure external connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

add the local zuul ssh public key (located here: /var/lib/software-factory/bootstrap-data/ssh_keys/zuul_rsa.pub)
to the remote `user ssh key setting page <https://review.openstack.org/r/#/settings/ssh-keys>`_.
Then add the new gerrit connection to /etc/software-factory/sfconfig.yaml file:

.. code-block:: yaml

  zuul:
    gerrit_connections:
      - name: review.openstack.org
        hostname: review.openstack.org
        port: 29418
        puburl: https://review.openstack.org
        username: external-gerrit-user-name
        # optional canonical_hostname
        canonical_hostname: git.openstack.org


CI resources
............

The third-party CI needs a place to run job.

Internal
~~~~~~~~
You can start by using the provided hypervisor role to use a local instance for test resources.
See the (TBD) k1s documentation

OpenStack
~~~~~~~~~

TBD (reference virt-customize doc to setup the images)

OpenShift
~~~~~~~~~

TBD

AWS
~~~

TBD


Log processing
..............

The third-party CI needs a place to store and analyze the logs

Basic logserver
~~~~~~~~~~~~~~~

TBD


ELK
~~~

TBD


Log-Classify
~~~~~~~~~~~~

TBD


Conclusion
..........

Here are the resulting configurations:

* config repos pipeline
* config repos base job
* elk configuration
