.. note::

  This is a lightweight documentation intended to get operators started with setting
  up the Zuul service. For more insight on what Zuul can do, please refer
  to upstream documentation_.

.. _documentation: https://zuul-ci.org/docs/zuul/5.0.0/

Operate zuul
============

* The configuration is located in /etc/zuul
* The logs are written to /var/log/zuul

By default, no merger are being deployed because the executor service
can perform merge task. However, a merger can also be deployed to speed
up start time when there are many projects defined.

Jobs default nodeset
--------------------

The default configuration in */etc/software-factory/sfconfig.yaml* for zuul
nodeset is to use the label *pod-centos-7*. This label is only available if you
added the role *hypervisor-k1s* in */etc/software-factory/arch.yaml*. If you
don't use this role, you should specify the nodeset to use for jobs. For
example, if you have defined a cloud image in nodepool configuration, you should
update */etc/software-factory/sfconfig.yaml* to specify the default nodeset name
and label, for instance:

.. code-block:: yaml

    zuul:
      default_nodeset_name: cloud-centos-7
      default_nodeset_label: cloud-centos-7

Then, run :ref:`sfconfig  <configure_reconfigure>` to apply the modification

Save and restore the queues
---------------------------

The zuul scheduler service is stateless and stopping the process will lose track
of running jobs. However the zuul-changes.py utility can be used
to save and restore the current state:

.. code-block:: bash

    # Print and save all builds in progress to /var/lib/zuul/zuul-queues-dump.sh
    /usr/libexec/software-factory/zuul-changes.py dump

    systemctl restart zuul-scheduler

    # Reload the previous state
    /usr/libexec/software-factory/zuul-changes.py load

The periodic and post pipelines are not dumped by this tool.

.. _restart-zuul-services:

Restart Zuul services
---------------------

The *zuul_restart.yml* playbook stops and restarts Zuul services and
automatically restore the scheduler's jobs queues.

.. code-block:: yaml

  ansible-playbook /var/lib/software-factory/ansible/zuul_restart.yml

Command Line Interfaces
-----------------------

Zuul Admin client
.................

The legacy admin client can be used to change Zuul's behavior, manage projects keys, create auth tokens (see below) or check its configuration. It can be invoked
by running the command `zuul` on the zuul scheduler node.

.. warning::

    Tenant-scoped operations are deprecated with the legacy admin client. For these, please use the zuul client (see below).

More information can be found on `zuul's upstream documentation about the admin client <https://zuul-ci.org/docs/zuul/latest/client.html>`_.

Zuul Client
...........

The REST client can be used for tenant-scoped operations related to normal workflow like enqueues, dequeues, autoholds, promotions and secrets encryption.
It can be invoked by running the command `zuul-client` on the scheduler node:

.. code-block:: bash

  [root@scheduler] zuul-client --help

.. code-block:: bash

  [root@scheduler] zuul-client autohold-list --tenant XXX

More information can be found on `zuul-client's upstream documentation <https://zuul-ci.org/docs/zuul-client/>`_.

Running Zuul Client anywhere
----------------------------

The REST client can be used anywhere as long as the Software Factory web interface can be reached. You can pull the container on your system with the following command:

.. code-block:: bash

  [user@computah] podman pull quay.io/softwarefactory/zuul-client:a6ce77acffd852219fd43a6dc61cbe637aa85bf2-1

Software Factory includes a script that can be used to generate an appropriate configuration file for zuul-client. Run the command below on the scheduler node:

.. code-block:: bash

  [root@<FQDN>] python3 /var/lib/zuul/scripts/generate-zuul-client-config.py https://<FQDN>/zuul/

The script will print a configuration to the shell's standard output. A configuration section will be created for each tenant,
setting the Zuul URL and a temporary authentication token. The configuration should be saved to $HOME/.config/zuul/client.conf 
on the system you intend to run the client from; zuul-client will automatically look for a configuration in that path.

You can then run the `zuul-client` container like so, assuming you saved the configuration to $HOME/.config/zuul/client.conf:

.. code-block:: bash

  [user@computah] podman run --rm --name zc_container -v $HOME/.config/zuul/:/config/:Z quay.io/software-factory/zuul-client:a6ce77acffd852219fd43a6dc61cbe637aa85bf2-1 -c /config/client.conf --use-config <tenant-name> ...

