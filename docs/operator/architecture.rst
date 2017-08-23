.. _architecture_config_file:

Configuration
-------------

The architecture is defined in /etc/software-factory/arch.yaml:

.. code-block:: yaml

  inventory:
    - name: node01
      ip: 192.168.240.10
      roles:
        - install-server
        - mysql

    - name: node02
      ip: 192.168.240.11
      roles:
        - gerrit

.. note::

  Any modification to arch.yaml needs to be manually applied with the sfconfig script.
  Run sfconfig after saving the sfconfig.yaml file.


The minimal architecture includes following components:

.. TODO Task: 566 update architecture with all available components
..      create one page per component if needed
..      explain how to use and deploy each component


* install-server
* mysql
* zookeeper
* gateway
* cauth
* `managesf </docs/managesf/>`_
* gitweb
* gerrit
* logserver
* zuul-server
* zuul-launcher
* zuul-merger
* nodepool-launcher
* jenkins

Optional services can be enabled:


* rabbitmq
* etherpad
* lodgeit
* gerritbot
* logserver
* nodepool-builder
* murmur
* elasticsearch
* job-logs-gearman-client
* job-logs-gearman-worker
* logstash
* kibana
* mirror
* storyboard
* storyboard-webclient
* repoxplorer
* firehose
* pages
* hydrant
* influxdb
* grafana

.. _architecture_extending:

Extending the architecture
--------------------------

To deploy a specific service on a dedicated instance:

* Start a new instance using the SF image (same version as the main one) on the same network with the desired flavor
* Attach a dedicated volume if needed
* Make sure other instances security group allows network access from the new instance
* Add root public ssh key (install-server:/root/.ssh/id_rsa.pub) to the new instance,
* Make sure remote ssh connection access happen without password authentication,
* Add the new instance to the arch inventory and set it's ip address,
* Add desired services in the roles list (e.g., elasticsearch), and
* Run sfconfig to reconfigure the deployment.

See sf-config/refarch
(https://softwarefactory-project.io/r/software-factory/sf-config) directory for
example architectures.

.. _architecture_migrate_service:

Migrate a service to a dedicated instance
-----------------------------------------

This procedure demonstrates how to run the log indexation services (ELK stack) on a dedicated instance:

* First stop and disable all elk related services (elasticsearch, logstash, log-gearman-client and log-gearman-worker)
* Copy the current data, e.g.: rsync -a /var/lib/elasticsearch/ new_instance_ip:/var/lib/elasticsearch/
* Add the new instances and roles to the /etc/software-factory/arch.yaml file:

.. code-block:: yaml

  inventory:
    - name: elk
      ip: new_instance_ip
      roles:
        - elasticsearch
        - logstash
        - log-gearman-client
        - log-gearman-worker

* Run sfconfig to apply the architecture modification
