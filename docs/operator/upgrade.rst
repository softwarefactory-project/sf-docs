.. _upgrade:

Upgrade Software Factory
========================

To maintain the Software Factory nodes (part of the architecture) up to date,
simply uses:

.. code-block:: bash

    sfconfig --update

The command takes care of updating packages (system and software factory) on
all nodes. Some services may be restarted in case of version change. sfconfig
will run migration tasks automatically if needed.

To upgrade to a new release of Software Factory, for example the version 3.2:

.. code-block:: bash

  yum install -y https://softwarefactory-project.io/repos/sf-release-3.2.rpm
  yum update -y sf-config
  sfconfig --update

Prevent services auto-restart
-----------------------------

The update process restart services in case of related packages update. This
behavior can be disabled for critical services like Zuul and Nodepool. To do
so add the following extra vars to the custom-vars file. Default is False.

.. code-block:: bash

  echo "disable_zuul_autorestart: True" >> /etc/software-factory/custom-vars.yaml
  echo "disable_nodepool_autorestart: True" >> /etc/software-factory/custom-vars.yaml

Then, you can restart such services by following the instuctions below:

 - :ref:`Restart Zuul services <restart-zuul-servcices>`
 - :ref:`Restart Nodepool services <restart-nodepool-services>`
