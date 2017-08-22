.. _nodepool-operator:

Configure nodepool to manage ephemeral test slaves
--------------------------------------------------

Nodepool automates management of test instances. It automatically prepares and
starts VMs that are used for a single job. After each job the VM is destroyed
and a fresh one is started for the next job. Nodepool also prepares the images
that are used for testing, for example when additional packages are required.

Nodepool needs 2 services to operate (to be defined in arch.yaml):

 * nodepool-launcher that schedules image build jobs and spawns slaves
 * nodepool-builder that builds image locally before uploading to the cloud


Add a cloud provider
^^^^^^^^^^^^^^^^^^^^

To do this, an account on an OpenStack cloud is required and credentials need to
be known by Nodepool. Moreover it is highly recommended to use a dedicated
network or tenant for slave instances.

In order to configure Nodepool to define a provider (an OpenStack cloud account) you need
to adapt sfconfig.yaml. Below is an example of configuration.

.. code-block:: yaml

 nodepool:
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

 $ nodepool list
 $ nodepool image-list

See the :ref:`Nodepool user documentation<nodepool-user>`

As an administrator, it can be really useful to check /var/log/nodepool/ to debug the Nodepool
configuration.


Manage diskimages
^^^^^^^^^^^^^^^^^

To manage diskimage, here are the relevant commands:

* nodepool image-build *image-name* # Trigger an image build
* nodepool image-upload *provider-name* *image-name* # Upload image to a cloud


What to do if nodepool is not working ?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Until this is provided as an automatic task, here is the manual process:

* Check OpenStack provider tenants and clean left-over resources:

  * server with an uptime more than 12 hours
  * glance images
  * unused floating ip

* Remove un-assigned floating-ip
* Check nodepool logs for permission errors or api failure

If nothing works, this is how to reset the service:

* Stop nodepool-launcher process
* Delete all OpenStack nodepool resources
* Connect to mysql and delete from node, snapshot_image tables
* Start nodepool-launcher process
* Follow the logs and wait for servers to be created.
* Check zuul log to verify it is submitting job request.

It might happen that some nodes are kept in the "delete" state for quite some
time, while they are already deleted. This blocks spawning of new instances.
The simplest way to fix this is to clean the stale entries in the nodepool DB
using the following command (deleting all entries older than 24 hours and in
state delete):

.. code-block:: mysql

     DELETE FROM node WHERE state_time < (UNIX_TIMESTAMP() - 86400) AND state = 4;
