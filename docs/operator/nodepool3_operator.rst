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


List instances
--------------

.. code-block:: bash

    nodepool3 list
