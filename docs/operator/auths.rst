.. _authentication:

Authentication
==============

.. note::

  This page is about basic administration of the authentication component in Software Factory.
  For more information on how to manage users and authorizations, see the :ref:`user management documentation<user_management>` 

Software Factory's IAM is handled by the `Keycloak component <https://www.keycloak.org>`_.
Keycloak also provides single sign-on on Software Factory's authenticated services via the OpenID Connect protocol.

Keycloak replaces the Cauth component in Software Factory 3.8 and above.

This page focuses on the specificities of how Keycloak is deployed in Software Factory.

For more details on how to actually manage the service as an administrator, `Keycloak's full documentation
can be found here <https://www.keycloak.org/archive/documentation-19.0.html>`_.

It is recommended to at least get familiar with common operations like handling users, handling social login
providers and managing groups and roles.

Features
^^^^^^^^

* Single Sign-on out of the box with Gerrit, Zuul, Opensearch Dashboards and Grafana
  when deploying these services in Software Factory
* Social login - Enable login with Github, Facebook, and many other services
* User Federation - Sync users from LDAP or Active Directory servers
* Two-factor authentication support
* Roles management for Zuul, Opensearch Dashboards and Grafana
* Events (Login, etc) are broadcast on the firehose (MQTT) under the secured topic "keycloak"
* Github users' public SSH keys are automatically imported from Github and provisioned into Gerrit

Using the CLI
^^^^^^^^^^^^^

Everything in Keycloak can be done through its web UI. Keycloak's container also comes with a CLI utility.

Assuming you are on a shell on the host running the Keycloak container (you can check this by running  `podman ps` and look for
the `keycloak` container), you can use the CLI by running as root:

.. code-block:: bash

  podman exec -ti keycloak /opt/keycloak/bin/kcadm.sh

Please refer to the `CLI's documentation <https://www.keycloak.org/docs/latest/server_admin/#admin-cli>`_ to authenticate and run commands with it.

Using the web UI
^^^^^^^^^^^^^^^^

The admin web UI can be reached at https://<FQDN>/auth/ . Note that this URL is "hidden", ie not visible from Software Factory's welcome page. Authenticate on
the admin page with the admin credentials, then select the "SF" realm. From there you can manage users and roles.

Migrating from cauth
^^^^^^^^^^^^^^^^^^^^

Changes
.......

If you are upgrading to Software Factory 3.8 from a previous version using Cauth for authentication,
you will notice some changes:

* Local users (ie created with `sfmanager`) must be imported manually into keycloak (see procedure and details below)
* Automated logging in on services is disabled: prior to version 3.8, if for example you were authenticated on Software Factory's
  landing page then browsed to Gerrit, you would be automatically authenticated on Gerrit. Starting from
  version 3.8, you need to click on each service's login button to get authenticated. As is expected
  of Single Sign-On however, if you authenticated once you won't have to re-enter your credentials for
  the duration of your session.
* Software Factory's User settings page is no longer available, and replaced by Keycloak's User account page.
* Social login and User Federation must be configured in Keycloak. All configuration fields
  related to external authentication in sfconfig.yaml are ignored as of version 3.8, **except for github authentication**.
  It will however likely be removed in a future version of Software Factory, meaning all external identity providers
  will have to be managed through Keycloak.

Regarding **github-based authentication specifically**:

* To enable SSH key synchronization between github and Gerrit for users authenticating via github, **you must enable the `firehose` service in your deployment architecture**.
* You must reconfigure the callback URL in your GitHub OAuth application settings page to this new value: ``https://<FQDN>/auth/realms/SF/broker/github/endpoint``

Regarding **service-specific changes**:

* Gerrit API keys for users are now managed in Gerrit rather than Software Factory's User Settings page.
  Existing API keys are not valid anymore.
* Kibana, OpenSearch dashboards no longer use a default read-only user; users can authenticate normally to use the services.

Importing local users
.....................

.. warning::

  Only do this if you created users on Software Factory with sfmanager!


As root on the install-server node, run:

.. code-block:: bash
  
    /usr/share/sf-config/scripts/sfusers_to_keycloak.sh

This script will dump existing local users from the mariadb database and create them in Keycloak. Note that
the database only holds hashes of the users' passwords, so these cannot be retrieved. A verification email
will be sent to the users so that they can reset their passwords.

Backup and Restore
^^^^^^^^^^^^^^^^^^

Keycloak uses the mariadb backend to store its configuration, users, groups and roles. Backups and restorations are therefore handled
via the mariadb backup/restore process.