Authentication
--------------

Zuul 5.0 requires authentication to execute administrative tasks such as enqueueing and dequeueing.
This means it is also possible to delegate and grant the right to perform these tasks to trusted users.

Several authenticators can be configured to enable authentication:

* **Internal authenticators**: these can be used by operators to generate authentication tokens manually.
  Token generation and validation is entirely handled by Zuul. The tokens generated in such a way can
  then be handed out to users, and are meant to be used with Zuul's CLI.
* **External authenticators**: OpenID Connect-compatible Identity Providers such as Keycloak, Glu, Auth0 ...
  These authenticators can be used to set up authentication on Zuul's web interface. Users will be redirected
  to the Identity Provider's login page whenever they authenticate.

.. note:: 

    When running zuul-client from the scheduler node, you don't need to generate a token prior to running a privileged command, the client will attempt to generate
    one for you automatically based on the zuul service's configuration. How convenient!

See the upstream documentation on `authentication <https://zuul-ci.org/docs/zuul/5.0.0/authentication.html>`_ and `access rules <https://zuul-ci.org/docs/zuul/5.0.0/tenants.html#access-rule>`_
for more details.

Authenticating with the CLI
............................

Software Factory configures automatically an internal authenticator that can be used to generate credentials to
use with the CLI when needed. The authenticator is called ``zuul_operator``.

To generate a token, run this command as root on the node where the zuul-scheduler service is up:

.. code-block:: bash

  [root@sftests.com]$ zuul create-auth-token --auth-config zuul_operator --tenant xyz --user XXX
  Bearer eyJ0eX[...]

The part after "Bearer" is the authentication token you can use with the argument ``--auth-token`` of the Zuul CLIs.

Authenticating on the web interface
...................................

Zuul 5.0 supports authentication via OpenID Connect in the web interface. The authentication
is tenant scoped, meaning you need to define a preferred way of authenticating per Zuul tenant, if you
choose to enable authentication for a specific tenant. Authentication is only used to allow specific users
to perform admin actions from the web GUI, such as dequeueing buildsets and managing autohold queries.

.. note::

  Software Factory's current SSO service **does not support** OpenID Connect. These features require the use of an external Identity Provider such as a Keycloak instance, or Google.

Assuming you have created an OpenID Connect client with the Identity Provider you wish to
use, edit the following part in sfconfig.yaml:

.. code-block:: yaml

  external_authenticators:
    - name: redhat_sso
      realm: redhat
      issuer_id: https://keycloak/auth/realms/redhat
      client_id: zuul

You can then use the ``realm`` value to set the authentication realm to redirect users to
when they browse Zuul's web interface for a given tenant:

.. code-block:: yaml

  - tenant:
      name: xyz
      # ...
      authentication-realm: redhat

Access rules
.............

By default authenticated users cannot perform any admin tasks on a tenant. Access rules, or ``admin-rules``
must be defined in Zuul's configuration to allow elevated privileges. The rules are based on conditions on
the claims of the access tokens issued by the OpenID Connect Identity Provider. Please contact your
Identity Provider to find out more about the claims that are being set in the access tokens.

By default, Software Factory will convert Gerrit ACL rules that are defined in the config repository,
to Zuul admin-rules of the same name. They can be used if the access tokens have a claim named ``groups``,
and the groups defined in Gerrit exist in the Identity Provider.

Your configuration may then look like this:

.. code-block:: yaml

  - admin-rule:
      name: custom_rule
      conditions:
        - email: admin@seriouscompany.com
  - tenant:
      name: xyz
      # ...
      authentication-realm: redhat
      admin-rules:
        - custom_rule
        - some_gerrit_ACL

Configure an external gerrit (use Software Factory as a Third-Party CI)
-----------------------------------------------------------------------

Refer to the :ref:`Third-Party-CI Quick Start guide <tpci-quickstart>`

.. _zuul-github-app-operator:

Add a git connection
--------------------

In /etc/software-factory/sfconfig.yaml add in *git_connections*:

.. code-block:: yaml

  - name: gerrithub
    baseurl: https://review.gerrithub.io

Then run **sfconfig** to apply the configuration.

.. _zuul-github-app-create:

Create a GitHub app
-------------------

