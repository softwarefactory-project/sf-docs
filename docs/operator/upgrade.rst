Upgrade Software Factory
========================

To maintain the deployment up-to-date, simply uses:

.. code-block:: bash

 $ sudo yum update -y

To upgrade to a new release of Software Factory, for example the version 3.0:

.. code-block:: bash

  $ sudo yum install -y --nogpgcheck https://softwarefactory-project.io/repos/sf-release-3.0.rpm
  $ sudo yum update -y sf-config
  $ sudo sfconfig --upgrade

This process turns off all the services and perform data upgrade if necessary.
