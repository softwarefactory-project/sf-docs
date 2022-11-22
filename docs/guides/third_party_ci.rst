.. _third_party_ci_guide:

Deploy a third-party CI with Software Factory
---------------------------------------------

In this guide, we will create a third-party CI with Software Factory including:

* Services configuration
* Test resources configuration
* Extra services such as :ref:`log-classify` and :ref:`log_search_engine`.
* Zuul tenant with pipelines and base job

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
follow `this guide <https://docs.opendev.org/opendev/system-config/latest/third_party.html#creating-a-service-account>`_ to configure it.

Once Software Factory is deployed, add the local Zuul ssh public key
(located on `<https://\<fqdn\>/keys/zuul_rsa.pub>`_ or /var/lib/software-factory/bootstrap-data/ssh_keys/zuul_rsa.pub)
to the remote `user ssh key setting page <https://review.opendev.org/#/settings/ssh-keys>`_.

GitHub
~~~~~~

Create an application by following this guide: :ref:`zuul-github-app-create`.

GitLab
~~~~~~

Create a dedicated account, generate a web-hook secret, generate the account personal API token and ensure web hook target URL is properly set for the repositories Zuul will react on.

Pagure
~~~~~~

Create a dedicated account, generate the account personal API token and ensure web hook target URL is properly set for the repositories Zuul will react on.

Refer to the platform's user manual

CI services
...........

The third-party CI needs a CentOS instance to run on.
See the :ref:`deployment_requirements` section for resources requirements per services.

It is recommended to start with an all-in-one installation that can be scaled up once the services are working.
Below are some instance sizing recommendations:

===== ===== ====== ===========================================
 Ram   CPU   Disk   Services
===== ===== ====== ===========================================
 4GB    1    40GB   Bare minimal: Zuul / Nodepool / Zookeeper
 4GB    2    80GB   Above + logserver
 8GB    4   120GB   Above + Opensearch / Opensearch Dashboards
===== ===== ====== ===========================================

Initial configuration
~~~~~~~~~~~~~~~~~~~~~

Follow the all-in-one quickstart guide: :ref:`allinone-quickstart`.
This will setup a config repository hosted on the provided Gerrit service to simplify configuration
maintenance. Note that the config repository can be hosted on an external service too by following
this guide: :ref:`create_config_job_repos`.

Configure external connections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the service is running locally, you can add the connection to the external system
in the */etc/software-factory/sfconfig.yaml* file:

For gerrit:

.. code-block:: yaml

  zuul:
    gerrit_connections:
      - name: review.opendev.org
        hostname: review.opendev.org
        port: 29418
        puburl: https://review.opendev.org
        username: external-gerrit-user-name
        canonical_hostname: opendev.org

For GitHub:

.. code-block:: yaml

   zuul:
     github_connections:
       - name: github.com
         webhook_token: XXX
         app_id: YYY
         app_name: app-name
         label_name: merge
         app_key: /etc/software-factory/github.key
         # Get the webhook token and the app key from the
         # github app creation guide

For GitLab

.. code-block:: yaml

   zuul:
     gitlab_connections:
       - name: gitlab.com
         hostname: gitlab.com
         api_token: XXX
         webhook_token: XXX

For Pagure:

.. code-block:: yaml

   zuul:
     pagure_connections:
       - api_token: XXX
         baseurl: https://pagure.io
         default_pipelines: false
         name: pagure.io
         hostname: pagure.io
         source_whitelist: <pagure-ips-comma-separated>

Then run *sfconfig* again to setup the connection.

You can check that the connection is enabled by looking at:
  https://<fqdn>/zuul/api/connections

CI resources
............

The third-party CI needs a place to run jobs.

Internal
~~~~~~~~

You can start by using the provided hypervisor role to use a local instance for test resources.
Add the *hypervisor-k1s* role to the */etc/software-factory/arch.yaml* file and run *sfconfig* again.
This will setup a new nodepool provider to run job with podman.

OpenStack
~~~~~~~~~

Follow this guide to setup an OpenStack cloud provider: :ref:`nodepool_cloud_provider`.
Diskimage can be created using virt-customize playbook, see :ref:`nodepool-virt-customize`.

Log processing
..............

The third-party CI needs a place to store and analyze the logs.

Basic logserver
~~~~~~~~~~~~~~~

By default sfconfig configures an apache based logserver with the ara middleware,
provided the *logserver* role is in the arch.

ELK
~~~

To enable logs to be exported in ELK, follow this guide: :ref:`elk-operator`.

Log-Classify
~~~~~~~~~~~~

To enable log analysis, follow this guide: :ref:`log-classify-operator`.


Zuul tenant for third-party CI
..............................

While the local tenant can be used for third-party CI jobs, it might be easier
to create a dedicated tenant by following this guide: :ref:`unmanaged_tenant`.

Third-Party CI Jobs configurations
..................................

A common strategy is to define project template in a regular (untrusted
project) and assign them from a config project. This let you try jobs
speculatively (e.g. without merging potentially breaking change).

Here is an example from the rdo project configuration:

- https://review.rdoproject.org/cgit/rdo-jobs/tree/zuul.d/project-templates.yaml#n171
- https://review.rdoproject.org/cgit/config/tree/zuul.d/projects.yaml#n249

You can put both configuration into a single config project if you
prefer, but that you will not be able to test the job modification.
The update workflow goes looks like this:

- Propose a change (A) to your jobs project (e.g. modifying an existing job
  or adding a new job to the template)
- Propose a change (B) in opendev with a depends on (A)
- If that does not work, update the change (A) and recheck the change
  (B).

Conclusion
..........

At the end of this guide, you should have:

* A working software-factory with a config project to manage Zuul and Nodepool user configuration,
* A set of pipelines and base job ready to be used,
* One or more resources providers configured, and
* A Logserver service to share the build logs.
