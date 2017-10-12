Configure nodepool(V3)
----------------------

The nodepool(V3) service is installed with the rh-python35 software collections:
* The configuration is located in /etc/opt/rh/rh-python35/nodepool
* The logs are written to /var/opt/rh/rh-python35/log/nodepool
* The services are prefixed with rh-python35-

A convenient wrapper for the command line is installed in /usr/bin/nodepool3.

... Use a local build of nodepool-doc instead of external link

Please check upstream `documentation <https://docs.openstack.org/infra/nodepool/feature/zuulv3>`
first, here are a few hints to debug the service.


Required architecture
^^^^^^^^^^^^^^^^^^^^^

For a minimal deployment, limited to containerized nodes, only the **nodepool3-launcher**
component is required in the architecture file.

In order to use virtual nodes based on diskimage-builder, the **nodepool3-builder**
component must be present in the architecture file.

Add a cloud provider
^^^^^^^^^^^^^^^^^^^^

To do this, an account on an OpenStack cloud is required and credentials need to
be known by Nodepool. Moreover it is highly recommended to use a dedicated
network or tenant for slave instances.

In order to configure Nodepool to define a provider (an OpenStack cloud account) you need
to adapt sfconfig.yaml. Below is an example of configuration.

.. code-block:: yaml

 nodepool3:
   providers:
     - name: default
       auth_url: http://localhost:5000/v2.0
       project_id: 'tenantname'
       username: 'user'
       password: 'secret'
       region_name: ''

To apply the configuration you need to run again the sfconfig script.

You should be able to validate the configuration via the nodepool client by checking if
Nodepool is able to authenticate on the cloud account.

.. code-block:: bash

 $ nodepool3 list
 $ nodepool3 image-list

See the :ref:`Nodepool user documentation<nodepool-user>`

As an administrator, it can be really useful to check
/var/opt/rh/rh-python35/log/nodepool/ to debug the Nodepool configuration.


Manage diskimages
^^^^^^^^^^^^^^^^^

To manage diskimage, here are the relevant commands:

.. code-block:: bash

 $ nodepool3 image-build *image-name* # Trigger an image build
 $ nodepool3 image-upload *provider-name* *image-name* # Upload image to a cloud


List instances
--------------

.. code-block:: bash

 $ nodepool3 list
