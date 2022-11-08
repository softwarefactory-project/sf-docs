.. _tenant_deployment:

Deploy a tenant instance of Software Factory
--------------------------------------------

A tenant SF is an instance that does not run Zuul services. Zuul
services (Zuul, Nodepool) will be shared with a Master SF. Users of a
tenant SF benefit from their own SF services like Gerrit or ELK.

In this guide, we will deploy a SF for a tenant. This tenant
will run Gerrit. Some tasks will be executed on the Tenant SF
and some others on the master SF.

It is assumed the Master SF instance is already up and running and we will call it
*master-sf*, or its FQDN *master-sf.com*, in the rest of this document.


Deploy the minimal tenant architecture
......................................

.. warning::

  **if the master SF instance uses self-signed certificates**, you must first copy
  '/etc/pki/ca-trust/source/anchors/localCA.pem' from master-sf to
  '/etc/pki/ca-trust/source/anchors/master-sf.pem' on the tenant instance, then run
  'update-ca-trust' on the tenant instance to trust this CA.

On a CentOS-7 system, deploy the tenant minimal architecture:

.. code-block:: bash

  yum install -y https://softwarefactory-project.io/repos/sf-release-3.7.rpm
  yum install -y sf-config
  cp /usr/share/sf-config/refarch/tenant-minimal.yaml /etc/software-factory/arch.yaml
  sed -i '/      - keycloak/a\      - gerrit\n' /etc/software-factory/arch.yaml

Edit /etc/software-factory/sfconfig.yaml to set the fqdn for the deployment and add:

.. code-block:: yaml

  tenant-deployment:
    name: tenant-sf
    master-sf: https://master-sf.com

.. note::

  If the tenant config repositories are on Github, follow :ref:`Create a config and
  jobs repository<create_config_job_repos>` to create the projects and the section
  :ref:`Update the configuration<update_the_configuration>` without the
  github_connection section since it is already set in the main instance.

Then run sfconfig:

.. code-block:: bash

  sfconfig

Add the new tenant on the Master SF
...................................

Define the tenant's default connection in /etc/software-factory/sfconfig.yaml:

.. code-block:: yaml

  gerrit_connections:
    - name: tenant-sf
      hostname: tenant-sf.com
      port: 29418
      puburl: https://tenant-sf.com/r/
      username: zuul
      default_pipelines: false

**If the tenant-sf instance uses self-signed certificates**, you must copy
'/etc/pki/ca-trust/source/anchors/localCA.pem' from tenant-sf to
'/etc/pki/ca-trust/source/anchors/tenant-sf.pem' on the host(s) where the
zuul-executor, zuul-scheduler and managesf containers are running,
then run 'update-ca-trust' to trust this CA. Then to update the containers' certificates,
you need to restart the associated services. Run this on the install server node:

.. code-block:: bash

  for s in "managesf zuul-executor zuul-scheduler"; do
  ansible $s -b -m shell -a "systemctl restart $s"
  done;

Run sfconfig to apply the change:

.. code-block:: yaml

  sfconfig --skip-install


Define the new tenant inside the resources. Create the following file
config/resources/tenant.yaml:

.. code-block:: yaml

  resources:
    tenants:
      tenant-sf:
        description: "The new tenant"
        url: "https://tenant-sf.com/manage"
        default-connection: tenant-sf

.. code-block:: bash

  git add resources/tenant.yaml && git commit -m"Add new tenant" && git review

Once the change is approved, merged and the *config-update* finished with success,
operator can run sfconfig on the tenant SF instance.


Finalize the tenant SF configuration
....................................

The Master is now configured and knows about the new tenant, then
a final sfconfig run on the tenant SF will finalize the pairing.

.. code-block:: bash

  sfconfig --skip-install


Workflow details
................

A tenant SF gets its own SF config repository. The tenant can manage its own resources
like CRUD on Gerrit repositories. *config-check* and *config-update* jobs are triggered
during a change lifecycle for the tenant's config repository. Both are executed on
the Master SF's Zuul executor.