To create a GitHub app on my-org follow this
`github documentation <https://developer.github.com/apps/building-integrations/setting-up-and-registering-github-apps/registering-github-apps/>`_:

* Open the App creation form:

  * to create the app under an organization, go to `https://github.com/organizations/<organization>/settings/apps/new`
  * to create the app under a user account, go to `https://github.com/settings/apps/new`

* Set GitHub App name to "my-org-zuul"
* Set Homepage URL to "https://fqdn"
* Set Setup URL to "https://fqdn/docs/user/zuul_user.html"
* Set Webhook URL to "https://fqdn/zuul/api/connection/github.com/payload"
* Create a Webhook secret
* Set permissions:

  * Repository Administraion: Read (get branch protection status)
  * Repository contents: Read & Write (write to let zuul merge change)
  * Issues: Read & Write
  * Pull requests: Read & Write
  * Commit statuses: Read & Write

* Set events subscription:

  * Commit comment
  * Create
  * Push
  * Release
  * Issue comment
  * Issues
  * Label
  * Pull request
  * Pull request review
  * Pull request review comment
  * Status

* Set Where can this GitHub App be installed to "Any account"
* Create the App
* In the 'General' tab generate a Private key for your application, and download the key to a secure location

To configure the Github connection in sfconfig.yaml, add to the **github_connections** section:

.. code-block:: yaml

  - name: "github.com"
    webhook_token: XXXX # The Webhook secret defined earlier
    app_id: 42 # The ID shown in the about section of the app.
    app_key: /etc/software-factory/github.key # Path to the private key generated during the setup of the app.
    app_name: app-name
    label_name: mergeit # Label of the tag that must be set to let Zuul trigger the gate pipeline.

Then run **sfconfig** to apply the configuration. And finally verify in the 'Advanced'
tab that the Ping payload works (green tick and 200 response). Click "Redeliver" if needed.

.. note::

   It's recommended to use a GitHub app instead of manual webhook. When using
   manual webhook, set the api_token instead of the app_id and app_key.
   Manual webhook documentation is still TBD...


Check out the :ref:`Zuul GitHub App user documentation<zuul-github-app-user>` to start using the application.

More information about the Zuul's Github driver can be found in the Zuul Github driver manual_.

.. _manual: https://docs.openstack.org/infra/zuul/admin/drivers/github.html


Use openstack-infra/zuul-jobs
-----------------------------

The zuul-scheduler can automatically import all the jobs defined in
the zuul-ci.org/zuul-jobs repository. Set the zuul.upstream_zuul_jobs options
to True in sfconfig.yaml


.. _restart_config_update:

Restarting a config-update job
----------------------------------

When the *config-update* job fails, you can manually restart the job using
the command bellow. Make sure to set the *ref-sha* which is the last commit
hash of the config repository.

.. code-block:: bash

    zuul-client enqueue-ref --tenant local --pipeline post --project config --ref master --newrev ref-sha

The job will be running in the post pipeline of the Zuul status page.


Troubleshooting non starting jobs
---------------------------------

* First check that the project is defined in /etc/zuul/main.yaml
* Then check in scheduler.log that it correctly requested a node and submitted a
  job to the executor
* When zuul reports *PRE_FAILURE* or *POST_FAILURE*,
  then the executor's debugging needs to be turned on
* Finally passing all loggers' level to DEBUG in
  /etc/zuul/scheduler-logging.yaml then restarting the service
  zuul-scheduler might help to debug.


Troubleshooting the executor
----------------------------

First you need to enable the executor's *keepjob* option so that ansible logs are available on dist:

.. code-block:: bash

    podman exec -ti zuul-executor /usr/local/bin/zuul-executor keep
    podman exec -ti zuul-executor /usr/local/bin/zuul-executor verbose

Then next job execution will be available in /var/lib/zuul/builds/.

In particular, the work/ansible/job-logs.txt usually tells why a job failed.

When done with debugging, deactivate the keepjob option by running:

.. code-block:: bash

    podman exec -ti zuul-executor /usr/local/bin/zuul-executor nokeep
    podman exec -ti zuul-executor /usr/local/bin/zuul-executor unverbose


Accessing test resources on failure (autohold)
----------------------------------------------

See the :ref:`nodepool operator documentation <nodepool-autohold>`.
